from bson import ObjectId
from pymongo.database import Database

from core.errors import APIException
from core.utils.db import map_db_to_response
from schemas.pagination import PaginatedResponse
from schemas.user.response import UserResponse
from services.log import create_log


def get_user(db: Database, user_id: str, requester_id: str, ip_address: str) -> UserResponse:
    try:
        user = db.users.find_one({"_id": ObjectId(user_id)})
    except ValueError:
        raise APIException("INVALID_ID", "Invalid user ID format")

    if not user:
        raise APIException("VENDOR_NOT_FOUND", "User not found")

    create_log(db, "read", "user", user_id, requester_id, None, None, ip_address)
    return map_db_to_response(user, UserResponse)


def get_users(db: Database, requester_id: str, limit: int, offset: int, ip_address: str) -> PaginatedResponse[
    UserResponse]:
    users = db.users.find().skip(offset).limit(limit)
    total = db.users.count_documents({})
    items = [map_db_to_response(user, UserResponse) for user in users]

    create_log(db, "read", "user", "list", requester_id, None, None, ip_address)
    return PaginatedResponse[UserResponse](
        items=items,
        total=total,
        limit=limit,
        offset=offset
    )