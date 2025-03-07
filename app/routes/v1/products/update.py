from fastapi import APIRouter, Depends, Request
from pymongo.database import Database
from slowapi import Limiter
from slowapi.util import get_remote_address

from app.dependencies.auth import get_current_vendor
from app.dependencies.db import get_db
from schemas.product.response import ProductResponse
from schemas.product.update import ProductUpdateRequest
from services.product.update import update_product

router = APIRouter()
limiter = Limiter(key_func=get_remote_address)


@router.put("/{product_id}", response_model=ProductResponse)
@limiter.limit("5/minute")
async def update_product_route(
        request: Request,
        product_id: str,
        product_request: ProductUpdateRequest,
        db: Database = Depends(get_db),
        vendor_id: str = Depends(get_current_vendor)
):
    return update_product(db, product_id, product_request, vendor_id, request.client.host)
