from pydantic import BaseModel


class CollaborationCreateRequest(BaseModel):
    target_id: str
