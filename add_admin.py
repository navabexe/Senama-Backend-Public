from datetime import datetime, timezone

from bson import ObjectId
from pymongo import MongoClient

# اتصال به دیتابیس
client = MongoClient("mongodb://localhost:27017")
db = client["senama_db"]

# ساخت یوزر ادمین
admin_user = {
    "_id": ObjectId(),
    "phone": "+989000000000",
    "roles": ["admin"],
    "status": "active",
    "created_at": datetime.now(timezone.utc).isoformat(),
    "updated_at": datetime.now(timezone.utc).isoformat()
}

# اضافه کردن به دیتابیس
result = db.users.insert_one(admin_user)
print(f"Admin added with ID: {result.inserted_id}")