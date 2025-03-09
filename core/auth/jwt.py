from datetime import datetime, timedelta, timezone

import jwt

from app.config.settings import settings
from core.errors import APIException


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire.timestamp()})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm="HS256")

def create_refresh_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(days=7)
    to_encode.update({"exp": expire.timestamp()})
    return jwt.encode(to_encode, settings.REFRESH_SECRET_KEY, algorithm="HS256")

def decode_access_token(token: str) -> dict:
    try:
        return jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        raise APIException("UNAUTHORIZED", "Access token has expired", status_code=401)
    except jwt.InvalidTokenError:
        raise APIException("UNAUTHORIZED", "Invalid access token", status_code=401)

def decode_refresh_token(token: str) -> dict:
    try:
        return jwt.decode(token, settings.REFRESH_SECRET_KEY, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        raise APIException("UNAUTHORIZED", "Refresh token has expired", status_code=401)
    except jwt.InvalidTokenError:
        raise APIException("UNAUTHORIZED", "Invalid refresh token", status_code=401)