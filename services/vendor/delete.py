from pymongo.database import Database
from schemas.vendor.response import VendorResponse
from core.errors import APIException
from services.log import create_log
from core.utils.db import map_db_to_response
from bson import ObjectId


def delete_vendor(db: Database, vendor_id: str, admin_id: str, ip_address: str) -> VendorResponse:
    try:
        vendor = db.vendors.find_one({"_id": ObjectId(vendor_id)})
    except ValueError:
        raise APIException("INVALID_ID", "Invalid vendor ID format")

    if not vendor:
        raise APIException("VENDOR_NOT_FOUND", "Vendor not found")

    if db.products.count_documents({"vendor_id": vendor_id}) > 0:
        raise APIException("FORBIDDEN", "Cannot delete vendor with existing products")

    previous_data = vendor.copy()
    db.vendors.delete_one({"_id": ObjectId(vendor_id)})

    create_log(db, "delete", "vendor", vendor_id, admin_id, previous_data, None, ip_address)
    return map_db_to_response(previous_data, VendorResponse)