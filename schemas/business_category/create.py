from typing import Optional

from pydantic import BaseModel, Field


class BusinessCategoryCreateRequest(BaseModel):
    name: str = Field(min_length=2)
    image_url: Optional[str] = None
