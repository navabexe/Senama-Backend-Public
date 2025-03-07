from bson import ObjectId
from pymongo.database import Database

from core.errors import APIException
from core.utils.db import map_db_to_response
from schemas.notification.response import NotificationResponse
from schemas.pagination import PaginatedResponse
from services.log.log import create_log


def get_notification(db: Database, notif_id: str, user_id: str, ip_address: str) -> NotificationResponse:
    try:
        notification = db.notifications.find_one({"_id": ObjectId(notif_id), "user_id": user_id})
    except ValueError:
        raise APIException("INVALID_ID", "Invalid notification ID format")

    if not notification:
        raise APIException("VENDOR_NOT_FOUND", "Notification not found or not owned by you")

    create_log(db, "read", "notification", notif_id, user_id, None, None, ip_address)

    return map_db_to_response(notification, NotificationResponse)


def get_notifications(db: Database, user_id: str, limit: int, offset: int, ip_address: str) -> PaginatedResponse[
    NotificationResponse]:
    notifications = db.notifications.find({"user_id": user_id}).skip(offset).limit(limit)
    total = db.notifications.count_documents({"user_id": user_id})
    items = [NotificationResponse(**notif) for notif in notifications]

    create_log(db, "read", "notification", "list", user_id, None, None, ip_address)

    return PaginatedResponse[NotificationResponse](
        items=items,
        total=total,
        limit=limit,
        offset=offset
    )
