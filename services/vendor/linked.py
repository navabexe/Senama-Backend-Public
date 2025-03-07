from typing import List, Tuple

from bson import ObjectId
from pymongo.database import Database

from app.exceptions.validation import ValidationException
from core.utils.pagination import paginate_query
from schemas.pagination import PaginationParams
from schemas.product.response import ProductResponse


def get_linked_products(
        db: Database,
        vendor_id: str,
        pagination: PaginationParams
) -> Tuple[List[ProductResponse], int]:
    try:
        vendor = db.vendors.find_one({"_id": ObjectId(vendor_id)})
    except ValueError:
        raise ValidationException(detail="Invalid vendor ID format")

    if not vendor:
        raise ValidationException(detail="Vendor not found")

    linked_product_ids = vendor.get("linked_products", [])
    if not linked_product_ids:
        return [], 0

    query = db.products.find({"_id": {"$in": [ObjectId(pid) for pid in linked_product_ids]}})
    total = len(linked_product_ids)
    products = paginate_query(query, pagination.limit, pagination.offset)

    result = [ProductResponse(**{**p, "product_id": str(p["_id"])}) for p in products]
    return result, total
