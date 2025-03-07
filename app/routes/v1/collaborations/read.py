from fastapi import APIRouter, Depends, Request
from pymongo.database import Database
from slowapi import Limiter
from slowapi.util import get_remote_address

from app.dependencies.auth import get_current_vendor
from app.dependencies.db import get_db
from schemas.collaboration.response import CollaborationResponse
from schemas.pagination import PaginationParams, PaginatedResponse
from services.collaborations.read import get_collaboration, get_collaborations

router = APIRouter()
limiter = Limiter(key_func=get_remote_address)


@router.get("/{collab_id}", response_model=CollaborationResponse)
@limiter.limit("10/minute")
async def read_collaboration(
        request: Request,
        collab_id: str,
        db: Database = Depends(get_db),
        vendor_id: str = Depends(get_current_vendor)
):
    return get_collaboration(db, collab_id, vendor_id, request.client.host)


@router.get("", response_model=PaginatedResponse[CollaborationResponse])
@limiter.limit("10/minute")
async def read_collaborations_list(
        request: Request,
        pagination: PaginationParams = Depends(),
        db: Database = Depends(get_db),
        vendor_id: str = Depends(get_current_vendor)
):
    return get_collaborations(db, vendor_id, pagination.limit, pagination.offset, request.client.host)
