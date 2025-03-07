from fastapi import APIRouter, Depends, Request
from pymongo.database import Database
from app.dependencies.db import get_db
from schemas.user.create import UserCreateRequest
from schemas.user.response import UserResponse
from services.users.create import create_user
from slowapi import Limiter
from slowapi.util import get_remote_address

router = APIRouter()
limiter = Limiter(key_func=get_remote_address)

@router.post("", response_model=UserResponse)
@limiter.limit("5/minute")
async def create_user_route(
    request: Request,
    user_request: UserCreateRequest,
    db: Database = Depends(get_db)
):
    return create_user(db, user_request, request.client.host)