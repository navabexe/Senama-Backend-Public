from bson import ObjectId
from pymongo.database import Database

from app.exceptions.validation import ValidationException
from schemas.product.response import ProductResponse


def update_product_position(db: Database, vendor_id: str, product_id: str, new_position: int) -> ProductResponse:
    try:
        product = db.products.find_one({"_id": ObjectId(product_id), "vendor_id": vendor_id})
    except ValueError:
        raise ValidationException(detail="Invalid product ID format")

    if not product:
        raise ValidationException(detail="Product not found")

    db.products.update_one(
        {"_id": ObjectId(product_id)},
        {"$set": {"position": new_position}}
    )

    updated_product = db.products.find_one({"_id": ObjectId(product_id)})
    return ProductResponse(**{**updated_product, "product_id": str(updated_product["_id"])})
