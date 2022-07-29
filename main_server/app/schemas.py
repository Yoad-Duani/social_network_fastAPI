
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
from pydantic import BaseModel, validator, Field
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
    name: Optional[str] = Field(default= None, title="The new name of the group", min_length=const.MIN_LENGTH_NAME_GROUP_SCHEMAS, max_length= const.MAX_LENGTH_NAME_GROUP_SCHEMAS)
    description: Optional[str] = Field(default= None, title= "The new description of the group", min_length=const.MIN_LENGTH_DESCRIPTION_GROUP_SCHEMAS, max_length=const.MAX_LENGTH_DESCRIPTION_GROUP_SCHEMAS)
    group_private: Optional[bool] = Field(default= None, title= "group private or public", description= "Defines whether the group is public or not")
    
class GroupCreate(BaseModel):
    name: str = Field(default= Required, title= "The name of the group", min_length=const.MIN_LENGTH_NAME_GROUP_SCHEMAS, max_length= const.MAX_LENGTH_NAME_GROUP_SCHEMAS)
    description: str = Field(default= Required, title= "The description of the group", min_length=const.MIN_LENGTH_DESCRIPTION_GROUP_SCHEMAS, max_length=const.MAX_LENGTH_DESCRIPTION_GROUP_SCHEMAS)
    group_private: bool = Field(default= Required, title= "group private or public", description= "Defines whether the group is public or not")
    
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
    content: str = Field(default= Required, title= "The content of the comment", min_length= const.MIN_LENGTH_CONTENT_COMMENT_SCHEMAS, max_length= const.MAX_LENGTH_CONTENT_COMMENT_SCHEMAS)

class CommentCreate(BaseModel):
    content: str = Field(default= Required, title= "The content of the comment", min_length= const.MIN_LENGTH_CONTENT_COMMENT_SCHEMAS, max_length= const.MAX_LENGTH_CONTENT_COMMENT_SCHEMAS)
    
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
    post_id: int = Query(default= Required, ge= const.POST_ID_GE)
    dir: int = Field(default= Required, ge= const.VOTE_MIN_VALUE, le= const.VOTE_MAX_VALUE)

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
    email: EmailStr = Field(default= Required)
    password: str = Field(default= Required ,min_length= const.MIN_LENGTH_PASSWORD_USER_SCHEMA)
    name: str = Field(default= Required ,min_length= const.MIN_LENGTH_NAME_USER_SCHEMA, max_length= const.MAX_LENGTH_NAME_USER_SCHEMA)
    birth_date: date = Field(default= Required)
    company_name: str = Field(default= Required, min_length= const.MIN_LENGTH_COMPANY_NAME_USER_SCHEMA, max_length= const.MAX_LENGTH_COMPANY_NAME_USER_SCHEMA)
    description: str = Field(default= Required, min_length= const.MIN_LENGTH_DESCRIPTION_USER_SCHEMA, max_length= const.MAX_LENGTH_DESCRIPTION_USER_SCHEMA)
    position: str = Field(default= Required, min_length= const.MIN_LENGTH_POSITION_USER_SCHEMA, max_length= const.MAX_LENGTH_POSITION_USER_SCHEMA)

    _validator_password = validator("password", allow_reuse= True)(validators.validator_password)
    _validator_name = validator("name", allow_reuse= True)(validators.validator_name)
    _validator_company_name = validator("company_name", allow_reuse= True)(validators.validator_name_only_special_characters)
    _validator_position = validator("position", allow_reuse= True)(validators.validator_name_only_special_characters)



class UserUpdate(BaseModel):
    password: Optional[str] = Field(default= None ,min_length= const.MIN_LENGTH_PASSWORD_USER_SCHEMA)
    company_name: Optional[str] = Field(default= None, min_length= const.MIN_LENGTH_COMPANY_NAME_USER_SCHEMA, max_length= const.MAX_LENGTH_COMPANY_NAME_USER_SCHEMA)
    description: Optional[str] = Field(default= None, min_length= const.MIN_LENGTH_DESCRIPTION_USER_SCHEMA, max_length= const.MAX_LENGTH_DESCRIPTION_USER_SCHEMA)
    position: Optional[str] = Field(default= None, min_length= const.MIN_LENGTH_POSITION_USER_SCHEMA, max_length= const.MAX_LENGTH_POSITION_USER_SCHEMA)

    _validator_password = validator("password", allow_reuse= True)(validators.validator_password)
    _validator_company_name = validator("company_name", allow_reuse= True)(validators.validator_name_only_special_characters)
    _validator_position = validator("position", allow_reuse= True)(validators.validator_name_only_special_characters)



### Login ###
# class UserLogin(BaseModel):
#     email: EmailStr
#     password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None
    verified: Optional[bool] = None
    is_blocked: Optional[bool] = None

### Post ###
class PostBase(BaseModel):
    title: str = Field(default= Required, min_length= const.MIN_LENGTH_TITLE_POST_SCHEMAS, max_length= const.MAX_LENGTH_TITLE_POST_SCHEMAS)
    content: str = Field(default= Required, min_length= const.MIN_LENGTH_CONTENT_POST_SCHEMAS, max_length= const.MAX_LENGTH_CONTENT_POST_SCHEMAS)
    published : bool = Field(default= True, title= "published post", description= "Defines whether the post is public or not")

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
    new_manager_id: int = Field(default= Required,title= "new owner id", description="The ID of the user going to be new owner",  ge=const.USER_ID_GE, example=const.EXAMPLE_USER_ID)


class EmailSchema(BaseModel):
    email: List[EmailStr]




