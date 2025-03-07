from pydantic import BaseModel


class BlockResponse(BaseModel):
    id: str
    user_id: str
    blocked_id: str
    created_at: str
