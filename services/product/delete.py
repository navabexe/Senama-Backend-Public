from bson import ObjectId
from pymongo.database import Database

from core.errors import APIException
from core.utils.db import map_db_to_response
from schemas.product.response import ProductResponse
from services.log.log import create_log


def delete_product(db: Database, product_id: str, vendor_id: str, ip_address: str) -> ProductResponse:
    try:
        product = db.products.find_one({"_id": ObjectId(product_id), "vendor_id": vendor_id})
    except ValueError:
        raise APIException("INVALID_ID", "Invalid product ID format")

    if not product:
        raise APIException("VENDOR_NOT_FOUND", "Product not found or not owned by you")

    previous_data = product.copy()
    db.products.delete_one({"_id": ObjectId(product_id)})

    create_log(db, "delete", "product", product_id, vendor_id, previous_data, None, ip_address)

    return map_db_to_response(product, ProductResponse)
