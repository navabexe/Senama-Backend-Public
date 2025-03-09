from datetime import datetime, timezone
from typing import Optional

from pydantic import BaseModel, Field


class Transaction(BaseModel):
    id: Optional[str] = None
    vendor_id: str
    type: str = Field(pattern=r"^(charge|withdraw|ad_payment)$")
    amount: float = Field(gt=0)
    status: str = "pending"  # "pending", "completed", "failed"
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
