from datetime import datetime, timezone
from typing import Optional, Dict, Any

from pydantic import BaseModel, Field
from pymongo.database import Database


class Log(BaseModel):
    model_type: str = Field(..., pattern="^(user|vendor|product|story|category|collaboration|order|notification|block|report|advertisement|transaction|session|auth)$")
    model_id: Optional[str] = None
    action: str = Field(..., pattern="^(create|update|delete|approve|reject|block|report|charge|withdraw|login|logout|otp_sent|otp_verified|read|search|sponsor)$")
    changed_by: Optional[str] = None
    previous_data: Optional[Dict[str, Any]] = None
    new_data: Optional[Dict[str, Any]] = None
    request_data: Optional[Dict[str, Any]] = None
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    ip_address: str

def create_log(
    db: Database,
    action: str,
    model_type: str,
    model_id: str | None,
    changed_by: str | None,
    previous_data: Dict | None,
    new_data: Dict | None,
    ip_address: str,
    request_data: Dict | None = None
):
    log = Log(
        model_type=model_type,
        model_id=model_id,
        action=action,
        changed_by=changed_by,
        previous_data=previous_data,
        new_data=new_data,
        request_data=request_data,
        ip_address=ip_address
    )
    db.logs.insert_one(log.model_dump())