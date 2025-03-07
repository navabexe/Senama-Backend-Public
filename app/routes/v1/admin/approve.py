from fastapi import APIRouter, Depends
from pymongo.database import Database
from slowapi import Limiter
from slowapi.util import get_remote_address
from starlette.requests import Request

from app.dependencies.auth import get_admin_user
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
        admin_id: str = Depends(get_admin_user)
):
    return approve_vendor(db, vendor_id, admin_id, request.client.host)
