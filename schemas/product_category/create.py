from typing import Optional

from pydantic import BaseModel, Field


class ProductCategoryCreateRequest(BaseModel):
    name: str = Field(min_length=2)
    image_url: Optional[str] = None
    parent_category_id: Optional[str] = None
