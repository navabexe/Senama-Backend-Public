from datetime import datetime, timezone
from typing import Optional, List

from pydantic import BaseModel, Field

from models.common import Price, Image, AudioFile, Spec, Color


class Product(BaseModel):
    id: Optional[str] = None
    vendor_id: str
    names: List[str] = Field(min_items=1)
    short_descriptions: List[str] = Field(default_factory=list)  # از تو
    prices: List[Price] = Field(default_factory=list)
    colors: List[Color] = Field(default_factory=list)  # از تو
    images: List[Image] = Field(default_factory=list)
    video_urls: List[str] = Field(default_factory=list)
    audio_files: List[AudioFile] = Field(default_factory=list)  # از تو
    technical_specs: List[Spec] = Field(default_factory=list)
    tags: List[str] = Field(default_factory=list)
    thumbnail_urls: List[str] = Field(default_factory=list)
    suggested_products: List[str] = Field(default_factory=list)
    status: str = "active"
    qr_code_url: Optional[str] = None
    category_ids: List[str] = Field(min_items=1)
    subcategory_ids: List[str] = Field(default_factory=list)
    created_by: str
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    updated_by: str
    updated_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    draft: bool = False
