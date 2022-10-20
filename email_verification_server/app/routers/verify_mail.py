from fastapi import Body, FastAPI, Path, Query , Response ,status , HTTPException, Depends, APIRouter
from .. import schemas
from ..models import user_serializer, users_serializer
from ..database import get_db_collection
from bson import ObjectId
from pymongo.collection import Collection

# router = APIRouter(
#     prefix= "/email-verification",
#     tags= ['email-verification']
#     )

router = APIRouter(
    prefix= "/user-test",
    tags= ['user-test']
    )

# @router.get('/')
# async def create_user():
#     info = client.server_info()
#     print(info )
#     return info

@router.get('/')
async def get_users(collection: Collection = Depends(get_db_collection)):
    users = users_serializer(collection.find())
    return users

@router.get("/{user_id}")
async def get_user(user_id: int, collection: Collection = Depends(get_db_collection)):
    user = users_serializer(collection.find({"user_id": user_id}))
    return user

@router.post("/")
async def create_user(user: schemas.User, collection: Collection = Depends(get_db_collection)):
    _id = collection.insert_one(dict(user))
    user = users_serializer(collection.find({"_id": ObjectId(_id.inserted_id)}))
    return user

@router.put("/{user_id}")
async def update_user(user_id: int, user: schemas.User, collection: Collection = Depends(get_db_collection)):
    collection.find_one_and_update({"user_id": user_id}, {"$set": dict(user)})
    user = collection.find({"user_id": user_id})
    return user

@router.delete("/{user_id}")
async def delete_user(user_id: int, collection: Collection = Depends(get_db_collection)):
    collection.find_one_and_delete({"user_id": user_id})
    user = collection.find({"user_id": user_id})
    return user
