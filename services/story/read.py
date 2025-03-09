from bson import ObjectId
from pymongo.database import Database

from core.errors import APIException
from core.utils.db import map_db_to_response
from schemas.pagination import PaginatedResponse
from schemas.story.response import StoryResponse
from services.log import create_log


def get_story(db: Database, story_id: str, user_id: str, ip_address: str) -> StoryResponse:
    try:
        story = db.stories.find_one({"_id": ObjectId(story_id)})
    except ValueError:
        raise APIException("INVALID_ID", "Invalid story ID format")

    if not story:
        raise APIException("NOT_FOUND", "Story not found")

    if story["vendor_id"] != user_id and story["status"] != "active":
        raise APIException("FORBIDDEN", "You can only view your own or active stories")

    create_log(db, "read", "story", story_id, user_id, None, None, ip_address)
    return map_db_to_response(story, StoryResponse)


def get_stories(db: Database, user_id: str, limit: int, offset: int, ip_address: str) -> PaginatedResponse[
    StoryResponse]:
    query = {"status": "active"} if user_id != "admin" else {"vendor_id": user_id}
    stories = db.stories.find(query).skip(offset).limit(limit)
    total = db.stories.count_documents(query)
    items = [map_db_to_response(story, StoryResponse) for story in stories]

    create_log(db, "read", "story", "list", user_id, None, None, ip_address)
    return PaginatedResponse[StoryResponse](
        items=items,
        total=total,
        limit=limit,
        offset=offset
    )