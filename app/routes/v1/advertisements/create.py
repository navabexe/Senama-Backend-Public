from fastapi import APIRouter, Depends, Request
from pymongo.database import Database
from slowapi import Limiter
from slowapi.util import get_remote_address

from app.dependencies.auth import get_current_vendor
from app.dependencies.db import get_db
from schemas.advertisement.create import AdvertisementCreateRequest
from schemas.advertisement.response import AdvertisementResponse
from services.advertisements.create import create_advertisement

router = APIRouter()
limiter = Limiter(key_func=get_remote_address)


@router.post("", response_model=AdvertisementResponse)
@limiter.limit("5/minute")
async def create_advertisement_route(
        request: Request,
        ad_request: AdvertisementCreateRequest,
        db: Database = Depends(get_db),
        vendor_id: str = Depends(get_current_vendor)
):
    return create_advertisement(db, ad_request, vendor_id, request.client.host)
