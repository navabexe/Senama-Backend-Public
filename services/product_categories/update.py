from datetime import datetime, timezone

from bson import ObjectId
from pymongo.database import Database

from core.errors import APIException
from core.utils.db import map_db_to_response
from schemas.product_category.response import ProductCategoryResponse
from schemas.product_category.update import ProductCategoryUpdateRequest
from services.log import create_log


def update_product_category(db: Database, category_id: str, request: ProductCategoryUpdateRequest, admin_id: str,
                            ip_address: str) -> ProductCategoryResponse:
    try:
        category = db.product_categories.find_one({"_id": ObjectId(category_id)})
    except ValueError:
        raise APIException("INVALID_ID", "Invalid category ID format")

    if not category:
        raise APIException("NOT_FOUND", "Product category not found")

    update_data = request.dict(exclude_unset=True)
    update_data["updated_at"] = datetime.now(timezone.utc).isoformat()

    previous_data = category.copy()
    db.product_categories.update_one({"_id": ObjectId(category_id)}, {"$set": update_data})
    updated_category = db.product_categories.find_one({"_id": ObjectId(category_id)})

    create_log(db, "update", "product_category", category_id, admin_id, previous_data, updated_category, ip_address)
    return map_db_to_response(updated_category, ProductCategoryResponse)