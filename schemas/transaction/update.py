from typing import Optional

from pydantic import BaseModel, Field


class TransactionUpdateRequest(BaseModel):
    type: Optional[str] = Field(None, pattern=r"^(charge|withdraw|ad_payment)$", description="به‌روزرسانی نوع تراکنش")
    amount: Optional[float] = Field(None, gt=0, description="به‌روزرسانی مقدار تراکنش، باید مثبت باشد")
    status: Optional[str] = Field(None, pattern=r"^(pending|completed|failed)$", description="به‌روزرسانی وضعیت تراکنش")
