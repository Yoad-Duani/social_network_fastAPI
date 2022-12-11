from typing import List, Optional
# from fastapi import Query
# from psycopg2 import connect
from pydantic import BaseModel, EmailStr, validator, Field, Required
# from datetime import date, datetime
# from pydantic.types import conint
# from pydantic import Required
# from . import validators
# from app import constants as const
from . import validators
from app import constants as const


class TokenResponse(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None
    verified: Optional[bool] = None
    is_blocked: Optional[bool] = None

class CreateUserCredentials(BaseModel):
    email: EmailStr = Field(default= Required)
    password: str = Field(default= Required ,min_length= const.MIN_LENGTH_PASSWORD_USER_SCHEMA)
    _validator_password = validator("password", allow_reuse= True)(validators.validator_password)

class ResponseUserCredentials(BaseModel):
    id: int
    email: EmailStr
    class Config:
        orm_mode = True

class UpdateUserCredentials(BaseModel):
    id: int
    email: EmailStr = Field(default= Required)
    password: str = Field(default= Required ,min_length= const.MIN_LENGTH_PASSWORD_USER_SCHEMA)
