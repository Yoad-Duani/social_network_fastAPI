# from os import name
from os import name
from typing import List, Optional
from psycopg2 import connect
from pydantic import BaseModel, EmailStr
from datetime import date, datetime
from pydantic.types import conint

# from sqlalchemy.sql.functions import user

# from app.database import Base
# from app.routers.vote import vote


# class WorkPlace(BaseModel):
#     company_name: str
#     description: str
#     position: str
#     class Config:
#         orm_mode = True
class groupsResponse(BaseModel):
    groups_id: int
    name: str
    description: str
    group_private: bool
    members: int
    last_activity: datetime # need to add groups_id to post, to check last post
    class Config:
        orm_mode = True

class GroupUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    group_private: Optional[bool] = None
    # name: str
    # description: str
    # group_private: bool



class CommentUpdate(BaseModel):
    # comment_id: int
    # user_id: int
    # post_id: int
    content: str

class GroupCreate(BaseModel):
    name: str
    description: str
    group_private: bool
    # creator_id: int


class CommentCreate(BaseModel):
    user_id: int
    post_id: int
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
    dir: conint(le = 1)

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
    email: EmailStr
    password: str
    name: str
    birth_date: date
    company_name: str
    description: str
    position: str



### Login ###
class UserLogin(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None




### Post ###
class PostBase(BaseModel):
    title: str
    content: str
    published : bool = True

class PostCreate(PostBase):
    pass

class PostResponse(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserResponse
    #comments: List[CommentResponse]
    class Config:
        orm_mode = True


class PostOut(BaseModel):
    Post: PostResponse
    votes: int
    comments: int
    class Config:
        orm_mode = True



