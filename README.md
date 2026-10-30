# Smart Housing Management System

A simulated IoT building monitoring system. It generates fake sensor data (temperature, humidity, electricity), detects abnormal situations, stores history, and shows everything on a real-time dashboard.

No physical devices are needed. Everything runs on a laptop.

## Features

- Simulated sensors for 3 rooms (temperature, humidity, electricity)
- Automatic status detection: NORMAL, WARNING, CRITICAL
- Readings generated every 3 seconds
- History saved in JSON and SQLite
- REST API built with FastAPI
- Real-time dashboard built with Next.js, with charts and alerts

## Alert Rules

| Condition | Result |
|---|---|
| Temperature > 35°C | HIGH TEMPERATURE (WARNING) |
| Humidity > 70% | HIGH HUMIDITY (WARNING) |
| Electricity > 4 kWh | HIGH ELECTRICITY USAGE (WARNING) |
| Temperature >= 40°C | CRITICAL |

## Architecture

```text
Sensor Simulator -> SQLite -> FastAPI (:8000) -> Next.js Dashboard (:3000)
```

## Project Structure

```text
smart-housing-system/
├── src/
│   ├── main.py      # simulator and storage
│   └── api.py       # FastAPI backend
├── dashboard/       # Next.js dashboard
├── data/            # database and history files
├── README.md
└── .gitignore
```

## How to Run

Open 3 terminal windows.

**1. Simulator**

```bash
python3 src/main.py
```

**2. API**

```bash
python3 -m venv venv
source venv/bin/activate
pip install fastapi uvicorn
uvicorn src.api:app --reload
```

**3. Dashboard**

```bash
cd dashboard
npm install
npm run dev
```

Then open http://localhost:3000

## API Endpoints

| Endpoint | Description |
|---|---|
| GET /rooms | Latest reading for every room |
| GET /rooms/{id} | Latest reading for one room |
| GET /alerts | Active warnings with reasons |
| GET /building/status | General building condition |
| GET /readings | Historical readings |

## Technologies

Python, SQLite, FastAPI, Next.js, Tailwind CSS, Recharts, Git

## Author

Malek
