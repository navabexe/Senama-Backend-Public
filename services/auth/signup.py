from pymongo.database import Database

from core.errors import APIException
from core.validators import Validators
from models.vendor import Vendor
from schemas.auth.signup import VendorSignupRequest, VendorSignupResponse
from services.log import create_log


def signup_vendor(db: Database, request: VendorSignupRequest, ip_address: str) -> VendorSignupResponse:
    Validators.validate_phone(request.owner_phone)
    Validators.validate_not_null(request.business_category_ids, "business_category_ids")
    if db.vendors.find_one({"owner_phone": request.owner_phone}):
        raise APIException("INVALID_PHONE", "Phone number already registered")

    vendor = Vendor(
        username=request.username,
        name=request.name,
        owner_name=request.owner_name,
        owner_phone=request.owner_phone,
        address=request.address,
        location=request.location.model_dump(),
        city=request.city,
        province=request.province,
        business_category_ids=request.business_category_ids,
        created_by="self"
    )
    result = db.vendors.insert_one(vendor.model_dump(exclude={"id"}))
    vendor_id = str(result.inserted_id)

    create_log(db, "create", "vendor", vendor_id, "self", None, vendor.model_dump(exclude={"id"}), ip_address)
    return VendorSignupResponse(
        message="Vendor registration submitted. Awaiting admin approval.",
        vendor_id=vendor_id,
        status="pending"
    )
