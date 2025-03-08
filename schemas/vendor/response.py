from pydantic import BaseModel
from typing import Optional, List, Dict
from bson import ObjectId

class VendorResponse(BaseModel):
    id: str
    username: Optional[str] = None
    name: Optional[str] = None
    owner_name: Optional[str] = None
    owner_phone: Optional[str] = None
    address: Optional[str] = None
    location: Optional[Dict[str, float]] = None
    city: Optional[str] = None
    province: Optional[str] = None
    logo_urls: Optional[List[str]] = []
    banner_urls: Optional[List[str]] = []
    bios: Optional[List[str]] = []
    about_us: Optional[List[str]] = []
    branches: Optional[List[Dict]] = []
    business_details: Optional[List[Dict]] = []
    visibility: Optional[bool] = True
    attached_vendors: Optional[List[str]] = []
    blocked_vendors: Optional[List[str]] = []
    account_types: Optional[List[str]] = ["free"]
    status: Optional[str] = "active"
    vendor_type: Optional[str] = "basic"
    social_links: Optional[List[str]] = []
    messenger_links: Optional[List[str]] = []
    followers_count: Optional[int] = 0
    following_count: Optional[int] = 0
    business_category_ids: Optional[List[str]] = []
    created_by: Optional[str] = None
    created_at: Optional[str] = None
    updated_by: Optional[str] = None
    updated_at: Optional[str] = None
    otp: Optional[str] = None
    otp_expires_at: Optional[str] = None
    language: Optional[str] = None
    notification_settings: Optional[Dict] = None
    privacy_settings: Optional[Dict] = None
    connected_devices: Optional[List[Dict]] = []
    followers: Optional[List[str]] = []
    following: Optional[List[str]] = []
    shipping_methods: Optional[List[Dict]] = []

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class DeleteVendorResponse(BaseModel):
    message: str