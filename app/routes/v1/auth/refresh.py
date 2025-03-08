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
        payload = decode_refresh_token(request_data.refresh_token)
        entity_id = payload.get("sub")
        entity_type = payload.get("entity_type", "user")
        role = payload.get("role")

        if not entity_id or not role:
            raise APIException("INVALID_TOKEN", "Invalid refresh token payload", status_code=401)

        user = db.users.find_one({"_id": ObjectId(entity_id)})
        if not user:
            raise APIException("NOT_FOUND", "User not found", status_code=404)

        if role not in user.get("roles", []):
            raise APIException("FORBIDDEN", f"User does not have role {role}", status_code=403)

        access_token = create_access_token({"sub": entity_id, "entity_type": entity_type, "role": role})
        return TokenResponse(
            message="Token refreshed successfully",
            token=access_token,
            refresh_token=request_data.refresh_token,
            entity_id=entity_id,
            entity_type=entity_type,
            status=user.get("status", "active")
        )
    except APIException as ae:
        raise ae
    except Exception as e:
        raise APIException("INTERNAL_ERROR", f"Failed to refresh token: {str(e)}", status_code=500)