from fastapi import APIRouter, Depends, Request
from pymongo.database import Database
from slowapi import Limiter
from slowapi.util import get_remote_address

from app.dependencies.auth import get_current_user
from app.dependencies.db import get_db
from schemas.pagination import PaginationParams, PaginatedResponse
from schemas.session.response import SessionResponse
from services.sessions.read import get_session, get_sessions

router = APIRouter()
limiter = Limiter(key_func=get_remote_address)


@router.get("/{session_id}", response_model=SessionResponse)
@limiter.limit("10/minute")
async def read_session(
        request: Request,
        session_id: str,
        db: Database = Depends(get_db),
        user_id: str = Depends(get_current_user)
):
    return get_session(db, session_id, user_id, request.client.host)


@router.get("", response_model=PaginatedResponse[SessionResponse])
@limiter.limit("10/minute")
async def read_sessions_list(
        request: Request,
        pagination: PaginationParams = Depends(),
        db: Database = Depends(get_db),
        user_id: str = Depends(get_current_user)
):
    return get_sessions(db, user_id, pagination.limit, pagination.offset, request.client.host)
