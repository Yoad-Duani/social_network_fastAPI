from pymongo import MongoClient, ASCENDING
from .config import settings

client = MongoClient(
            f"mongodb://{settings.mongodb_username}:{settings.mongodb_password}@{settings.mongodb_url}:27017/{settings.mongodb_db_name}?authSource=admin",
            connect=True,
            serverSelectionTimeoutMS=5000,
            # tls=True,
        )

   

def get_db_collection():
    try:
        db_client = client
    except Exception as error:
        print("Eror:")
        print(str(error))
    db = db_client.verification_db
    collection_name = db.verification_collection
    # collection_name.create_index([('user_id', ASCENDING)], unique=True)
    return collection_name


# client = MongoClient(
#     f"mongodb://{settings.mongodb_username}:{settings.mongodb_password}@{settings.mongodb_url}:27017/{settings.mongodb_db_name}?authSource=admin",
#     connect=True,
#     serverSelectionTimeoutMS=5000,
#     tls=True,
# )
# db = client.verification_db
# collection_name = db["verification_collection"]


