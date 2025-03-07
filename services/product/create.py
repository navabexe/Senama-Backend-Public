from datetime import datetime, UTC

from bson import ObjectId
from pymongo.database import Database

from core.errors import APIException
from core.validators import Validators
from models.product import Product
from schemas.product.create import ProductCreateRequest
from schemas.product.response import ProductResponse
from services.log.log import create_log


def create_product(db: Database, request: ProductCreateRequest, vendor_id: str, ip_address: str) -> ProductResponse:
    Validators.validate_not_null(request.names, "names")
    Validators.validate_not_null(request.category_ids, "category_ids")

    if not db.vendors.find_one({"_id": ObjectId(vendor_id)}):
        raise APIException("VENDOR_NOT_FOUND")

    for category_id in request.category_ids:
        try:
            if not db.product_categories.find_one({"_id": ObjectId(category_id)}):
                raise APIException("VENDOR_NOT_FOUND", f"Category {category_id} not found")
        except ValueError:
            raise APIException("INVALID_ID", f"Invalid category ID: {category_id}")

    product = Product(
        vendor_id=vendor_id,
        names=request.names,
        short_descriptions=request.short_descriptions,
        prices=request.prices,
        colors=request.colors,
        images=request.images,
        video_urls=request.video_urls,
        audio_files=request.audio_files,
        technical_specs=request.technical_specs,
        tags=request.tags,
        thumbnail_urls=request.thumbnail_urls,
        suggested_products=request.suggested_products,
        category_ids=request.category_ids,
        subcategory_ids=request.subcategory_ids,
        created_by=vendor_id,
        updated_by=vendor_id,
        created_at=datetime.now(UTC).isoformat(),
        updated_at=datetime.now(UTC).isoformat()
    )

    result = db.products.insert_one(product.dict(exclude={"id"}))
    product_id = str(result.inserted_id)

    create_log(db, "create", "product", product_id, vendor_id, None, product.dict(exclude={"id"}), ip_address)

    return ProductResponse(
        id=product_id,
        vendor_id=product.vendor_id,
        names=product.names,
        short_descriptions=product.short_descriptions,
        prices=product.prices,
        colors=product.colors,
        images=product.images,
        video_urls=product.video_urls,
        audio_files=product.audio_files,
        technical_specs=product.technical_specs,
        tags=product.tags,
        thumbnail_urls=product.thumbnail_urls,
        suggested_products=product.suggested_products,
        status=product.status,
        qr_code_url=product.qr_code_url,
        category_ids=product.category_ids,
        subcategory_ids=product.subcategory_ids,
        created_by=product.created_by,
        created_at=product.created_at,
        updated_by=product.updated_by,
        updated_at=product.updated_at,
        draft=product.draft
    )
