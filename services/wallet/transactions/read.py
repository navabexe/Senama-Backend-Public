from bson import ObjectId
from pymongo.database import Database

from core.errors import APIException
from schemas.pagination import PaginatedResponse
from schemas.transaction.response import TransactionResponse
from services.log.log import create_log


def get_transaction(db: Database, trans_id: str, vendor_id: str, ip_address: str) -> TransactionResponse:
    try:
        transaction = db.transactions.find_one({"_id": ObjectId(trans_id), "vendor_id": vendor_id})
    except ValueError:
        raise APIException("INVALID_ID", "Invalid transaction ID format")

    if not transaction:
        raise APIException("VENDOR_NOT_FOUND", "Transaction not found or not owned by you")

    create_log(db, "read", "transaction", trans_id, vendor_id, None, None, ip_address)

    from core.utils.db import map_db_to_response
    return map_db_to_response(transaction, TransactionResponse)


def get_transactions(db: Database, vendor_id: str, limit: int, offset: int, ip_address: str) -> PaginatedResponse[
    TransactionResponse]:
    transactions = db.transactions.find({"vendor_id": vendor_id}).skip(offset).limit(limit)
    total = db.transactions.count_documents({"vendor_id": vendor_id})
    items = [TransactionResponse(**trans) for trans in transactions]

    create_log(db, "read", "transaction", "list", vendor_id, None, None, ip_address)

    return PaginatedResponse[TransactionResponse](
        items=items,
        total=total,
        limit=limit,
        offset=offset
    )
