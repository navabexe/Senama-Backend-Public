from bson import ObjectId
from pymongo.database import Database

from core.errors import APIException
from core.utils.db import map_db_to_response
from schemas.notification.response import NotificationResponse
from services.log import create_log


def delete_notification(db: Database, notif_id: str, user_id: str, ip_address: str) -> NotificationResponse:
    try:
        notification = db.notifications.find_one({"_id": ObjectId(notif_id), "receiver_id": user_id})
    except ValueError:
        raise APIException("INVALID_ID", "Invalid notification ID format")

    if not notification:
        raise APIException("NOT_FOUND", "Notification not found or not owned by you")

    previous_data = notification.copy()
    db.notifications.delete_one({"_id": ObjectId(notif_id)})

    create_log(db, "delete", "notification", notif_id, user_id, previous_data, None, ip_address)
    return map_db_to_response(previous_data, NotificationResponse)