# app/routes/v1/auth/otp_verify.py
from fastapi import APIRouter, Depends, Request
from pymongo.database import Database
from app.dependencies.db import get_db
from schemas.auth.otp import OTPSendRequest
from schemas.auth.response import TokenResponse
from services.auth import otp_verify as service_otp_verify
from slowapi import Limiter
from slowapi.util import get_remote_address

router = APIRouter()
limiter = Limiter(key_func=get_remote_address)

@router.post("/verify-otp", response_model=TokenResponse)
@limiter.limit("5/minute")
async def verify_otp_route(
    otp_request: OTPSendRequest,
    request: Request,
    db: Database = Depends(get_db)
):
    return service_otp_verify.verify_otp(db, otp_request, request.client.host)