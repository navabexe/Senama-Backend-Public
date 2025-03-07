from pydantic import BaseModel, Field


class TransactionCreateRequest(BaseModel):
    type: str = Field(pattern=r"^(charge|withdraw|ad_payment)$",
                      description="نوع تراکنش: شارژ، برداشت یا پرداخت تبلیغات")
    amount: float = Field(gt=0, description="مقدار تراکنش، باید مثبت باشد")
