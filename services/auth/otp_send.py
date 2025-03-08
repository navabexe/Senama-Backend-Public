from datetime import datetime, UTC, timedelta

from bson import ObjectId
from pymongo.database import Database
from core.errors import APIException
from core.validators import Validators
from schemas.auth.otp import OTPSendRequest, OTPSendResponse
from services.log import create_log
import random

VALID_ROLES = ["admin", "vendor", "customer"]

def send_otp(db: Database, request: OTPSendRequest, ip_address: str) -> OTPSendResponse:
    Validators.validate_phone(request.phone)

    if request.role not in VALID_ROLES:
        raise APIException("INVALID_ROLE", f"Role must be one of {VALID_ROLES}", status_code=400)

    user = db.users.find_one({"phone": request.phone})
    if not user:
        user = {
            "_id": ObjectId(),
            "phone": request.phone,
            "roles": [request.role],
            "status": "pending",
            "created_at": datetime.now(UTC).isoformat(),
            "updated_at": datetime.now(UTC).isoformat()
        }
        db.users.insert_one(user)
    else:
        if request.role not in user.get("roles", []):
            db.users.update_one(
                {"_id": user["_id"]},
                {"$push": {"roles": request.role}}
            )

    otp = str(random.randint(100000, 999999))
    expires_at = datetime.now(UTC) + timedelta(minutes=5)

    db.users.update_one(
        {"phone": request.phone},
        {"$set": {"otp": otp, "otp_expires_at": expires_at.isoformat()}}
    )

    create_log(db, "otp_sent", "auth", str(user["_id"]), None, None, None, ip_address, {"phone": request.phone, "role": request.role})
    return OTPSendResponse(message=f"OTP sent to {request.phone}", otp=otp)