from typing import Optional

from pydantic import BaseModel, Field


class BusinessCategoryUpdateRequest(BaseModel):
    name: Optional[str] = Field(None, min_length=2)
    image_url: Optional[str] = None
