from typing import Optional, List, Dict

from pydantic import BaseModel, Field


class StoryCreateRequest(BaseModel):
    media_type: str = Field(pattern=r"^(image|video)$")
    image_url: Optional[str] = None
    video_url: Optional[str] = None
    category: str = Field(min_length=1)
    description: str = Field(min_length=1)
    external_link: Optional[str] = None
    hashtags: List[str] = Field(default_factory=list)
    product_id: Optional[str] = None
    visibility: str = "public"
    duration: int = 24
    is_highlight: bool = False
    is_sponsored: bool = False
    sponsored_settings: Optional[Dict] = None
