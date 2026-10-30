"use client";

import { useEffect, useState } from "react";
import {
  CartesianGrid,
  Legend,
  Line,
  LineChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";

const API = "http://127.0.0.1:8000";

type Reading = {
  id: number;
  room_id: number;
  temperature: number;
  humidity: number;
  electricity: number;
  status: string;
  timestamp: string;
};

type BuildingStatus = {
  building: string;
  total_rooms: number;
  average_temperature: number;
  normal: number;
  warning: number;
  critical: number;
  condition: string;
};

type Alert = {
  room_id: number;
  status: string;
  reasons: string[];
  timestamp: string;
};

type Field = "temperature" | "humidity" | "electricity";
type ChartRow = Record<string, string | number>;

const BADGE: Record<string, string> = {
  NORMAL: "bg-emerald-500/15 text-emerald-400 ring-emerald-500/30",
  WARNING: "bg-amber-500/15 text-amber-400 ring-amber-500/30",
  CRITICAL: "bg-red-500/15 text-red-400 ring-red-500/30",
};

const BORDER: Record<string, string> = {
  NORMAL: "border-emerald-500/30",
  WARNING: "border-amber-500/40",
  CRITICAL: "border-red-500/60",
};

const LINE_COLORS = ["#38bdf8", "#f472b6", "#a3e635", "#fbbf24", "#c084fc"];

function buildChart(readings: Reading[], field: Field): ChartRow[] {
  const map = new Map<string, ChartRow>();
  [...readings].reverse().forEach((r) => {
    const time = r.timestamp.slice(11);
    const row = map.get(time) ?? { time };
    row["Room " + r.room_id] = r[field];
    map.set(time, row);
  });
  return Array.from(map.values());
}

function Badge({ status }: { status: string }) {
  return (
    <span
      className={`rounded-full px-3 py-1 text-xs font-semibold ring-1 ring-inset ${BADGE[status] ?? ""}`}
    >
      {status}
    </span>
  );
}

function StatCard({
  label,
  value,
  accent,
}: {
  label: string;
  value: string | number;
  accent?: string;
}) {
  return (
    <div className="rounded-2xl border border-slate-800 bg-slate-900/60 p-5">
      <p className="text-sm text-slate-400">{label}</p>
      <p className={`mt-2 text-3xl font-bold ${accent ?? "text-white"}`}>{value}</p>
    </div>
  );
}

function ChartCard({
  title,
  unit,
  data,
  rooms,
}: {
  title: string;
  unit: string;
  data: ChartRow[];
  rooms: number[];
}) {
  return (
    <div className="rounded-2xl border border-slate-800 bg-slate-900/60 p-5">
      <h3 className="mb-4 text-sm font-semibold text-slate-300">
        {title} <span className="text-slate-500">({unit})</span>
      </h3>
      <div className="h-64">
        <ResponsiveContainer width="100%" height="100%">
          <LineChart data={data}>
            <CartesianGrid stroke="#1e293b" strokeDasharray="3 3" />
            <XAxis dataKey="time" stroke="#64748b" fontSize={11} />
            <YAxis stroke="#64748b" fontSize={11} />
            <Tooltip
              contentStyle={{
                background: "#0f172a",
                border: "1px solid #1e293b",
                borderRadius: 12,
              }}
            />
            <Legend />
            {rooms.map((id, i) => (
              <Line
                key={id}
                type="monotone"
                dataKey={"Room " + id}
                stroke={LINE_COLORS[i % LINE_COLORS.length]}
                strokeWidth={2}
                dot={false}
                isAnimationActive={false}
              />
            ))}
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}

export default function Dashboard() {
  const [status, setStatus] = useState<BuildingStatus | null>(null);
  const [rooms, setRooms] = useState<Reading[]>([]);
  const [alerts, setAlerts] = useState<Alert[]>([]);
  const [history, setHistory] = useState<Reading[]>([]);
  const [online, setOnline] = useState(true);
  const [updated, setUpdated] = useState("");

  useEffect(() => {
    async function load() {
      try {
        const [s, r, a, h] = await Promise.all([
          fetch(API + "/building/status").then((x) => x.json()),
          fetch(API + "/rooms").then((x) => x.json()),
          fetch(API + "/alerts").then((x) => x.json()),
          fetch(API + "/readings?limit=60").then((x) => x.json()),
        ]);
        if (s.condition) setStatus(s);
        setRooms(r);
        setAlerts(a);
        setHistory(h);
        setOnline(true);
        setUpdated(new Date().toLocaleTimeString());
      } catch {
        setOnline(false);
      }
    }
    load();
    const timer = setInterval(load, 3000);
    return () => clearInterval(timer);
  }, []);

  const roomIds = rooms.map((r) => r.room_id);

  return (
    <main className="min-h-screen bg-slate-950 text-slate-100">
      <div className="mx-auto max-w-7xl space-y-8 px-6 py-8">
        {/* Header */}
        <header className="flex flex-wrap items-center justify-between gap-4">
          <div>
            <h1 className="text-3xl font-bold tracking-tight">
              {status?.building ?? "Smart Housing Building"}
            </h1>
            <p className="mt-1 text-sm text-slate-400">
              Real-time IoT monitoring dashboard
            </p>
          </div>
          <div className="flex items-center gap-4">
            <div className="flex items-center gap-2 text-sm text-slate-400">
              <span
                className={`h-2.5 w-2.5 rounded-full ${online ? "animate-pulse bg-emerald-400" : "bg-red-500"}`}
              />
              {online ? "Live · " + updated : "API offline"}
            </div>
            {status && <Badge status={status.condition} />}
          </div>
        </header>

        {!online && (
          <div className="rounded-xl border border-red-500/40 bg-red-500/10 p-4 text-sm text-red-300">
            Cannot reach the API. Make sure uvicorn is running on port 8000.
          </div>
        )}

        {/* Overview */}
        <section className="grid grid-cols-2 gap-4 lg:grid-cols-5">
          <StatCard label="Total rooms" value={status?.total_rooms ?? "-"} />
          <StatCard
            label="Avg temperature"
            value={status ? status.average_temperature + "°C" : "-"}
          />
          <StatCard label="Normal" value={status?.normal ?? "-"} accent="text-emerald-400" />
          <StatCard label="Warning" value={status?.warning ?? "-"} accent="text-amber-400" />
          <StatCard label="Critical" value={status?.critical ?? "-"} accent="text-red-400" />
        </section>

        {/* Rooms + Alerts */}
        <section className="grid gap-6 lg:grid-cols-3">
          <div className="lg:col-span-2">
            <h2 className="mb-4 text-lg font-semibold">Room monitoring</h2>
            <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-3">
              {rooms.map((room) => (
                <div
                  key={room.room_id}
                  className={`rounded-2xl border bg-slate-900/60 p-5 ${BORDER[room.status] ?? "border-slate-800"}`}
                >
                  <div className="flex items-center justify-between">
                    <h3 className="text-lg font-semibold">Room {room.room_id}</h3>
                    <Badge status={room.status} />
                  </div>
                  <dl className="mt-4 space-y-3 text-sm">
                    <div className="flex justify-between">
                      <dt className="text-slate-400">🌡️ Temperature</dt>
                      <dd className="font-semibold">{room.temperature}°C</dd>
                    </div>
                    <div className="flex justify-between">
                      <dt className="text-slate-400">💧 Humidity</dt>
                      <dd className="font-semibold">{room.humidity}%</dd>
                    </div>
                    <div className="flex justify-between">
                      <dt className="text-slate-400">⚡ Electricity</dt>
                      <dd className="font-semibold">{room.electricity} kWh</dd>
                    </div>
                  </dl>
                  <p className="mt-4 text-xs text-slate-500">{room.timestamp}</p>
                </div>
              ))}
            </div>
          </div>

          <div>
            <h2 className="mb-4 text-lg font-semibold">Active alerts</h2>
            <div className="space-y-3">
              {alerts.length === 0 && (
                <div className="rounded-2xl border border-emerald-500/30 bg-emerald-500/10 p-5 text-sm text-emerald-300">
                  ✅ No active alerts
                </div>
              )}
              {alerts.map((alert) => (
                <div
                  key={alert.room_id}
                  className="rounded-2xl border border-slate-800 bg-slate-900/60 p-4"
                >
                  <div className="flex items-center justify-between">
                    <span className="font-semibold">Room {alert.room_id}</span>
                    <Badge status={alert.status} />
                  </div>
                  <ul className="mt-3 space-y-1 text-sm text-slate-300">
                    {alert.reasons.map((reason) => (
                      <li key={reason}>• {reason}</li>
                    ))}
                  </ul>
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* Charts */}
        <section>
          <h2 className="mb-4 text-lg font-semibold">History</h2>
          <div className="grid gap-6 lg:grid-cols-2">
            <ChartCard
              title="Temperature history"
              unit="°C"
              data={buildChart(history, "temperature")}
              rooms={roomIds}
            />
            <ChartCard
              title="Humidity history"
              unit="%"
              data={buildChart(history, "humidity")}
              rooms={roomIds}
            />
            <div className="lg:col-span-2">
              <ChartCard
                title="Electricity consumption history"
                unit="kWh"
                data={buildChart(history, "electricity")}
                rooms={roomIds}
              />
            </div>
          </div>
        </section>
      </div>
    </main>
  );
}
