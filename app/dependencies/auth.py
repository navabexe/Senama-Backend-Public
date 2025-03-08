from datetime import datetime, UTC

from bson import ObjectId
from fastapi import Depends
from pymongo.database import Database

from app.dependencies.db import get_db
from core.auth.jwt import decode_access_token
from fastapi import Header
from core.errors import APIException

def get_token(authorization: str = Header(...)) -> str:
    if not authorization.startswith("Bearer "):
        raise APIException("UNAUTHORIZED", "Invalid token format", status_code=401)
    return authorization.split(" ")[1]

async def get_current_user(
        authorization: str = Header(...),
        db: Database = Depends(get_db)
) -> str:
    if not authorization.startswith("Bearer "):
        raise APIException("UNAUTHORIZED", "Invalid authorization header")
    token = authorization.split("Bearer ")[1]
    payload = decode_access_token(token)
    user_id = payload.get("sub")
    if not user_id:
        raise APIException("UNAUTHORIZED", "Invalid token")

    user = db.users.find_one({"_id": ObjectId(user_id)})
    vendor = db.vendors.find_one({"_id": ObjectId(user_id)})
    if not user and not vendor:
        raise APIException("UNAUTHORIZED", "Invalid or unknown user")

    session = db.sessions.find_one({"access_token": token, "user_id": user_id})
    if not session or datetime.fromisoformat(session["expires_at"]) < datetime.now(UTC):
        raise APIException("UNAUTHORIZED", "Session expired or invalid")

    return user_id


async def get_current_vendor(
        user_id: str = Depends(get_current_user),
        db: Database = Depends(get_db)
) -> str:
    vendor = db.vendors.find_one({"_id": ObjectId(user_id)})
    if not vendor:
        raise APIException("FORBIDDEN", "Vendor access required")
    return user_id


async def get_admin_user(
        user_id: str = Depends(get_current_user),
        db: Database = Depends(get_db)
) -> str:
    user = db.users.find_one({"_id": ObjectId(user_id)})
    if not user or "admin" not in user.get("roles", []):
        raise APIException("FORBIDDEN", "Admin access required")
    return user_id
