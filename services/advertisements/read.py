from bson import ObjectId
from pymongo.database import Database

from core.errors import APIException
from core.utils.db import map_db_to_response
from schemas.advertisement.response import AdvertisementResponse
from schemas.pagination import PaginatedResponse
from services.log.log import create_log


def get_advertisement(db: Database, ad_id: str, user_id: str, ip_address: str) -> AdvertisementResponse:
    try:
        advertisement = db.advertisements.find_one({"_id": ObjectId(ad_id)})
    except ValueError:
        raise APIException("INVALID_ID", "Invalid advertisement ID format")

    if not advertisement:
        raise APIException("VENDOR_NOT_FOUND", "Advertisement not found")

    # فقط صاحب تبلیغ یا کاربران عادی (برای مشاهده تبلیغ فعال) می‌تونن ببینن
    if advertisement["vendor_id"] != user_id and advertisement["status"] != "active":
        raise APIException("FORBIDDEN", "You can only view your own or active advertisements")

    create_log(db, "read", "advertisement", ad_id, user_id, None, None, ip_address)

    return map_db_to_response(advertisement, AdvertisementResponse)


def get_advertisements(db: Database, user_id: str, limit: int, offset: int, ip_address: str) -> PaginatedResponse[
    AdvertisementResponse]:
    # برای کاربران عادی فقط تبلیغ‌های فعال، برای وندورها فقط تبلیغ‌های خودشون
    query = {"status": "active"} if user_id != "admin" else {"vendor_id": user_id}
    advertisements = db.advertisements.find(query).skip(offset).limit(limit)
    total = db.advertisements.count_documents(query)
    items = [AdvertisementResponse(**ad) for ad in advertisements]

    create_log(db, "read", "advertisement", "list", user_id, None, None, ip_address)

    return PaginatedResponse[AdvertisementResponse](
        items=items,
        total=total,
        limit=limit,
        offset=offset
    )
