from fastapi import APIRouter, Depends
from pymongo.database import Database
from slowapi import Limiter
from slowapi.util import get_remote_address
from starlette.requests import Request

from app.dependencies.db import get_db
from schemas.auth.signup import VendorSignupRequest, VendorSignupResponse
from services.auth.signup import signup_vendor

router = APIRouter()
limiter = Limiter(key_func=get_remote_address)


@router.post("/register", response_model=VendorSignupResponse)
@limiter.limit("5/minute")
async def register_vendor(request: Request, signup_request: VendorSignupRequest, db: Database = Depends(get_db)):
    return signup_vendor(db, signup_request, request.client.host)
