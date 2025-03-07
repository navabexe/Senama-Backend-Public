from fastapi import APIRouter, Depends, Request
from pymongo.database import Database
from slowapi import Limiter
from slowapi.util import get_remote_address

from app.dependencies.auth import get_admin_user
from app.dependencies.db import get_db
from schemas.product_category.response import ProductCategoryResponse
from schemas.product_category.update import ProductCategoryUpdateRequest
from services.product_categories.update import update_product_category

router = APIRouter()
limiter = Limiter(key_func=get_remote_address)


@router.put("/{category_id}", response_model=ProductCategoryResponse)
@limiter.limit("5/minute")
async def update_product_category_route(
        request: Request,
        category_id: str,
        category_request: ProductCategoryUpdateRequest,
        db: Database = Depends(get_db),
        admin_id: str = Depends(get_admin_user)
):
    return update_product_category(db, category_id, category_request, admin_id, request.client.host)
