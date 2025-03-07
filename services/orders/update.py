from datetime import datetime, UTC

from bson import ObjectId
from pymongo.database import Database

from core.errors import APIException
from core.utils.db import map_db_to_response
from schemas.order.response import OrderResponse
from schemas.order.update import OrderUpdateRequest
from services.log.log import create_log


def update_order(db: Database, order_id: str, request: OrderUpdateRequest, vendor_id: str,
                 ip_address: str) -> OrderResponse:
    try:
        order = db.orders.find_one({"_id": ObjectId(order_id), "vendor_id": vendor_id})
    except ValueError:
        raise APIException("INVALID_ID", "Invalid order ID format")

    if not order:
        raise APIException("VENDOR_NOT_FOUND", "Order not found or not owned by you")

    update_data = request.dict(exclude_unset=True)
    if "quantity" in update_data and update_data["quantity"] <= 0:
        raise APIException("INVALID_AMOUNT", "Quantity must be positive")
    if "status" in update_data and update_data["status"] not in ["new", "processing", "completed", "cancelled"]:
        raise APIException("INVALID_ID", "Invalid status value")

    previous_data = order.copy()
    update_data["updated_at"] = datetime.now(UTC).isoformat()

    db.orders.update_one({"_id": ObjectId(order_id)}, {"$set": update_data})
    updated_order = db.orders.find_one({"_id": ObjectId(order_id)})

    create_log(db, "update", "order", order_id, vendor_id, previous_data, updated_order, ip_address)

    return map_db_to_response(updated_order, OrderResponse)
