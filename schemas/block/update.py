from typing import Optional

from pydantic import BaseModel


class BlockUpdateRequest(BaseModel):
    blocked_id: Optional[str] = None
