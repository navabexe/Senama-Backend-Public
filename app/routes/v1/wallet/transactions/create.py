from fastapi import APIRouter, Depends, Request
from pymongo.database import Database
from slowapi import Limiter
from slowapi.util import get_remote_address

from app.dependencies.auth import get_current_vendor
from app.dependencies.db import get_db
from schemas.transaction.create import TransactionCreateRequest
from schemas.transaction.response import TransactionResponse
from services.wallet.transactions.create import create_transaction

router = APIRouter()
limiter = Limiter(key_func=get_remote_address)


@router.post("", response_model=TransactionResponse)
@limiter.limit("5/minute")
async def create_transaction_route(
        request: Request,
        trans_request: TransactionCreateRequest,
        db: Database = Depends(get_db),
        vendor_id: str = Depends(get_current_vendor)
):
    return create_transaction(db, trans_request, vendor_id, request.client.host)
