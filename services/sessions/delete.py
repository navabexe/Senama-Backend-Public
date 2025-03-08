from pymongo.database import Database
from schemas.session.response import SessionResponse
from core.errors import APIException
from services.log import create_log
from core.utils.db import map_db_to_response
from bson import ObjectId


def delete_session(db: Database, session_id: str, user_id: str, ip_address: str) -> SessionResponse:
    try:
        session = db.sessions.find_one({"_id": ObjectId(session_id), "entity_id": user_id})
    except ValueError:
        raise APIException("INVALID_ID", "Invalid session ID format")

    if not session:
        raise APIException("NOT_FOUND", "Session not found or not owned by you")

    previous_data = session.copy()
    db.sessions.delete_one({"_id": ObjectId(session_id)})

    create_log(db, "delete", "session", session_id, user_id, previous_data, None, ip_address)
    return map_db_to_response(previous_data, SessionResponse)