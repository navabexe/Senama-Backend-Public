from fastapi import APIRouter, Depends, Request
from pymongo.database import Database
from slowapi import Limiter
from slowapi.util import get_remote_address

from app.dependencies.auth import get_current_user
from app.dependencies.db import get_db
from schemas.pagination import PaginationParams, PaginatedResponse
from schemas.story.response import StoryResponse
from services.story.read import get_story, get_stories

router = APIRouter()
limiter = Limiter(key_func=get_remote_address)


@router.get("/{story_id}", response_model=StoryResponse)
@limiter.limit("10/minute")
async def read_story(
        request: Request,
        story_id: str,
        db: Database = Depends(get_db),
        user_id: str = Depends(get_current_user)
):
    return get_story(db, story_id, user_id, request.client.host)


@router.get("", response_model=PaginatedResponse[StoryResponse])
@limiter.limit("10/minute")
async def read_stories_list(
        request: Request,
        pagination: PaginationParams = Depends(),
        db: Database = Depends(get_db),
        user_id: str = Depends(get_current_user)
):
    return get_stories(db, user_id, pagination.limit, pagination.offset, request.client.host)
