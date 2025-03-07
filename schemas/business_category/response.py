from typing import Optional

from pydantic import BaseModel


class BusinessCategoryResponse(BaseModel):
    id: str
    name: str
    image_url: Optional[str]
    created_at: str
    updated_at: str
