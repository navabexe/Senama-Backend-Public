from typing import Optional, Dict

from pydantic import BaseModel, Field


class LogUpdateRequest(BaseModel):
    model_type: Optional[str] = Field(None,
                                      pattern=r"^(user|vendor|product|story|category|collaboration|order|notification|block|report|advertisement|transaction|session)$")
    model_id: Optional[str] = None
    action: Optional[str] = Field(None,
                                  pattern=r"^(create|update|delete|approve|reject|block|report|charge|withdraw|login|logout|otp_sent|read|search|sponsor)$")
    changed_by: Optional[str] = None
    previous_data: Optional[Dict] = None
    new_data: Optional[Dict] = None
    ip_address: Optional[str] = None
    request_data: Optional[Dict] = None
