from fastapi import APIRouter, Depends, Request
from pymongo.database import Database
from slowapi import Limiter
from slowapi.util import get_remote_address

from app.dependencies.auth import get_current_user
from app.dependencies.db import get_db
from schemas.notification.response import NotificationResponse
from services.notifications.delete import delete_notification

router = APIRouter()
limiter = Limiter(key_func=get_remote_address)


@router.delete("/{notif_id}", response_model=NotificationResponse)
@limiter.limit("5/minute")
async def delete_notification_route(
        request: Request,
        notif_id: str,
        db: Database = Depends(get_db),
        user_id: str = Depends(get_current_user)
):
    return delete_notification(db, notif_id, user_id, request.client.host)
