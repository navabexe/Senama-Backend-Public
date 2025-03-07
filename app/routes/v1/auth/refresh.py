from fastapi import APIRouter, Depends, Request
from pymongo.database import Database
from app.dependencies.db import get_db
from schemas.auth.response import TokenResponse
from core.auth.jwt import create_access_token, decode_refresh_token
from slowapi import Limiter
from slowapi.util import get_remote_address

router = APIRouter()
limiter = Limiter(key_func=get_remote_address)


@router.post("/refresh", response_model=TokenResponse)
@limiter.limit("5/minute")
async def refresh_token_route(
        request: Request,
        refresh_token: str,
        db: Database = Depends(get_db)
):
    payload = decode_refresh_token(refresh_token)
    entity_id = payload["sub"]
    entity_type = payload.get("entity_type", "user")

    if entity_type == "user":
        entity = db.users.find_one({"_id": ObjectId(entity_id)})
    elif entity_type == "vendor":
        entity = db.vendors.find_one({"_id": ObjectId(entity_id)})
    else:
        raise HTTPException(status_code=400, detail="Invalid entity type")

    if not entity:
        raise HTTPException(status_code=404, detail="Entity not found")

    access_token = create_access_token({"sub": entity_id, "entity_type": entity_type})
    return TokenResponse(
        message="Token refreshed successfully",
        token=access_token,
        refresh_token=refresh_token,
        entity_id=entity_id,
        entity_type=entity_type,
        status=entity.get("status", "active")
    )