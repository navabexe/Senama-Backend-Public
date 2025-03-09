from datetime import datetime, timezone

from bson import ObjectId
from pymongo.database import Database

from core.errors import APIException
from core.validators import Validators
from models.notification import Notification
from schemas.notification.create import NotificationCreateRequest
from schemas.notification.response import NotificationResponse
from services.log import create_log


def create_notification(db: Database, request: NotificationCreateRequest, admin_id: str,
                        ip_address: str) -> NotificationResponse:
    Validators.validate_not_null(request.user_id, "user_id")
    Validators.validate_not_null(request.type, "type")
    Validators.validate_not_null(request.message, "message")

    try:
        if not db.vendors.find_one({"_id": ObjectId(request.user_id)}) and not db.users.find_one(
                {"_id": ObjectId(request.user_id)}):
            raise APIException("VENDOR_NOT_FOUND", "User not found")
    except ValueError:
        raise APIException("INVALID_ID", "Invalid user ID format")

    notification = Notification(
        user_id=request.user_id,
        type=request.type,
        message=request.message,
        read=False,
        created_at=datetime.now(timezone.utc).isoformat()
    )

    result = db.notifications.insert_one(notification.model_dump(exclude={"id"}))
    notif_id = str(result.inserted_id)

    create_log(db, "create", "notification", notif_id, admin_id, None, notification.model_dump(exclude={"id"}), ip_address)

    return NotificationResponse(
        id=notif_id,
        user_id=notification.user_id,
        type=notification.type,
        message=notification.message,
        read=notification.read,
        created_at=notification.created_at
    )
