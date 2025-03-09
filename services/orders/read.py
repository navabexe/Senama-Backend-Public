from bson import ObjectId
from pymongo.database import Database

from core.errors import APIException
from core.utils.db import map_db_to_response
from schemas.order.response import OrderResponse
from schemas.pagination import PaginatedResponse
from services.log import create_log


def get_order(db: Database, order_id: str, user_id: str, ip_address: str) -> OrderResponse:
    try:
        order = db.orders.find_one({"_id": ObjectId(order_id)})
    except ValueError:
        raise APIException("INVALID_ID", "Invalid order ID format")

    if not order:
        raise APIException("NOT_FOUND", "Order not found")

    if order["customer_id"] != user_id and order["vendor_id"] != user_id:
        raise APIException("FORBIDDEN", "You can only view your own orders")

    create_log(db, "read", "order", order_id, user_id, None, None, ip_address)
    return map_db_to_response(order, OrderResponse)


def get_orders(db: Database, user_id: str, limit: int, offset: int, ip_address: str) -> PaginatedResponse[
    OrderResponse]:
    query = {"$or": [{"customer_id": user_id}, {"vendor_id": user_id}]}
    orders = db.orders.find(query).skip(offset).limit(limit)
    total = db.orders.count_documents(query)
    items = [map_db_to_response(order, OrderResponse) for order in orders]

    create_log(db, "read", "order", "list", user_id, None, None, ip_address)
    return PaginatedResponse[OrderResponse](
        items=items,
        total=total,
        limit=limit,
        offset=offset
    )