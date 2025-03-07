from datetime import datetime, UTC
from typing import Optional, List, Dict

from pydantic import BaseModel, Field

from models.common import Branch, Location, BusinessDetail, SocialLink, MessengerLink


class Vendor(BaseModel):
    id: Optional[str] = None
    username: str = Field(min_length=3)
    name: str = Field(min_length=2)
    owner_name: str = Field(min_length=2)
    owner_phone: str = Field(pattern=r"^\+?[0-9]{10,14}$")
    address: str
    location: Location  # از تو
    city: str
    province: str
    logo_urls: List[str] = Field(default_factory=list)  # از تو
    banner_urls: List[str] = Field(default_factory=list)  # از تو
    bios: List[str] = Field(default_factory=list)  # از تو
    about_us: List[str] = Field(default_factory=list)  # از تو
    branches: List[Branch] = Field(default_factory=list)
    business_details: List[BusinessDetail] = Field(default_factory=list)  # از تو
    visibility: bool = True  # از تو
    attached_vendors: List[str] = Field(default_factory=list)  # از تو
    blocked_vendors: List[str] = Field(default_factory=list)  # از تو
    account_types: List[str] = Field(default_factory=lambda: ["free"])  # از تو
    status: str = "pending"
    vendor_type: str = "basic"  # از تو
    social_links: List[SocialLink] = Field(default_factory=list)  # از تو
    messenger_links: List[MessengerLink] = Field(default_factory=list)  # از تو
    followers_count: int = 0  # از تو
    following_count: int = 0  # از تو
    business_category_ids: List[str] = Field(min_items=1)
    created_by: str  # از تو
    created_at: str = Field(default_factory=lambda: datetime.now(UTC).isoformat())
    updated_by: Optional[str] = None  # از تو
    updated_at: str = Field(default_factory=lambda: datetime.now(UTC).isoformat())
    # اضافه‌شده از من
    profile_picture: Optional[str] = None
    gender: Optional[str] = None
    birth_date: Optional[str] = None
    language: str = "fa"
    notification_settings: Dict = Field(default_factory=lambda: {"push": True, "email": False})
    privacy_settings: Dict = Field(default_factory=lambda: {"public": True})
    connected_devices: List[Dict] = Field(default_factory=list)  # {device_id: str, last_login: str}
    followers: List[str] = Field(default_factory=list)
    following: List[str] = Field(default_factory=list)
    working_hours: Optional[Dict[str, str]] = None  # {"Saturday": "9-17"}
    shipping_methods: List[str] = Field(default_factory=list)
