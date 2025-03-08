from pymongo.database import Database
from schemas.product.response import ProductResponse
from schemas.pagination import PaginatedResponse
from services.log import create_log
from core.errors import APIException
from core.utils.db import map_db_to_response
from bson import ObjectId


def get_product(db: Database, product_id: str, user_id: str, ip_address: str) -> ProductResponse:
    try:
        product = db.products.find_one({"_id": ObjectId(product_id)})
    except ValueError:
        raise APIException("INVALID_ID", "Invalid product ID format")

    if not product:
        raise APIException("NOT_FOUND", "Product not found")

    if product["vendor_id"] != user_id and product["status"] != "active":
        raise APIException("FORBIDDEN", "You can only view your own or active products")

    create_log(db, "read", "product", product_id, user_id, None, None, ip_address)
    return map_db_to_response(product, ProductResponse)


def get_products(db: Database, user_id: str, limit: int, offset: int, ip_address: str) -> PaginatedResponse[
    ProductResponse]:
    query = {"status": "active"} if user_id != "admin" else {"vendor_id": user_id}
    products = db.products.find(query).skip(offset).limit(limit)
    total = db.products.count_documents(query)
    items = [map_db_to_response(product, ProductResponse) for product in products]

    create_log(db, "read", "product", "list", user_id, None, None, ip_address)
    return PaginatedResponse[ProductResponse](
        items=items,
        total=total,
        limit=limit,
        offset=offset
    )