from datetime import datetime, timedelta, timezone

from bson import ObjectId
from pymongo.database import Database

from core.errors import APIException
from core.validators import Validators
from models.story import Story
from schemas.story.create import StoryCreateRequest
from schemas.story.response import StoryResponse
from services.log import create_log


def create_story(db: Database, request: StoryCreateRequest, vendor_id: str, ip_address: str) -> StoryResponse:
    Validators.validate_not_null(request.description, "description")
    Validators.validate_not_null(request.category, "category")

    if request.media_type not in ["image", "video"]:
        raise APIException("INVALID_ID", "Media type must be 'image' or 'video'")
    if request.media_type == "image" and not request.image_url:
        raise APIException("FIELD_REQUIRED", "image_url required for image type")
    if request.media_type == "video" and not request.video_url:
        raise APIException("FIELD_REQUIRED", "video_url required for video type")

    if not db.vendors.find_one({"_id": ObjectId(vendor_id)}):
        raise APIException("VENDOR_NOT_FOUND")

    if request.product_id:
        try:
            if not db.products.find_one({"_id": ObjectId(request.product_id), "vendor_id": vendor_id}):
                raise APIException("VENDOR_NOT_FOUND", "Product not found or not owned by you")
        except ValueError:
            raise APIException("INVALID_ID", "Invalid product ID format")

    expires_at = datetime.now(timezone.utc) + timedelta(hours=request.duration)

    story = Story(
        vendor_id=vendor_id,
        media_type=request.media_type,
        image_url=request.image_url,
        video_url=request.video_url,
        category=request.category,
        description=request.description,
        external_link=request.external_link,
        hashtags=request.hashtags,
        product_id=request.product_id,
        visibility=request.visibility,
        duration=request.duration,
        is_highlight=request.is_highlight,
        is_sponsored=request.is_sponsored,
        sponsored_settings=request.sponsored_settings,
        created_at=datetime.now(timezone.utc).isoformat(),
        expires_at=expires_at.isoformat()
    )

    result = db.stories.insert_one(story.model_dump(exclude={"id"}))
    story_id = str(result.inserted_id)

    create_log(db, "create", "story", story_id, vendor_id, None, story.model_dump(exclude={"id"}), ip_address)

    return StoryResponse(
        id=story_id,
        vendor_id=story.vendor_id,
        media_type=story.media_type,
        image_url=story.image_url,
        video_url=story.video_url,
        category=story.category,
        description=story.description,
        external_link=story.external_link,
        hashtags=story.hashtags,
        product_id=story.product_id,
        visibility=story.visibility,
        duration=story.duration,
        is_highlight=story.is_highlight,
        is_sponsored=story.is_sponsored,
        sponsored_settings=story.sponsored_settings,
        created_at=story.created_at,
        expires_at=story.expires_at,
        views_count=story.views_count,
        likes_count=story.likes_count,
        shares_count=story.shares_count
    )
