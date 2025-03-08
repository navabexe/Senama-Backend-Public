from pymongo.database import Database
from schemas.business_category.update import BusinessCategoryUpdateRequest
from schemas.business_category.response import BusinessCategoryResponse
from core.errors import APIException
from services.log import create_log
from core.utils.db import map_db_to_response
from bson import ObjectId
from datetime import datetime, UTC


def update_business_category(db: Database, category_id: str, request: BusinessCategoryUpdateRequest, admin_id: str,
                             ip_address: str) -> BusinessCategoryResponse:
    try:
        category = db.business_categories.find_one({"_id": ObjectId(category_id)})
    except ValueError:
        raise APIException("INVALID_ID", "Invalid category ID format")

    if not category:
        raise APIException("VENDOR_NOT_FOUND", "Business category not found")

    update_data = request.dict(exclude_unset=True)
    update_data["updated_at"] = datetime.now(UTC).isoformat()

    previous_data = category.copy()
    db.business_categories.update_one({"_id": ObjectId(category_id)}, {"$set": update_data})
    updated_category = db.business_categories.find_one({"_id": ObjectId(category_id)})

    create_log(db, "update", "business_category", category_id, admin_id, previous_data, updated_category, ip_address)
    return map_db_to_response(updated_category, BusinessCategoryResponse)