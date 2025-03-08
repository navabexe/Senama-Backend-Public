from pymongo.database import Database
from schemas.user.create import UserCreateRequest
from schemas.user.response import UserResponse
from models.user import User
from services.log import create_log
from core.errors import APIException
from core.utils.hash import hash_password
from datetime import datetime, UTC


def create_user(db: Database, request: UserCreateRequest, ip_address: str) -> UserResponse:
    existing_user = db.users.find_one({"phone": request.phone})
    if existing_user:
        raise APIException("FORBIDDEN", "Phone number already registered")

    user = User(
        phone=request.phone,
        first_name=request.first_name,
        last_name=request.last_name,
        password=hash_password(request.password) if request.password else None,
        roles=["user"],
        status="active",
        created_at=datetime.now(UTC).isoformat(),
        updated_at=datetime.now(UTC).isoformat()
    )

    result = db.users.insert_one(user.dict(exclude={"id"}))
    user_id = str(result.inserted_id)

    create_log(db, "create", "user", user_id, user_id, None, user.dict(exclude={"id"}), ip_address)

    return UserResponse(
        id=user_id,
        phone=user.phone,
        first_name=user.first_name,
        last_name=user.last_name,
        password=user.password,
        roles=user.roles,
        status=user.status,
        otp=None,
        otp_expires_at=None,
        bio=user.bio,
        avatar_urls=user.avatar_urls,
        phones=user.phones,
        birthdate=user.birthdate,
        gender=user.gender,
        languages=user.languages,
        created_at=user.created_at,
        updated_at=user.updated_at
    )