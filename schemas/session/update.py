from typing import Optional

from pydantic import BaseModel


class SessionUpdateRequest(BaseModel):
    access_token: Optional[str] = None
    refresh_token: Optional[str] = None
    device_info: Optional[str] = None
    ip_address: Optional[str] = None
