import sqlite3
from fastapi import FastAPI

app = FastAPI()

def get_connection():
    conn = sqlite3.connect("data/building.db")
    conn.row_factory = sqlite3.Row
    return conn

@app.get("/")
def home():
    return {"message": "Smart Housing API is running"}

@app.get("/readings")
def get_readings():
    conn = get_connection()
    rows = conn.execute(
        "SELECT * FROM readings ORDER BY id DESC LIMIT 10"
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