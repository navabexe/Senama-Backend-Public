from fastapi import Depends
from pymongo import MongoClient

from app.config.settings import settings


def get_db_client() -> MongoClient:
    return MongoClient(settings.MONGO_URI)


def get_db(client: MongoClient = Depends(get_db_client)):
    return client.get_default_database()
