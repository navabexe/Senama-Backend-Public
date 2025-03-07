from pydantic import BaseModel


class BlockCreateRequest(BaseModel):
    blocked_id: str
