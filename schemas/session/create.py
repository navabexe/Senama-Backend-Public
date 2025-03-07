from pydantic import BaseModel


class SessionCreateRequest(BaseModel):
    user_id: str
    access_token: str
    refresh_token: str
    device_info: str
    ip_address: str
