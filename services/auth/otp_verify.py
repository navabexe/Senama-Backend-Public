import logging
from datetime import datetime, UTC

from pymongo.database import Database

from core.auth.jwt import create_access_token
from core.errors import APIException
from core.session import create_session
from core.validators import Validators
from schemas.auth.otp import OTPVerifyRequest, OTPVerifyResponse
from services.log.log import create_log

logger = logging.getLogger(__name__)


def verify_otp(db: Database, request: OTPVerifyRequest, device_info: str, ip_address: str) -> OTPVerifyResponse:
    Validators.validate_phone(request.phone)

    user = db.users.find_one({"phone": request.phone})
    vendor = db.vendors.find_one({"owner_phone": request.phone})

    if not user and not vendor:
        raise APIException(
            error_code="VENDOR_NOT_FOUND",
            detail="No user or vendor registered with this phone number.",
            status_code=400
        )

    entity = vendor if vendor else user
    entity_collection = "vendors" if vendor else "users"
    entity_id = str(entity["_id"])
    phone_field = "owner_phone" if vendor else "phone"
    entity_type = "vendor" if vendor else "user"  # تعیین نوع موجودیت

    if "otp" not in entity or "otp_expires_at" not in entity:
        raise APIException("INVALID_OTP", "No OTP registered for this phone")

    stored_otp = entity["otp"]
    expires_at = datetime.fromisoformat(entity["otp_expires_at"])

    if stored_otp != request.otp_code:
        raise APIException("INVALID_OTP")
    if expires_at < datetime.now(UTC):
        raise APIException("INVALID_OTP", "OTP code has expired")

    db[entity_collection].update_one(
        {phone_field: request.phone},
        {"$unset": {"otp": "", "otp_expires_at": ""}}
    )
    token = create_access_token(data={"sub": entity_id})
    session = create_session(db, entity_id, device_info, ip_address)

    session_doc = db.sessions.find_one({"refresh_token": session.refresh_token})
    if not session_doc:
        logger.error(f"Session not stored for entity_id: {entity_id}, refresh_token: {session.refresh_token}")
        raise Exception("Failed to store session in database")
    logger.info(f"Session stored successfully: {session_doc}")

    create_log(db, "login", entity_collection[:-1], entity_id, entity_id, None, {"session_id": session.id}, ip_address)
    return OTPVerifyResponse(
        message="Login successful",
        token=token,
        refresh_token=session.refresh_token,
        entity_id=entity_id,
        entity_type=entity_type,  # مشخص کردن نوع (user یا vendor)
        status=entity.get("status", "unknown")
    )
