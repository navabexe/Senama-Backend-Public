from typing import Optional

from pydantic import BaseModel


class ProductCategoryResponse(BaseModel):
    id: str
    name: str
    image_url: Optional[str]
    parent_category_id: Optional[str]
    created_at: str
    updated_at: str
