from pymongo.database import Database

from app.exceptions.auth import AuthException
from core.auth.blacklist import blacklist_token
from schemas.auth.response import LogoutResponse


def logout_vendor(db: Database, vendor_id: str, token: str) -> LogoutResponse:
    vendor = db.vendors.find_one({"_id": vendor_id})
    if not vendor:
        raise AuthException(detail="Vendor not found")

    blacklist_token(db, token, vendor_id)
    return LogoutResponse(message="Logged out successfully")
