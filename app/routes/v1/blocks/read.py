from fastapi import APIRouter, Depends, Request
from pymongo.database import Database
from slowapi import Limiter
from slowapi.util import get_remote_address

from app.dependencies.auth import get_current_user
from app.dependencies.db import get_db
from schemas.block.response import BlockResponse
from schemas.pagination import PaginationParams, PaginatedResponse
from services.blocks.read import get_block, get_blocks

router = APIRouter()
limiter = Limiter(key_func=get_remote_address)


@router.get("/{block_id}", response_model=BlockResponse)
@limiter.limit("10/minute")
async def read_block(
        request: Request,
        block_id: str,
        db: Database = Depends(get_db),
        user_id: str = Depends(get_current_user)
):
    return get_block(db, block_id, user_id, request.client.host)


@router.get("", response_model=PaginatedResponse[BlockResponse])
@limiter.limit("10/minute")
async def read_blocks_list(
        request: Request,
        pagination: PaginationParams = Depends(),
        db: Database = Depends(get_db),
        user_id: str = Depends(get_current_user)
):
    return get_blocks(db, user_id, pagination.limit, pagination.offset, request.client.host)
