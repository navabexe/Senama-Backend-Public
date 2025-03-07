from fastapi import APIRouter, Depends, Request
from pymongo.database import Database
from slowapi import Limiter
from slowapi.util import get_remote_address

from app.dependencies.auth import get_current_vendor
from app.dependencies.db import get_db
from schemas.product.response import ProductResponse
from services.product.delete import delete_product

router = APIRouter()
limiter = Limiter(key_func=get_remote_address)


@router.delete("/{product_id}", response_model=ProductResponse)
@limiter.limit("5/minute")
async def delete_product_route(
        request: Request,
        product_id: str,
        db: Database = Depends(get_db),
        vendor_id: str = Depends(get_current_vendor)
):
    return delete_product(db, product_id, vendor_id, request.client.host)
