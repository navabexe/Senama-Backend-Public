from datetime import datetime, UTC
from typing import Optional

from pydantic import BaseModel, Field


class Report(BaseModel):
    id: Optional[str] = None
    reporter_id: str
    target_id: str
    reason: str = Field(pattern=r"^(inappropriate|abuse|fraud|violation)$")
    note: Optional[str] = None
    status: str = "pending"  # "pending", "resolved", "dismissed"
    created_at: str = Field(default_factory=lambda: datetime.now(UTC).isoformat())
