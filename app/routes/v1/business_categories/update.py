from fastapi import APIRouter, Depends, Request
from pymongo.database import Database
from slowapi import Limiter
from slowapi.util import get_remote_address

from app.dependencies.auth import get_admin_user
from app.dependencies.db import get_db
from schemas.business_category.response import BusinessCategoryResponse
from schemas.business_category.update import BusinessCategoryUpdateRequest
from services.business_categories.update import update_business_category

router = APIRouter()
limiter = Limiter(key_func=get_remote_address)


@router.put("/{category_id}", response_model=BusinessCategoryResponse)
@limiter.limit("5/minute")
async def update_business_category_route(
        request: Request,
        category_id: str,
        category_request: BusinessCategoryUpdateRequest,
        db: Database = Depends(get_db),
        admin_id: str = Depends(get_admin_user)
):
    return update_business_category(db, category_id, category_request, admin_id, request.client.host)
