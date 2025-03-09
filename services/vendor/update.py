from datetime import datetime, timezone

from bson import ObjectId
from pymongo.database import Database

from core.errors import APIException
from core.utils.db import map_db_to_response
from schemas.vendor.response import VendorResponse
from schemas.vendor.update import VendorUpdateRequest
from services.log import create_log


def update_vendor(db: Database, vendor_id: str, request: VendorUpdateRequest, user_id: str,
                  ip_address: str) -> VendorResponse:
    try:
        vendor = db.vendors.find_one({"_id": ObjectId(vendor_id)})
    except ValueError:
        raise APIException("INVALID_ID", "Invalid vendor ID format")

    if not vendor:
        raise APIException("VENDOR_NOT_FOUND", "Vendor not found")

    if str(vendor["_id"]) != user_id:
        raise APIException("FORBIDDEN", "You can only update your own vendor profile")

    update_data = request.model_dump(exclude_unset=True)
    if "status" in update_data and update_data["status"] not in ["active", "inactive", "pending"]:
        raise APIException("INVALID_ID", "Invalid status value")
    update_data["updated_at"] = datetime.now(timezone.utc).isoformat()

    previous_data = vendor.copy()
    db.vendors.update_one({"_id": ObjectId(vendor_id)}, {"$set": update_data})
    updated_vendor = db.vendors.find_one({"_id": ObjectId(vendor_id)})

    create_log(db, "update", "vendor", vendor_id, user_id, previous_data, updated_vendor, ip_address)
    return map_db_to_response(updated_vendor, VendorResponse)