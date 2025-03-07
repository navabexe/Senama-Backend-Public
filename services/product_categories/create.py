from bson import ObjectId
from pymongo.database import Database

from core.errors import APIException
from core.validators import Validators
from models.product_category import ProductCategory
from schemas.product_category.create import ProductCategoryCreateRequest
from schemas.product_category.response import ProductCategoryResponse
from services.log.log import create_log


def create_product_category(db: Database, request: ProductCategoryCreateRequest, admin_id: str,
                            ip_address: str) -> ProductCategoryResponse:
    Validators.validate_not_null(request.name, "name")

    existing_category = db.product_categories.find_one({"name": request.name})
    if existing_category:
        raise APIException("FORBIDDEN", "Category name already exists")

    if request.parent_category_id:
        try:
            parent = db.product_categories.find_one({"_id": ObjectId(request.parent_category_id)})
            if not parent:
                raise APIException("VENDOR_NOT_FOUND", "Parent category not found")
        except ValueError:
            raise APIException("INVALID_ID", "Invalid parent category ID format")

    category = ProductCategory(
        name=request.name,
        image_url=request.image_url,
        parent_category_id=request.parent_category_id
    )

    result = db.product_categories.insert_one(category.dict(exclude={"id"}))
    category_id = str(result.inserted_id)

    create_log(db, "create", "category", category_id, admin_id, None, category.dict(exclude={"id"}), ip_address)

    return ProductCategoryResponse(
        id=category_id,
        name=category.name,
        image_url=category.image_url,
        parent_category_id=category.parent_category_id,
        created_at=category.created_at,
        updated_at=category.updated_at
    )
