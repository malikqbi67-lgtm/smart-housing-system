import json
from datetime import datetime

# 1. اقرأ القديم (أو ابدأ بقائمة فارغة)
try:
    with open("data/history.json", "r") as f:
        history = json.load(f)
except FileNotFoundError:
    history = []

# 2. أضف قراءة جديدة
reading = {
    "room_id": 101,
    "temperature": 27,
    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
}
history.append(reading)

# 3. احفظ الكل
with open("data/history.json", "w") as f:
    json.dump(history, f, indent=2)

print("Total saved readings:", len(history))