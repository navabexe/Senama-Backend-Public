ERRORS = {
    "INVALID_PHONE": {"code": 1001, "message": "Invalid phone number", "fa": "شماره تلفن نامعتبر"},
    "INVALID_EMAIL": {"code": 1002, "message": "Invalid email", "fa": "ایمیل نامعتبر"},
    "INVALID_WEBSITE": {"code": 1003, "message": "Invalid website URL", "fa": "آدرس وب‌سایت نامعتبر"},
    "FIELD_REQUIRED": {"code": 1004, "message": "This field is required", "fa": "این فیلد الزامی است"},
    "VENDOR_NOT_FOUND": {"code": 1005, "message": "Vendor not found", "fa": "وندور یافت نشد"},
    "INVALID_OTP": {"code": 1006, "message": "Invalid OTP code", "fa": "کد OTP نامعتبر"},
    "UNAUTHORIZED": {"code": 1007, "message": "Unauthorized access", "fa": "دسترسی غیرمجاز"},
    "FORBIDDEN": {"code": 1008, "message": "Forbidden action", "fa": "اقدام ممنوع"},
    "INVALID_ID": {"code": 1009, "message": "Invalid ID format", "fa": "فرمت شناسه نامعتبر"},
    "INVALID_AMOUNT": {"code": 1010, "message": "Amount must be positive", "fa": "مقدار باید مثبت باشد"}
}


from typing import Optional

from starlette.exceptions import HTTPException


class APIException(HTTPException):
    def __init__(self, error_code: str, detail: Optional[str] = None, status_code: int = 400):
        super().__init__(status_code=status_code, detail=detail or error_code)
        self.error_code = error_code