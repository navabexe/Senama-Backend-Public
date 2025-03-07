from typing import Optional

from pydantic import BaseModel, Field


class ReportUpdateRequest(BaseModel):
    reason: Optional[str] = Field(None, pattern=r"^(inappropriate|abuse|fraud|violation)$")
    note: Optional[str] = None
    status: Optional[str] = Field(None, pattern=r"^(pending|resolved|dismissed)$")
