from pymongo.database import Database
from schemas.transaction.response import TransactionResponse
from core.errors import APIException
from services.log import create_log
from core.utils.db import map_db_to_response
from bson import ObjectId


def delete_transaction(db: Database, transaction_id: str, admin_id: str, ip_address: str) -> TransactionResponse:
    try:
        transaction = db.transactions.find_one({"_id": ObjectId(transaction_id)})
    except ValueError:
        raise APIException("INVALID_ID", "Invalid transaction ID format")

    if not transaction:
        raise APIException("NOT_FOUND", "Transaction not found")

    if transaction["status"] == "completed":
        raise APIException("FORBIDDEN", "Cannot delete a completed transaction")

    previous_data = transaction.copy()
    db.transactions.delete_one({"_id": ObjectId(transaction_id)})

    create_log(db, "delete", "transaction", transaction_id, admin_id, previous_data, None, ip_address)
    return map_db_to_response(previous_data, TransactionResponse)