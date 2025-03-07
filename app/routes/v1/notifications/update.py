from fastapi import APIRouter, Depends, Request
from pymongo.database import Database
from slowapi import Limiter
from slowapi.util import get_remote_address

from app.dependencies.auth import get_current_user
from app.dependencies.db import get_db
from schemas.notification.response import NotificationResponse
from schemas.notification.update import NotificationUpdateRequest
from services.notifications.update import update_notification

router = APIRouter()
limiter = Limiter(key_func=get_remote_address)


@router.put("/{notif_id}", response_model=NotificationResponse)
@limiter.limit("5/minute")
async def update_notification_route(
        request: Request,
        notif_id: str,
        notif_request: NotificationUpdateRequest,
        db: Database = Depends(get_db),
        user_id: str = Depends(get_current_user)
):
    return update_notification(db, notif_id, notif_request, user_id, request.client.host)
