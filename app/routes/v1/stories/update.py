from fastapi import APIRouter, Depends, Request
from pymongo.database import Database
from slowapi import Limiter
from slowapi.util import get_remote_address

from app.dependencies.auth import get_current_vendor
from app.dependencies.db import get_db
from schemas.story.response import StoryResponse
from schemas.story.update import StoryUpdateRequest
from services.story.update import update_story

router = APIRouter()
limiter = Limiter(key_func=get_remote_address)


@router.put("/{story_id}", response_model=StoryResponse)
@limiter.limit("5/minute")
async def update_story_route(
        request: Request,
        story_id: str,
        story_request: StoryUpdateRequest,
        db: Database = Depends(get_db),
        vendor_id: str = Depends(get_current_vendor)
):
    return update_story(db, story_id, story_request, vendor_id, request.client.host)
