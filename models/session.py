from datetime import datetime, timezone
from typing import Optional

from pydantic import BaseModel, Field


class Session(BaseModel):
    id: Optional[str] = None
    user_id: str
    access_token: str
    refresh_token: str
    device_info: str
    role: str
    ip_address: str
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    expires_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).replace(day=7).isoformat())
