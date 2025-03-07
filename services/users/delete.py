from pymongo.database import Database
from schemas.user.response import UserResponse
from core.errors import APIException
from services.log.log import create_log
from core.utils.db import map_db_to_response
from bson import ObjectId


def delete_user(db: Database, user_id: str, admin_id: str, ip_address: str) -> UserResponse:
    try:
        user = db.users.find_one({"_id": ObjectId(user_id)})
    except ValueError:
        raise APIException("INVALID_ID", "Invalid user ID format")

    if not user:
        raise APIException("VENDOR_NOT_FOUND", "User not found")

    vendor = db.vendors.find_one({"user_id": user_id})
    if vendor:
        raise APIException("FORBIDDEN", "Cannot delete user with associated vendor. Delete the vendor first.")

    previous_data = user.copy()
    db.users.delete_one({"_id": ObjectId(user_id)})

    create_log(db, "delete", "user", user_id, admin_id, previous_data, None, ip_address)

    return map_db_to_response(previous_data, UserResponse)