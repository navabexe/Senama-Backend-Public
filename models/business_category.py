from datetime import datetime, UTC
from typing import Optional

from pydantic import BaseModel, Field


class BusinessCategory(BaseModel):
    id: Optional[str] = None
    name: str = Field(min_length=2)  # از تو
    image_url: Optional[str] = None
    created_at: str = Field(default_factory=lambda: datetime.now(UTC).isoformat())
    updated_at: str = Field(default_factory=lambda: datetime.now(UTC).isoformat())
