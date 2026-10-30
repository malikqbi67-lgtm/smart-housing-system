import json
import sqlite3
from datetime import datetime

import random
import time

building = {
    "name": "Smart Housing Building"
}

def generate_room(room_id):
    room = {
        "room_id": room_id,
        "temperature": random.randint(20, 45),
        "humidity": random.randint(30, 90),
        "electricity": round(random.uniform(0.5, 8), 1)
    }
    return room
def init_db():
    conn = sqlite3.connect("data/building.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS readings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            room_id INTEGER,
            temperature INTEGER,
            humidity INTEGER,
            electricity REAL,
            status TEXT,
            timestamp TEXT
        )
    """)
    conn.commit()
    conn.close()

def save_to_db(new_readings):
    conn = sqlite3.connect("data/building.db")
    cursor = conn.cursor()
    for r in new_readings:
        cursor.execute(
            "INSERT INTO readings (room_id, temperature, humidity, electricity, status, timestamp) VALUES (?, ?, ?, ?, ?, ?)",
            (r["room_id"], r["temperature"], r["humidity"], r["electricity"], r["status"], r["timestamp"])
        )
    conn.commit()
    conn.close()

def save_readings(new_readings):
    try:
        with open("data/history.json", "r") as f:
            history = json.load(f)
    except FileNotFoundError:
        history = []

    history.extend(new_readings)

    with open("data/history.json", "w") as f:
        json.dump(history, f, indent=2)

init_db()

while True:
    rooms = [generate_room(101), generate_room(102), generate_room(103)]

    print("=============================")
    print(building["name"])

    for room in rooms:
        print("Room:", room["room_id"], "| Temp:", room["temperature"], "| Humidity:", room["humidity"], "| Electricity:", room["electricity"])

    total_temp = 0
    for room in rooms:
        total_temp += room["temperature"]
    average_temp = total_temp / len(rooms)

    print("--- Warnings ---")
    rooms_with_warnings = 0
    for room in rooms:
        if room["temperature"] > 35:
            print("Room", room["room_id"], ": HIGH TEMPERATURE")
        if room["humidity"] > 70:
            print("Room", room["room_id"], ": HIGH HUMIDITY")
        if room["electricity"] > 4:
            print("Room", room["room_id"], ": HIGH ELECTRICITY USAGE")
        if room["temperature"] > 35 or room["humidity"] > 70 or room["electricity"] > 4:
            rooms_with_warnings += 1

    print("--- Building Report ---")
    print("Total rooms:", len(rooms))
    print("Average temperature:", round(average_temp, 2))
    print("Rooms with warnings:", rooms_with_warnings)
    if rooms_with_warnings == 0:
        print("Building condition: NORMAL")
    else:
        print("Building condition: WARNING")

    print("--- Room Status ---")
    normal_count = 0
    warning_count = 0
    critical_count = 0
    for room in rooms:
        if room["temperature"] >= 40:
            status = "CRITICAL"
            critical_count += 1
        elif room["temperature"] > 35 or room["humidity"] > 70 or room["electricity"] > 4:
            status = "WARNING"
            warning_count += 1
        else:
            status = "NORMAL"
            normal_count += 1
        room["status"] = status
        room["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print("Room", room["room_id"], ":", status)

    print("Normal:", normal_count)
    print("Warning:", warning_count)
    print("Critical:", critical_count)

    save_readings(rooms)
    save_to_db(rooms)

    time.sleep(3)
