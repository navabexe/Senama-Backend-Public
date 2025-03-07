from fastapi import APIRouter, Depends, Request
from pymongo.database import Database
from slowapi import Limiter
from slowapi.util import get_remote_address

from app.dependencies.auth import get_current_user
from app.dependencies.db import get_db
from schemas.report.create import ReportCreateRequest
from schemas.report.response import ReportResponse
from services.reports.create import create_report

router = APIRouter()
limiter = Limiter(key_func=get_remote_address)


@router.post("", response_model=ReportResponse)
@limiter.limit("5/minute")
async def create_report_route(
        request: Request,
        report_request: ReportCreateRequest,
        db: Database = Depends(get_db),
        user_id: str = Depends(get_current_user)
):
    return create_report(db, report_request, user_id, request.client.host)
