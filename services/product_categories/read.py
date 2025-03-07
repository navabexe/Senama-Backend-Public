from bson import ObjectId
from pymongo.database import Database

from core.errors import APIException
from core.utils.db import map_db_to_response
from schemas.pagination import PaginatedResponse
from schemas.product_category.response import ProductCategoryResponse
from services.log.log import create_log


def get_product_category(db: Database, category_id: str, user_id: str, ip_address: str) -> ProductCategoryResponse:
    try:
        category = db.product_categories.find_one({"_id": ObjectId(category_id)})
    except ValueError:
        raise APIException("INVALID_ID", "Invalid category ID format")

    if not category:
        raise APIException("VENDOR_NOT_FOUND", "Product category not found")

    create_log(db, "read", "category", category_id, user_id, None, None, ip_address)

    return map_db_to_response(category, ProductCategoryResponse)


def get_product_categories(db: Database, user_id: str, limit: int, offset: int, ip_address: str) -> PaginatedResponse[
    ProductCategoryResponse]:
    categories = db.product_categories.find().skip(offset).limit(limit)
    total = db.product_categories.count_documents({})
    items = [ProductCategoryResponse(**category) for category in categories]

    create_log(db, "read", "category", "list", user_id, None, None, ip_address)

    return PaginatedResponse[ProductCategoryResponse](
        items=items,
        total=total,
        limit=limit,
        offset=offset
    )
