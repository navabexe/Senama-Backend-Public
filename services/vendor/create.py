from pymongo.database import Database

from core.errors import APIException
from core.validators import Validators
from models.vendor import Vendor
from schemas.vendor.create import VendorCreateRequest
from schemas.vendor.response import VendorResponse
from services.log import create_log


def create_vendor(db: Database, request: VendorCreateRequest, admin_id: str, ip_address: str) -> VendorResponse:
    Validators.validate_not_null(request.business_category_ids, "business_category_ids")

    existing_vendor = db.vendors.find_one({"username": request.username})
    if existing_vendor:
        raise APIException("FORBIDDEN", "Username already taken")

    vendor = Vendor(
        username=request.username,
        name=request.name,
        owner_name=request.owner_name,
        owner_phone=request.owner_phone,
        address=request.address,
        location=request.location.model_dump(),
        city=request.city,
        province=request.province,
        business_category_ids=request.business_category_ids,
        created_by=admin_id,
        updated_by=admin_id
    )

    result = db.vendors.insert_one(vendor.model_dump(exclude={"id"}))
    vendor_id = str(result.inserted_id)

    create_log(db, "create", "vendor", vendor_id, admin_id, None, vendor.model_dump(exclude={"id"}), ip_address)

    return VendorResponse(
        id=vendor_id,
        username=vendor.username,
        name=vendor.name,
        owner_name=vendor.owner_name,
        owner_phone=vendor.owner_phone,
        address=vendor.address,
        location=vendor.location,
        city=vendor.city,
        province=vendor.province,
        logo_urls=vendor.logo_urls,
        banner_urls=vendor.banner_urls,
        bios=vendor.bios,
        about_us=vendor.about_us,
        branches=vendor.branches,
        business_details=vendor.business_details,
        visibility=vendor.visibility,
        attached_vendors=vendor.attached_vendors,
        blocked_vendors=vendor.blocked_vendors,
        account_types=vendor.account_types,
        status=vendor.status,
        vendor_type=vendor.vendor_type,
        social_links=vendor.social_links,
        messenger_links=vendor.messenger_links,
        followers_count=vendor.followers_count,
        following_count=vendor.following_count,
        business_category_ids=vendor.business_category_ids,
        created_by=vendor.created_by,
        created_at=vendor.created_at,
        updated_by=vendor.updated_by,
        updated_at=vendor.updated_at,
        profile_picture=vendor.profile_picture,
        gender=vendor.gender,
        birth_date=vendor.birth_date,
        language=vendor.language,
        notification_settings=vendor.notification_settings,
        privacy_settings=vendor.privacy_settings,
        connected_devices=vendor.connected_devices,
        followers=vendor.followers,
        following=vendor.following,
        working_hours=vendor.working_hours,
        shipping_methods=vendor.shipping_methods
    )
