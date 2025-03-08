# from datetime import datetime, UTC, timedelta
# from pymongo.database import Database
# from core.errors import APIException
# from core.validators import Validators
# from schemas.auth.otp import OTPSendRequest, OTPSendResponse
# from services.log import create_log
#
# def send_otp(db: Database, request: OTPSendRequest, ip_address: str) -> OTPSendResponse:
#     Validators.validate_phone(request.phone)
#
#     user = db.users.find_one({"phone": request.phone})
#     vendor = db.vendors.find_one({"owner_phone": request.phone})
#
#     if not user and not vendor:
#         raise APIException(
#             error_code="NOT_FOUND",
#             detail="No user or vendor registered with this phone number. Please register first.",
#             status_code=400
#         )
#
#     entity = vendor if vendor else user
#     entity_collection = "vendors" if vendor else "users"
#     phone_field = "owner_phone" if vendor else "phone"
#     entity_id = str(entity["_id"])
#
#     otp_code = "123456"  # در عمل باید تصادفی تولید بشه
#     expires_at = datetime.now(UTC) + timedelta(minutes=5)
#
#     db[entity_collection].update_one(
#         {phone_field: request.phone},
#         {"$set": {"otp": otp_code, "otp_expires_at": expires_at.isoformat()}},
#         upsert=False
#     )
#
#     create_log(db, "otp_sent", "auth", entity_id, entity_id, None, None, ip_address, {"phone": request.phone})
#     return OTPSendResponse(
#         message=f"OTP sent to {request.phone}",
#         otp_sent=True,
#         otp=otp_code  # مقدار OTP رو اینجا برمی‌گردونیم
#     )

from datetime import datetime, UTC, timedelta
from pymongo.database import Database
from core.errors import APIException
from core.validators import Validators
from schemas.auth.otp import OTPSendRequest, OTPSendResponse
from services.log import create_log
import random

def send_otp(db: Database, request: OTPSendRequest, ip_address: str) -> OTPSendResponse:
    Validators.validate_phone(request.phone)

    user = db.users.find_one({"phone": request.phone})
    vendor = db.vendors.find_one({"owner_phone": request.phone})

    if not user and not vendor:
        raise APIException(
            error_code="NOT_FOUND",
            detail="No user or vendor registered with this phone number. Please register first.",
            status_code=400
        )

    entity = vendor if vendor else user
    entity_collection = "vendors" if vendor else "users"
    phone_field = "owner_phone" if vendor else "phone"
    entity_id = str(entity["_id"])

    # تولید OTP رندوم ۶ رقمی
    otp_code = str(random.randint(100000, 999999))
    expires_at = datetime.now(UTC) + timedelta(minutes=5)

    db[entity_collection].update_one(
        {phone_field: request.phone},
        {"$set": {"otp": otp_code, "otp_expires_at": expires_at.isoformat()}},
        upsert=False
    )

    create_log(db, "otp_sent", "auth", entity_id, entity_id, None, None, ip_address, {"phone": request.phone})
    return OTPSendResponse(
        message=f"OTP sent to {request.phone}",
        otp_sent=True,
        otp=otp_code  # OTP رندوم اینجا برمی‌گرده
    )