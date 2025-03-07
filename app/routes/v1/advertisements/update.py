from fastapi import APIRouter, Depends, Request
from pymongo.database import Database
from slowapi import Limiter
from slowapi.util import get_remote_address

from app.dependencies.auth import get_current_vendor
from app.dependencies.db import get_db
from schemas.advertisement.response import AdvertisementResponse
from schemas.advertisement.update import AdvertisementUpdateRequest
from services.advertisements.update import update_advertisement

router = APIRouter()
limiter = Limiter(key_func=get_remote_address)


@router.put("/{ad_id}", response_model=AdvertisementResponse)
@limiter.limit("5/minute")
async def update_advertisement_route(
        request: Request,
        ad_id: str,
        ad_request: AdvertisementUpdateRequest,
        db: Database = Depends(get_db),
        vendor_id: str = Depends(get_current_vendor)
):
    return update_advertisement(db, ad_id, ad_request, vendor_id, request.client.host)
