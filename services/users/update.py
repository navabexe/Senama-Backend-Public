from pymongo.database import Database
from schemas.user.update import UserUpdateRequest
from schemas.user.response import UserResponse
from core.errors import APIException
from services.log import create_log
from core.utils.hash import hash_password
from core.utils.db import map_db_to_response
from bson import ObjectId
from datetime import datetime, UTC


def update_user(db: Database, user_id: str, request: UserUpdateRequest, requester_id: str,
                ip_address: str) -> UserResponse:
    try:
        user = db.users.find_one({"_id": ObjectId(user_id)})
    except ValueError:
        raise APIException("INVALID_ID", "Invalid user ID format")

    if not user:
        raise APIException("VENDOR_NOT_FOUND", "User not found")
    if user_id != requester_id:
        raise APIException("FORBIDDEN", "You can only update your own profile")

    update_data = request.dict(exclude_unset=True)
    if "password" in update_data:
        update_data["password"] = hash_password(update_data["password"])
    update_data["updated_at"] = datetime.now(UTC).isoformat()

    previous_data = user.copy()
    db.users.update_one({"_id": ObjectId(user_id)}, {"$set": update_data})
    updated_user = db.users.find_one({"_id": ObjectId(user_id)})

    create_log(db, "update", "user", user_id, requester_id, previous_data, updated_user, ip_address)
    return map_db_to_response(updated_user, UserResponse)