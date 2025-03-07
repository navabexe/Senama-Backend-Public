from bson import ObjectId
from pymongo.database import Database
from core.utils.db import map_db_to_response
from core.errors import APIException
from schemas.transaction.response import TransactionResponse
from schemas.transaction.update import TransactionUpdateRequest
from services.log.log import create_log


def update_transaction(db: Database, trans_id: str, request: TransactionUpdateRequest, admin_id: str,
                       ip_address: str) -> TransactionResponse:
    try:
        transaction = db.transactions.find_one({"_id": ObjectId(trans_id)})
    except ValueError:
        raise APIException("INVALID_ID", "Invalid transaction ID format")

    if not transaction:
        raise APIException("VENDOR_NOT_FOUND", "Transaction not found")

    update_data = request.dict(exclude_unset=True)
    if "type" in update_data and update_data["type"] not in ["charge", "withdraw", "ad_payment"]:
        raise APIException("INVALID_ID", "Invalid transaction type")
    if "amount" in update_data and update_data["amount"] <= 0:
        raise APIException("INVALID_AMOUNT", "Amount must be positive")
    if "status" in update_data and update_data["status"] not in ["pending", "completed", "failed"]:
        raise APIException("INVALID_ID", "Invalid status value")

    previous_data = transaction.copy()
    db.transactions.update_one({"_id": ObjectId(trans_id)}, {"$set": update_data})
    updated_transaction = db.transactions.find_one({"_id": ObjectId(trans_id)})

    create_log(db, "update", "transaction", trans_id, admin_id, previous_data, updated_transaction, ip_address)
    return map_db_to_response(updated_transaction, TransactionResponse)

