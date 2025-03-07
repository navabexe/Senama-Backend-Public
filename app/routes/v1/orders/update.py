from fastapi import APIRouter, Depends, Request
from pymongo.database import Database
from slowapi import Limiter
from slowapi.util import get_remote_address

from app.dependencies.auth import get_current_vendor
from app.dependencies.db import get_db
from schemas.order.response import OrderResponse
from schemas.order.update import OrderUpdateRequest
from services.orders.update import update_order

router = APIRouter()
limiter = Limiter(key_func=get_remote_address)


@router.put("/{order_id}", response_model=OrderResponse)
@limiter.limit("5/minute")
async def update_order_route(
        request: Request,
        order_id: str,
        order_request: OrderUpdateRequest,
        db: Database = Depends(get_db),
        vendor_id: str = Depends(get_current_vendor)
):
    return update_order(db, order_id, order_request, vendor_id, request.client.host)
