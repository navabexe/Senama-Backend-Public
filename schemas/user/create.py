from typing import Optional

from pydantic import BaseModel, Field


class UserCreateRequest(BaseModel):
    phone: str = Field(pattern=r"^\+?[0-9]{10,14}$")
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    password: Optional[str] = None
