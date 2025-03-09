from datetime import datetime, timezone

from bson import ObjectId
from pymongo.database import Database

from core.errors import APIException
from core.validators import Validators
from models.report import Report
from schemas.report.create import ReportCreateRequest
from schemas.report.response import ReportResponse
from services.log import create_log


def create_report(db: Database, request: ReportCreateRequest, user_id: str, ip_address: str) -> ReportResponse:
    Validators.validate_not_null(request.target_id, "target_id")
    Validators.validate_not_null(request.reason, "reason")

    if user_id == request.target_id:
        raise APIException("FORBIDDEN", "Cannot report yourself")

    try:
        if not db.vendors.find_one({"_id": ObjectId(user_id)}) and not db.users.find_one({"_id": ObjectId(user_id)}):
            raise APIException("VENDOR_NOT_FOUND", "Reporter not found")
        if not db.vendors.find_one({"_id": ObjectId(request.target_id)}) and not db.users.find_one(
                {"_id": ObjectId(request.target_id)}):
            raise APIException("VENDOR_NOT_FOUND", "Target user not found")
    except ValueError:
        raise APIException("INVALID_ID", "Invalid ID format")

    existing_report = db.reports.find_one({"reporter_id": user_id, "target_id": request.target_id, "status": "pending"})
    if existing_report:
        raise APIException("FORBIDDEN", "You already have a pending report for this target")

    report = Report(
        reporter_id=user_id,
        target_id=request.target_id,
        reason=request.reason,
        note=request.note,
        status="pending",
        created_at=datetime.now(timezone.utc).isoformat()
    )

    result = db.reports.insert_one(report.dict(exclude={"id"}))
    report_id = str(result.inserted_id)

    create_log(db, "create", "report", report_id, user_id, None, report.dict(exclude={"id"}), ip_address)

    return ReportResponse(
        id=report_id,
        reporter_id=report.reporter_id,
        target_id=report.target_id,
        reason=report.reason,
        note=report.note,
        status=report.status,
        created_at=report.created_at
    )
