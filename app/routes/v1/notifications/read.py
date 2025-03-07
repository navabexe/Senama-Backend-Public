from fastapi import APIRouter, Depends, Request
from pymongo.database import Database
from slowapi import Limiter
from slowapi.util import get_remote_address

from app.dependencies.auth import get_current_user
from app.dependencies.db import get_db
from schemas.notification.response import NotificationResponse
from schemas.pagination import PaginationParams, PaginatedResponse
from services.notifications.read import get_notification, get_notifications

router = APIRouter()
limiter = Limiter(key_func=get_remote_address)


@router.get("/{notif_id}", response_model=NotificationResponse)
@limiter.limit("10/minute")
async def read_notification(
        request: Request,
        notif_id: str,
        db: Database = Depends(get_db),
        user_id: str = Depends(get_current_user)
):
    return get_notification(db, notif_id, user_id, request.client.host)


@router.get("", response_model=PaginatedResponse[NotificationResponse])
@limiter.limit("10/minute")
async def read_notifications_list(
        request: Request,
        pagination: PaginationParams = Depends(),
        db: Database = Depends(get_db),
        user_id: str = Depends(get_current_user)
):
    return get_notifications(db, user_id, pagination.limit, pagination.offset, request.client.host)
