import secrets
from datetime import datetime, UTC, timedelta

from pymongo.database import Database

from core.auth.jwt import create_access_token
from core.errors import APIException
from models.session import Session  # اضافه کردن ایمپورت


def create_session(db: Database, user_id: str, device_info: str, ip_address: str) -> Session:
    access_token = create_access_token({"sub": user_id})
    refresh_token = secrets.token_hex(32)
    session = Session(
        user_id=user_id,
        access_token=access_token,
        refresh_token=refresh_token,
        device_info=device_info,
        ip_address=ip_address,
        created_at=datetime.now(UTC).isoformat(),
        expires_at=(datetime.now(UTC) + timedelta(days=7)).isoformat()
    )
    db.sessions.insert_one(session.model_dump(exclude={"id"}))
    session.id = str(session.model_dump(exclude={"id"}))
    return session


def delete_session(db: Database, refresh_token: str):
    db.sessions.delete_one({"refresh_token": refresh_token})


def refresh_session(db: Database, refresh_token: str) -> Session:
    session = db.sessions.find_one({"refresh_token": refresh_token})
    if not session or datetime.fromisoformat(session["expires_at"]) < datetime.now(UTC):
        raise APIException("UNAUTHORIZED", "Session expired or invalid")
    new_access_token = create_access_token({"sub": session["user_id"]})
    db.sessions.update_one(
        {"refresh_token": refresh_token},
        {"$set": {"access_token": new_access_token}}
    )
    return Session(**{**session, "access_token": new_access_token})
