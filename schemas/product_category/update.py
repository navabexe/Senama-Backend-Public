from typing import Optional

from pydantic import BaseModel, Field


class ProductCategoryUpdateRequest(BaseModel):
    name: Optional[str] = Field(None, min_length=2)
    image_url: Optional[str] = None
    parent_category_id: Optional[str] = None
