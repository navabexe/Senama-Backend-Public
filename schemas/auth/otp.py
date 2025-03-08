from pydantic import BaseModel, Field


class OTPSendRequest(BaseModel):
    phone: str = Field(pattern=r"^\+?[0-9]{10,14}$")
    role: str  # "admin", "vendor", "customer"


class OTPSendResponse(BaseModel):
    message: str
    otp_sent: bool
    otp_sent: bool = True
    otp: str


class OTPVerifyRequest(BaseModel):
    phone: str = Field(pattern=r"^\+?[0-9]{10,14}$")
    otp_code: str = Field(pattern=r"^\d{6}$")


class OTPVerifyResponse(BaseModel):
    message: str
    token: str
    refresh_token: str
    entity_id: str  # تغییر از vendor_id به entity_id
    entity_type: str  # اضافه کردن نوع موجودیت (user یا vendor)
    status: str  # تغییر از vendor_status به status
