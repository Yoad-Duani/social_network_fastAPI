from typing import List, Optional
from fastapi import Query
# from psycopg2 import connect
from pydantic import BaseModel, EmailStr
from datetime import date, datetime
from pydantic.types import conint
from pydantic import Required
from . import validators
from app import constants as const


class TokenResponse(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None
    verified: Optional[bool] = None
    is_blocked: Optional[bool] = None