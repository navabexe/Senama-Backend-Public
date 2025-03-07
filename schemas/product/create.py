from typing import List

from pydantic import BaseModel, Field

from models.common import Price, Image, AudioFile, Spec, Color


class ProductCreateRequest(BaseModel):
    names: List[str] = Field(min_items=1)
    short_descriptions: List[str] = Field(default_factory=list)
    prices: List[Price] = Field(default_factory=list)
    colors: List[Color] = Field(default_factory=list)
    images: List[Image] = Field(default_factory=list)
    video_urls: List[str] = Field(default_factory=list)
    audio_files: List[AudioFile] = Field(default_factory=list)
    technical_specs: List[Spec] = Field(default_factory=list)
    tags: List[str] = Field(default_factory=list)
    thumbnail_urls: List[str] = Field(default_factory=list)
    suggested_products: List[str] = Field(default_factory=list)
    category_ids: List[str] = Field(min_items=1)
    subcategory_ids: List[str] = Field(default_factory=list)
