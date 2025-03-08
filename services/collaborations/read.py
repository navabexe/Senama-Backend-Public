from pymongo.database import Database
from schemas.collaboration.response import CollaborationResponse
from schemas.pagination import PaginatedResponse
from services.log import create_log
from core.errors import APIException
from core.utils.db import map_db_to_response
from bson import ObjectId


def get_collaboration(db: Database, collab_id: str, user_id: str, ip_address: str) -> CollaborationResponse:
    try:
        collaboration = db.collaborations.find_one({"_id": ObjectId(collab_id)})
    except ValueError:
        raise APIException("INVALID_ID", "Invalid collaboration ID format")

    if not collaboration:
        raise APIException("NOT_FOUND", "Collaboration not found")

    if collaboration["vendor_id"] != user_id and collaboration["collaborator_id"] != user_id:
        raise APIException("FORBIDDEN", "You can only view your own collaborations")

    create_log(db, "read", "collaboration", collab_id, user_id, None, None, ip_address)
    return map_db_to_response(collaboration, CollaborationResponse)


def get_collaborations(db: Database, user_id: str, limit: int, offset: int, ip_address: str) -> PaginatedResponse[
    CollaborationResponse]:
    query = {"$or": [{"vendor_id": user_id}, {"collaborator_id": user_id}]}
    collaborations = db.collaborations.find(query).skip(offset).limit(limit)
    total = db.collaborations.count_documents(query)
    items = [map_db_to_response(collab, CollaborationResponse) for collab in collaborations]

    create_log(db, "read", "collaboration", "list", user_id, None, None, ip_address)
    return PaginatedResponse[CollaborationResponse](
        items=items,
        total=total,
        limit=limit,
        offset=offset
    )