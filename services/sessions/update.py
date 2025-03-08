from pymongo.database import Database
from schemas.session.update import SessionUpdateRequest
from schemas.session.response import SessionResponse
from core.errors import APIException
from services.log import create_log
from core.utils.db import map_db_to_response
from bson import ObjectId
from datetime import datetime, UTC


def update_session(db: Database, session_id: str, request: SessionUpdateRequest, user_id: str,
                   ip_address: str) -> SessionResponse:
    try:
        session = db.sessions.find_one({"_id": ObjectId(session_id), "entity_id": user_id})
    except ValueError:
        raise APIException("INVALID_ID", "Invalid session ID format")

    if not session:
        raise APIException("NOT_FOUND", "Session not found or not owned by you")

    update_data = request.dict(exclude_unset=True)
    update_data["updated_at"] = datetime.now(UTC).isoformat()

    previous_data = session.copy()
    db.sessions.update_one({"_id": ObjectId(session_id)}, {"$set": update_data})
    updated_session = db.sessions.find_one({"_id": ObjectId(session_id)})

    create_log(db, "update", "session", session_id, user_id, previous_data, updated_session, ip_address)
    return map_db_to_response(updated_session, SessionResponse)