from bson import ObjectId
from pymongo.database import Database

from core.errors import APIException
from core.utils.db import map_db_to_response
from schemas.session.response import SessionResponse
from schemas.session.update import SessionUpdateRequest
from services.log.log import create_log


def update_session(db: Database, session_id: str, request: SessionUpdateRequest, user_id: str,
                   ip_address: str) -> SessionResponse:
    try:
        session = db.sessions.find_one({"_id": ObjectId(session_id), "user_id": user_id})
    except ValueError:
        raise APIException("INVALID_ID", "Invalid session ID format")

    if not session:
        raise APIException("VENDOR_NOT_FOUND", "Session not found or not owned by you")

    update_data = request.dict(exclude_unset=True)
    if "access_token" in update_data:
        existing_session = db.sessions.find_one(
            {"access_token": update_data["access_token"], "_id": {"$ne": ObjectId(session_id)}})
        if existing_session:
            raise APIException("FORBIDDEN", "Access token already in use")

    previous_data = session.copy()
    db.sessions.update_one({"_id": ObjectId(session_id)}, {"$set": update_data})
    updated_session = db.sessions.find_one({"_id": ObjectId(session_id)})

    create_log(db, "update", "session", session_id, user_id, previous_data, updated_session, ip_address)

    return map_db_to_response(updated_session, SessionResponse)
