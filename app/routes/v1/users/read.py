from fastapi import APIRouter, Depends, Request
from pymongo.database import Database
from slowapi import Limiter
from slowapi.util import get_remote_address

from app.dependencies.auth import get_current_user
from app.dependencies.db import get_db
from schemas.pagination import PaginationParams, PaginatedResponse
from schemas.user.response import UserResponse
from services.users.read import get_user, get_users

router = APIRouter()
limiter = Limiter(key_func=get_remote_address)

@router.get("/me", response_model=UserResponse)
@limiter.limit("10/minute")
async def read_current_user(
    request: Request,
    db: Database = Depends(get_db),
    user_id: str = Depends(get_current_user)
):
    return get_user(db, user_id, user_id, request.client.host)

@router.get("/{user_id}", response_model=UserResponse)
@limiter.limit("10/minute")
async def read_user(
    request: Request,
    user_id: str,
    db: Database = Depends(get_db),
    current_user_id: str = Depends(get_current_user)
):
    return get_user(db, user_id, current_user_id, request.client.host)

@router.get("", response_model=PaginatedResponse[UserResponse])
@limiter.limit("10/minute")
async def read_users_list(
    request: Request,
    pagination: PaginationParams = Depends(),
    db: Database = Depends(get_db),
    user_id: str = Depends(get_current_user)
):
    return get_users(db, user_id, pagination.limit, pagination.offset, request.client.host)