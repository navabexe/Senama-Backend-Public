from fastapi import APIRouter, Depends
from pymongo.database import Database
from slowapi import Limiter
from slowapi.util import get_remote_address
from starlette.requests import Request
from app.dependencies.auth import get_token  # تغییر به get_token
from app.dependencies.db import get_db
from schemas.vendor.response import VendorResponse
from services.admin.approve import approve_vendor

router = APIRouter()
limiter = Limiter(key_func=get_remote_address)

@router.put("/{vendor_id}/approve", response_model=VendorResponse)
@limiter.limit("5/minute")
async def approve_vendor_route(
        request: Request,
        vendor_id: str,
        db: Database = Depends(get_db),
        token: str = Depends(get_token)  # تغییر به توکن
):
    return approve_vendor(db, vendor_id, token, request.client.host)  # پاس دادن توکن