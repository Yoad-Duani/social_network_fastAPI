from os import name
import re
from typing import List, Optional
from fastapi import Query
from psycopg2 import connect
from pydantic import BaseModel, EmailStr
from datetime import date, datetime
from pydantic.types import conint
from pydantic import Required
# from . import validators
from app import constants as const
from pydantic import EmailStr
# import uvicorn
# from fastapi import FastAPI, Path, Depends
from fastapi.exceptions import RequestValidationError, ValidationError
# from fastapi.responses import JSONResponse
from pydantic import BaseModel, validator, Field
# import calendar
# import datetime
# import json
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

'''
    All the schemas that used for get input have a strict input validation using pydantic validator and fastapi Query
    All the schemas that used for output have a basic out validation
'''

class UserCredentails(BaseModel):
    pass


class LoginResponse(BaseModel):
    access_token: str
    token_type: str




# class TokenData(BaseModel):
#     id: Optional[str] = None
#     verified: Optional[bool] = None
#     is_blocked: Optional[bool] = None

# ### Post ###
# class PostBase(BaseModel):
#     title: str = Field(default= Required, min_length= const.MIN_LENGTH_TITLE_POST_SCHEMAS, max_length= const.MAX_LENGTH_TITLE_POST_SCHEMAS)
#     content: str = Field(default= Required, min_length= const.MIN_LENGTH_CONTENT_POST_SCHEMAS, max_length= const.MAX_LENGTH_CONTENT_POST_SCHEMAS)
#     published : bool = Field(default= True, title= "published post", description= "Defines whether the post is public or not")

# class PostCreate(PostBase):
#     pass

# class PostResponse(PostBase):
#     id: int
#     created_at: datetime
#     group_id: int
#     owner_id: int
#     owner: UserResponse
#     class Config:
#         orm_mode = True