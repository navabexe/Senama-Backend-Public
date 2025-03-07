from bson import ObjectId
from pymongo.database import Database

from core.errors import APIException
from core.utils.db import map_db_to_response
from schemas.block.response import BlockResponse
from schemas.block.update import BlockUpdateRequest
from services.log.log import create_log


def update_block(db: Database, block_id: str, request: BlockUpdateRequest, user_id: str,
                 ip_address: str) -> BlockResponse:
    try:
        block = db.blocks.find_one({"_id": ObjectId(block_id), "user_id": user_id})
    except ValueError:
        raise APIException("INVALID_ID", "Invalid block ID format")

    if not block:
        raise APIException("VENDOR_NOT_FOUND", "Block not found or not owned by you")

    update_data = request.dict(exclude_unset=True)
    if "blocked_id" in update_data:
        if user_id == update_data["blocked_id"]:
            raise APIException("FORBIDDEN", "Cannot block yourself")
        try:
            if not db.vendors.find_one({"_id": ObjectId(update_data["blocked_id"])}) and not db.users.find_one(
                    {"_id": ObjectId(update_data["blocked_id"])}):
                raise APIException("VENDOR_NOT_FOUND", "Blocked user not found")
        except ValueError:
            raise APIException("INVALID_ID", "Invalid blocked ID format")

    previous_data = block.copy()
    db.blocks.update_one({"_id": ObjectId(block_id)}, {"$set": update_data})
    updated_block = db.blocks.find_one({"_id": ObjectId(block_id)})

    create_log(db, "update", "block", block_id, user_id, previous_data, updated_block, ip_address)

    return map_db_to_response(updated_block, BlockResponse)
