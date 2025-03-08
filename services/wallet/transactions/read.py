from pymongo.database import Database
from schemas.transaction.response import TransactionResponse
from schemas.pagination import PaginatedResponse
from services.log import create_log
from core.errors import APIException
from core.utils.db import map_db_to_response
from bson import ObjectId


def get_transaction(db: Database, transaction_id: str, user_id: str, ip_address: str) -> TransactionResponse:
    try:
        transaction = db.transactions.find_one({"_id": ObjectId(transaction_id)})
    except ValueError:
        raise APIException("INVALID_ID", "Invalid transaction ID format")

    if not transaction:
        raise APIException("NOT_FOUND", "Transaction not found")

    if transaction["entity_id"] != user_id:
        raise APIException("FORBIDDEN", "You can only view your own transactions")

    create_log(db, "read", "transaction", transaction_id, user_id, None, None, ip_address)
    return map_db_to_response(transaction, TransactionResponse)


def get_transactions(db: Database, user_id: str, limit: int, offset: int, ip_address: str) -> PaginatedResponse[
    TransactionResponse]:
    transactions = db.transactions.find({"entity_id": user_id}).skip(offset).limit(limit)
    total = db.transactions.count_documents({"entity_id": user_id})
    items = [map_db_to_response(transaction, TransactionResponse) for transaction in transactions]

    create_log(db, "read", "transaction", "list", user_id, None, None, ip_address)
    return PaginatedResponse[TransactionResponse](
        items=items,
        total=total,
        limit=limit,
        offset=offset
    )