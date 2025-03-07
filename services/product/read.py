from bson import ObjectId
from pymongo.database import Database

from core.errors import APIException
from core.utils.db import map_db_to_response
from schemas.pagination import PaginatedResponse
from schemas.product.response import ProductResponse
from services.log.log import create_log


def get_product(db: Database, product_id: str, user_id: str, ip_address: str) -> ProductResponse:
    try:
        product = db.products.find_one({"_id": ObjectId(product_id)})
    except ValueError:
        raise APIException("INVALID_ID", "Invalid product ID format")

    if not product:
        raise APIException("VENDOR_NOT_FOUND", "Product not found")

    create_log(db, "read", "product", product_id, user_id, None, None, ip_address)

    return map_db_to_response(product, ProductResponse)


def get_products(db: Database, user_id: str, limit: int, offset: int, ip_address: str) -> PaginatedResponse[
    ProductResponse]:
    products = db.products.find().skip(offset).limit(limit)
    total = db.products.count_documents({})
    items = [ProductResponse(**product) for product in products]

    create_log(db, "read", "product", "list", user_id, None, None, ip_address)

    return PaginatedResponse[ProductResponse](
        items=items,
        total=total,
        limit=limit,
        offset=offset
    )
