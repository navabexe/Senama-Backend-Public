from typing import List, Tuple

from pymongo.database import Database

from core.utils.pagination import paginate_query
from schemas.pagination import PaginationParams
from schemas.vendor.response import VendorResponse
from services.log import create_log


def search_vendors(
        db: Database,
        name: str | None,
        category: str | None,
        pagination: PaginationParams,
        current_user: str,
        ip_address: str
) -> Tuple[List[VendorResponse], int]:
    query = {"status": "active", "visibility": True}  # فقط active و public
    if name:
        query["name"] = {"$regex": name, "$options": "i"}
    if category:
        query["business_category_ids"] = category

    total = db.vendors.count_documents(query)
    vendors = paginate_query(db.vendors.find(query), pagination.limit, pagination.offset)
    result = [VendorResponse(**v) for v in vendors]

    create_log(db, "search", "vendor", "multiple", current_user, None, {"count": len(result)}, ip_address)
    return result, total
