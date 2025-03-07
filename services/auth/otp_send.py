from datetime import datetime, UTC, timedelta

from pymongo.database import Database

from app.config.settings import settings
from core.auth.otp import generate_otp
from core.errors import APIException
from core.validators import Validators
from schemas.auth.otp import OTPSendRequest, OTPSendResponse
from services.log.log import create_log


def send_otp(db: Database, request: OTPSendRequest, ip_address: str) -> OTPSendResponse:
    Validators.validate_phone(request.phone)

    # چک کردن هم توی users و هم vendors
    user = db.users.find_one({"phone": request.phone})
    vendor = db.vendors.find_one({"owner_phone": request.phone})

    if not user and not vendor:
        raise APIException(
            error_code="VENDOR_NOT_FOUND",
            detail="No user or vendor registered with this phone number. Please register first.",
            status_code=400
        )

    # انتخاب موجودیت (اولویت با vendor اگه هر دو باشن)
    entity = vendor if vendor else user
    entity_collection = "vendors" if vendor else "users"
    entity_id = str(entity["_id"])
    phone_field = "owner_phone" if vendor else "phone"

    otp = generate_otp()
    expires_at = datetime.now(UTC) + timedelta(minutes=settings.OTP_EXPIRE_MINUTES)
    db[entity_collection].update_one(
        {phone_field: request.phone},
        {"$set": {"otp": otp, "otp_expires_at": expires_at.isoformat()}}
    )

    create_log(db, "otp_sent", entity_collection[:-1], entity_id, "system", None, {"otp": otp}, ip_address)
    return OTPSendResponse(
        message="OTP sent to phone number.",
        otp_sent=True,
        otp=otp  # فقط برای تست
    )
