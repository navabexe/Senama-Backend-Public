from fastapi import APIRouter, Depends, Request
from pymongo.database import Database
from slowapi import Limiter
from slowapi.util import get_remote_address

from app.dependencies.auth import get_current_vendor
from app.dependencies.db import get_db
from schemas.collaboration.response import CollaborationResponse
from schemas.collaboration.update import CollaborationUpdateRequest
from services.collaborations.update import update_collaboration

router = APIRouter()
limiter = Limiter(key_func=get_remote_address)


@router.put("/{collab_id}", response_model=CollaborationResponse)
@limiter.limit("5/minute")
async def update_collaboration_route(
        request: Request,
        collab_id: str,
        collab_request: CollaborationUpdateRequest,
        db: Database = Depends(get_db),
        vendor_id: str = Depends(get_current_vendor)
):
    return update_collaboration(db, collab_id, collab_request, vendor_id, request.client.host)
