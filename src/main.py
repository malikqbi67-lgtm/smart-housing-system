building = {
    "name": "Smart Housing Building"
}

room1 = {
    "room_id": 101,
    "temperature": 27,
    "humidity": 60,
    "electricity": 2.5
}

print(building["name"])
print(room1)

room2 = {
    "room_id": 102,
    "temperature":36,
    "humidity": 75,
    "electricity": 4.8

}
room3 = {
    "room_id": 103,
    "temperature": 25,
    "humidity": 50,
    "electricity": 1.0
}
rooms = [room1, room2, room3]

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