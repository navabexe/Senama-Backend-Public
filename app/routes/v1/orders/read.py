from fastapi import APIRouter, Depends, Request
from pymongo.database import Database
from slowapi import Limiter
from slowapi.util import get_remote_address

from app.dependencies.auth import get_current_vendor
from app.dependencies.db import get_db
from schemas.order.response import OrderResponse
from schemas.pagination import PaginationParams, PaginatedResponse
from services.orders.read import get_order, get_orders

router = APIRouter()
limiter = Limiter(key_func=get_remote_address)


@router.get("/{order_id}", response_model=OrderResponse)
@limiter.limit("10/minute")
async def read_order(
        request: Request,
        order_id: str,
        db: Database = Depends(get_db),
        vendor_id: str = Depends(get_current_vendor)
):
    return get_order(db, order_id, vendor_id, request.client.host)


@router.get("", response_model=PaginatedResponse[OrderResponse])
@limiter.limit("10/minute")
async def read_orders_list(
        request: Request,
        pagination: PaginationParams = Depends(),
        db: Database = Depends(get_db),
        vendor_id: str = Depends(get_current_vendor)
):
    return get_orders(db, vendor_id, pagination.limit, pagination.offset, request.client.host)
