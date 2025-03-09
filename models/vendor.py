from datetime import datetime, timezone
from typing import Optional, List, Dict

from bson import ObjectId
from pydantic import BaseModel, Field

from models.common import Branch, Location, BusinessDetail, SocialLink, MessengerLink


class Vendor(BaseModel):
    id: Optional[ObjectId] = None
    user_id: ObjectId  # اضافه کردن user_id
    username: str = Field(min_length=3)
    name: str = Field(min_length=2)
    owner_name: str = Field(min_length=2)
    owner_phone: str = Field(pattern=r"^\+?[0-9]{10,14}$")
    address: str
    location: Location
    city: str
    province: str
    logo_urls: List[str] = Field(default_factory=list)
    banner_urls: List[str] = Field(default_factory=list)
    bios: List[str] = Field(default_factory=list)
    about_us: List[str] = Field(default_factory=list)
    branches: List[Branch] = Field(default_factory=list)
    business_details: List[BusinessDetail] = Field(default_factory=list)
    visibility: bool = True
    attached_vendors: List[str] = Field(default_factory=list)
    blocked_vendors: List[str] = Field(default_factory=list)
    account_types: List[str] = Field(default_factory=lambda: ["free"])
    status: str = "pending"
    vendor_type: str = "basic"
    social_links: List[SocialLink] = Field(default_factory=list)
    messenger_links: List[MessengerLink] = Field(default_factory=list)
    followers_count: int = 0
    following_count: int = 0
    business_category_ids: List[str] = Field(min_items=1)
    created_by: str
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    updated_by: Optional[str] = None
    updated_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    profile_picture: Optional[str] = None
    gender: Optional[str] = None
    birth_date: Optional[str] = None
    language: str = "fa"
    notification_settings: Dict = Field(default_factory=lambda: {"push": True, "email": False})
    privacy_settings: Dict = Field(default_factory=lambda: {"public": True})
    connected_devices: List[Dict] = Field(default_factory=list)
    followers: List[str] = Field(default_factory=list)
    following: List[str] = Field(default_factory=list)
    working_hours: Optional[Dict[str, str]] = None
    shipping_methods: List[str] = Field(default_factory=list)

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}