from typing import Optional, Dict

from pydantic import BaseModel


class OrderResponse(BaseModel):
    id: str
    product_id: str
    vendor_id: str
    customer_info: Dict
    quantity: int
    note: Optional[str]
    status: str
    created_at: str
