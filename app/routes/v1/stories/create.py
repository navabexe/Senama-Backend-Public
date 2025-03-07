from fastapi import APIRouter, Depends, Request
from pymongo.database import Database
from slowapi import Limiter
from slowapi.util import get_remote_address

from app.dependencies.auth import get_current_vendor
from app.dependencies.db import get_db
from schemas.story.create import StoryCreateRequest
from schemas.story.response import StoryResponse
from services.story.create import create_story

router = APIRouter()
limiter = Limiter(key_func=get_remote_address)


@router.post("", response_model=StoryResponse)
@limiter.limit("5/minute")
async def create_story_route(
        request: Request,
        story_request: StoryCreateRequest,
        db: Database = Depends(get_db),
        vendor_id: str = Depends(get_current_vendor)
):
    return create_story(db, story_request, vendor_id, request.client.host)
