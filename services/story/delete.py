from bson import ObjectId
from pymongo.database import Database

from core.errors import APIException
from core.utils.db import map_db_to_response
from schemas.story.response import StoryResponse
from services.log import create_log


def delete_story(db: Database, story_id: str, vendor_id: str, ip_address: str) -> StoryResponse:
    try:
        story = db.stories.find_one({"_id": ObjectId(story_id), "vendor_id": vendor_id})
    except ValueError:
        raise APIException("INVALID_ID", "Invalid story ID format")

    if not story:
        raise APIException("VENDOR_NOT_FOUND", "Story not found or not owned by you")

    previous_data = story.copy()
    db.stories.delete_one({"_id": ObjectId(story_id)})

    create_log(db, "delete", "story", story_id, vendor_id, previous_data, None, ip_address)

    return map_db_to_response(story, StoryResponse)
