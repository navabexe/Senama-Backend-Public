from datetime import datetime, UTC, timedelta

import jwt

from app.config.settings import settings
from core.errors import APIException


def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    to_encode = data.copy()
    expire = datetime.now(UTC) + (expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": int(expire.timestamp())})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm="HS256")


def decode_access_token(token: str) -> dict:
    try:
        return jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        raise APIException("UNAUTHORIZED", "Token has expired")
    except jwt.InvalidTokenError:
        raise APIException("UNAUTHORIZED", "Invalid token")

def decode_refresh_token(token: str) -> dict:
    try:
        return jwt.decode(token, settings.REFRESH_SECRET_KEY, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        raise APIException("UNAUTHORIZED", "Refresh token has expired")
    except jwt.InvalidTokenError:
        raise APIException("UNAUTHORIZED", "Invalid refresh token")