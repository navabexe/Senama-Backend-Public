import re

from pydantic import ValidationError


class Validators:
    @staticmethod
    def validate_phone(phone: str) -> str:
        if not re.match(r"^\+?[0-9]{10,14}$", phone):
            raise ValidationError("Phone must be in international format (+1234567890)")
        return phone

    @staticmethod
    def validate_email(email: str | None) -> str | None:
        if email and not re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email):
            raise ValidationError("Invalid email format")
        return email

    @staticmethod
    def validate_website(url: str | None) -> str | None:
        if url and not re.match(r"^(https?://)?[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}(/.*)?$", url):
            raise ValidationError("Invalid website URL")
        return url

    @staticmethod
    def validate_not_null(value, field_name: str):
        if value is None or (isinstance(value, (list, str, dict)) and not value):
            raise ValidationError(f"{field_name} cannot be null or empty")
        return value
