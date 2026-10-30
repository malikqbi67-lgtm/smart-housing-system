import sqlite3
from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_connection():
    conn = sqlite3.connect("data/building.db")
    conn.row_factory = sqlite3.Row
    return conn

@app.get("/")
def home():
    return {"message": "Smart Housing API is running"}

@app.get("/readings")
def get_readings(limit: int = 60):
    conn = get_connection()
    rows = conn.execute(
        "SELECT * FROM readings ORDER BY id DESC LIMIT ?", (limit,)
    ).fetchall()
    conn.close()
    return [dict(row) for row in rows]
from fastapi import HTTPException

@app.get("/rooms")
def get_rooms():
    conn = get_connection()
    rows = conn.execute("""
        SELECT * FROM readings
        WHERE id IN (SELECT MAX(id) FROM readings GROUP BY room_id)
        ORDER BY room_id
    """).fetchall()
    conn.close()
    return [dict(row) for row in rows]

@app.get("/rooms/{room_id}")
def get_room(room_id: int):
    conn = get_connection()
    row = conn.execute(
        "SELECT * FROM readings WHERE room_id = ? ORDER BY id DESC LIMIT 1",
        (room_id,)
    ).fetchone()
    conn.close()
    if row is None:
        raise HTTPException(status_code=404, detail="Room not found")
    return dict(row)
@app.get("/alerts")
def get_alerts():
    conn = get_connection()
    rows = conn.execute("""
        SELECT * FROM readings
        WHERE id IN (SELECT MAX(id) FROM readings GROUP BY room_id)
        AND status != 'NORMAL'
        ORDER BY room_id
    """).fetchall()
    conn.close()

    alerts = []
    for row in rows:
        reasons = []
        if row["temperature"] > 35:
            reasons.append("HIGH TEMPERATURE")
        if row["humidity"] > 70:
            reasons.append("HIGH HUMIDITY")
        if row["electricity"] > 4:
            reasons.append("HIGH ELECTRICITY USAGE")
        alerts.append({
            "room_id": row["room_id"],
            "status": row["status"],
            "reasons": reasons,
            "timestamp": row["timestamp"]
        })
    return alerts


@app.get("/building/status")
def get_building_status():
    conn = get_connection()
    rows = conn.execute("""
        SELECT * FROM readings
        WHERE id IN (SELECT MAX(id) FROM readings GROUP BY room_id)
    """).fetchall()
    conn.close()

    total = len(rows)
    if total == 0:
        return {"message": "No readings yet"}

    normal = sum(1 for r in rows if r["status"] == "NORMAL")
    warning = sum(1 for r in rows if r["status"] == "WARNING")
    critical = sum(1 for r in rows if r["status"] == "CRITICAL")
    avg_temp = round(sum(r["temperature"] for r in rows) / total, 2)

    if critical > 0:
        condition = "CRITICAL"
    elif warning > 0:
        condition = "WARNING"
    else:
        condition = "NORMAL"

    return {
        "building": "Smart Housing Building",
        "total_rooms": total,
        "average_temperature": avg_temp,
        "normal": normal,
        "warning": warning,
        "critical": critical,
        "condition": condition
    }