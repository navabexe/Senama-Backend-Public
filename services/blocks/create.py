from datetime import datetime, UTC

from bson import ObjectId
from pymongo.database import Database

from core.errors import APIException
from core.validators import Validators
from models.block import Block
from schemas.block.create import BlockCreateRequest
from schemas.block.response import BlockResponse
from services.log import create_log


def create_block(db: Database, request: BlockCreateRequest, user_id: str, ip_address: str) -> BlockResponse:
    Validators.validate_not_null(request.blocked_id, "blocked_id")

    if user_id == request.blocked_id:
        raise APIException("FORBIDDEN", "Cannot block yourself")

    try:
        if not db.vendors.find_one({"_id": ObjectId(user_id)}) and not db.users.find_one({"_id": ObjectId(user_id)}):
            raise APIException("VENDOR_NOT_FOUND", "User not found")
        if not db.vendors.find_one({"_id": ObjectId(request.blocked_id)}) and not db.users.find_one(
                {"_id": ObjectId(request.blocked_id)}):
            raise APIException("VENDOR_NOT_FOUND", "Blocked user not found")
    except ValueError:
        raise APIException("INVALID_ID", "Invalid ID format")

    existing_block = db.blocks.find_one({"user_id": user_id, "blocked_id": request.blocked_id})
    if existing_block:
        raise APIException("FORBIDDEN", "User already blocked")

    block = Block(
        user_id=user_id,
        blocked_id=request.blocked_id,
        created_at=datetime.now(UTC).isoformat()
    )

    result = db.blocks.insert_one(block.dict(exclude={"id"}))
    block_id = str(result.inserted_id)

    create_log(db, "create", "block", block_id, user_id, None, block.dict(exclude={"id"}), ip_address)

    return BlockResponse(
        id=block_id,
        user_id=block.user_id,
        blocked_id=block.blocked_id,
        created_at=block.created_at
    )
