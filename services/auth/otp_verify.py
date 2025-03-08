import logging
from datetime import datetime, UTC
from pymongo.database import Database
from core.errors import APIException
from core.session import create_session
from core.validators import Validators
from schemas.auth.otp import OTPSendRequest
from schemas.auth.response import TokenResponse
from services.log import create_log
from bson import ObjectId

logger = logging.getLogger(__name__)

def verify_otp(db: Database, request: OTPSendRequest, device_info: str, ip_address: str) -> TokenResponse:
    Validators.validate_phone(request.phone)
    Validators.validate_not_null(request.otp, "otp")

    user = db.users.find_one({"phone": request.phone})
    if not user:
        raise APIException("NOT_FOUND", "User not found", status_code=404)

    if request.role not in user.get("roles", []):
        raise APIException("INVALID_ROLE", f"User does not have role {request.role}", status_code=403)

    if "otp" not in user or "otp_expires_at" not in user:
        raise APIException("INVALID_OTP", "No OTP registered for this phone", status_code=400)

    stored_otp = user["otp"]
    expires_at = datetime.fromisoformat(user["otp_expires_at"])

    if stored_otp != request.otp:
        raise APIException("INVALID_OTP", "Invalid OTP code", status_code=400)
    if expires_at < datetime.now(UTC):
        raise APIException("INVALID_OTP", "OTP code has expired", status_code=400)

    # چک وضعیت برای رول وندور
    entity_id = str(user["_id"])
    if request.role == "vendor":
        vendor = db.vendors.find_one({"user_id": ObjectId(entity_id)})
        if not vendor or vendor["status"] != "active":
            raise APIException("PENDING_APPROVAL", "Vendor is pending admin approval", status_code=403)

    db.users.update_one(
        {"_id": user["_id"]},
        {"$set": {"status": "active"}, "$unset": {"otp": "", "otp_expires_at": ""}}
    )

    session = create_session(db, entity_id, request.role, device_info, ip_address)
    session_doc = db.sessions.find_one({"refresh_token": session.refresh_token})
    if not session_doc:
        logger.error(f"Session not stored for entity_id: {entity_id}, refresh_token: {session.refresh_token}")
        raise APIException("INTERNAL_ERROR", "Failed to store session in database", status_code=500)

    logger.info(f"Session stored successfully: {session_doc}")
    create_log(db, "login", "user", entity_id, entity_id, None, {"session_id": session.id, "role": request.role}, ip_address)

    return TokenResponse(
        message="Login successful",
        token=session.access_token,
        refresh_token=session.refresh_token,
        entity_id=entity_id,
        entity_type="user",
        status=user.get("status", "active")
    )