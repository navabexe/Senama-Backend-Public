from fastapi import APIRouter, Depends, Request
from pymongo.database import Database
from slowapi import Limiter
from slowapi.util import get_remote_address

from app.dependencies.auth import get_current_vendor
from app.dependencies.db import get_db
from schemas.pagination import PaginationParams, PaginatedResponse
from schemas.transaction.response import TransactionResponse
from services.wallet.transactions.read import get_transaction, get_transactions

router = APIRouter()
limiter = Limiter(key_func=get_remote_address)


@router.get("/{trans_id}", response_model=TransactionResponse)
@limiter.limit("10/minute")
async def read_transaction(
        request: Request,
        trans_id: str,
        db: Database = Depends(get_db),
        vendor_id: str = Depends(get_current_vendor)
):
    return get_transaction(db, trans_id, vendor_id, request.client.host)


@router.get("", response_model=PaginatedResponse[TransactionResponse])
@limiter.limit("10/minute")
async def read_transactions_list(
        request: Request,
        pagination: PaginationParams = Depends(),
        db: Database = Depends(get_db),
        vendor_id: str = Depends(get_current_vendor)
):
    return get_transactions(db, vendor_id, pagination.limit, pagination.offset, request.client.host)
