from fastapi import APIRouter, Depends, Request
from pymongo.database import Database
from slowapi import Limiter
from slowapi.util import get_remote_address

from app.dependencies.auth import get_current_user
from app.dependencies.db import get_db
from schemas.order.create import OrderCreateRequest
from schemas.order.response import OrderResponse
from services.orders.create import create_order

router = APIRouter()
limiter = Limiter(key_func=get_remote_address)


@router.post("", response_model=OrderResponse)
@limiter.limit("5/minute")
async def create_order_route(
        request: Request,
        order_request: OrderCreateRequest,
        db: Database = Depends(get_db),
        user_id: str = Depends(get_current_user)
):
    return create_order(db, order_request, user_id, request.client.host)
