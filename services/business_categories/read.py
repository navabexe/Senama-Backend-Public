from bson import ObjectId
from pymongo.database import Database
from core.errors import APIException
from schemas.business_category.response import BusinessCategoryResponse
from schemas.pagination import PaginatedResponse
from services.log import create_log
from core.utils.db import map_db_to_response

def get_business_category(db: Database, category_id: str, user_id: str, ip_address: str) -> BusinessCategoryResponse:
    try:
        category = db.business_categories.find_one({"_id": ObjectId(category_id)})
    except ValueError:
        raise APIException("INVALID_ID", "Invalid category ID format")

    if not category:
        raise APIException("VENDOR_NOT_FOUND", "Business category not found")

    create_log(db, "read", "category", category_id, user_id, None, None, ip_address)
    return map_db_to_response(category, BusinessCategoryResponse)

def get_business_categories(db: Database, user_id: str, limit: int, offset: int, ip_address: str) -> PaginatedResponse[BusinessCategoryResponse]:
    categories = db.business_categories.find().skip(offset).limit(limit)
    total = db.business_categories.count_documents({})
    items = [map_db_to_response(category, BusinessCategoryResponse) for category in categories]

    create_log(db, "read", "category", "list", user_id, None, None, ip_address)
    return PaginatedResponse[BusinessCategoryResponse](
        items=items,
        total=total,
        limit=limit,
        offset=offset
    )