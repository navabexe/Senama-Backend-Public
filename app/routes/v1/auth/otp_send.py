from fastapi import APIRouter, Depends
from pymongo.database import Database
from slowapi import Limiter
from slowapi.util import get_remote_address
from starlette.requests import Request

from app.dependencies.db import get_db
from schemas.auth.otp import OTPSendRequest, OTPSendResponse
from services.auth.otp_send import send_otp

router = APIRouter()
limiter = Limiter(key_func=get_remote_address)


@router.post("/send-otp", response_model=OTPSendResponse)
@limiter.limit("5/minute")
async def send_otp_route(request: Request, otp_request: OTPSendRequest, db: Database = Depends(get_db)):
    return send_otp(db, otp_request, request.client.host)
