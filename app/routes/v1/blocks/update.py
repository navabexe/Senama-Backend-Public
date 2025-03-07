from fastapi import APIRouter, Depends, Request
from pymongo.database import Database
from slowapi import Limiter
from slowapi.util import get_remote_address

from app.dependencies.auth import get_current_user
from app.dependencies.db import get_db
from schemas.block.response import BlockResponse
from schemas.block.update import BlockUpdateRequest
from services.blocks.update import update_block

router = APIRouter()
limiter = Limiter(key_func=get_remote_address)


@router.put("/{block_id}", response_model=BlockResponse)
@limiter.limit("5/minute")
async def update_block_route(
        request: Request,
        block_id: str,
        block_request: BlockUpdateRequest,
        db: Database = Depends(get_db),
        user_id: str = Depends(get_current_user)
):
    return update_block(db, block_id, block_request, user_id, request.client.host)
