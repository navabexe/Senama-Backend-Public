from pymongo.database import Database

from core.errors import APIException
from core.validators import Validators
from models.business_category import BusinessCategory
from schemas.business_category.create import BusinessCategoryCreateRequest
from schemas.business_category.response import BusinessCategoryResponse
from services.log import create_log


def create_business_category(db: Database, request: BusinessCategoryCreateRequest, admin_id: str,
                             ip_address: str) -> BusinessCategoryResponse:
    Validators.validate_not_null(request.name, "name")

    existing_category = db.business_categories.find_one({"name": request.name})
    if existing_category:
        raise APIException("FORBIDDEN", "Category name already exists")

    category = BusinessCategory(
        name=request.name,
        image_url=request.image_url
    )

    result = db.business_categories.insert_one(category.model_dump(exclude={"id"}))
    category_id = str(result.inserted_id)

    create_log(db, "create", "category", category_id, admin_id, None, category.model_dump(exclude={"id"}), ip_address)

    return BusinessCategoryResponse(
        id=category_id,
        name=category.name,
        image_url=category.image_url,
        created_at=category.created_at,
        updated_at=category.updated_at
    )
