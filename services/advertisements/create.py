from datetime import datetime, UTC

from bson import ObjectId
from pymongo.database import Database

from core.errors import APIException
from core.validators import Validators
from models.advertisement import Advertisement
from schemas.advertisement.create import AdvertisementCreateRequest
from schemas.advertisement.response import AdvertisementResponse
from services.log import create_log


def create_advertisement(db: Database, request: AdvertisementCreateRequest, vendor_id: str,
                         ip_address: str) -> AdvertisementResponse:
    Validators.validate_not_null(request.type, "type")
    Validators.validate_not_null(request.target_id, "target_id")
    Validators.validate_not_null(request.budget, "budget")
    Validators.validate_not_null(request.targeting, "targeting")
    Validators.validate_not_null(request.duration, "duration")

    if request.type not in ["product", "story", "profile"]:
        raise APIException("INVALID_ID", "Invalid advertisement type")
    if request.budget <= 0:
        raise APIException("INVALID_AMOUNT", "Budget must be positive")
    if request.duration <= 0:
        raise APIException("INVALID_AMOUNT", "Duration must be positive")

    if not db.vendors.find_one({"_id": ObjectId(vendor_id)}):
        raise APIException("VENDOR_NOT_FOUND", "Vendor not found")

    try:
        if request.type == "product" and not db.products.find_one(
                {"_id": ObjectId(request.target_id), "vendor_id": vendor_id}):
            raise APIException("VENDOR_NOT_FOUND", "Product not found or not owned by you")
        elif request.type == "story" and not db.stories.find_one(
                {"_id": ObjectId(request.target_id), "vendor_id": vendor_id}):
            raise APIException("VENDOR_NOT_FOUND", "Story not found or not owned by you")
        elif request.type == "profile" and request.target_id != vendor_id:
            raise APIException("FORBIDDEN", "Profile advertisement must target your own profile")
    except ValueError:
        raise APIException("INVALID_ID", "Invalid target ID format")

    advertisement = Advertisement(
        vendor_id=vendor_id,
        type=request.type,
        target_id=request.target_id,
        budget=request.budget,
        targeting=request.targeting,
        duration=request.duration,
        status="active",
        created_at=datetime.now(UTC).isoformat()
    )

    result = db.advertisements.insert_one(advertisement.dict(exclude={"id"}))
    ad_id = str(result.inserted_id)

    create_log(db, "create", "advertisement", ad_id, vendor_id, None, advertisement.dict(exclude={"id"}), ip_address)

    return AdvertisementResponse(
        id=ad_id,
        vendor_id=advertisement.vendor_id,
        type=advertisement.type,
        target_id=advertisement.target_id,
        budget=advertisement.budget,
        targeting=advertisement.targeting,
        duration=advertisement.duration,
        status=advertisement.status,
        created_at=advertisement.created_at
    )
