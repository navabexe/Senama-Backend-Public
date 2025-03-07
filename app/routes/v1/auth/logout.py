from fastapi import APIRouter, Depends
from pymongo.database import Database
from slowapi import Limiter
from slowapi.util import get_remote_address
from starlette.requests import Request

from app.dependencies.auth import get_current_user
from app.dependencies.db import get_db
from core.session import delete_session

router = APIRouter()
limiter = Limiter(key_func=get_remote_address)


@router.post("/logout")
@limiter.limit("5/minute")
async def logout(
        request: Request,
        db: Database = Depends(get_db),
        user_id: str = Depends(get_current_user)
):
    session = db.sessions.find_one(
        {"user_id": user_id, "access_token": request.headers.get("Authorization", "").split("Bearer ")[1]})
    if session:
        delete_session(db, session["refresh_token"])
    return {"message": "Logged out successfully"}
