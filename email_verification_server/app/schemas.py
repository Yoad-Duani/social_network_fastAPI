# from os import name
# import re
from typing import List, Optional
# from fastapi import Query
# from psycopg2 import connect
from pydantic import BaseModel, EmailStr, validator, Field
from . import validators

# from datetime import date, datetime
# from pydantic.types import conint
from pydantic import Required
# from . import validators
from app import constants as const

# import uvicorn
from fastapi import FastAPI, Path, Depends
# from fastapi.exceptions import RequestValidationError, ValidationError
# from fastapi.responses import JSONResponse


class UserVerify(BaseModel):
    email: EmailStr

class CodeVerify(BaseModel):
    code: str

class EmailVerify(BaseModel):
    email: EmailStr

class User(BaseModel):
    email: EmailStr
    user_id: int = Path(default= Required,title= "user id", description="The ID of the user", ge=const.USER_ID_GE, example=const.EXAMPLE_USER_ID)
    name: str = Field(default= Required ,min_length= const.MIN_LENGTH_NAME_USER_SCHEMA, max_length= const.MAX_LENGTH_NAME_USER_SCHEMA)
    _validator_name = validator("name", allow_reuse= True)(validators.validator_name)
