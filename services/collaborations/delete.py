from pymongo.database import Database
from schemas.collaboration.response import CollaborationResponse
from core.errors import APIException
from services.log import create_log
from core.utils.db import map_db_to_response
from bson import ObjectId


def delete_collaboration(db: Database, collab_id: str, user_id: str, ip_address: str) -> CollaborationResponse:
    try:
        collaboration = db.collaborations.find_one({"_id": ObjectId(collab_id)})
    except ValueError:
        raise APIException("INVALID_ID", "Invalid collaboration ID format")

    if not collaboration:
        raise APIException("NOT_FOUND", "Collaboration not found")

    if collaboration["vendor_id"] != user_id and collaboration["collaborator_id"] != user_id:
        raise APIException("FORBIDDEN", "You can only delete your own collaborations")

    if collaboration["status"] == "accepted":
        raise APIException("FORBIDDEN", "Cannot delete an accepted collaboration")

    previous_data = collaboration.copy()
    db.collaborations.delete_one({"_id": ObjectId(collab_id)})

    create_log(db, "delete", "collaboration", collab_id, user_id, previous_data, None, ip_address)
    return map_db_to_response(previous_data, CollaborationResponse)