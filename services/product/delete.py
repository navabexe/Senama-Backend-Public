from pymongo.database import Database
from schemas.product.response import ProductResponse
from core.errors import APIException
from services.log import create_log
from core.utils.db import map_db_to_response
from bson import ObjectId


def delete_product(db: Database, product_id: str, vendor_id: str, ip_address: str) -> ProductResponse:
    try:
        product = db.products.find_one({"_id": ObjectId(product_id), "vendor_id": vendor_id})
    except ValueError:
        raise APIException("INVALID_ID", "Invalid product ID format")

    if not product:
        raise APIException("NOT_FOUND", "Product not found or not owned by you")

    if db.orders.count_documents({"product_ids": product_id, "status": {"$nin": ["cancelled", "delivered"]}}) > 0:
        raise APIException("FORBIDDEN", "Cannot delete product with active orders")

    previous_data = product.copy()
    db.products.delete_one({"_id": ObjectId(product_id)})

    create_log(db, "delete", "product", product_id, vendor_id, previous_data, None, ip_address)
    return map_db_to_response(previous_data, ProductResponse)