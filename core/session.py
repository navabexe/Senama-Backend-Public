from datetime import datetime, timedelta, timezone

from pymongo.database import Database

from core.auth.jwt import create_access_token, create_refresh_token
from core.errors import APIException
from models.session import Session


def create_session(db: Database, user_id: str, role: str, device_info: str, ip_address: str) -> Session:
    access_token = create_access_token({"sub": user_id, "entity_type": "user", "role": role})
    refresh_token = create_refresh_token({"sub": user_id, "entity_type": "user", "role": role})
    session = Session(
        user_id=user_id,
        access_token=access_token,
        refresh_token=refresh_token,
        device_info=device_info,
        ip_address=ip_address,
        role=role,
        created_at=datetime.now(timezone.utc).isoformat(),
        expires_at=(datetime.now(timezone.utc) + timedelta(days=7)).isoformat()
    )
    result = db.sessions.insert_one(session.model_dump(exclude={"id"}))
    session.id = str(result.inserted_id)  
    return session

def delete_session(db: Database, refresh_token: str):
    db.sessions.delete_one({"refresh_token": refresh_token})

def refresh_session(db: Database, refresh_token: str) -> Session:
    session = db.sessions.find_one({"refresh_token": refresh_token})
    if not session or datetime.fromisoformat(session["expires_at"]) < datetime.now(timezone.utc):
        raise APIException("UNAUTHORIZED", "Session expired or invalid", status_code=401)
    new_access_token = create_access_token({"sub": session["user_id"], "entity_type": "user", "role": session.get("role")})
    db.sessions.update_one(
        {"refresh_token": refresh_token},
        {"$set": {"access_token": new_access_token}}
    )
    return Session(**{**session, "access_token": new_access_token})