from fastapi import APIRouter, Depends, Request
from pymongo.database import Database
from slowapi import Limiter
from slowapi.util import get_remote_address

from app.dependencies.auth import get_current_user
from app.dependencies.db import get_db
from schemas.business_category.response import BusinessCategoryResponse
from schemas.pagination import PaginationParams, PaginatedResponse
from services.business_categories.read import get_business_category, get_business_categories

router = APIRouter()
limiter = Limiter(key_func=get_remote_address)


@router.get("/{category_id}", response_model=BusinessCategoryResponse)
@limiter.limit("10/minute")
async def read_business_category(
        request: Request,
        category_id: str,
        db: Database = Depends(get_db),
        user_id: str = Depends(get_current_user)
):
    return get_business_category(db, category_id, user_id, request.client.host)


@router.get("", response_model=PaginatedResponse[BusinessCategoryResponse])
@limiter.limit("10/minute")
async def read_business_categories_list(
        request: Request,
        pagination: PaginationParams = Depends(),
        db: Database = Depends(get_db),
        user_id: str = Depends(get_current_user)
):
    return get_business_categories(db, user_id, pagination.limit, pagination.offset, request.client.host)
