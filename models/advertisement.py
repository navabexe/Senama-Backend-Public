from datetime import datetime, UTC
from typing import Optional, Dict

from pydantic import BaseModel, Field


class Advertisement(BaseModel):
    id: Optional[str] = None
    vendor_id: str
    type: str = Field(pattern=r"^(product|story|profile)$")
    target_id: str
    budget: float = Field(gt=0)
    targeting: Dict  # {city: str, category: str, ...}
    duration: int = Field(gt=0)  # روز
    status: str = "active"  # "active", "paused", "completed"
    created_at: str = Field(default_factory=lambda: datetime.now(UTC).isoformat())
