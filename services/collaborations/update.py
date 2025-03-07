from bson import ObjectId
from pymongo.database import Database

from core.errors import APIException
from core.utils.db import map_db_to_response
from schemas.collaboration.response import CollaborationResponse
from schemas.collaboration.update import CollaborationUpdateRequest
from services.log.log import create_log


def update_collaboration(db: Database, collab_id: str, request: CollaborationUpdateRequest, vendor_id: str,
                         ip_address: str) -> CollaborationResponse:
    try:
        collaboration = db.collaborations.find_one({"_id": ObjectId(collab_id)})
    except ValueError:
        raise APIException("INVALID_ID", "Invalid collaboration ID format")

    if not collaboration:
        raise APIException("VENDOR_NOT_FOUND", "Collaboration not found")

    if collaboration["target_id"] != vendor_id:
        raise APIException("FORBIDDEN", "Only the target vendor can update collaboration status")

    if collaboration["status"] != "pending":
        raise APIException("FORBIDDEN", "Collaboration status already finalized")

    update_data = request.dict(exclude_unset=True)
    if "status" in update_data and update_data["status"] not in ["approved", "rejected"]:
        raise APIException("INVALID_ID", "Status must be 'approved' or 'rejected'")

    previous_data = collaboration.copy()
    db.collaborations.update_one({"_id": ObjectId(collab_id)}, {"$set": update_data})
    updated_collaboration = db.collaborations.find_one({"_id": ObjectId(collab_id)})

    create_log(db, "update", "collaboration", collab_id, vendor_id, previous_data, updated_collaboration, ip_address)

    if updated_collaboration["status"] == "approved":
        db.vendors.update_one(
            {"_id": ObjectId(updated_collaboration["requester_id"])},
            {"$addToSet": {"attached_vendors": updated_collaboration["target_id"]}}
        )

    return map_db_to_response(updated_collaboration, CollaborationResponse)
