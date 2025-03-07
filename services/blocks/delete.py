from bson import ObjectId
from pymongo.database import Database

from core.errors import APIException
from core.utils.db import map_db_to_response
from schemas.block.response import BlockResponse
from services.log.log import create_log


def delete_block(db: Database, block_id: str, user_id: str, ip_address: str) -> BlockResponse:
    try:
        block = db.blocks.find_one({"_id": ObjectId(block_id), "user_id": user_id})
    except ValueError:
        raise APIException("INVALID_ID", "Invalid block ID format")

    if not block:
        raise APIException("VENDOR_NOT_FOUND", "Block not found or not owned by you")

    previous_data = block.copy()
    db.blocks.delete_one({"_id": ObjectId(block_id)})

    create_log(db, "delete", "block", block_id, user_id, previous_data, None, ip_address)

    return map_db_to_response(block, BlockResponse)
