from datetime import datetime, UTC

from bson import ObjectId
from pymongo.database import Database

from core.errors import APIException
from core.utils.db import map_db_to_response
from schemas.vendor.response import VendorResponse
from schemas.vendor.update import VendorUpdateRequest
from services.log.log import create_log


def update_vendor(db: Database, vendor_id: str, request: VendorUpdateRequest, user_id: str,
                  ip_address: str) -> VendorResponse:
    try:
        vendor = db.vendors.find_one({"_id": ObjectId(vendor_id)})
    except ValueError:
        raise APIException("INVALID_ID", "Invalid vendor ID format")

    if not vendor:
        raise APIException("VENDOR_NOT_FOUND")

    update_data = request.dict(exclude_unset=True)
    if "business_category_ids" in update_data and not update_data["business_category_ids"]:
        raise APIException("FIELD_REQUIRED", "business_category_ids cannot be empty")

    previous_data = vendor.copy()
    update_data["updated_by"] = user_id
    update_data["updated_at"] = datetime.now(UTC).isoformat()

    db.vendors.update_one({"_id": ObjectId(vendor_id)}, {"$set": update_data})
    updated_vendor = db.vendors.find_one({"_id": ObjectId(vendor_id)})

    create_log(db, "update", "vendor", vendor_id, user_id, previous_data, updated_vendor, ip_address)

    return map_db_to_response(updated_vendor, VendorResponse)
