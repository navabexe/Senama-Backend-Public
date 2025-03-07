from pydantic import BaseModel


class CollaborationResponse(BaseModel):
    id: str
    requester_id: str
    target_id: str
    status: str
    created_at: str
