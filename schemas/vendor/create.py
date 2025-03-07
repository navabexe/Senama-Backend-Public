from typing import List

from pydantic import BaseModel, Field

from models.common import Location


class VendorCreateRequest(BaseModel):
    username: str = Field(min_length=3)
    name: str = Field(min_length=2)
    owner_name: str = Field(min_length=2)
    owner_phone: str = Field(pattern=r"^\+?[0-9]{10,14}$")
    address: str
    location: Location
    city: str
    province: str
    business_category_ids: List[str] = Field(min_items=1)
