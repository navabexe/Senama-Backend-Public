from typing import Optional, List, Dict

from pydantic import BaseModel, Field


class StoryUpdateRequest(BaseModel):
    media_type: Optional[str] = Field(None, pattern=r"^(image|video)$")
    image_url: Optional[str] = None
    video_url: Optional[str] = None
    category: Optional[str] = Field(None, min_length=1)
    description: Optional[str] = Field(None, min_length=1)
    external_link: Optional[str] = None
    hashtags: Optional[List[str]] = None
    product_id: Optional[str] = None
    visibility: Optional[str] = None
    duration: Optional[int] = None
    is_highlight: Optional[bool] = None
    is_sponsored: Optional[bool] = None
    sponsored_settings: Optional[Dict] = None
