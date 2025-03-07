from typing import Optional, List, Dict

from pydantic import BaseModel

from models.common import Location, Branch, BusinessDetail, SocialLink, MessengerLink


class VendorResponse(BaseModel):
    id: str
    username: str
    name: str
    owner_name: str
    owner_phone: str
    address: str
    location: Location
    city: str
    province: str
    logo_urls: List[str]
    banner_urls: List[str]
    bios: List[str]
    about_us: List[str]
    branches: List[Branch]
    business_details: List[BusinessDetail]
    visibility: bool
    attached_vendors: List[str]
    blocked_vendors: List[str]
    account_types: List[str]
    status: str
    vendor_type: str
    social_links: List[SocialLink]
    messenger_links: List[MessengerLink]
    followers_count: int
    following_count: int
    business_category_ids: List[str]
    created_by: str
    created_at: str
    updated_by: Optional[str]
    updated_at: str
    profile_picture: Optional[str]
    gender: Optional[str]
    birth_date: Optional[str]
    language: str
    notification_settings: Dict
    privacy_settings: Dict
    connected_devices: List[Dict]
    followers: List[str]
    following: List[str]
    working_hours: Optional[Dict[str, str]]
    shipping_methods: List[str]
