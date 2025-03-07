from datetime import datetime, UTC
from typing import Optional

from pydantic import BaseModel, Field


class Notification(BaseModel):
    id: Optional[str] = None
    user_id: str
    type: str  # "follow", "order", "collaboration", "security"
    message: str
    read: bool = False
    created_at: str = Field(default_factory=lambda: datetime.now(UTC).isoformat())
