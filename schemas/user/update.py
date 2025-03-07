from typing import List, Optional

from pydantic import BaseModel, Field


class UserUpdateRequest(BaseModel):
    phone: Optional[str] = Field(None, pattern=r"^\+?[0-9]{10,14}$")
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    password: Optional[str] = None
    roles: Optional[List[str]] = None
    status: Optional[str] = None
    bio: Optional[str] = None
    avatar_urls: Optional[List[str]] = None
    phones: Optional[List[str]] = None
    birthdate: Optional[str] = None
    gender: Optional[str] = None
    languages: Optional[List[str]] = None
