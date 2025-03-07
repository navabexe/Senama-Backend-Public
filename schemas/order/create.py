from typing import Optional, Dict

from pydantic import BaseModel, Field


class OrderCreateRequest(BaseModel):
    product_id: str
    customer_info: Dict  # {name: str, phone: str, email: Optional[str]}
    quantity: int = Field(gt=0)
    note: Optional[str] = None
