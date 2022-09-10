# from os import name
# import re
# from typing import List, Optional
# from fastapi import Query
# from psycopg2 import connect
from pydantic import BaseModel, EmailStr
# from datetime import date, datetime
# from pydantic.types import conint
# from pydantic import Required
# from . import validators
# from app import constants as const

# import uvicorn
# from fastapi import FastAPI, Path, Depends
# from fastapi.exceptions import RequestValidationError, ValidationError
# from fastapi.responses import JSONResponse


class UserVerify(BaseModel):
    email: EmailStr

class CodeVerify(BaseModel):
    code: str
