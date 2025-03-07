from fastapi import APIRouter, Depends, Request
from pymongo.database import Database
from slowapi import Limiter
from slowapi.util import get_remote_address

from app.dependencies.auth import get_current_user
from app.dependencies.db import get_db
from schemas.pagination import PaginationParams, PaginatedResponse
from schemas.vendor.response import VendorResponse
from services.vendor.read import get_vendor, get_vendors

router = APIRouter()
limiter = Limiter(key_func=get_remote_address)


@router.get("/me", response_model=VendorResponse)
@limiter.limit("10/minute")
async def read_current_vendor(
        request: Request,
        db: Database = Depends(get_db),
        vendor_id: str = Depends(get_current_user)
):
    return get_vendor(db, vendor_id, vendor_id, request.client.host)


@router.get("/{vendor_id}", response_model=VendorResponse)
@limiter.limit("10/minute")
async def read_vendor(
        request: Request,
        vendor_id: str,
        db: Database = Depends(get_db),
        user_id: str = Depends(get_current_user)
):
    return get_vendor(db, vendor_id, user_id, request.client.host)


@router.get("", response_model=PaginatedResponse[VendorResponse])
@limiter.limit("10/minute")
async def read_vendors_list(
        request: Request,
        pagination: PaginationParams = Depends(),
        db: Database = Depends(get_db),
        user_id: str = Depends(get_current_user)
):
    return get_vendors(db, user_id, pagination.limit, pagination.offset, request.client.host)
