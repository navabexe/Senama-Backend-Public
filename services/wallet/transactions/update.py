from datetime import datetime, timezone

from bson import ObjectId
from pymongo.database import Database

from core.errors import APIException
from core.utils.db import map_db_to_response
from schemas.transaction.response import TransactionResponse
from schemas.transaction.update import TransactionUpdateRequest
from services.log import create_log


def update_transaction(db: Database, transaction_id: str, request: TransactionUpdateRequest, admin_id: str,
                       ip_address: str) -> TransactionResponse:
    try:
        transaction = db.transactions.find_one({"_id": ObjectId(transaction_id)})
    except ValueError:
        raise APIException("INVALID_ID", "Invalid transaction ID format")

    if not transaction:
        raise APIException("NOT_FOUND", "Transaction not found")

    update_data = request.model_dump(exclude_unset=True)
    if "status" in update_data and update_data["status"] not in ["pending", "completed", "failed"]:
        raise APIException("INVALID_ID", "Invalid status value")
    update_data["updated_at"] = datetime.now(timezone.utc).isoformat()

    previous_data = transaction.copy()
    db.transactions.update_one({"_id": ObjectId(transaction_id)}, {"$set": update_data})
    updated_transaction = db.transactions.find_one({"_id": ObjectId(transaction_id)})

    create_log(db, "update", "transaction", transaction_id, admin_id, previous_data, updated_transaction, ip_address)
    return map_db_to_response(updated_transaction, TransactionResponse)