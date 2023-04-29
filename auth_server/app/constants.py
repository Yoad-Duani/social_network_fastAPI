from ast import List
from typing import Final, Dict, Any




###  User Routers Constants  ###

USER_ID_GE: Final[int] = 1  # The user's id must be 1 or more (g = Greater than, e = equal to)

EXAMPLE_USER_ID: Final[int] = 1  # Example of a user id


###  User_Auth Schemas Constants  ###

MIN_LENGTH_PASSWORD_USER_SCHEMA: Final[int] = 8



###  FastAPI Middleware  ###
ALLOW_ORIGINS : Final[List] = ["https://127.0.0.1:8002", "http://127.0.0.1:8002","https://social-network-fastapi-yoad.herokuapp.com/","https://social-network-fastapi.xyz", "*"] 

ALLOW_METHODS : Final[List] = ["GET", "POST", "PUT", "DELETE"]



###  FastAPI Metadata  ###

FASTAPI_METADATA_DESCRIPTION: Final[str] = '''
This is a full API for simaple social network develop with FastApi and Postgresql
- auth_server -

'''
FASTAPI_METADATA_TITLE: Final[str] = "Social Network FastAPI Documentation - auth_server"

FASTAPI_METADATA_VERSION: Final[str]= "0.0.1"

FASTAPI_METADATA_CONTACT_NAME: Final[str]= "Yoad Duani"

# ###  User Schemas Constants  ###

# MIN_LENGTH_PASSWORD_USER_SCHEMA: Final[int] = 8

MIN_LENGTH_NAME_USER_SCHEMA: Final[int] = 2

MAX_LENGTH_NAME_USER_SCHEMA: Final[int] = 16