from bson import ObjectId
from pymongo.database import Database

from core.errors import APIException
from core.utils.db import map_db_to_response
from schemas.order.response import OrderResponse
from schemas.pagination import PaginatedResponse
from services.log.log import create_log


def get_order(db: Database, order_id: str, vendor_id: str, ip_address: str) -> OrderResponse:
    try:
        order = db.orders.find_one({"_id": ObjectId(order_id), "vendor_id": vendor_id})
    except ValueError:
        raise APIException("INVALID_ID", "Invalid order ID format")

    if not order:
        raise APIException("VENDOR_NOT_FOUND", "Order not found or not owned by you")

    create_log(db, "read", "order", order_id, vendor_id, None, None, ip_address)

    return map_db_to_response(order, OrderResponse)


def get_orders(db: Database, vendor_id: str, limit: int, offset: int, ip_address: str) -> PaginatedResponse[
    OrderResponse]:
    orders = db.orders.find({"vendor_id": vendor_id}).skip(offset).limit(limit)
    total = db.orders.count_documents({"vendor_id": vendor_id})
    items = [OrderResponse(**order) for order in orders]

    create_log(db, "read", "order", "list", vendor_id, None, None, ip_address)

    return PaginatedResponse[OrderResponse](
        items=items,
        total=total,
        limit=limit,
        offset=offset
    )
