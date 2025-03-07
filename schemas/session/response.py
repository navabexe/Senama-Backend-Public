from pydantic import BaseModel


class SessionResponse(BaseModel):
    id: str
    user_id: str
    access_token: str
    refresh_token: str
    device_info: str
    ip_address: str
    created_at: str
    expires_at: str
