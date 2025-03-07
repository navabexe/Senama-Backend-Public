from typing import Optional, List, Dict

from pydantic import BaseModel


class StoryResponse(BaseModel):
    id: str
    vendor_id: str
    media_type: str
    image_url: Optional[str]
    video_url: Optional[str]
    category: str
    description: str
    external_link: Optional[str]
    hashtags: List[str]
    product_id: Optional[str]
    visibility: str
    duration: int
    is_highlight: bool
    is_sponsored: bool
    sponsored_settings: Optional[Dict]
    created_at: str
    expires_at: Optional[str]
    views_count: int
    likes_count: int
    shares_count: int
