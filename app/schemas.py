
from os import name
import re
from typing import List, Optional
from fastapi import Query
from psycopg2 import connect
from pydantic import BaseModel, EmailStr
from datetime import date, datetime
from pydantic.types import conint
from pydantic import Required
from . import validators
from app import constants as const

# import uvicorn
# from fastapi import FastAPI, Path, Depends
from fastapi.exceptions import RequestValidationError, ValidationError
# from fastapi.responses import JSONResponse
from pydantic import BaseModel, validator
# import calendar
# import datetime
# import json


'''
    All the schemas that used for get input have a strict input validation using pydantic validator and fastapi Query
    All the schemas that used for output have a basic out validation
'''


class GroupsResponse(BaseModel):
    groups_id: int
    creator_id: int
    name: str
    description: str
    created_at: datetime
    update_at: datetime
    group_private: bool
    members: int
    class Config:
        orm_mode = True

class GroupsUpdateResponse(BaseModel):
    groups_id: int
    creator_id: int
    name: str
    description: str
    created_at: datetime
    update_at: datetime
    group_private: bool
    class Config:
        orm_mode = True

# class UsersInGroupsUpdate(BaseModel):
#     is_blocked: Optional[bool] = None
#     request_accepted: Optional[bool] = None


class UsersInGroupsResponse(BaseModel):
    user_id: int
    groups_id: int
    class Config:
        orm_mode = True

class GroupUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    group_private: Optional[bool] = None
    
class GroupCreate(BaseModel):
    name: str
    description: str
    group_private: bool
    
class GroupCreateRespone(BaseModel):
    groups_id: int
    creator_id: int
    name: str
    description: str
    group_private: bool
    class Config:
        orm_mode = True


#Comments
class CommentUpdate(BaseModel):
    content: str

class CommentCreate(BaseModel):
    content: str
    
class CommentResponse(BaseModel):
    comment_id: int
    user_id: int
    post_id: int
    content: str
    created_at: datetime
    update_at: datetime
    class Config:
        orm_mode = True

### Vote ###
class Vote(BaseModel):
    post_id: int
    dir: conint(ge=0, le=1)

### User ###
class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    name: str
    birth_date: date
    company_name: str
    description: str
    position: str
    class Config:
        orm_mode = True

class UserCreate(BaseModel):
    email: EmailStr = Query(default= Required)
    password: str = Query(default= Required ,min_length=8)
    name: str = Query(default= Required ,min_length=2, max_length=16)
    birth_date: date = Query(default= Required)
    company_name: str = Query(default= Required, min_length=2, max_length= 18)
    description: str = Query(default= Required, min_length=1, max_length= 100)
    position: str = Query(default= Required, min_length= 2, max_length= 18)

    _validator_password = validator("password", allow_reuse= True)(validators.validator_password)
    _validator_name = validator("name", allow_reuse= True)(validators.validator_name)
    _validator_company_name = validator("company_name", allow_reuse= True)(validators.validator_name_only_special_characters)
    _validator_position = validator("position", allow_reuse= True)(validators.validator_name_only_special_characters)



class UserUpdate(BaseModel):
    password: Optional[str] = Query(default= None ,min_length=8)
    company_name: Optional[str] = Query(default= None, min_length=2, max_length= 18)
    description: Optional[str] = Query(default= None, min_length=1, max_length= 100)
    position: Optional[str] = Query(default= None, min_length= 2, max_length= 18)

    _validator_password = validator("password", allow_reuse= True)(validators.validator_password)
    _validator_company_name = validator("company_name", allow_reuse= True)(validators.validator_name_only_special_characters)
    _validator_position = validator("position", allow_reuse= True)(validators.validator_name_only_special_characters)



### Login ###
class UserLogin(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None
    verified: Optional[bool] = None
    is_blocked: Optional[bool] = None

### Post ###
class PostBase(BaseModel):
    title: str = Query(default= Required, min_length= const.MIN_LENGTH_TITLE_POST_SCHEMAS, max_length= const.MAX_LENGTH_TITLE_POST_SCHEMAS)
    content: str = Query(default= Required, min_length= const.MIN_LENGTH_CONTENT_POST_SCHEMAS, max_length= const.MAX_LENGTH_CONTENT_POST_SCHEMAS)
    published : bool = Query(default= True, title= "published post", description= "Defines whether the post is public or not")

class PostCreate(PostBase):
    pass

class PostResponse(PostBase):
    id: int
    created_at: datetime
    group_id: int
    owner_id: int
    owner: UserResponse
    class Config:
        orm_mode = True

class PostOut(BaseModel):
    Post: PostResponse
    votes: int
    comments: int
    class Config:
        orm_mode = True

class JoinRequestGroupResponse(BaseModel):
    user_id: int
    groups_id: int
    name: str
    group_name: str
    class Config:
        orm_mode = True

class ReplaceManager(BaseModel):
    new_manager_id: int


class EmailSchema(BaseModel):
    email: List[EmailStr]




