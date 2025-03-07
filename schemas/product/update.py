from typing import List, Optional

from pydantic import BaseModel

from models.common import Price, Image, AudioFile, Spec, Color


class ProductUpdateRequest(BaseModel):
    names: Optional[List[str]] = None
    short_descriptions: Optional[List[str]] = None
    prices: Optional[List[Price]] = None
    colors: Optional[List[Color]] = None
    images: Optional[List[Image]] = None
    video_urls: Optional[List[str]] = None
    audio_files: Optional[List[AudioFile]] = None
    technical_specs: Optional[List[Spec]] = None
    tags: Optional[List[str]] = None
    thumbnail_urls: Optional[List[str]] = None
    suggested_products: Optional[List[str]] = None
    status: Optional[str] = None
    qr_code_url: Optional[str] = None
    category_ids: Optional[List[str]] = None
    subcategory_ids: Optional[List[str]] = None
    draft: Optional[bool] = None
