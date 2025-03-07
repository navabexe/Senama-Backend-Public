from bson import ObjectId
from pymongo.database import Database

from core.errors import APIException
from core.utils.db import map_db_to_response
from schemas.business_category.response import BusinessCategoryResponse
from services.log.log import create_log


def delete_business_category(db: Database, category_id: str, admin_id: str,
                             ip_address: str) -> BusinessCategoryResponse:
    try:
        category = db.business_categories.find_one({"_id": ObjectId(category_id)})
    except ValueError:
        raise APIException("INVALID_ID", "Invalid category ID format")

    if not category:
        raise APIException("VENDOR_NOT_FOUND", "Business category not found")

    previous_data = category.copy()
    db.business_categories.delete_one({"_id": ObjectId(category_id)})

    create_log(db, "delete", "category", category_id, admin_id, previous_data, None, ip_address)

    return map_db_to_response(category, BusinessCategoryResponse)
