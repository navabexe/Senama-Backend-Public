from bson import ObjectId
from pymongo.database import Database

from core.errors import APIException
from core.utils.db import map_db_to_response
from schemas.collaboration.response import CollaborationResponse
from schemas.pagination import PaginatedResponse
from services.log.log import create_log


def get_collaboration(db: Database, collab_id: str, vendor_id: str, ip_address: str) -> CollaborationResponse:
    try:
        collaboration = db.collaborations.find_one({"_id": ObjectId(collab_id)})
    except ValueError:
        raise APIException("INVALID_ID", "Invalid collaboration ID format")

    if not collaboration:
        raise APIException("VENDOR_NOT_FOUND", "Collaboration not found")

    if collaboration["requester_id"] != vendor_id and collaboration["target_id"] != vendor_id:
        raise APIException("FORBIDDEN", "You are not part of this collaboration")

    create_log(db, "read", "collaboration", collab_id, vendor_id, None, None, ip_address)

    return map_db_to_response(collaboration, CollaborationResponse)


def get_collaborations(db: Database, vendor_id: str, limit: int, offset: int, ip_address: str) -> PaginatedResponse[
    CollaborationResponse]:
    collaborations = db.collaborations.find({
        "$or": [
            {"requester_id": vendor_id},
            {"target_id": vendor_id}
        ]
    }).skip(offset).limit(limit)

    total = db.collaborations.count_documents({
        "$or": [
            {"requester_id": vendor_id},
            {"target_id": vendor_id}
        ]
    })

    items = [CollaborationResponse(**collab) for collab in collaborations]

    create_log(db, "read", "collaboration", "list", vendor_id, None, None, ip_address)

    return PaginatedResponse[CollaborationResponse](
        items=items,
        total=total,
        limit=limit,
        offset=offset
    )
