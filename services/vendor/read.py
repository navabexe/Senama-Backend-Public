from pymongo.database import Database
from schemas.vendor.response import VendorResponse
from schemas.pagination import PaginatedResponse
from services.log import create_log
from core.errors import APIException
from core.utils.db import map_db_to_response
from bson import ObjectId


def get_vendor(db: Database, vendor_id: str, user_id: str, ip_address: str) -> VendorResponse:
    try:
        vendor = db.vendors.find_one({"_id": ObjectId(vendor_id)})
    except ValueError:
        raise APIException("INVALID_ID", "Invalid vendor ID format")

    if not vendor:
        raise APIException("VENDOR_NOT_FOUND", "Vendor not found")

    if vendor["_id"] != ObjectId(user_id) and vendor["status"] != "active":
        raise APIException("FORBIDDEN", "You can only view your own or active vendors")

    create_log(db, "read", "vendor", vendor_id, user_id, None, None, ip_address)
    return map_db_to_response(vendor, VendorResponse)


def get_vendors(db: Database, user_id: str, limit: int, offset: int, ip_address: str) -> PaginatedResponse[
    VendorResponse]:
    query = {"status": "active"} if user_id != "admin" else {}
    vendors = db.vendors.find(query).skip(offset).limit(limit)
    total = db.vendors.count_documents(query)
    items = [map_db_to_response(vendor, VendorResponse) for vendor in vendors]

    create_log(db, "read", "vendor", "list", user_id, None, None, ip_address)
    return PaginatedResponse[VendorResponse](
        items=items,
        total=total,
        limit=limit,
        offset=offset
    )