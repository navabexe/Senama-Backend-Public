from fastapi import APIRouter, Depends, Request
from pymongo.database import Database
from slowapi import Limiter
from slowapi.util import get_remote_address

from app.dependencies.auth import get_current_vendor
from app.dependencies.db import get_db
from schemas.order.response import OrderResponse
from services.orders.delete import delete_order

router = APIRouter()
limiter = Limiter(key_func=get_remote_address)


@router.delete("/{order_id}", response_model=OrderResponse)
@limiter.limit("5/minute")
async def delete_order_route(
        request: Request,
        order_id: str,
        db: Database = Depends(get_db),
        vendor_id: str = Depends(get_current_vendor)
):
    return delete_order(db, order_id, vendor_id, request.client.host)
