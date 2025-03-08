from pymongo.database import Database
from core.auth.jwt import decode_access_token
from core.errors import APIException
from bson import ObjectId

def get_current_user(token: str, db: Database) -> dict:
    payload = decode_access_token(token)
    entity_id = payload.get("sub")
    entity_type = payload.get("entity_type", "user")
    requested_role = payload.get("role")

    if not entity_id or not requested_role:
        raise APIException("UNAUTHORIZED", "Invalid token payload", status_code=401)

    user = db.users.find_one({"_id": ObjectId(entity_id)})
    if not user:
        raise APIException("NOT_FOUND", "User not found", status_code=404)

    if requested_role not in user.get("roles", []):
        raise APIException("FORBIDDEN", f"User does not have role {requested_role}", status_code=403)

    return user

def get_admin_user(token: str, db: Database) -> dict:
    user = get_current_user(token, db)
    if "admin" not in user.get("roles", []):
        raise APIException("FORBIDDEN", "Admin access required", status_code=403)
    return user