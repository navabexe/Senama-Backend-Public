from fastapi import APIRouter, Depends, Request
from pymongo.database import Database
from slowapi import Limiter
from slowapi.util import get_remote_address

from app.dependencies.auth import get_current_user
from app.dependencies.db import get_db
from schemas.user.response import UserResponse
from schemas.user.update import UserUpdateRequest
from services.users.update import update_user

router = APIRouter()
limiter = Limiter(key_func=get_remote_address)

@router.put("/me", response_model=UserResponse)
@limiter.limit("5/minute")
async def update_user_route(
    request: Request,
    user_request: UserUpdateRequest,
    db: Database = Depends(get_db),
    user_id: str = Depends(get_current_user)
):
    return update_user(db, user_id, user_request, user_id, request.client.host)