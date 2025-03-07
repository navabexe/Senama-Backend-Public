from fastapi import APIRouter, Depends
from pymongo.database import Database
from slowapi import Limiter
from slowapi.util import get_remote_address
from starlette.requests import Request

from app.dependencies.db import get_db
from schemas.auth.otp import OTPVerifyRequest, OTPVerifyResponse
from services.auth.otp_verify import verify_otp

router = APIRouter()
limiter = Limiter(key_func=get_remote_address)


@router.post("/verify-otp", response_model=OTPVerifyResponse)
@limiter.limit("5/minute")
async def verify_otp_route(request: Request, otp_request: OTPVerifyRequest, db: Database = Depends(get_db)):
    return verify_otp(db, otp_request, request.headers.get("User-Agent", "unknown"), request.client.host)
