from datetime import datetime, timezone
from typing import Optional

from pydantic import BaseModel, Field


class Block(BaseModel):
    id: Optional[str] = None
    user_id: str
    blocked_id: str
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
