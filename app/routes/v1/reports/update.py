from fastapi import APIRouter, Depends, Request
from pymongo.database import Database
from slowapi import Limiter
from slowapi.util import get_remote_address

from app.dependencies.auth import get_admin_user
from app.dependencies.db import get_db
from schemas.report.response import ReportResponse
from schemas.report.update import ReportUpdateRequest
from services.reports.update import update_report

router = APIRouter()
limiter = Limiter(key_func=get_remote_address)


@router.put("/{report_id}", response_model=ReportResponse)
@limiter.limit("5/minute")
async def update_report_route(
        request: Request,
        report_id: str,
        report_request: ReportUpdateRequest,
        db: Database = Depends(get_db),
        admin_id: str = Depends(get_admin_user)
):
    return update_report(db, report_id, report_request, admin_id, request.client.host)
