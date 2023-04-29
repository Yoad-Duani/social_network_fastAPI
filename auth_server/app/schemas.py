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
from fastapi import FastAPI, Path, Depends


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


class UserVerify(BaseModel):
    email: EmailStr

class CodeVerify(BaseModel):
    code: str

class EmailVerify(BaseModel):
    email: EmailStr

class User(BaseModel):
    email: EmailStr
    # user_id: int = Path(default= Required,title= "user id", description="The ID of the user", ge=const.USER_ID_GE, example=const.EXAMPLE_USER_ID)
    user_id: str = Path(default= Required,title= "user id", description="The ID of the user")
    name: str = Field(default= Required ,min_length= const.MIN_LENGTH_NAME_USER_SCHEMA, max_length= const.MAX_LENGTH_NAME_USER_SCHEMA)
    _validator_name = validator("name", allow_reuse= True)(validators.validator_name)
    # def __init__(self, email, user_id, name) -> None:
    #    self.email = email
    #    self.user_id = user_id
    #    self.name = name
    # def __hash__(self):
    #     return hash(self.email, self.user_id, self.name)

class UserEmail(BaseModel):
    email: EmailStr
    user_id: str = Path(default= Required,title= "user id", description="The ID of the user")
    name: str = Field(default= Required ,min_length= const.MIN_LENGTH_NAME_USER_SCHEMA, max_length= const.MAX_LENGTH_NAME_USER_SCHEMA)
    _validator_name = validator("name", allow_reuse= True)(validators.validator_name)

class UserRegistration(BaseModel):
    email: EmailStr
    username: str
    password: str
    first_name: str
    last_name: str

