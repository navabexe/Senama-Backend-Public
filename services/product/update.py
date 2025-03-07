from datetime import datetime, UTC

from bson import ObjectId
from pymongo.database import Database

from core.errors import APIException
from core.utils.db import map_db_to_response
from schemas.product.response import ProductResponse
from schemas.product.update import ProductUpdateRequest
from services.log.log import create_log


def update_product(db: Database, product_id: str, request: ProductUpdateRequest, vendor_id: str,
                   ip_address: str) -> ProductResponse:
    try:
        product = db.products.find_one({"_id": ObjectId(product_id), "vendor_id": vendor_id})
    except ValueError:
        raise APIException("INVALID_ID", "Invalid product ID format")

    if not product:
        raise APIException("VENDOR_NOT_FOUND", "Product not found or not owned by you")

    update_data = request.dict(exclude_unset=True)
    if "names" in update_data and not update_data["names"]:
        raise APIException("FIELD_REQUIRED", "names cannot be empty")
    if "category_ids" in update_data and not update_data["category_ids"]:
        raise APIException("FIELD_REQUIRED", "category_ids cannot be empty")

    if "category_ids" in update_data:
        for category_id in update_data["category_ids"]:
            try:
                if not db.product_categories.find_one({"_id": ObjectId(category_id)}):
                    raise APIException("VENDOR_NOT_FOUND", f"Category {category_id} not found")
            except ValueError:
                raise APIException("INVALID_ID", f"Invalid category ID: {category_id}")

    previous_data = product.copy()
    update_data["updated_by"] = vendor_id
    update_data["updated_at"] = datetime.now(UTC).isoformat()

    db.products.update_one({"_id": ObjectId(product_id)}, {"$set": update_data})
    updated_product = db.products.find_one({"_id": ObjectId(product_id)})

    create_log(db, "update", "product", product_id, vendor_id, previous_data, updated_product, ip_address)

    return map_db_to_response(updated_product, ProductResponse)
