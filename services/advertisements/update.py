from bson import ObjectId
from pymongo.database import Database

from core.errors import APIException
from core.utils.db import map_db_to_response
from schemas.advertisement.response import AdvertisementResponse
from schemas.advertisement.update import AdvertisementUpdateRequest
from services.log import create_log


def update_advertisement(db: Database, ad_id: str, request: AdvertisementUpdateRequest, vendor_id: str,
                         ip_address: str) -> AdvertisementResponse:
    try:
        advertisement = db.advertisements.find_one({"_id": ObjectId(ad_id), "vendor_id": vendor_id})
    except ValueError:
        raise APIException("INVALID_ID", "Invalid advertisement ID format")

    if not advertisement:
        raise APIException("VENDOR_NOT_FOUND", "Advertisement not found or not owned by you")

    update_data = request.model_dump(exclude_unset=True)
    if "type" in update_data and update_data["type"] not in ["product", "story", "profile"]:
        raise APIException("INVALID_ID", "Invalid advertisement type")
    if "budget" in update_data and update_data["budget"] <= 0:
        raise APIException("INVALID_AMOUNT", "Budget must be positive")
    if "duration" in update_data and update_data["duration"] <= 0:
        raise APIException("INVALID_AMOUNT", "Duration must be positive")
    if "status" in update_data and update_data["status"] not in ["active", "paused", "completed"]:
        raise APIException("INVALID_ID", "Invalid status value")

    previous_data = advertisement.copy()
    db.advertisements.update_one({"_id": ObjectId(ad_id)}, {"$set": update_data})
    updated_advertisement = db.advertisements.find_one({"_id": ObjectId(ad_id)})

    create_log(db, "update", "advertisement", ad_id, vendor_id, previous_data, updated_advertisement, ip_address)
    return map_db_to_response(updated_advertisement, AdvertisementResponse)