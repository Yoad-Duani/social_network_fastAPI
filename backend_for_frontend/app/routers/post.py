from fastapi import APIRouter, Depends, status, HTTPException, Response, Query, Body, Request
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy import schema
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import null
# from .. import database, schemas, models, utils, oauth2
from app.config import settings
from fastapi import Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from pydantic import Required
# from app.main import log
from pydantic import EmailStr
import requests
import traceback
from .. import schemas
from pydantic import Field
from app.log_config import init_loggers
import httpx
import json
from typing_extensions import Annotated
from typing import Union
from fastapi.responses import HTMLResponse
from fastapi.exception_handlers import (
    http_exception_handler,
    request_validation_exception_handler,
)
from pydantic import BaseModel


log = init_loggers(logger_name="auth-logger")
router = APIRouter(tags= ['Authentication'])

AUTH_SERVICE = f"http://{settings.auth_service_url}:{settings.auth_service_port}"
MAIN_SERVICE = f"http://{settings.main_service_url}:{settings.main_service_port}"

class Message(BaseModel):
    message: str

router = APIRouter(
    prefix= "/post",
    tags= ['Users']
    )




# TODO:
# create response_model=schemas.createPostResponse
# update meassage response
# create get_current_user for auth user
# create schema for schemas.PostCreate
# @router.post("/create",
#     responses= {
#         400: {"model": Message, "description": "The login is not possible due to mandatory actions"},
#         401: {"model": Message, "description": "Invalid credentials enterd or unauthorized."},
#     }
# )
# async def create_post(request: Request,
#     response: Response,
#     current_user: int = Depends(oauth2.get_current_user),
# ):
#     request_id = request.state.request_id
#     # email =user_credentails.username

#     # try create post
#     # message should send to rabitmq
#     try:
#         log.debug(f"Try to login for user {user_credentails.username}", extra={"request_id": request_id})
#         headers = {'X-Request-ID': request_id}
#         data = {
#             "username": user_credentails.username,
#             "password": user_credentails.password
#         }
#         request = httpx.Request(method="POST", url=f"{AUTH_SERVICE}/auth/login", headers=headers, params=data)
#         async with httpx.AsyncClient() as client:
#             response_auth = await client.send(request)

#     except:
#         log.error(f"An error occurred while try to connect to auth service: {traceback.format_exc()} ", extra={"request_id": request_id})
#         raise HTTPException(status.HTTP_503_SERVICE_UNAVAILABLE, detail= f"An error occurred while to connect to auth service")
#     if response_auth.status_code == 400:
#         log.info(f"The login is not possible due to mandatory actions", extra={"request_id": request_id})
#         raise HTTPException(status.HTTP_400_BAD_REQUEST, detail= f"The login is not possible due to mandatory actions")
#     if response_auth.status_code == 401:
#         log.info(f"Invalid credentials enterd or unauthorized", extra={"request_id": request_id})
#         raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail= f"Invalid credentials enterd or unauthorized")
#     if response_auth.status_code != 200:
#         log.info(f"An error occurred while try to login", extra={"request_id": request_id})
#         raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail= f"An error occurred while try to login")
#     token = response_auth.json().get('access_token', {}).get('access_token')
#     response.set_cookie(key='access_token', value=token, httponly=True)
#     response.headers["Authorization"] = token
#     log.info(f"Login was successful", extra={"request_id": request_id})
#     return {"access_token": token, "token_type": "bearer"}