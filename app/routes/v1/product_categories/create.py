from fastapi import APIRouter, Depends, Request
from pymongo.database import Database
from slowapi import Limiter
from slowapi.util import get_remote_address

from app.dependencies.auth import get_admin_user
from app.dependencies.db import get_db
from schemas.product_category.create import ProductCategoryCreateRequest
from schemas.product_category.response import ProductCategoryResponse
from services.product_categories.create import create_product_category

router = APIRouter()
limiter = Limiter(key_func=get_remote_address)


@router.post("", response_model=ProductCategoryResponse)
@limiter.limit("5/minute")
async def create_product_category_route(
        request: Request,
        category_request: ProductCategoryCreateRequest,
        db: Database = Depends(get_db),
        admin_id: str = Depends(get_admin_user)
):
    return create_product_category(db, category_request, admin_id, request.client.host)
