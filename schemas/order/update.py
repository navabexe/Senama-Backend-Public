from typing import Optional, Dict

from pydantic import BaseModel, Field


class OrderUpdateRequest(BaseModel):
    customer_info: Optional[Dict] = None
    quantity: Optional[int] = Field(None, gt=0)
    note: Optional[str] = None
    status: Optional[str] = Field(None, pattern=r"^(new|processing|completed|cancelled)$")
