from bson import ObjectId
from pymongo.database import Database

from core.errors import APIException
from core.utils.db import map_db_to_response
from schemas.collaboration.response import CollaborationResponse
from services.log.log import create_log


def delete_collaboration(db: Database, collab_id: str, vendor_id: str, ip_address: str) -> CollaborationResponse:
    try:
        collaboration = db.collaborations.find_one({"_id": ObjectId(collab_id)})
    except ValueError:
        raise APIException("INVALID_ID", "Invalid collaboration ID format")

    if not collaboration:
        raise APIException("VENDOR_NOT_FOUND", "Collaboration not found")

    if collaboration["requester_id"] != vendor_id or collaboration["status"] != "pending":
        raise APIException("FORBIDDEN", "Only the requester can delete a pending collaboration")

    previous_data = collaboration.copy()
    db.collaborations.delete_one({"_id": ObjectId(collab_id)})

    create_log(db, "delete", "collaboration", collab_id, vendor_id, previous_data, None, ip_address)

    return map_db_to_response(collaboration, CollaborationResponse)