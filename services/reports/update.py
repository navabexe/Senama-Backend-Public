from datetime import datetime, timezone

from bson import ObjectId
from pymongo.database import Database

from core.errors import APIException
from core.utils.db import map_db_to_response
from schemas.report.response import ReportResponse
from schemas.report.update import ReportUpdateRequest
from services.log import create_log


def update_report(db: Database, report_id: str, request: ReportUpdateRequest, user_id: str,
                  ip_address: str) -> ReportResponse:
    try:
        report = db.reports.find_one({"_id": ObjectId(report_id), "reporter_id": user_id})
    except ValueError:
        raise APIException("INVALID_ID", "Invalid report ID format")

    if not report:
        raise APIException("NOT_FOUND", "Report not found or not owned by you")

    update_data = request.dict(exclude_unset=True)
    if "status" in update_data and update_data["status"] not in ["pending", "resolved", "dismissed"]:
        raise APIException("INVALID_ID", "Invalid status value")
    update_data["updated_at"] = datetime.now(timezone.utc).isoformat()

    previous_data = report.copy()
    db.reports.update_one({"_id": ObjectId(report_id)}, {"$set": update_data})
    updated_report = db.reports.find_one({"_id": ObjectId(report_id)})

    create_log(db, "update", "report", report_id, user_id, previous_data, updated_report, ip_address)
    return map_db_to_response(updated_report, ReportResponse)