from typing import List

from pydantic import BaseModel, Field, model_validator

class Location(BaseModel):
    lat: float
    lng: float

class VendorSignupRequest(BaseModel):
    username: str = Field(min_length=3)
    name: str = Field(min_length=2)
    owner_name: str = Field(min_length=2)
    owner_phone: str = Field(pattern=r"^\+?[0-9]{10,14}$")
    address: str
    location: Location
    city: str
    province: str
    business_category_ids: List[str] = Field(min_items=1)

    @model_validator(mode='after')
    def check_categories(cls, values):
        if not values.business_category_ids:
            raise ValueError("Business categories must contain at least one item")
        return values


class VendorSignupResponse(BaseModel):
    message: str
    vendor_id: str
    status: str
