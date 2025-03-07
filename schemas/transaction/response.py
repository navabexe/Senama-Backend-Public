from pydantic import BaseModel, Field


class TransactionResponse(BaseModel):
    id: str = Field(description="شناسه یکتای تراکنش")
    vendor_id: str = Field(description="شناسه وندور صاحب تراکنش")
    type: str = Field(pattern=r"^(charge|withdraw|ad_payment)$", description="نوع تراکنش")
    amount: float = Field(gt=0, description="مقدار تراکنش")
    status: str = Field(pattern=r"^(pending|completed|failed)$",
                        description="وضعیت تراکنش: در انتظار، تکمیل‌شده یا ناموفق")
    created_at: str = Field(description="زمان ایجاد تراکنش به فرمت ISO")
