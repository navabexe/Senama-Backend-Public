from app.exceptions.base import BaseAPIException


class ValidationException(BaseAPIException):
    def __init__(self, detail: str):
        super().__init__(status_code=400, detail=detail)
