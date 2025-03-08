# app/routes/v1/auth/otp_send.py
from fastapi import APIRouter, Depends, Request
from pymongo.database import Database
from app.dependencies.db import get_db
from schemas.auth.otp import OTPSendRequest, OTPSendResponse
from services.auth import otp_send as service_otp_send
from slowapi import Limiter
from slowapi.util import get_remote_address

router = APIRouter()
limiter = Limiter(key_func=get_remote_address)

@router.post("/send-otp", response_model=OTPSendResponse)
@limiter.limit("5/minute")
async def send_otp_route(
    otp_request: OTPSendRequest,
    request: Request,
    db: Database = Depends(get_db)
):
    return service_otp_send.send_otp(db, otp_request, request.client.host)