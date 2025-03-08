from datetime import datetime, UTC, timedelta

from bson import ObjectId
from pymongo.database import Database

from core.errors import APIException
from core.utils.db import map_db_to_response
from schemas.story.response import StoryResponse
from schemas.story.update import StoryUpdateRequest
from services.log import create_log


def update_story(db: Database, story_id: str, request: StoryUpdateRequest, vendor_id: str,
                 ip_address: str) -> StoryResponse:
    try:
        story = db.stories.find_one({"_id": ObjectId(story_id), "vendor_id": vendor_id})
    except ValueError:
        raise APIException("INVALID_ID", "Invalid story ID format")

    if not story:
        raise APIException("VENDOR_NOT_FOUND", "Story not found or not owned by you")

    update_data = request.dict(exclude_unset=True)
    if "description" in update_data and not update_data["description"]:
        raise APIException("FIELD_REQUIRED", "description cannot be empty")
    if "category" in update_data and not update_data["category"]:
        raise APIException("FIELD_REQUIRED", "category cannot be empty")

    if "media_type" in update_data:
        if update_data["media_type"] not in ["image", "video"]:
            raise APIException("INVALID_ID", "Media type must be 'image' or 'video'")
        if update_data["media_type"] == "image" and not update_data.get("image_url", story["image_url"]):
            raise APIException("FIELD_REQUIRED", "image_url required for image type")
        if update_data["media_type"] == "video" and not update_data.get("video_url", story["video_url"]):
            raise APIException("FIELD_REQUIRED", "video_url required for video type")

    if "product_id" in update_data and update_data["product_id"]:
        try:
            if not db.products.find_one({"_id": ObjectId(update_data["product_id"]), "vendor_id": vendor_id}):
                raise APIException("VENDOR_NOT_FOUND", "Product not found or not owned by you")
        except ValueError:
            raise APIException("INVALID_ID", "Invalid product ID format")

    if "duration" in update_data:
        expires_at = datetime.now(UTC) + timedelta(hours=update_data["duration"])
        update_data["expires_at"] = expires_at.isoformat()

    previous_data = story.copy()
    update_data["updated_at"] = datetime.now(UTC).isoformat()

    db.stories.update_one({"_id": ObjectId(story_id)}, {"$set": update_data})
    updated_story = db.stories.find_one({"_id": ObjectId(story_id)})

    create_log(db, "update", "story", story_id, vendor_id, previous_data, updated_story, ip_address)

    return map_db_to_response(updated_story, StoryResponse)