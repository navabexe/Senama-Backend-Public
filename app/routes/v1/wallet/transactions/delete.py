from fastapi import APIRouter, Depends, Request
from pymongo.database import Database
from slowapi import Limiter
from slowapi.util import get_remote_address

from app.dependencies.auth import get_admin_user
from app.dependencies.db import get_db
from schemas.transaction.response import TransactionResponse
from services.wallet.transactions.delete import delete_transaction

router = APIRouter()
limiter = Limiter(key_func=get_remote_address)


@router.delete("/{trans_id}", response_model=TransactionResponse)
@limiter.limit("5/minute")
async def delete_transaction_route(
        request: Request,
        trans_id: str,
        db: Database = Depends(get_db),
        admin_id: str = Depends(get_admin_user)
):
    return delete_transaction(db, trans_id, admin_id, request.client.host)
