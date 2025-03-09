from bson import ObjectId
from pymongo.database import Database

from core.errors import APIException
from core.utils.db import map_db_to_response
from schemas.order.response import OrderResponse
from services.log import create_log


def delete_order(db: Database, order_id: str, user_id: str, ip_address: str) -> OrderResponse:
    try:
        order = db.orders.find_one({"_id": ObjectId(order_id)})
    except ValueError:
        raise APIException("INVALID_ID", "Invalid order ID format")

    if not order:
        raise APIException("NOT_FOUND", "Order not found")

    if order["vendor_id"] != user_id and order["customer_id"] != user_id:
        raise APIException("FORBIDDEN", "You can only delete your own orders")

    if order["status"] not in ["pending", "cancelled"]:
        raise APIException("FORBIDDEN", "Cannot delete an order that is confirmed, shipped, or delivered")

    previous_data = order.copy()
    db.orders.delete_one({"_id": ObjectId(order_id)})

    create_log(db, "delete", "order", order_id, user_id, previous_data, None, ip_address)
    return map_db_to_response(previous_data, OrderResponse)