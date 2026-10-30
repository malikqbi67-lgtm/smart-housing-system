import json

reading = {"room_id": 101, "temperature": 27}

with open("data/test.json", "w") as f:
    json.dump(reading, f)

print("Saved!")
