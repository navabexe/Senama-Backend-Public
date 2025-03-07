from pydantic import BaseModel


class NotificationCreateRequest(BaseModel):
    user_id: str
    type: str
    message: str
