from fastapi import APIRouter, Depends, Request
from pymongo.database import Database
from slowapi import Limiter
from slowapi.util import get_remote_address

from app.dependencies.auth import get_admin_user
from app.dependencies.db import get_db
from schemas.transaction.response import TransactionResponse
from schemas.transaction.update import TransactionUpdateRequest
from services.wallet.transactions.update import update_transaction

router = APIRouter()
limiter = Limiter(key_func=get_remote_address)


@router.put("/{trans_id}", response_model=TransactionResponse)
@limiter.limit("5/minute")
async def update_transaction_route(
        request: Request,
        trans_id: str,
        trans_request: TransactionUpdateRequest,
        db: Database = Depends(get_db),
        admin_id: str = Depends(get_admin_user)
):
    return update_transaction(db, trans_id, trans_request, admin_id, request.client.host)
