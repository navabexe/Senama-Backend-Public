from typing import Optional

from pydantic import BaseModel, Field


class ReportCreateRequest(BaseModel):
    target_id: str
    reason: str = Field(pattern=r"^(inappropriate|abuse|fraud|violation)$")
    note: Optional[str] = None
