from bson import ObjectId
from pymongo.database import Database

from core.errors import APIException
from core.utils.db import map_db_to_response
from schemas.pagination import PaginatedResponse
from schemas.vendor.response import VendorResponse
from services.log.log import create_log


def get_vendor(db: Database, vendor_id: str, user_id: str, ip_address: str) -> VendorResponse:
    try:
        vendor = db.vendors.find_one({"_id": ObjectId(vendor_id)})
    except ValueError:
        raise APIException("INVALID_ID", "Invalid vendor ID format")

    if not vendor:
        raise APIException("VENDOR_NOT_FOUND")

    create_log(db, "read", "vendor", vendor_id, user_id, None, None, ip_address)

    return map_db_to_response(vendor, VendorResponse)


def get_vendors(db: Database, user_id: str, limit: int, offset: int, ip_address: str) -> PaginatedResponse[
    VendorResponse]:
    vendors = db.vendors.find().skip(offset).limit(limit)
    total = db.vendors.count_documents({})
    items = [map_db_to_response(vendor, VendorResponse) for vendor in vendors]

    create_log(db, "read", "vendor", "list", user_id, None, None, ip_address)

    return PaginatedResponse[VendorResponse](
        items=items,
        total=total,
        limit=limit,
        offset=offset
    )
