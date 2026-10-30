import random
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
room1 = {
    "room_id": 101,
    "temperature": 27,
    "humidity": 60,
    "electricity": 2.5
}

print(building["name"])


room2 = {
    "room_id": 102,
    "temperature":36,
    "humidity": 75,
    "electricity": 4.8

}
room3 = {
    "room_id": 103,
    "temperature": 40,
    "humidity": 50,
    "electricity": 1.0
}
rooms = [generate_room(101), generate_room(102), generate_room(103)]

for room in rooms:
    print(room)
    total_temp = 0

for room in rooms:
    total_temp = total_temp + room["temperature"]

average_temp = total_temp / len(rooms)

print("Average temperature:", round(average_temp, 2))

print("--- Warnings ---")

for room in rooms:
    if room["temperature"] > 35:
        print("Room", room["room_id"], ": HIGH TEMPERATURE")

    if room["humidity"] > 70:
        print("Room", room["room_id"], ": HIGH HUMIDITY")

    if room["electricity"] > 4:
        print("Room", room["room_id"], ": HIGH ELECTRICITY USAGE")

print("--- Building Report ---")

rooms_with_warnings = 0

for room in rooms:
    if room["temperature"] > 35 or room["humidity"] > 70 or room["electricity"] > 4:
        rooms_with_warnings += 1

print("Building:", building["name"])
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

    print("Room", room["room_id"], ":", status)

print("Normal:", normal_count)
print("Warning:", warning_count)
print("Critical:", critical_count)