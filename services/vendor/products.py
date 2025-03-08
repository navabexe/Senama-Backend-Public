from typing import List, Tuple

from bson import ObjectId
from pymongo.database import Database

from core.errors import APIException
from core.utils.pagination import paginate_query
from schemas.pagination import PaginationParams
from schemas.product.response import ProductResponse
from services.log import create_log


def get_vendor_products(
        db: Database,
        vendor_id: str,
        pagination: PaginationParams,
        current_user: str,
        ip_address: str
) -> Tuple[List[ProductResponse], int]:
    try:
        vendor = db.vendors.find_one({"_id": ObjectId(vendor_id)})
    except ValueError:
        raise APIException("INVALID_ID", "Invalid vendor ID format")

    if not vendor:
        raise APIException("VENDOR_NOT_FOUND")
    if vendor["status"] != "active" or not vendor["visibility"]:
        if current_user != str(vendor["_id"]):
            user = db.users.find_one({"_id": current_user})
            if "admin" not in user.get("roles", []):
                raise APIException("FORBIDDEN", "Vendor is not accessible")

    query = {"vendor_id": vendor_id}
    total = db.products.count_documents(query)
    products = paginate_query(db.products.find(query), pagination.limit, pagination.offset)

    result = [ProductResponse(**p) for p in products]
    create_log(db, "read", "product", f"vendor_{vendor_id}", current_user, None, {"count": len(result)}, ip_address)
    return result, total
