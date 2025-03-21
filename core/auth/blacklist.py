from datetime import datetime, timedelta, timezone

from pymongo.database import Database

from app.config.settings import settings


def blacklist_token(db: Database, token: str, vendor_id: str):
    db.blacklist.insert_one({
        "token": token,
        "vendor_id": vendor_id,
        "blacklisted_at": datetime.now(timezone.utc).isoformat(),
        "expires_at": (datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)).isoformat()
    })
