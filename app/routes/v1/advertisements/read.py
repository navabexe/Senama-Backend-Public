from fastapi import APIRouter, Depends, Request
from pymongo.database import Database
from slowapi import Limiter
from slowapi.util import get_remote_address

from app.dependencies.auth import get_current_user
from app.dependencies.db import get_db
from schemas.advertisement.response import AdvertisementResponse
from schemas.pagination import PaginationParams, PaginatedResponse
from services.advertisements.read import get_advertisement, get_advertisements

router = APIRouter()
limiter = Limiter(key_func=get_remote_address)


@router.get("/{ad_id}", response_model=AdvertisementResponse)
@limiter.limit("10/minute")
async def read_advertisement(
        request: Request,
        ad_id: str,
        db: Database = Depends(get_db),
        user_id: str = Depends(get_current_user)
):
    return get_advertisement(db, ad_id, user_id, request.client.host)


@router.get("", response_model=PaginatedResponse[AdvertisementResponse])
@limiter.limit("10/minute")
async def read_advertisements_list(
        request: Request,
        pagination: PaginationParams = Depends(),
        db: Database = Depends(get_db),
        user_id: str = Depends(get_current_user)
):
    return get_advertisements(db, user_id, pagination.limit, pagination.offset, request.client.host)
