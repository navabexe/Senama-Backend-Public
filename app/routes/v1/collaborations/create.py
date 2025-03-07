from fastapi import APIRouter, Depends, Request
from pymongo.database import Database
from slowapi import Limiter
from slowapi.util import get_remote_address

from app.dependencies.auth import get_current_vendor
from app.dependencies.db import get_db
from schemas.collaboration.create import CollaborationCreateRequest
from schemas.collaboration.response import CollaborationResponse
from services.collaborations.create import create_collaboration

router = APIRouter()
limiter = Limiter(key_func=get_remote_address)


@router.post("", response_model=CollaborationResponse)
@limiter.limit("5/minute")
async def create_collaboration_route(
        request: Request,
        collab_request: CollaborationCreateRequest,
        db: Database = Depends(get_db),
        vendor_id: str = Depends(get_current_vendor)
):
    return create_collaboration(db, collab_request, vendor_id, request.client.host)
