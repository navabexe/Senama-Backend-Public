from datetime import datetime, timezone
from typing import Optional

from pydantic import BaseModel, Field


class Collaboration(BaseModel):
    id: Optional[str] = None
    requester_id: str
    target_id: str
    status: str = "pending"  # "pending", "approved", "rejected"
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
