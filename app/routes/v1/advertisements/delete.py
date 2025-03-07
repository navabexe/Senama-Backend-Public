from fastapi import APIRouter, Depends, Request
from pymongo.database import Database
from slowapi import Limiter
from slowapi.util import get_remote_address

from app.dependencies.auth import get_current_vendor
from app.dependencies.db import get_db
from schemas.advertisement.response import AdvertisementResponse
from services.advertisements.delete import delete_advertisement

router = APIRouter()
limiter = Limiter(key_func=get_remote_address)


@router.delete("/{ad_id}", response_model=AdvertisementResponse)
@limiter.limit("5/minute")
async def delete_advertisement_route(
        request: Request,
        ad_id: str,
        db: Database = Depends(get_db),
        vendor_id: str = Depends(get_current_vendor)
):
    return delete_advertisement(db, ad_id, vendor_id, request.client.host)
