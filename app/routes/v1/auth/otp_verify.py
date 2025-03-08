# app/routes/v1/auth/otp_verify.py
from fastapi import APIRouter, Depends, Request
from pymongo.database import Database
from app.dependencies.db import get_db
from schemas.auth.otp import OTPVerifyRequest
from schemas.auth.response import TokenResponse
from services.auth import otp_verify as service_otp_verify
from slowapi import Limiter
from slowapi.util import get_remote_address
from core.errors import APIException  # اضافه کردن مدیریت خطا

router = APIRouter()
limiter = Limiter(key_func=get_remote_address)

@router.post("/verify-otp", response_model=TokenResponse)
@limiter.limit("5/minute")
async def verify_otp_route(
    otp_request: OTPVerifyRequest,
    request: Request,
    db: Database = Depends(get_db)
):
    device_info = request.headers.get("User-Agent", "Unknown Device")
    client_ip = request.client.host

    # بررسی اینکه مقدار role حتماً ارسال شده باشد
    if not otp_request.role:
        raise APIException("INVALID_REQUEST", "Role is required", status_code=400)

    return service_otp_verify.verify_otp(db, otp_request, device_info, client_ip)
