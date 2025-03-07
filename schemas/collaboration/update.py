from typing import Optional

from pydantic import BaseModel, Field


class CollaborationUpdateRequest(BaseModel):
    status: Optional[str] = Field(None, pattern=r"^(pending|approved|rejected)$")
