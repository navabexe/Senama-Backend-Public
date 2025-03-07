from bson import ObjectId
from pymongo.database import Database

from core.errors import APIException
from core.utils.db import map_db_to_response
from schemas.vendor.response import VendorResponse
from services.log.log import create_log


def delete_vendor(db: Database, vendor_id: str, user_id: str, ip_address: str) -> VendorResponse:
    try:
        vendor = db.vendors.find_one({"_id": ObjectId(vendor_id)})
    except ValueError:
        raise APIException("INVALID_ID", "Invalid vendor ID format")

    if not vendor:
        raise APIException("VENDOR_NOT_FOUND")

    previous_data = vendor.copy()
    db.vendors.delete_one({"_id": ObjectId(vendor_id)})

    create_log(db, "delete", "vendor", vendor_id, user_id, previous_data, None, ip_address)

    return map_db_to_response(vendor, VendorResponse)