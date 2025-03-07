from fastapi import APIRouter, Depends, Request
from pymongo.database import Database
from app.dependencies.db import get_db
from app.dependencies.auth import get_admin_user  # عوض شده از get_current_user
from schemas.user.response import UserResponse
from services.users.delete import delete_user
from slowapi import Limiter
from slowapi.util import get_remote_address

router = APIRouter()
limiter = Limiter(key_func=get_remote_address)

@router.delete("/{user_id}", response_model=UserResponse)
@limiter.limit("5/minute")
async def delete_user_route(
    request: Request,
    user_id: str,
    db: Database = Depends(get_db),
    admin_id: str = Depends(get_admin_user)
):
    return delete_user(db, user_id, admin_id, request.client.host)