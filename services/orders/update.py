from datetime import datetime, timezone

from bson import ObjectId
from pymongo.database import Database

from core.errors import APIException
from core.utils.db import map_db_to_response
from schemas.order.response import OrderResponse
from schemas.order.update import OrderUpdateRequest
from services.log import create_log


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

    update_data = request.model_dump(exclude_unset=True)
    if "status" in update_data and update_data["status"] not in ["pending", "confirmed", "shipped", "delivered",
                                                                 "cancelled"]:
        raise APIException("INVALID_ID", "Invalid status value")
    update_data["updated_at"] = datetime.now(timezone.utc).isoformat()

    previous_data = order.copy()
    db.orders.update_one({"_id": ObjectId(order_id)}, {"$set": update_data})
    updated_order = db.orders.find_one({"_id": ObjectId(order_id)})

    create_log(db, "update", "order", order_id, user_id, previous_data, updated_order, ip_address)
    return map_db_to_response(updated_order, OrderResponse)