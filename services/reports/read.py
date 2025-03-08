from pymongo.database import Database
from schemas.report.response import ReportResponse
from schemas.pagination import PaginatedResponse
from services.log import create_log
from core.errors import APIException
from core.utils.db import map_db_to_response
from bson import ObjectId


def get_report(db: Database, report_id: str, user_id: str, ip_address: str) -> ReportResponse:
    try:
        report = db.reports.find_one({"_id": ObjectId(report_id)})
    except ValueError:
        raise APIException("INVALID_ID", "Invalid report ID format")

    if not report:
        raise APIException("NOT_FOUND", "Report not found")

    if report["reporter_id"] != user_id:
        raise APIException("FORBIDDEN", "You can only view your own reports")

    create_log(db, "read", "report", report_id, user_id, None, None, ip_address)
    return map_db_to_response(report, ReportResponse)


def get_reports(db: Database, user_id: str, limit: int, offset: int, ip_address: str) -> PaginatedResponse[
    ReportResponse]:
    reports = db.reports.find({"reporter_id": user_id}).skip(offset).limit(limit)
    total = db.reports.count_documents({"reporter_id": user_id})
    items = [map_db_to_response(report, ReportResponse) for report in reports]

    create_log(db, "read", "report", "list", user_id, None, None, ip_address)
    return PaginatedResponse[ReportResponse](
        items=items,
        total=total,
        limit=limit,
        offset=offset
    )