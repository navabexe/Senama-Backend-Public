from fastapi import APIRouter, Depends, Request
from pymongo.database import Database
from slowapi import Limiter
from slowapi.util import get_remote_address

from app.dependencies.auth import get_current_vendor
from app.dependencies.db import get_db
from schemas.vendor.response import VendorResponse
from schemas.vendor.update import VendorUpdateRequest
from services.vendor.update import update_vendor

router = APIRouter()
limiter = Limiter(key_func=get_remote_address)


@router.put("/me", response_model=VendorResponse)
@limiter.limit("5/minute")
async def update_vendor_route(
        request: Request,
        vendor_request: VendorUpdateRequest,
        db: Database = Depends(get_db),
        vendor_id: str = Depends(get_current_vendor)
):
    return update_vendor(db, vendor_id, vendor_request, vendor_id, request.client.host)
