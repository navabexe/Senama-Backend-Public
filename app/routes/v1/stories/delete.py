from fastapi import APIRouter, Depends, Request
from pymongo.database import Database
from slowapi import Limiter
from slowapi.util import get_remote_address

from app.dependencies.auth import get_current_vendor
from app.dependencies.db import get_db
from schemas.story.response import StoryResponse
from services.story.delete import delete_story

router = APIRouter()
limiter = Limiter(key_func=get_remote_address)


@router.delete("/{story_id}", response_model=StoryResponse)
@limiter.limit("5/minute")
async def delete_story_route(
        request: Request,
        story_id: str,
        db: Database = Depends(get_db),
        vendor_id: str = Depends(get_current_vendor)
):
    return delete_story(db, story_id, vendor_id, request.client.host)
