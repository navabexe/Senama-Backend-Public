from datetime import datetime, timezone
from typing import Optional

from pydantic import BaseModel, Field


class ProductCategory(BaseModel):
    id: Optional[str] = None
    name: str = Field(min_length=2)  # از تو
    image_url: Optional[str] = None
    parent_category_id: Optional[str] = None
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    updated_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
