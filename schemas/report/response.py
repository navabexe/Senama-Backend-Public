from typing import Optional

from pydantic import BaseModel


class ReportResponse(BaseModel):
    id: str
    reporter_id: str
    target_id: str
    reason: str
    note: Optional[str]
    status: str
    created_at: str
