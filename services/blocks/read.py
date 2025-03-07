from bson import ObjectId
from pymongo.database import Database

from core.errors import APIException
from core.utils.db import map_db_to_response
from schemas.block.response import BlockResponse
from schemas.pagination import PaginatedResponse
from services.log.log import create_log


def get_block(db: Database, block_id: str, user_id: str, ip_address: str) -> BlockResponse:
    try:
        block = db.blocks.find_one({"_id": ObjectId(block_id), "user_id": user_id})
    except ValueError:
        raise APIException("INVALID_ID", "Invalid block ID format")

    if not block:
        raise APIException("VENDOR_NOT_FOUND", "Block not found or not owned by you")

    create_log(db, "read", "block", block_id, user_id, None, None, ip_address)

    return map_db_to_response(block, BlockResponse)


def get_blocks(db: Database, user_id: str, limit: int, offset: int, ip_address: str) -> PaginatedResponse[
    BlockResponse]:
    blocks = db.blocks.find({"user_id": user_id}).skip(offset).limit(limit)
    total = db.blocks.count_documents({"user_id": user_id})
    items = [BlockResponse(**block) for block in blocks]

    create_log(db, "read", "block", "list", user_id, None, None, ip_address)

    return PaginatedResponse[BlockResponse](
        items=items,
        total=total,
        limit=limit,
        offset=offset
    )
