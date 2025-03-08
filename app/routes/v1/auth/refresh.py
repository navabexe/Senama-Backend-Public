from fastapi import APIRouter, Depends, Request
from pymongo.database import Database
from app.dependencies.db import get_db
from schemas.auth.response import TokenResponse
from core.auth.jwt import create_access_token, decode_refresh_token
from core.errors import APIException
from slowapi import Limiter
from slowapi.util import get_remote_address
from pydantic import BaseModel
from bson import ObjectId

router = APIRouter()
limiter = Limiter(key_func=get_remote_address)

class RefreshTokenRequest(BaseModel):
    refresh_token: str

@router.post("/refresh", response_model=TokenResponse)
@limiter.limit("5/minute")
async def refresh_token_route(
    request_data: RefreshTokenRequest,
    request: Request,
    db: Database = Depends(get_db)
):
    try:
        # رمزگشایی رفرش توکن
        payload = decode_refresh_token(request_data.refresh_token)
        entity_id = payload.get("sub")
        entity_type = payload.get("entity_type", "user")

        if not entity_id:
            raise APIException("INVALID_TOKEN", "Invalid refresh token payload", status_code=401)

        # پیدا کردن موجودیت (کاربر یا وندور)
        if entity_type == "user":
            entity = db.users.find_one({"_id": ObjectId(entity_id)})
        elif entity_type == "vendor":
            entity = db.vendors.find_one({"_id": ObjectId(entity_id)})
        else:
            raise APIException("INVALID_ID", "Invalid entity type", status_code=400)

        if not entity:
            raise APIException("NOT_FOUND", "Entity not found", status_code=404)

        # تولید توکن دسترسی جدید
        access_token = create_access_token({"sub": entity_id, "entity_type": entity_type})

        return TokenResponse(
            message="Token refreshed successfully",
            token=access_token,
            refresh_token=request_data.refresh_token,  # همون رفرش توکن قبلی رو برمی‌گردونیم
            entity_id=entity_id,
            entity_type=entity_type,
            status=entity.get("status", "active")
        )
    except APIException as ae:
        raise ae
    except Exception as e:
        raise APIException("INTERNAL_ERROR", f"Failed to refresh token: {str(e)}", status_code=500)