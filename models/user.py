from datetime import datetime, timezone
from typing import List, Optional

from bson import ObjectId
from pydantic import BaseModel, Field


class User(BaseModel):
    id: Optional[ObjectId] = None
    phone: str = Field(pattern=r"^\+?[0-9]{10,14}$")
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    password: Optional[str] = None
    roles: List[str] = Field(default_factory=list)
    status: str = "pending"
    otp: Optional[str] = None
    otp_expires_at: Optional[str] = None
    bio: Optional[str] = None
    avatar_urls: List[str] = Field(default_factory=list)
    phones: List[str] = Field(default_factory=list)
    birthdate: Optional[str] = None
    gender: Optional[str] = None
    languages: List[str] = Field(default_factory=list)
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    updated_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}