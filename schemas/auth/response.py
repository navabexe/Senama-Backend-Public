from pydantic import BaseModel

class LogoutResponse(BaseModel):
    message: str

class TokenResponse(BaseModel):
    message: str
    token: str
    refresh_token: str
    entity_id: str
    entity_type: str
    status: str