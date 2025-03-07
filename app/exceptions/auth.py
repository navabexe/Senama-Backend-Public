from app.exceptions.base import BaseAPIException


class AuthException(BaseAPIException):
    def __init__(self, detail: str):
        super().__init__(status_code=401, detail=detail)
