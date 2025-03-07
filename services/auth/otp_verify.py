import logging
from datetime import datetime, UTC

from pymongo.database import Database
from jwt import PyJWTError

from core.auth.jwt import create_access_token, create_refresh_token
from core.errors import APIException
from core.session import create_session
from core.validators import Validators
from schemas.auth.otp import OTPVerifyRequest, OTPVerifyResponse
from services.log.log import create_log

logger = logging.getLogger(__name__)

def verify_otp(db: Database, request: OTPVerifyRequest, device_info: str, ip_address: str) -> OTPVerifyResponse:
    try:
        # ولیدیشن ورودی‌ها
        Validators.validate_phone(request.phone)
        Validators.validate_not_null(request.otp_code, "otp_code")

        # پیدا کردن کاربر یا وندور
        user = db.users.find_one({"phone": request.phone})
        vendor = db.vendors.find_one({"owner_phone": request.phone})

        if not user and not vendor:
            raise APIException(
                error_code="NOT_FOUND",
                detail="No user or vendor registered with this phone number.",
                status_code=404
            )

        # تعیین موجودیت
        entity = vendor if vendor else user
        entity_collection = "vendors" if vendor else "users"
        entity_id = str(entity["_id"])
        phone_field = "owner_phone" if vendor else "phone"
        entity_type = "vendor" if vendor else "user"

        # چک کردن وجود OTP
        if "otp" not in entity or "otp_expires_at" not in entity:
            raise APIException("INVALID_OTP", "No OTP registered for this phone", status_code=400)

        stored_otp = entity["otp"]
        expires_at = datetime.fromisoformat(entity["otp_expires_at"])

        # ولیدیشن OTP
        if stored_otp != request.otp_code:
            raise APIException("INVALID_OTP", "Invalid OTP code", status_code=400)
        if expires_at < datetime.now(UTC):
            raise APIException("INVALID_OTP", "OTP code has expired", status_code=400)

        # حذف OTP بعد از تأیید
        db[entity_collection].update_one(
            {phone_field: request.phone},
            {"$unset": {"otp": "", "otp_expires_at": ""}}
        )

        # ساخت توکن‌ها
        token = create_access_token(data={"sub": entity_id, "entity_type": entity_type})
        refresh_token = create_refresh_token(data={"sub": entity_id, "entity_type": entity_type})

        # ساخت و چک کردن سشن
        session = create_session(db, entity_id, device_info, ip_address)
        session_doc = db.sessions.find_one({"refresh_token": session.refresh_token})
        if not session_doc:
            logger.error(f"Session not stored for entity_id: {entity_id}, refresh_token: {session.refresh_token}")
            raise APIException("INTERNAL_ERROR", "Failed to store session in database", status_code=500)

        logger.info(f"Session stored successfully: {session_doc}")
        create_log(db, "login", entity_collection[:-1], entity_id, entity_id, None, {"session_id": session.id}, ip_address)

        # برگرداندن پاسخ
        return OTPVerifyResponse(
            message="Login successful",
            token=token,
            refresh_token=refresh_token,
            entity_id=entity_id,
            entity_type=entity_type,
            status=entity.get("status", "unknown")
        )

    except ValueError as ve:
        raise APIException("INVALID_DATA", f"Invalid data format: {str(ve)}", status_code=400)
    except PyJWTError:
        raise APIException("INTERNAL_ERROR", "Failed to generate token", status_code=500)
    except APIException as ae:
        raise ae  # خطاهای تعریف‌شده رو دوباره پرتاب کن
    except Exception as e:
        logger.error(f"Unexpected error in verify_otp: {str(e)}")
        raise APIException("INTERNAL_ERROR", f"An unexpected error occurred: {str(e)}", status_code=500)