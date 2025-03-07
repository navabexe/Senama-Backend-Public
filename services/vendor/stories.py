from typing import List, Tuple

from bson import ObjectId
from pymongo.database import Database

from app.exceptions.validation import ValidationException
from core.utils.pagination import paginate_query
from schemas.pagination import PaginationParams
from schemas.story.response import StoryResponse


def get_vendor_stories(
        db: Database,
        vendor_id: str,
        pagination: PaginationParams
) -> Tuple[List[StoryResponse], int]:
    try:
        if not db.vendors.find_one({"_id": ObjectId(vendor_id)}):
            raise ValidationException(detail="Vendor not found")
    except ValueError:
        raise ValidationException(detail="Invalid vendor ID format")

    query = db.stories.find({"vendor_id": vendor_id})
    total = db.stories.count_documents({"vendor_id": vendor_id})
    stories = paginate_query(query, pagination.limit, pagination.offset)

    result = [StoryResponse(**{**s, "story_id": str(s["_id"])}) for s in stories]
    return result, total
