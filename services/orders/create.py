from datetime import datetime, timezone

from bson import ObjectId
from pymongo.database import Database

from core.errors import APIException
from core.validators import Validators
from models.order import Order
from schemas.order.create import OrderCreateRequest
from schemas.order.response import OrderResponse
from services.log import create_log


def create_order(db: Database, request: OrderCreateRequest, user_id: str, ip_address: str) -> OrderResponse:
    Validators.validate_not_null(request.product_id, "product_id")
    Validators.validate_not_null(request.customer_info, "customer_info")
    Validators.validate_not_null(request.quantity, "quantity")

    try:
        product = db.products.find_one({"_id": ObjectId(request.product_id)})
        if not product:
            raise APIException("VENDOR_NOT_FOUND", "Product not found")
    except ValueError:
        raise APIException("INVALID_ID", "Invalid product ID format")

    vendor_id = product["vendor_id"]

    order = Order(
        product_id=request.product_id,
        vendor_id=vendor_id,
        customer_info=request.customer_info,
        quantity=request.quantity,
        note=request.note,
        status="new",
        created_at=datetime.now(timezone.utc).isoformat()
    )

    result = db.orders.insert_one(order.dict(exclude={"id"}))
    order_id = str(result.inserted_id)

    create_log(db, "create", "order", order_id, user_id, None, order.dict(exclude={"id"}), ip_address)

    return OrderResponse(
        id=order_id,
        product_id=order.product_id,
        vendor_id=order.vendor_id,
        customer_info=order.customer_info,
        quantity=order.quantity,
        note=order.note,
        status=order.status,
        created_at=order.created_at
    )
