from fastapi import APIRouter, Depends, Request
from pymongo.database import Database
from slowapi import Limiter
from slowapi.util import get_remote_address

from app.dependencies.auth import get_current_user
from app.dependencies.db import get_db
from schemas.pagination import PaginationParams, PaginatedResponse
from schemas.product.response import ProductResponse
from services.product.read import get_product, get_products

router = APIRouter()
limiter = Limiter(key_func=get_remote_address)


@router.get("/{product_id}", response_model=ProductResponse)
@limiter.limit("10/minute")
async def read_product(
        request: Request,
        product_id: str,
        db: Database = Depends(get_db),
        user_id: str = Depends(get_current_user)
):
    return get_product(db, product_id, user_id, request.client.host)


@router.get("", response_model=PaginatedResponse[ProductResponse])
@limiter.limit("10/minute")
async def read_products_list(
        request: Request,
        pagination: PaginationParams = Depends(),
        db: Database = Depends(get_db),
        user_id: str = Depends(get_current_user)
):
    return get_products(db, user_id, pagination.limit, pagination.offset, request.client.host)
