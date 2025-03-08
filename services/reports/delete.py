from pymongo.database import Database
from schemas.report.response import ReportResponse
from core.errors import APIException
from services.log import create_log
from core.utils.db import map_db_to_response
from bson import ObjectId


def delete_report(db: Database, report_id: str, user_id: str, ip_address: str) -> ReportResponse:
    try:
        report = db.reports.find_one({"_id": ObjectId(report_id), "reporter_id": user_id})
    except ValueError:
        raise APIException("INVALID_ID", "Invalid report ID format")

    if not report:
        raise APIException("NOT_FOUND", "Report not found or not owned by you")

    previous_data = report.copy()
    db.reports.delete_one({"_id": ObjectId(report_id)})

    create_log(db, "delete", "report", report_id, user_id, previous_data, None, ip_address)
    return map_db_to_response(previous_data, ReportResponse)