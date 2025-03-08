from pymongo.database import Database
from core.errors import APIException
from core.validators import Validators
from schemas.auth.signup import VendorSignupRequest, VendorSignupResponse
from services.log import create_log
from bson import ObjectId
from datetime import datetime, UTC

def signup_vendor(db: Database, request: VendorSignupRequest, ip_address: str) -> VendorSignupResponse:
    Validators.validate_phone(request.owner_phone)
    Validators.validate_not_null(request.business_category_ids, "business_category_ids")

    user = db.users.find_one({"phone": request.owner_phone})
    if not user:
        user = {
            "_id": ObjectId(),
            "phone": request.owner_phone,
            "roles": ["vendor"],
            "status": "pending",
            "created_at": datetime.now(UTC).isoformat(),
            "updated_at": datetime.now(UTC).isoformat()
        }
        db.users.insert_one(user)
    else:
        if "vendor" not in user.get("roles", []):
            db.users.update_one(
                {"_id": user["_id"]},
                {"$push": {"roles": "vendor"}}
            )

    if db.vendors.find_one({"user_id": user["_id"]}):
        raise APIException("INVALID_PHONE", "Vendor already registered for this user", status_code=400)

    vendor = {
        "user_id": user["_id"],
        "username": request.username,
        "name": request.name,
        "owner_name": request.owner_name,
        "owner_phone": request.owner_phone,
        "address": request.address,
        "location": request.location.model_dump(),
        "city": request.city,
        "province": request.province,
        "business_category_ids": request.business_category_ids,
        "status": "pending",
        "created_by": "self",
        "created_at": datetime.now(UTC).isoformat(),
        "updated_at": datetime.now(UTC).isoformat()
    }
    result = db.vendors.insert_one(vendor)
    vendor_id = str(result.inserted_id)

    create_log(db, "create", "vendor", vendor_id, "self", None, vendor, ip_address)
    return VendorSignupResponse(
        message="Vendor registration submitted. Awaiting admin approval.",
        vendor_id=vendor_id,
        status="pending"
    )