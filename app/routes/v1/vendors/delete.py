from fastapi import APIRouter, Depends, Request
from pymongo.database import Database
from slowapi import Limiter
from slowapi.util import get_remote_address

from app.dependencies.auth import get_current_vendor
from app.dependencies.db import get_db
from schemas.vendor.response import VendorResponse
from services.vendor.delete import delete_vendor

router = APIRouter()
limiter = Limiter(key_func=get_remote_address)


@router.delete("/me", response_model=VendorResponse)
@limiter.limit("5/minute")
async def delete_vendor_route(
        request: Request,
        db: Database = Depends(get_db),
        vendor_id: str = Depends(get_current_vendor)
):
    return delete_vendor(db, vendor_id, vendor_id, request.client.host)
