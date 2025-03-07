from typing import Optional, Dict

from pydantic import BaseModel, Field


class AdvertisementUpdateRequest(BaseModel):
    type: Optional[str] = Field(None, pattern=r"^(product|story|profile)$")
    target_id: Optional[str] = None
    budget: Optional[float] = Field(None, gt=0)
    targeting: Optional[Dict] = None
    duration: Optional[int] = Field(None, gt=0)
    status: Optional[str] = Field(None, pattern=r"^(active|paused|completed)$")
