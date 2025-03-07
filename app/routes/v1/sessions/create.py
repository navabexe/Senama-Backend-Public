from fastapi import APIRouter, Depends, Request
from pymongo.database import Database
from slowapi import Limiter
from slowapi.util import get_remote_address

from app.dependencies.auth import get_admin_user
from app.dependencies.db import get_db
from schemas.session.create import SessionCreateRequest
from schemas.session.response import SessionResponse
from services.sessions.create import create_session

router = APIRouter()
limiter = Limiter(key_func=get_remote_address)


@router.post("", response_model=SessionResponse)
@limiter.limit("5/minute")
async def create_session_route(
        request: Request,
        session_request: SessionCreateRequest,
        db: Database = Depends(get_db),
        admin_id: str = Depends(get_admin_user)
):
    return create_session(db, session_request, admin_id, request.client.host)
