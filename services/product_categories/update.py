from pymongo.database import Database
from schemas.product_category.update import ProductCategoryUpdateRequest
from schemas.product_category.response import ProductCategoryResponse
from core.errors import APIException
from services.log import create_log
from core.utils.db import map_db_to_response
from bson import ObjectId
from datetime import datetime, UTC


def update_product_category(db: Database, category_id: str, request: ProductCategoryUpdateRequest, admin_id: str,
                            ip_address: str) -> ProductCategoryResponse:
    try:
        category = db.product_categories.find_one({"_id": ObjectId(category_id)})
    except ValueError:
        raise APIException("INVALID_ID", "Invalid category ID format")

    if not category:
        raise APIException("NOT_FOUND", "Product category not found")

    update_data = request.dict(exclude_unset=True)
    update_data["updated_at"] = datetime.now(UTC).isoformat()

    previous_data = category.copy()
    db.product_categories.update_one({"_id": ObjectId(category_id)}, {"$set": update_data})
    updated_category = db.product_categories.find_one({"_id": ObjectId(category_id)})

    create_log(db, "update", "product_category", category_id, admin_id, previous_data, updated_category, ip_address)
    return map_db_to_response(updated_category, ProductCategoryResponse)