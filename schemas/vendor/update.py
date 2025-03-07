from typing import List, Dict, Optional

from pydantic import BaseModel, Field

from models.common import Location, Branch, BusinessDetail, SocialLink, MessengerLink


class VendorUpdateRequest(BaseModel):
    username: Optional[str] = Field(None, min_length=3)
    name: Optional[str] = Field(None, min_length=2)
    owner_name: Optional[str] = Field(None, min_length=2)
    owner_phone: Optional[str] = Field(None, pattern=r"^\+?[0-9]{10,14}$")
    address: Optional[str] = None
    location: Optional[Location] = None
    city: Optional[str] = None
    province: Optional[str] = None
    logo_urls: Optional[List[str]] = None
    banner_urls: Optional[List[str]] = None
    bios: Optional[List[str]] = None
    about_us: Optional[List[str]] = None
    branches: Optional[List[Branch]] = None
    business_details: Optional[List[BusinessDetail]] = None
    visibility: Optional[bool] = None
    attached_vendors: Optional[List[str]] = None
    blocked_vendors: Optional[List[str]] = None
    account_types: Optional[List[str]] = None
    status: Optional[str] = None
    vendor_type: Optional[str] = None
    social_links: Optional[List[SocialLink]] = None
    messenger_links: Optional[List[MessengerLink]] = None
    business_category_ids: Optional[List[str]] = None
    profile_picture: Optional[str] = None
    gender: Optional[str] = None
    birth_date: Optional[str] = None
    language: Optional[str] = None
    notification_settings: Optional[Dict] = None
    privacy_settings: Optional[Dict] = None
    connected_devices: Optional[List[Dict]] = None
    followers: Optional[List[str]] = None
    following: Optional[List[str]] = None
    working_hours: Optional[Dict[str, str]] = None
    shipping_methods: Optional[List[str]] = None
