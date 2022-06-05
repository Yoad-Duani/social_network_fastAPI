
from os import name
from typing import List, Optional
from psycopg2 import connect
from pydantic import BaseModel, EmailStr
from datetime import date, datetime
from pydantic.types import conint


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
    email: EmailStr
    password: str
    name: str
    birth_date: date
    company_name: str
    description: str
    position: str

class UserUpdate(BaseModel):
    password: Optional[str] = None
    company_name: Optional[str] = None
    description: Optional[str] = None
    position: Optional[str] = None
    

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
    title: str
    content: str
    published : bool = True

class PostCreate(PostBase):
    pass
    # group_id: Optional[int] = 0

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