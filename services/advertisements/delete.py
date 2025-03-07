from bson import ObjectId
from pymongo.database import Database

from core.errors import APIException
from core.utils.db import map_db_to_response
from schemas.advertisement.response import AdvertisementResponse
from services.log.log import create_log


def delete_advertisement(db: Database, ad_id: str, vendor_id: str, ip_address: str) -> AdvertisementResponse:
    try:
        advertisement = db.advertisements.find_one({"_id": ObjectId(ad_id), "vendor_id": vendor_id})
    except ValueError:
        raise APIException("INVALID_ID", "Invalid advertisement ID format")

    if not advertisement:
        raise APIException("VENDOR_NOT_FOUND", "Advertisement not found or not owned by you")

    if advertisement["status"] == "active":
        raise APIException("FORBIDDEN", "Cannot delete an active advertisement")

    previous_data = advertisement.copy()
    db.advertisements.delete_one({"_id": ObjectId(ad_id)})

    create_log(db, "delete", "advertisement", ad_id, vendor_id, previous_data, None, ip_address)

    return map_db_to_response(advertisement, AdvertisementResponse)
