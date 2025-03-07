from bson import ObjectId
from pymongo.database import Database

from core.errors import APIException
from core.utils.db import map_db_to_response
from schemas.order.response import OrderResponse
from services.log.log import create_log


def delete_order(db: Database, order_id: str, vendor_id: str, ip_address: str) -> OrderResponse:
    try:
        order = db.orders.find_one({"_id": ObjectId(order_id), "vendor_id": vendor_id})
    except ValueError:
        raise APIException("INVALID_ID", "Invalid order ID format")

    if not order:
        raise APIException("VENDOR_NOT_FOUND", "Order not found or not owned by you")

    if order["status"] not in ["new", "cancelled"]:
        raise APIException("FORBIDDEN", "Cannot delete an order in progress or completed")

    previous_data = order.copy()
    db.orders.delete_one({"_id": ObjectId(order_id)})

    create_log(db, "delete", "order", order_id, vendor_id, previous_data, None, ip_address)

    return map_db_to_response(order, OrderResponse)
