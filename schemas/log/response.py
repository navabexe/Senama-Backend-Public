from typing import Optional, Dict

from pydantic import BaseModel


class LogResponse(BaseModel):
    id: str
    model_type: str
    model_id: str
    action: str
    changed_by: str
    changed_at: str
    previous_data: Optional[Dict]
    new_data: Optional[Dict]
    ip_address: str
    request_data: Optional[Dict]
