from pymongo.database import Database
from schemas.business_category.response import BusinessCategoryResponse
from core.errors import APIException
from services.log import create_log
from core.utils.db import map_db_to_response
from bson import ObjectId


def delete_business_category(db: Database, category_id: str, admin_id: str,
                             ip_address: str) -> BusinessCategoryResponse:
    try:
        category = db.business_categories.find_one({"_id": ObjectId(category_id)})
    except ValueError:
        raise APIException("INVALID_ID", "Invalid category ID format")

    if not category:
        raise APIException("VENDOR_NOT_FOUND", "Business category not found")

    # چک کردن اینکه آیا این دسته‌بندی استفاده شده
    if db.vendors.count_documents({"business_category_ids": category_id}) > 0:
        raise APIException("FORBIDDEN", "Cannot delete category in use by vendors")

    previous_data = category.copy()
    db.business_categories.delete_one({"_id": ObjectId(category_id)})

    create_log(db, "delete", "business_category", category_id, admin_id, previous_data, None, ip_address)
    return map_db_to_response(previous_data, BusinessCategoryResponse)