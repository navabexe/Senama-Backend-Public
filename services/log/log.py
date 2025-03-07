from datetime import datetime, UTC

from pymongo.database import Database

from models.log import Log


def create_log(
        db: Database,
        action: str,
        model_type: str,
        model_id: str,
        changed_by: str,
        previous_data: dict | None,
        new_data: dict | None,
        ip_address: str,
        request_data: dict | None = None
):
    log = Log(
        model_type=model_type,
        model_id=model_id,
        action=action,
        changed_by=changed_by,
        changed_at=datetime.now(UTC).isoformat(),
        previous_data=previous_data,
        new_data=new_data,
        ip_address=ip_address,
        request_data=request_data
    )
    result = db.logs.insert_one(log.dict(exclude={"id"}))
    log.id = str(result.inserted_id)
    return log
