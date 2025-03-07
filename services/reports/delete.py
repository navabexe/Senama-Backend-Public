from bson import ObjectId
from pymongo.database import Database

from core.errors import APIException
from core.utils.db import map_db_to_response
from schemas.report.response import ReportResponse
from services.log.log import create_log


def delete_report(db: Database, report_id: str, admin_id: str, ip_address: str) -> ReportResponse:
    try:
        report = db.reports.find_one({"_id": ObjectId(report_id)})
    except ValueError:
        raise APIException("INVALID_ID", "Invalid report ID format")

    if not report:
        raise APIException("VENDOR_NOT_FOUND", "Report not found")

    previous_data = report.copy()
    db.reports.delete_one({"_id": ObjectId(report_id)})

    create_log(db, "delete", "report", report_id, admin_id, previous_data, None, ip_address)

    return map_db_to_response(report, ReportResponse)
