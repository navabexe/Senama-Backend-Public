from typing import Dict

from pydantic import BaseModel, Field


class AdvertisementCreateRequest(BaseModel):
    type: str = Field(pattern=r"^(product|story|profile)$")
    target_id: str
    budget: float = Field(gt=0)
    targeting: Dict
    duration: int = Field(gt=0)
