from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from colorama import init, Fore
from .config import settings
from pymongo import MongoClient, ASCENDING 
from pymongo.errors import ServerSelectionTimeoutError, WriteError, OperationFailure
from app.log_config import init_loggers
from fastapi import Request
from contextlib import contextmanager
from pymongo.collection import Collection, InsertOneResult
from typing import List
from . import schemas
from bson import ObjectId, json_util

import traceback

# from fastapi import status , HTTPException
log = init_loggers(logger_name="mongo-logger")




# user_mongo_schema = schema.Schema({
#     "name": str,
#     "email": str,
#     "age": int
# })


@contextmanager
def get_mongodb(request: Request = None):
    if request is not None:
        request_id = request.headers.get("X-Request-ID")
    else:
        request_id = ""
    log.info(f"Trying to connect to mongo.", extra={"request_id": request_id})
    client = MongoClient(
        f"mongodb://{settings.mongodb_username}:{settings.mongodb_password}@{settings.mongodb_url}:27017/{settings.mongodb_db_name}?authSource=admin",
        connect=True,
        serverSelectionTimeoutMS=3000,
    )
    try:
        yield client
    except Exception as ex:
        print(ex)
    # finally:
    #     client.close()



# TODO:
# It should not return a value
def check_or_create_collections(mongo_client: MongoClient, db_name: str, collection_names: List[str]):
    db = mongo_client[db_name]
    existing_collection_names = db.list_collection_names()
    # collections = []
    for collection_name in collection_names:
        if collection_name in existing_collection_names:
            # collections.append(db[collection_name])
            log.info(f"Collection {collection_name} already exists.")
        else:
            db.create_collection(collection_name)
            # collections.append(db[collection_name])
            log.info(f"Collection {collection_name} created.")
            try:
                db.collection_name.create_index("created_at", expireAfterSeconds=86400)
            except:
                log.error(f"error while creating index.")
    # return collections


def get_db_collection(request_id: str, client: MongoClient, db_name: str, collection_name: str)-> Collection:
    log.info(f"Getting collection from mongo.", extra={"request_id": request_id})
    try:
        db = client[db_name]
        collection_name = db[collection_name]
    except Exception as ex:
       log.error(f"Failed get collection from mongo.", extra={"request_id": request_id}) 
    return collection_name


def insert_one_to_collection(request_id: str, client: MongoClient, db_name: str, collection_name: str, user_mongo: schemas.UserMongo) -> InsertOneResult:
    """insert one to collection to the collection provided

    Args:
            request_id (str): For logging purposes\n
            client (MongoClient):\n
            db_name (str):\n
            collection_name (str):\n
            user_mongo (schemas.UserMongo):
    Returns:
            InsertOneResult: The result of the insert
    Raises:
            pymongo.errors.WriteError: 
    """
    mongo_collection = get_db_collection(
                    request_id= request_id,
                    client= client,
                    db_name= db_name,
                    collection_name= collection_name
                )
    user_mongo_dict = user_mongo.dict()
    user_mongo_dict["_id"] = ObjectId()
    try:
        _id = mongo_collection.insert_one(user_mongo_dict)
        log.info(f"User {user_mongo.email} has been added to mongo for email verification.", extra={"request_id": request_id})
    except WriteError as ex:
        log.error(f"Failed insert user to mongo. {ex}", extra={"request_id": request_id})
        raise Exception(f"Failed insert user to mongo: {ex}")
    return _id


# TODO:
# created_at should be a dynamic parameter
def create_index_created_at(mongo_client: MongoClient, db_name: str, collection_name: str, time_in_seconds: int):
    """create index created_at to the collection provided

    Args:
            mongo_client (MongoClient):\n
            db_name (str):\n
            collection_name (str):\n
            time_in_seconds (int): The time for the record to be in Mongo before it is deleted
    """
    db = mongo_client[db_name]
    collection = db[collection_name]
    if "created_at_index" not in collection.index_information():
        try:
            log.info(f"Index created_at does not exist, create index.")
            # collection.create_index("created_at", expireAfterSeconds=time_in_seconds,)
            collection.create_index([("created_at", ASCENDING)],
                                    name='created_at_index',
                                    background=True,
                                    expireAfterSeconds=time_in_seconds
            )
            log.info(f"An index created_at is currently being created in the background.")
        except OperationFailure as ex:
            log.error(f"Failed to create index created_at for mongo: {ex}")
            log.warning(f"Lack of indexing can cause poor performance.")
    else:
        log.info(f"Index created_at already exists, skip.")


def create_index_user_id(mongo_client: MongoClient, db_name: str, collection_name: str):
    """create index user_id to the collection provided

    Args:
            mongo_client (MongoClient):\n
            db_name (str):\n
            collection_name (str):\n
    """
    db = mongo_client[db_name]
    collection = db[collection_name]
    if "user_id_index" not in collection.index_information():
        try:
            log.info(f"Index user_id does not exist, create index.")
            # collection.create_index("created_at", expireAfterSeconds=time_in_seconds,)
            collection.create_index([("user_id", ASCENDING)],
                                    name='user_id_index',
                                    background=True,
                                    unique=True,
            )
            log.info(f"An index user_id is currently being created in the background.")
        except Exception as ex:
            log.error(f"Failed to create index user_id for mongo: {ex}")
            log.warning(f"Lack of indexing can cause poor performance.")
    else:
        log.info(f"Index user_id already exists, skip.")


def find_user_by_user_id(request_id: str, mongo_client: MongoClient, collection_name: str, user_id: str):
    db = mongo_client.get_database()
    collection = db[collection_name]
    try:
        user = collection.find_one({"user_id": user_id})
    except Exception as ex:
        log.error(f"Failed to search for user in mongo: {ex}", extra={"request_id": request_id})
        raise Exception(f"Failed to search for user in mongo: {ex}")
    return user


def delete_user_by_user_id(request_id: str, mongo_client: MongoClient, collection_name: str, user_id: str):
    db = mongo_client.get_database()
    collection = db[collection_name]
    try:
        result = collection.delete_one({"user_id": user_id})
    except Exception as ex:
        log.error(f"Error during user deletion: {ex}", extra={"request_id": request_id})
        raise Exception(f"Error during user deletion: {ex}")
    return result