from fastapi import APIRouter, Depends, Request
from pymongo.database import Database
from slowapi import Limiter
from slowapi.util import get_remote_address

from app.dependencies.auth import get_current_user
from app.dependencies.db import get_db
from schemas.block.response import BlockResponse
from services.blocks.delete import delete_block

router = APIRouter()
limiter = Limiter(key_func=get_remote_address)


@router.delete("/{block_id}", response_model=BlockResponse)
@limiter.limit("5/minute")
async def delete_block_route(
        request: Request,
        block_id: str,
        db: Database = Depends(get_db),
        user_id: str = Depends(get_current_user)
):
    return delete_block(db, block_id, user_id, request.client.host)
