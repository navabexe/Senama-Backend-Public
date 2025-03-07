from datetime import datetime, UTC

from bson import ObjectId
from pymongo.database import Database

from core.errors import APIException
from core.utils.db import map_db_to_response
from schemas.product_category.response import ProductCategoryResponse
from schemas.product_category.update import ProductCategoryUpdateRequest
from services.log.log import create_log


def update_product_category(db: Database, category_id: str, request: ProductCategoryUpdateRequest, admin_id: str,
                            ip_address: str) -> ProductCategoryResponse:
    try:
        category = db.product_categories.find_one({"_id": ObjectId(category_id)})
    except ValueError:
        raise APIException("INVALID_ID", "Invalid category ID format")

    if not category:
        raise APIException("VENDOR_NOT_FOUND", "Product category not found")

    update_data = request.dict(exclude_unset=True)
    if "name" in update_data and not update_data["name"]:
        raise APIException("FIELD_REQUIRED", "name cannot be empty")

    if "parent_category_id" in update_data and update_data["parent_category_id"]:
        try:
            parent = db.product_categories.find_one({"_id": ObjectId(update_data["parent_category_id"])})
            if not parent:
                raise APIException("VENDOR_NOT_FOUND", "Parent category not found")
        except ValueError:
            raise APIException("INVALID_ID", "Invalid parent category ID format")

    previous_data = category.copy()
    update_data["updated_at"] = datetime.now(UTC).isoformat()

    db.product_categories.update_one({"_id": ObjectId(category_id)}, {"$set": update_data})
    updated_category = db.product_categories.find_one({"_id": ObjectId(category_id)})

    create_log(db, "update", "category", category_id, admin_id, previous_data, updated_category, ip_address)

    return map_db_to_response(updated_category, ProductCategoryResponse)

