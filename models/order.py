from datetime import datetime, UTC
from typing import Optional, Dict

from pydantic import BaseModel, Field


class Order(BaseModel):
    id: Optional[str] = None
    product_id: str
    vendor_id: str
    customer_info: Dict  # {name: str, phone: str, email: Optional[str]}
    quantity: int = Field(gt=0)
    note: Optional[str] = None
    status: str = "new"  # "new", "processing", "completed", "cancelled"
    created_at: str = Field(default_factory=lambda: datetime.now(UTC).isoformat())
