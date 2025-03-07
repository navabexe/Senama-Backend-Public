from typing import Dict

from pydantic import BaseModel


class AdvertisementResponse(BaseModel):
    id: str
    vendor_id: str
    type: str
    target_id: str
    budget: float
    targeting: Dict
    duration: int
    status: str
    created_at: str
