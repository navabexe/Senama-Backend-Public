from bson import ObjectId
from pymongo.database import Database

from core.errors import APIException
from core.utils.db import map_db_to_response
from schemas.pagination import PaginatedResponse
from schemas.session.response import SessionResponse
from services.log import create_log


def get_session(db: Database, session_id: str, user_id: str, ip_address: str) -> SessionResponse:
    try:
        session = db.sessions.find_one({"_id": ObjectId(session_id)})
    except ValueError:
        raise APIException("INVALID_ID", "Invalid session ID format")

    if not session:
        raise APIException("NOT_FOUND", "Session not found")

    if session["entity_id"] != user_id:
        raise APIException("FORBIDDEN", "You can only view your own sessions")

    create_log(db, "read", "session", session_id, user_id, None, None, ip_address)
    return map_db_to_response(session, SessionResponse)


def get_sessions(db: Database, user_id: str, limit: int, offset: int, ip_address: str) -> PaginatedResponse[
    SessionResponse]:
    sessions = db.sessions.find({"entity_id": user_id}).skip(offset).limit(limit)
    total = db.sessions.count_documents({"entity_id": user_id})
    items = [map_db_to_response(session, SessionResponse) for session in sessions]

    create_log(db, "read", "session", "list", user_id, None, None, ip_address)
    return PaginatedResponse[SessionResponse](
        items=items,
        total=total,
        limit=limit,
        offset=offset
    )