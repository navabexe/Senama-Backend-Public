from pymongo.database import Database
from schemas.product.update import ProductUpdateRequest
from schemas.product.response import ProductResponse
from core.errors import APIException
from services.log import create_log
from core.utils.db import map_db_to_response
from bson import ObjectId
from datetime import datetime, UTC


def update_product(db: Database, product_id: str, request: ProductUpdateRequest, vendor_id: str,
                   ip_address: str) -> ProductResponse:
    try:
        product = db.products.find_one({"_id": ObjectId(product_id), "vendor_id": vendor_id})
    except ValueError:
        raise APIException("INVALID_ID", "Invalid product ID format")

    if not product:
        raise APIException("NOT_FOUND", "Product not found or not owned by you")

    update_data = request.dict(exclude_unset=True)
    if "status" in update_data and update_data["status"] not in ["active", "inactive"]:
        raise APIException("INVALID_ID", "Invalid status value")
    if "price" in update_data and update_data["price"] <= 0:
        raise APIException("INVALID_AMOUNT", "Price must be positive")
    update_data["updated_at"] = datetime.now(UTC).isoformat()

    previous_data = product.copy()
    db.products.update_one({"_id": ObjectId(product_id)}, {"$set": update_data})
    updated_product = db.products.find_one({"_id": ObjectId(product_id)})

    create_log(db, "update", "product", product_id, vendor_id, previous_data, updated_product, ip_address)
    return map_db_to_response(updated_product, ProductResponse)