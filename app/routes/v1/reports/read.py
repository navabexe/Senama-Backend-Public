from fastapi import APIRouter, Depends, Request
from pymongo.database import Database
from slowapi import Limiter
from slowapi.util import get_remote_address

from app.dependencies.auth import get_admin_user, get_current_user
from app.dependencies.db import get_db
from schemas.pagination import PaginationParams, PaginatedResponse
from schemas.report.response import ReportResponse
from services.reports.read import get_report, get_reports

router = APIRouter()
limiter = Limiter(key_func=get_remote_address)


@router.get("/{report_id}", response_model=ReportResponse)
@limiter.limit("10/minute")
async def read_report(
        request: Request,
        report_id: str,
        db: Database = Depends(get_db),
        user_id: str = Depends(get_current_user)
):
    return get_report(db, report_id, user_id, request.client.host)


@router.get("", response_model=PaginatedResponse[ReportResponse])
@limiter.limit("10/minute")
async def read_reports_list(
        request: Request,
        pagination: PaginationParams = Depends(),
        db: Database = Depends(get_db),
        admin_id: str = Depends(get_admin_user)
):
    return get_reports(db, admin_id, pagination.limit, pagination.offset, request.client.host)
