from datetime import datetime, UTC

from bson import ObjectId
from pymongo.database import Database

from core.errors import APIException
from core.utils.db import map_db_to_response
from schemas.pagination import PaginatedResponse
from schemas.story.response import StoryResponse
from services.log.log import create_log


def get_story(db: Database, story_id: str, user_id: str, ip_address: str) -> StoryResponse:
    try:
        story = db.stories.find_one({"_id": ObjectId(story_id)})
    except ValueError:
        raise APIException("INVALID_ID", "Invalid story ID format")

    if not story:
        raise APIException("VENDOR_NOT_FOUND", "Story not found")

    if story["visibility"] == "followers":
        vendor = db.vendors.find_one({"_id": ObjectId(story["vendor_id"])})
        if user_id not in vendor.get("followers", []):
            raise APIException("FORBIDDEN", "Story is only visible to followers")

    create_log(db, "read", "story", story_id, user_id, None, None, ip_address)

    return map_db_to_response(story, StoryResponse)


def get_stories(db: Database, user_id: str, limit: int, offset: int, ip_address: str) -> PaginatedResponse[
    StoryResponse]:
    now = datetime.now(UTC).isoformat()
    stories = db.stories.find({
        "$or": [
            {"expires_at": {"$gt": now}},
            {"is_highlight": True}
        ]
    }).skip(offset).limit(limit)

    total = db.stories.count_documents({
        "$or": [
            {"expires_at": {"$gt": now}},
            {"is_highlight": True}
        ]
    })

    items = []
    for story in stories:
        if story["visibility"] == "followers":
            vendor = db.vendors.find_one({"_id": ObjectId(story["vendor_id"])})
            if user_id in vendor.get("followers", []):
                items.append(StoryResponse(**story))
        else:
            items.append(StoryResponse(**story))

    create_log(db, "read", "story", "list", user_id, None, None, ip_address)

    return PaginatedResponse[StoryResponse](
        items=items,
        total=total,
        limit=limit,
        offset=offset
    )
