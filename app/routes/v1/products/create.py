from fastapi import APIRouter, Depends, Request
from pymongo.database import Database
from slowapi import Limiter
from slowapi.util import get_remote_address

from app.dependencies.auth import get_current_vendor
from app.dependencies.db import get_db
from schemas.product.create import ProductCreateRequest
from schemas.product.response import ProductResponse
from services.product.create import create_product

router = APIRouter()
limiter = Limiter(key_func=get_remote_address)


@router.post("", response_model=ProductResponse)
@limiter.limit("5/minute")
async def create_product_route(
        request: Request,
        product_request: ProductCreateRequest,
        db: Database = Depends(get_db),
        vendor_id: str = Depends(get_current_vendor)
):
    return create_product(db, product_request, vendor_id, request.client.host)
