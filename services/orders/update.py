from pymongo.database import Database
from schemas.order.update import OrderUpdateRequest
from schemas.order.response import OrderResponse
from core.errors import APIException
from services.log import create_log
from core.utils.db import map_db_to_response
from bson import ObjectId
from datetime import datetime, UTC


def update_order(db: Database, order_id: str, request: OrderUpdateRequest, user_id: str,
                 ip_address: str) -> OrderResponse:
    try:
        order = db.orders.find_one({"_id": ObjectId(order_id)})
    except ValueError:
        raise APIException("INVALID_ID", "Invalid order ID format")

    if not order:
        raise APIException("NOT_FOUND", "Order not found")

    if order["vendor_id"] != user_id:
        raise APIException("FORBIDDEN", "You can only update your own orders")

    update_data = request.dict(exclude_unset=True)
    if "status" in update_data and update_data["status"] not in ["pending", "confirmed", "shipped", "delivered",
                                                                 "cancelled"]:
        raise APIException("INVALID_ID", "Invalid status value")
    update_data["updated_at"] = datetime.now(UTC).isoformat()

    previous_data = order.copy()
    db.orders.update_one({"_id": ObjectId(order_id)}, {"$set": update_data})
    updated_order = db.orders.find_one({"_id": ObjectId(order_id)})

    create_log(db, "update", "order", order_id, user_id, previous_data, updated_order, ip_address)
    return map_db_to_response(updated_order, OrderResponse)