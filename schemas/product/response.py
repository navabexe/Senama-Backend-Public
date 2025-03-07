from typing import Optional, List

from pydantic import BaseModel

from models.common import Price, Image, AudioFile, Spec, Color


class ProductResponse(BaseModel):
    id: str
    vendor_id: str
    names: List[str]
    short_descriptions: List[str]
    prices: List[Price]
    colors: List[Color]
    images: List[Image]
    video_urls: List[str]
    audio_files: List[AudioFile]
    technical_specs: List[Spec]
    tags: List[str]
    thumbnail_urls: List[str]
    suggested_products: List[str]
    status: str
    qr_code_url: Optional[str]
    category_ids: List[str]
    subcategory_ids: List[str]
    created_by: str
    created_at: str
    updated_by: str
    updated_at: str
    draft: bool
