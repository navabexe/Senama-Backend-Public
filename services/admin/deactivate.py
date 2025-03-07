from datetime import datetime, UTC

from bson import ObjectId
from pymongo.database import Database

from core.errors import APIException
from core.utils.db import map_db_to_response
from schemas.vendor.response import VendorResponse
from services.log.log import create_log


def deactivate_vendor(db: Database, vendor_id: str, admin_id: str, ip_address: str) -> VendorResponse:
    try:
        vendor = db.vendors.find_one({"_id": ObjectId(vendor_id)})
    except ValueError:
        raise APIException("INVALID_ID", "Invalid vendor ID format")

    if not vendor:
        raise APIException("VENDOR_NOT_FOUND")
    if vendor["status"] == "pending":
        raise APIException("FORBIDDEN", "Vendor already pending")

    previous_data = vendor.copy()
    db.vendors.update_one(
        {"_id": ObjectId(vendor_id)},
        {"$set": {"status": "pending", "updated_by": admin_id, "updated_at": datetime.now(UTC).isoformat()}}
    )

    updated_vendor = db.vendors.find_one({"_id": ObjectId(vendor_id)})
    create_log(db, "deactivate", "vendor", vendor_id, admin_id, previous_data, updated_vendor, ip_address)
    return map_db_to_response(updated_vendor, VendorResponse)
