from fastapi import APIRouter, Depends, Request
from pymongo.database import Database
from slowapi import Limiter
from slowapi.util import get_remote_address

from app.dependencies.auth import get_admin_user
from app.dependencies.db import get_db
from schemas.business_category.response import BusinessCategoryResponse
from services.business_categories.delete import delete_business_category

router = APIRouter()
limiter = Limiter(key_func=get_remote_address)


@router.delete("/{category_id}", response_model=BusinessCategoryResponse)
@limiter.limit("5/minute")
async def delete_business_category_route(
        request: Request,
        category_id: str,
        db: Database = Depends(get_db),
        admin_id: str = Depends(get_admin_user)
):
    return delete_business_category(db, category_id, admin_id, request.client.host)
