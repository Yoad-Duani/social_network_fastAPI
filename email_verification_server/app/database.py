from pymongo import MongoClient
from .config import settings

client = MongoClient(
    f"mongodb://{settings.mongodb_username}:{settings.mongodb_password}@{settings.mongodb_url}:27017/{settings.mongodb_db_name}?authSource=admin", connect=True,
    serverSelectionTimeoutMS=5000,
)  # The port of the server that mongdo need to connect
db = client.verification_db
collection_name = db["verification_collection"]

