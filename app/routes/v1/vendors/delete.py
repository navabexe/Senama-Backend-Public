from fastapi import APIRouter, Depends, Request
from pymongo.database import Database
from slowapi import Limiter
from slowapi.util import get_remote_address
from app.dependencies.auth import get_token
from app.dependencies.db import get_db
from schemas.vendor.response import DeleteVendorResponse
from services.vendor import delete as service_delete

router = APIRouter()
limiter = Limiter(key_func=get_remote_address)

@router.delete("/{vendor_id}", response_model=DeleteVendorResponse)
@limiter.limit("5/minute")
async def delete_vendor(
    vendor_id: str,
    request: Request,
    db: Database = Depends(get_db),
    token: str = Depends(get_token)
):
    return service_delete.delete_vendor(db, vendor_id, token, request.client.host)