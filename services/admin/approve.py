from datetime import datetime, timezone

from bson import ObjectId
from pymongo.database import Database

from core.auth.auth import get_admin_user
from core.errors import APIException
from core.utils.db import map_db_to_response
from schemas.vendor.response import VendorResponse
from services.log import create_log


def approve_vendor(db: Database, vendor_id: str, token: str, ip_address: str) -> VendorResponse:
    admin = get_admin_user(token, db)
    admin_id = str(admin["_id"])
    try:
        vendor = db.vendors.find_one({"_id": ObjectId(vendor_id)})
    except ValueError:
        raise APIException("INVALID_ID", "Invalid vendor ID format", status_code=400)
    if not vendor:
        raise APIException("VENDOR_NOT_FOUND", "Vendor not found", status_code=404)
    if vendor["status"] == "active":
        raise APIException("FORBIDDEN", "Vendor already active", status_code=400)
    previous_data = vendor.copy()
    db.vendors.update_one(
        {"_id": ObjectId(vendor_id)},
        {"$set": {"status": "active", "updated_by": admin_id, "updated_at": datetime.now(timezone.utc).isoformat()}}
    )
    updated_vendor = db.vendors.find_one({"_id": ObjectId(vendor_id)})
    create_log(db, "approve", "vendor", vendor_id, admin_id, previous_data, updated_vendor, ip_address)
    return map_db_to_response(updated_vendor, VendorResponse)