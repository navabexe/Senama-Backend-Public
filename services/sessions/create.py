from datetime import datetime, UTC, timedelta

from bson import ObjectId
from pymongo.database import Database

from core.errors import APIException
from core.validators import Validators
from models.session import Session
from schemas.session.create import SessionCreateRequest
from schemas.session.response import SessionResponse
from services.log import create_log


def create_session(db: Database, request: SessionCreateRequest, admin_id: str, ip_address: str) -> SessionResponse:
    Validators.validate_not_null(request.user_id, "user_id")
    Validators.validate_not_null(request.access_token, "access_token")
    Validators.validate_not_null(request.refresh_token, "refresh_token")
    Validators.validate_not_null(request.device_info, "device_info")
    Validators.validate_not_null(request.ip_address, "ip_address")

    try:
        if not db.vendors.find_one({"_id": ObjectId(request.user_id)}) and not db.users.find_one(
                {"_id": ObjectId(request.user_id)}):
            raise APIException("VENDOR_NOT_FOUND", "User not found")
    except ValueError:
        raise APIException("INVALID_ID", "Invalid user ID format")

    existing_session = db.sessions.find_one({"access_token": request.access_token})
    if existing_session:
        raise APIException("FORBIDDEN", "Access token already in use")

    expires_at = datetime.now(UTC) + timedelta(days=7)  # پیش‌فرض ۷ روز

    session = Session(
        user_id=request.user_id,
        access_token=request.access_token,
        refresh_token=request.refresh_token,
        device_info=request.device_info,
        ip_address=request.ip_address,
        created_at=datetime.now(UTC).isoformat(),
        expires_at=expires_at.isoformat()
    )

    result = db.sessions.insert_one(session.dict(exclude={"id"}))
    session_id = str(result.inserted_id)

    create_log(db, "create", "session", session_id, admin_id, None, session.dict(exclude={"id"}), ip_address)

    return SessionResponse(
        id=session_id,
        user_id=session.user_id,
        access_token=session.access_token,
        refresh_token=session.refresh_token,
        device_info=session.device_info,
        ip_address=session.ip_address,
        created_at=session.created_at,
        expires_at=session.expires_at
    )
