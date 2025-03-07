from typing import Optional

from pydantic import BaseModel


class NotificationUpdateRequest(BaseModel):
    read: Optional[bool] = None
