from datetime import datetime, timezone

from bson import ObjectId
from pymongo.database import Database

from core.errors import APIException
from core.validators import Validators
from models.transaction import Transaction
from schemas.transaction.create import TransactionCreateRequest
from schemas.transaction.response import TransactionResponse
from services.log import create_log


def create_transaction(db: Database, request: TransactionCreateRequest, vendor_id: str,
                       ip_address: str) -> TransactionResponse:
    Validators.validate_not_null(request.type, "type")
    Validators.validate_not_null(request.amount, "amount")

    if request.type not in ["charge", "withdraw", "ad_payment"]:
        raise APIException("INVALID_ID", "Invalid transaction type")
    if request.amount <= 0:
        raise APIException("INVALID_AMOUNT", "Amount must be positive")

    if not db.vendors.find_one({"_id": ObjectId(vendor_id)}):
        raise APIException("VENDOR_NOT_FOUND", "Vendor not found")

    transaction = Transaction(
        vendor_id=vendor_id,
        type=request.type,
        amount=request.amount,
        status="pending",
        created_at=datetime.now(timezone.utc).isoformat()
    )

    result = db.transactions.insert_one(transaction.model_dump(exclude={"id"}))
    trans_id = str(result.inserted_id)

    create_log(db, "create", "transaction", trans_id, vendor_id, None, transaction.model_dump(exclude={"id"}), ip_address)

    return TransactionResponse(
        id=trans_id,
        vendor_id=transaction.vendor_id,
        type=transaction.type,
        amount=transaction.amount,
        status=transaction.status,
        created_at=transaction.created_at
    )
