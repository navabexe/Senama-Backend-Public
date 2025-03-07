from fastapi import APIRouter, Depends, Request
from pymongo.database import Database
from slowapi import Limiter
from slowapi.util import get_remote_address

from app.dependencies.auth import get_admin_user
from app.dependencies.db import get_db
from schemas.notification.create import NotificationCreateRequest
from schemas.notification.response import NotificationResponse
from services.notifications.create import create_notification

router = APIRouter()
limiter = Limiter(key_func=get_remote_address)


@router.post("", response_model=NotificationResponse)
@limiter.limit("5/minute")
async def create_notification_route(
        request: Request,
        notif_request: NotificationCreateRequest,
        db: Database = Depends(get_db),
        admin_id: str = Depends(get_admin_user)
):
    return create_notification(db, notif_request, admin_id, request.client.host)
