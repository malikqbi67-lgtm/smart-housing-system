import random

def generate_room(room_id):
    room = {
        "room_id": room_id,
        "temperature": random.randint(20, 45),
        "humidity": random.randint(30, 90),
        "electricity": round(random.uniform(0.5, 8), 1)
    }
    return room

rooms = [generate_room(101), generate_room(102), generate_room(103)]

for room in rooms:
    print(room)