from pymongo import MongoClient

from app.config.settings import settings


def get_db_client() -> MongoClient:
    client = MongoClient(settings.MONGO_URI)
    return client


def get_db():
    client = get_db_client()
    try:
        yield client.get_default_database()
    finally:
        client.close()
