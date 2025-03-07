from datetime import datetime, UTC

from bson import ObjectId
from pymongo.database import Database

from core.errors import APIException
from core.utils.db import map_db_to_response
from schemas.business_category.response import BusinessCategoryResponse
from schemas.business_category.update import BusinessCategoryUpdateRequest
from services.log.log import create_log


def update_business_category(db: Database, category_id: str, request: BusinessCategoryUpdateRequest, admin_id: str,
                             ip_address: str) -> BusinessCategoryResponse:
    try:
        category = db.business_categories.find_one({"_id": ObjectId(category_id)})
    except ValueError:
        raise APIException("INVALID_ID", "Invalid category ID format")

    if not category:
        raise APIException("VENDOR_NOT_FOUND", "Business category not found")

    update_data = request.dict(exclude_unset=True)
    if "name" in update_data and not update_data["name"]:
        raise APIException("FIELD_REQUIRED", "name cannot be empty")

    previous_data = category.copy()
    update_data["updated_at"] = datetime.now(UTC).isoformat()

    db.business_categories.update_one({"_id": ObjectId(category_id)}, {"$set": update_data})
    updated_category = db.business_categories.find_one({"_id": ObjectId(category_id)})

    create_log(db, "update", "category", category_id, admin_id, previous_data, updated_category, ip_address)

    return map_db_to_response(category, BusinessCategoryResponse)
