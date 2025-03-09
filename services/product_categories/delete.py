from bson import ObjectId
from pymongo.database import Database

from core.errors import APIException
from core.utils.db import map_db_to_response
from schemas.product_category.response import ProductCategoryResponse
from services.log import create_log


def delete_product_category(db: Database, category_id: str, admin_id: str, ip_address: str) -> ProductCategoryResponse:
    try:
        category = db.product_categories.find_one({"_id": ObjectId(category_id)})
    except ValueError:
        raise APIException("INVALID_ID", "Invalid category ID format")

    if not category:
        raise APIException("NOT_FOUND", "Product category not found")

    if db.products.count_documents({"category_ids": category_id}) > 0:
        raise APIException("FORBIDDEN", "Cannot delete category in use by products")

    previous_data = category.copy()
    db.product_categories.delete_one({"_id": ObjectId(category_id)})

    create_log(db, "delete", "product_category", category_id, admin_id, previous_data, None, ip_address)
    return map_db_to_response(previous_data, ProductCategoryResponse)