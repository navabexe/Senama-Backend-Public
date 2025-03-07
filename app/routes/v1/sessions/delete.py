from fastapi import APIRouter, Depends, Request
from pymongo.database import Database
from slowapi import Limiter
from slowapi.util import get_remote_address

from app.dependencies.auth import get_current_user
from app.dependencies.db import get_db
from schemas.session.response import SessionResponse
from services.sessions.delete import delete_session

router = APIRouter()
limiter = Limiter(key_func=get_remote_address)


@router.delete("/{session_id}", response_model=SessionResponse)
@limiter.limit("5/minute")
async def delete_session_route(
        request: Request,
        session_id: str,
        db: Database = Depends(get_db),
        user_id: str = Depends(get_current_user)
):
    return delete_session(db, session_id, user_id, request.client.host)
