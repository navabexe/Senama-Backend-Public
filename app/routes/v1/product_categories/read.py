from fastapi import APIRouter, Depends, Request
from pymongo.database import Database
from slowapi import Limiter
from slowapi.util import get_remote_address

from app.dependencies.auth import get_current_user
from app.dependencies.db import get_db
from schemas.pagination import PaginationParams, PaginatedResponse
from schemas.product_category.response import ProductCategoryResponse
from services.product_categories.read import get_product_category, get_product_categories

router = APIRouter()
limiter = Limiter(key_func=get_remote_address)


@router.get("/{category_id}", response_model=ProductCategoryResponse)
@limiter.limit("10/minute")
async def read_product_category(
        request: Request,
        category_id: str,
        db: Database = Depends(get_db),
        user_id: str = Depends(get_current_user)
):
    return get_product_category(db, category_id, user_id, request.client.host)


@router.get("", response_model=PaginatedResponse[ProductCategoryResponse])
@limiter.limit("10/minute")
async def read_product_categories_list(
        request: Request,
        pagination: PaginationParams = Depends(),
        db: Database = Depends(get_db),
        user_id: str = Depends(get_current_user)
):
    return get_product_categories(db, user_id, pagination.limit, pagination.offset, request.client.host)
