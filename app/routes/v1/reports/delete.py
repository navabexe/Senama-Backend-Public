from fastapi import APIRouter, Depends, Request
from pymongo.database import Database
from slowapi import Limiter
from slowapi.util import get_remote_address

from app.dependencies.auth import get_admin_user
from app.dependencies.db import get_db
from schemas.report.response import ReportResponse
from services.reports.delete import delete_report

router = APIRouter()
limiter = Limiter(key_func=get_remote_address)


@router.delete("/{report_id}", response_model=ReportResponse)
@limiter.limit("5/minute")
async def delete_report_route(
        request: Request,
        report_id: str,
        db: Database = Depends(get_db),
        admin_id: str = Depends(get_admin_user)
):
    return delete_report(db, report_id, admin_id, request.client.host)
