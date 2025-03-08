from pymongo.database import Database
from schemas.notification.update import NotificationUpdateRequest
from schemas.notification.response import NotificationResponse
from core.errors import APIException
from services.log import create_log
from core.utils.db import map_db_to_response
from bson import ObjectId
from datetime import datetime, UTC


def update_notification(db: Database, notif_id: str, request: NotificationUpdateRequest, user_id: str,
                        ip_address: str) -> NotificationResponse:
    try:
        notification = db.notifications.find_one({"_id": ObjectId(notif_id), "receiver_id": user_id})
    except ValueError:
        raise APIException("INVALID_ID", "Invalid notification ID format")

    if not notification:
        raise APIException("NOT_FOUND", "Notification not found or not owned by you")

    update_data = request.dict(exclude_unset=True)
    if "status" in update_data and update_data["status"] not in ["unread", "read"]:
        raise APIException("INVALID_ID", "Invalid status value")
    update_data["updated_at"] = datetime.now(UTC).isoformat()

    previous_data = notification.copy()
    db.notifications.update_one({"_id": ObjectId(notif_id)}, {"$set": update_data})
    updated_notification = db.notifications.find_one({"_id": ObjectId(notif_id)})

    create_log(db, "update", "notification", notif_id, user_id, previous_data, updated_notification, ip_address)
    return map_db_to_response(updated_notification, NotificationResponse)