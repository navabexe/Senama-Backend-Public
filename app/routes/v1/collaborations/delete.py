from fastapi import APIRouter, Depends, Request
from pymongo.database import Database
from slowapi import Limiter
from slowapi.util import get_remote_address

from app.dependencies.auth import get_current_vendor
from app.dependencies.db import get_db
from schemas.collaboration.response import CollaborationResponse
from services.collaborations.delete import delete_collaboration

router = APIRouter()
limiter = Limiter(key_func=get_remote_address)


@router.delete("/{collab_id}", response_model=CollaborationResponse)
@limiter.limit("5/minute")
async def delete_collaboration_route(
        request: Request,
        collab_id: str,
        db: Database = Depends(get_db),
        vendor_id: str = Depends(get_current_vendor)
):
    return delete_collaboration(db, collab_id, vendor_id, request.client.host)
