from bson import ObjectId
from pymongo.database import Database

from core.auth.auth import get_current_user
from core.auth.blacklist import blacklist_token
from core.auth.jwt import decode_access_token
from core.errors import APIException
from schemas.auth.response import LogoutResponse
from services.log import create_log


def logout(db: Database, token: str, ip_address: str) -> LogoutResponse:
    user = get_current_user(token, db)  # رول از توکن چک می‌شه
    entity_id = str(user["_id"])

    # دیکد کردن توکن برای گرفتن رول
    token_payload = decode_access_token(token)
    requested_role = token_payload.get("role")  # حالا از payload می‌گیریم

    if requested_role == "vendor":
        vendor = db.vendors.find_one({"user_id": ObjectId(entity_id)})
        if not vendor:
            raise APIException("NOT_FOUND", "Vendor not found for this user", status_code=404)
        entity_id = str(vendor["_id"])  # برای بلک‌لیست از vendor_id استفاده می‌کنیم

    blacklist_token(db, token, entity_id)
    create_log(db, "logout", requested_role, entity_id, entity_id, None, None, ip_address)
    return LogoutResponse(message="Logged out successfully")