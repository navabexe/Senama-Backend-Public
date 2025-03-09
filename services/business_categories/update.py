from datetime import datetime, timezone

from bson import ObjectId
from pymongo.database import Database

from core.errors import APIException
from core.utils.db import map_db_to_response
from schemas.business_category.response import BusinessCategoryResponse
from schemas.business_category.update import BusinessCategoryUpdateRequest
from services.log import create_log


def update_business_category(db: Database, category_id: str, request: BusinessCategoryUpdateRequest, admin_id: str,
                             ip_address: str) -> BusinessCategoryResponse:
    try:
        category = db.business_categories.find_one({"_id": ObjectId(category_id)})
    except ValueError:
        raise APIException("INVALID_ID", "Invalid category ID format")

    if not category:
        raise APIException("VENDOR_NOT_FOUND", "Business category not found")

    update_data = request.model_dump(exclude_unset=True)
    update_data["updated_at"] = datetime.now(timezone.utc).isoformat()

    previous_data = category.copy()
    db.business_categories.update_one({"_id": ObjectId(category_id)}, {"$set": update_data})
    updated_category = db.business_categories.find_one({"_id": ObjectId(category_id)})

    create_log(db, "update", "business_category", category_id, admin_id, previous_data, updated_category, ip_address)
    return map_db_to_response(updated_category, BusinessCategoryResponse)