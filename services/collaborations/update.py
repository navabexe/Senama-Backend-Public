from pymongo.database import Database
from schemas.collaboration.update import CollaborationUpdateRequest
from schemas.collaboration.response import CollaborationResponse
from core.errors import APIException
from services.log import create_log
from core.utils.db import map_db_to_response
from bson import ObjectId
from datetime import datetime, UTC


def update_collaboration(db: Database, collab_id: str, request: CollaborationUpdateRequest, user_id: str,
                         ip_address: str) -> CollaborationResponse:
    try:
        collaboration = db.collaborations.find_one({"_id": ObjectId(collab_id)})
    except ValueError:
        raise APIException("INVALID_ID", "Invalid collaboration ID format")

    if not collaboration:
        raise APIException("NOT_FOUND", "Collaboration not found")

    if collaboration["vendor_id"] != user_id and collaboration["collaborator_id"] != user_id:
        raise APIException("FORBIDDEN", "You can only update your own collaborations")

    update_data = request.dict(exclude_unset=True)
    if "status" in update_data and update_data["status"] not in ["pending", "accepted", "rejected"]:
        raise APIException("INVALID_ID", "Invalid status value")
    update_data["updated_at"] = datetime.now(UTC).isoformat()

    previous_data = collaboration.copy()
    db.collaborations.update_one({"_id": ObjectId(collab_id)}, {"$set": update_data})
    updated_collaboration = db.collaborations.find_one({"_id": ObjectId(collab_id)})

    create_log(db, "update", "collaboration", collab_id, user_id, previous_data, updated_collaboration, ip_address)
    return map_db_to_response(updated_collaboration, CollaborationResponse)