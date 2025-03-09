from datetime import datetime, timezone

from bson import ObjectId
from pymongo.database import Database

from core.errors import APIException
from core.validators import Validators
from models.collaboration import Collaboration
from schemas.collaboration.create import CollaborationCreateRequest
from schemas.collaboration.response import CollaborationResponse
from services.log import create_log


def create_collaboration(db: Database, request: CollaborationCreateRequest, vendor_id: str,
                         ip_address: str) -> CollaborationResponse:
    Validators.validate_not_null(request.target_id, "target_id")

    if vendor_id == request.target_id:
        raise APIException("FORBIDDEN", "Cannot collaborate with yourself")

    if not db.vendors.find_one({"_id": ObjectId(vendor_id)}):
        raise APIException("VENDOR_NOT_FOUND", "Requesting vendor not found")

    try:
        target_vendor = db.vendors.find_one({"_id": ObjectId(request.target_id)})
        if not target_vendor:
            raise APIException("VENDOR_NOT_FOUND", "Target vendor not found")
    except ValueError:
        raise APIException("INVALID_ID", "Invalid target vendor ID format")

    existing_collab = db.collaborations.find_one({
        "requester_id": vendor_id,
        "target_id": request.target_id
    })
    if existing_collab:
        raise APIException("FORBIDDEN", "Collaboration request already exists")

    collaboration = Collaboration(
        requester_id=vendor_id,
        target_id=request.target_id,
        status="pending",
        created_at=datetime.now(timezone.utc).isoformat()
    )

    result = db.collaborations.insert_one(collaboration.model_dump(exclude={"id"}))
    collab_id = str(result.inserted_id)

    create_log(db, "create", "collaboration", collab_id, vendor_id, None, collaboration.model_dump(exclude={"id"}),
               ip_address)

    return CollaborationResponse(
        id=collab_id,
        requester_id=collaboration.requester_id,
        target_id=collaboration.target_id,
        status=collaboration.status,
        created_at=collaboration.created_at
    )
