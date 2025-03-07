from bson import ObjectId
from pymongo.database import Database

from core.errors import APIException
from schemas.transaction.response import TransactionResponse
from services.log.log import create_log


def delete_transaction(db: Database, trans_id: str, admin_id: str, ip_address: str) -> TransactionResponse:
    try:
        transaction = db.transactions.find_one({"_id": ObjectId(trans_id)})
    except ValueError:
        raise APIException("INVALID_ID", "Invalid transaction ID format")

    if not transaction:
        raise APIException("VENDOR_NOT_FOUND", "Transaction not found")

    if transaction["status"] == "completed":
        raise APIException("FORBIDDEN", "Cannot delete a completed transaction")

    previous_data = transaction.copy()
    db.transactions.delete_one({"_id": ObjectId(trans_id)})

    create_log(db, "delete", "transaction", trans_id, admin_id, previous_data, None, ip_address)

    return TransactionResponse(**previous_data)
