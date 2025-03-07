from datetime import datetime, UTC
from typing import Optional, Dict

from pydantic import BaseModel, Field


class Log(BaseModel):
    id: Optional[str] = None
    model_type: str = Field(
        pattern=r"^(user|vendor|product|story|category|collaboration|order|notification|block|report|advertisement|transaction|session)$")
    model_id: str
    action: str = Field(
        pattern=r"^(create|update|delete|approve|reject|block|report|charge|withdraw|login|logout|otp_sent|read|search|sponsor)$")
    changed_by: str
    changed_at: str = Field(default_factory=lambda: datetime.now(UTC).isoformat())
    previous_data: Optional[Dict] = None
    new_data: Optional[Dict] = None
    ip_address: str
    request_data: Optional[Dict] = None
