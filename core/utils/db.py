from typing import Dict, Any, Type, TypeVar
from bson import ObjectId
from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)


def map_db_to_response(db_data: Dict[str, Any], response_model: Type[T]) -> T:
    """
    تبدیل داده‌های دیتابیس به اسکیمای پاسخ Pydantic.
    :param db_data: داده خام از دیتابیس (دیکشنری)
    :param response_model: کلاس اسکیمای پاسخ (مثل UserResponse)
    :return: نمونه‌ای از response_model
    """
    # تبدیل _id به id
    if "_id" in db_data:
        db_data["id"] = str(db_data.pop("_id"))

    # برگرداندن نمونه اسکیما با داده‌های مپ‌شده
    return response_model(**{k: db_data.get(k) for k in response_model.__fields__})