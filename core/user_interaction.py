from pymongo.database import Database


def follow_vendor(db: Database, user_id: str, vendor_id: str):
    db.vendors.update_one({"_id": vendor_id}, {"$inc": {"followers_count": 1}})
    db.users.update_one({"_id": user_id}, {"$inc": {"following_count": 1}})
