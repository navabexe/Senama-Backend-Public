from datetime import datetime, UTC
from typing import Optional

from pydantic import BaseModel, Field


class Session(BaseModel):
    id: Optional[str] = None
    user_id: str
    access_token: str
    refresh_token: str
    device_info: str  # از User-Agent
    role: str
    ip_address: str
    created_at: str = Field(default_factory=lambda: datetime.now(UTC).isoformat())
    expires_at: str = Field(default_factory=lambda: datetime.now(UTC).replace(day=7).isoformat())
