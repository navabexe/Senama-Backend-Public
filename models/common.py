from typing import List

from pydantic import BaseModel, Field


class Price(BaseModel):
    variant_type: str = Field(min_length=1)  # از تو
    amount: float = Field(gt=0)
    currency: str = Field(default="IRR")  # از من


class Color(BaseModel):
    name: str = Field(min_length=1)
    hex: str = Field(pattern=r"^#[0-9A-Fa-f]{6}$")


class Image(BaseModel):
    url: str
    related_colors: List[str] = Field(default_factory=list)  # از تو
    textures: List[str] = Field(default_factory=list)
    is_thumbnail: bool = False  # از من


class AudioFile(BaseModel):
    url: str
    label: str = Field(min_length=1)


class Spec(BaseModel):
    key: str = Field(min_length=1)
    value: str = Field(min_length=1)


class Branch(BaseModel):
    label: str  # از تو
    city: str  # از تو
    province: str  # از تو
    address: str
    location: dict  # {lat: float, lng: float}
    phones: List[str] = Field(default_factory=list)  # از تو
    emails: List[str] = Field(default_factory=list)  # از تو


class Location(BaseModel):
    lat: float
    lng: float


class BusinessDetail(BaseModel):
    type: str
    values: List[str]


class SocialLink(BaseModel):
    platform: str
    url: str


class MessengerLink(BaseModel):
    platform: str
    url: str
