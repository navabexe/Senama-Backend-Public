from pymongo import ASCENDING

from app.dependencies.db import get_db_client


def setup_indexes():
    client = get_db_client()
    db = client.get_default_database()

    # Index for vendors collection
    db.vendors.create_index([("phone", ASCENDING)], unique=True)
    db.vendors.create_index([("business_name", ASCENDING)])
    db.vendors.create_index([("categories", ASCENDING)])


if __name__ == "__main__":
    setup_indexes()
