from fastapi import APIRouter, Depends, Request
from pymongo.database import Database
from slowapi import Limiter
from slowapi.util import get_remote_address

from app.dependencies.auth import get_admin_user
from app.dependencies.db import get_db
from schemas.vendor.create import VendorCreateRequest
from schemas.vendor.response import VendorResponse
from services.vendor.create import create_vendor

router = APIRouter()
limiter = Limiter(key_func=get_remote_address)


@router.post("", response_model=VendorResponse)
@limiter.limit("5/minute")
async def create_vendor_route(
        request: Request,
        vendor_request: VendorCreateRequest,
        db: Database = Depends(get_db),
        admin_id: str = Depends(get_admin_user)
):
    return create_vendor(db, vendor_request, admin_id, request.client.host)
