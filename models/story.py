from datetime import datetime, timezone
from typing import Optional, List, Dict

from pydantic import BaseModel, Field


class Story(BaseModel):
    id: Optional[str] = None
    vendor_id: str
    image_url: Optional[str] = None  # از تو
    video_url: Optional[str] = None  # از تو
    category: str = Field(min_length=1)  # از تو
    description: str = Field(min_length=1)  # از تو
    external_link: Optional[str] = None
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    expires_at: Optional[str] = Field(
        default_factory=lambda: (datetime.now(timezone.utc).replace(hour=23, minute=59, second=59)).isoformat())
    views_count: int = 0  # از تو
    likes_count: int = 0  # از تو
    shares_count: int = 0  # از تو
    # اضافه‌شده از من
    media_type: str = Field(pattern=r"^(image|video)$")
    hashtags: List[str] = Field(default_factory=list)
    product_id: Optional[str] = None
    visibility: str = "public"  # "public" یا "followers"
    duration: int = 24  # ساعت
    is_highlight: bool = False
    is_sponsored: bool = False
    sponsored_settings: Optional[Dict] = None  # {budget: float, targeting: Dict, duration: int}
