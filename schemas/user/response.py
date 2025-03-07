from typing import List, Optional

from pydantic import BaseModel


class UserResponse(BaseModel):
    id: str
    phone: str
    first_name: Optional[str]
    last_name: Optional[str]
    password: Optional[str]
    roles: List[str]
    status: str
    otp: Optional[str]
    otp_expires_at: Optional[str]
    bio: Optional[str]
    avatar_urls: List[str]
    phones: List[str]
    birthdate: Optional[str]
    gender: Optional[str]
    languages: List[str]
    created_at: str
    updated_at: str
