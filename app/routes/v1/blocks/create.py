from fastapi import APIRouter, Depends, Request
from pymongo.database import Database
from slowapi import Limiter
from slowapi.util import get_remote_address

from app.dependencies.auth import get_current_user
from app.dependencies.db import get_db
from schemas.block.create import BlockCreateRequest
from schemas.block.response import BlockResponse
from services.blocks.create import create_block

router = APIRouter()
limiter = Limiter(key_func=get_remote_address)


@router.post("", response_model=BlockResponse)
@limiter.limit("5/minute")
async def create_block_route(
        request: Request,
        block_request: BlockCreateRequest,
        db: Database = Depends(get_db),
        user_id: str = Depends(get_current_user)
):
    return create_block(db, block_request, user_id, request.client.host)
