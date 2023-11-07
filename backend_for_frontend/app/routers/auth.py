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
from .. import oauth2
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
    prefix= "/auth",
    tags= ['Users']
    )

# @router.exception_handler(HTTPException)
# @router


def validate_user_credentials(request: Request, user_credentials: OAuth2PasswordRequestForm = Depends()):
    email = EmailStr.validate(user_credentials.username)
    if email is None:
        log.debug(f"UNPROCESSABLE_ENTITY: This is not a valid email", extra={"request_id": request.state.request_id})
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, detail= f"This is not a valid email")
    return user_credentials







# TODO:
# create a schema for login, all the relevant values for keycloak should be included
# create a call to auth service, output logs
# return the token is got 200
# user_credentails: OAuth2PasswordRequestForm = Depends(validate_user_credentials),
# respone: Response
@router.post("/login", response_model=schemas.LoginResponse,
    responses= {
        400: {"model": Message, "description": "The login is not possible due to mandatory actions"},
        401: {"model": Message, "description": "Invalid credentials enterd or unauthorized."},
    }
)
async def login(request: Request,
    response: Response,
    user_credentails: OAuth2PasswordRequestForm = Depends()
):
    request_id = request.state.request_id
    # email =user_credentails.username
    try:
        log.debug(f"Try to login for user {user_credentails.username}", extra={"request_id": request_id})
        headers = {'X-Request-ID': request_id}
        data = {
            "username": user_credentails.username,
            "password": user_credentails.password
        }
        request = httpx.Request(method="POST", url=f"{AUTH_SERVICE}/auth/login", headers=headers, params=data)
        async with httpx.AsyncClient() as client:
            response_auth = await client.send(request)
        # async with httpx.AsyncClient() as client:
        #     response_auth = await client.get(
        #         f'{AUTH_SERVICE}/test',
        #         headers=headers,
        #         json={
        #             "email": email,
        #             "password": user_credentails.password
        #         }
        #     )
        # response_auth = await requests.get(f'{AUTH_SERVICE}/test',headers= headers, json= {
        #     "email": email,
        #     "password": user_credentails.password
        # })
    except:
        log.error(f"An error occurred while try to connect to auth service: {traceback.format_exc()} ", extra={"request_id": request_id})
        raise HTTPException(status.HTTP_503_SERVICE_UNAVAILABLE, detail= f"An error occurred while to connect to auth service")
    if response_auth.status_code == 400:
        log.info(f"The login is not possible due to mandatory actions", extra={"request_id": request_id})
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail= f"The login is not possible due to mandatory actions")
    if response_auth.status_code == 401:
        log.info(f"Invalid credentials enterd or unauthorized", extra={"request_id": request_id})
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail= f"Invalid credentials enterd or unauthorized")
    if response_auth.status_code != 200:
        log.info(f"An error occurred while try to login", extra={"request_id": request_id})
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail= f"An error occurred while try to login")
    # response_auth_json = response_auth.json()
    # token = response_auth_json.get('access_token')
    token = response_auth.json().get('access_token', {}).get('access_token')
    response.set_cookie(key='access_token', value=token, httponly=True)
    response.headers["Authorization"] = token
    log.info(f"Login was successful", extra={"request_id": request_id})
    return {"access_token": token, "token_type": "bearer"}
    # Since this is a study project, I returned the access_token in three forms, apparently not the best practice










# TODO:
# add response model for user
@router.post("/user-registration")
async def reg(request: Request, respone: Response, user_reg: schemas.UserRegistration
):
    request_id = request.state.request_id
    # email =user_credentails.username
    try:
        log.info(f"Try to create user", extra={"request_id": request_id})
        headers = {'X-Request-ID': request_id}
        data = {
            "email": user_reg.email,
            "username": user_reg.username,
            "password": user_reg.password,
            "first_name": user_reg.first_name,
            "last_name": user_reg.last_name
        }
        json_data = json.dumps(data)
        request = httpx.Request(method="POST", url=f"{AUTH_SERVICE}/auth/user-registration", headers=headers, data=json_data)
        async with httpx.AsyncClient() as client:
            response_auth = await client.send(request)
    except:
        log.error(f"An error occurred while try to connect to auth service: {traceback.format_exc()} ", extra={"request_id": request_id})
        raise HTTPException(status.HTTP_503_SERVICE_UNAVAILABLE, detail= f"An error occurred while to connect to auth service")
    if response_auth.status_code >= 300:
        log.warning(f"An error occurred while create a user: {response_auth.text}", extra={"request_id": request_id})
        raise HTTPException(status_code=response_auth.status_code, detail= f"An error occurred while create a user: {response_auth.text}")
    response_auth_json = response_auth.json()
    # print(response_auth_json)
    user_email = response_auth_json['User']['email']
    # token = response_auth_json.get('token')
    # respone.set_cookie(key='token', value=token, httponly=True)
    log.info(f"Create a user was successful", extra={"request_id": request_id})
    log.info(f"User {user_email} has been created", extra={"request_id": request_id})
    return {f"{response_auth_json}"}








@router.post("/send-email-verify-email-address")
async def send_email_verify_email_address(request: Request, user: schemas.User,
):
    request_id = request.state.request_id
    try:
        log.debug(f"Try send email to verify email address", extra={"request_id": request_id})
        headers = {'X-Request-ID': request_id}
        data = {
            "email": user.email,
            "user_id": user.user_id,
            "name": user.name
        }
        json_data = json.dumps(data)
        request = httpx.Request(method="POST", url=f"{AUTH_SERVICE}/email/send-verify-email-address", headers=headers, data=json_data)
        # print(request.body)
        async with httpx.AsyncClient() as client:
            response_auth = await client.send(request)
    except Exception as ex:
        log.error(f"An error occurred while try to connect to auth service: {ex}: {traceback.format_exc()} ", extra={"request_id": request_id})
        raise HTTPException(status.HTTP_503_SERVICE_UNAVAILABLE, detail= f"An error occurred while to connect to auth service")
    if response_auth.status_code != 200:
        log.error(f"An error occurred while try to Try send email to verify email address {response_auth.text}", extra={"request_id": request_id})
        raise HTTPException(status.HTTP_503_SERVICE_UNAVAILABLE, detail= f"error {response_auth.text}")
    log.info(f"The verification email to {user.email} has been sent", extra={"request_id": request_id})
    return {"access_token": "demo-token", "token_type": "bearer"}



@router.get("/request-verify-email-address", status_code = status.HTTP_202_ACCEPTED)
async def request_verify_email_address(request: Request, 
    action_token: str = Query(default= Required)
):
    request_id = request.state.request_id
    try:
        log.debug(f"Trying to validate action-token", extra={"request_id": request_id})
        headers = {'X-Request-ID': request_id}
        # param = {
        #     "action_token": action_token,
        # }
        request = httpx.Request(method="POST", url=f"{AUTH_SERVICE}/email/verify-email-address?action_token={action_token}", headers=headers)
        # print(request.body)
        async with httpx.AsyncClient() as client:
            response_auth = await client.send(request)
    except Exception as ex:
        log.error(f"An error occurred while try to connect to auth service: {ex}: {traceback.format_exc()} ", extra={"request_id": request_id})
        raise HTTPException(status.HTTP_503_SERVICE_UNAVAILABLE, detail= f"An error occurred while to connect to auth service")
    if response_auth.status_code == 208:
        log.info(f"The email address has already been verified", extra={"request_id": request_id})
        return {"message": "The email address has already been verified"}
    if response_auth.status_code == 401:
        log.info(f"Invalid Token entered: Incorrect or expired.", extra={"request_id": request_id})
        return {"message": "Invalid Token entered: Incorrect or expired."}
    if response_auth.status_code != 202:
        log.warning(f"An error occurred while try to validate action-token: {response_auth.text}", extra={"request_id": request_id})
        # raise HTTPException(status_code= response_auth.status_code, detail= f"error {response_auth.text}")
    else:
        log.info(f"The action-token is verified", extra={"request_id": request_id})
    # return HTMLResponse( content=response_auth, status_code=202)
    return {"message": "The email address verified. Enjoy!"}






# @app.get("/test-auth")
# async def root(request: Request):
#     log.info(f"/sent request to auth service", extra={"request_id": request.state.request_id})
#     headers = {'X-Request-ID': request.state.request_id}   
#     response = requests.get(f'http://{settings.auth_service_url}:{settings.auth_service_port}/test',headers= headers)
#     print("this is back in BFF") 
#     print(f"{response.json()}")
#     return response.json()


# try:
#     # ...
# except:
#     logging.error("the error is %s", traceback.format_exc())

# log.info(f"/sent request to auth service", extra={"request_id": request.state.request_id})

# @app.get("/login")
# def login(email: str, password: SecretStr, respone: Response,):
#     token = idp.user_login(username=email, password=password.get_secret_value())
#     respone.set_cookie(key='token', value=token, httponly=True)
#     return {"access_token": token, "token_type": "bearer"}









# @router.post("/login", response_model=schemas.TokenResponse)
# def login(respone: Response, user_credentails: OAuth2PasswordRequestForm = Depends()):
#     pass
#     # TODO:
#     # call auth sever to verify credentails - return JWT


#     # try:
#     #     user = db.query(models.User).filter(models.User.email == user_credentails.username).first()
#     # except:
#     #     raise HTTPException(status.HTTP_503_SERVICE_UNAVAILABLE, detail= f"An error occurred while connecting to the database")
#     # if not user:
#     #     raise HTTPException(status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")
#     # if not utils.verify(user_credentails.password, user.password):
#     #     raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")
#     # access_token = oauth2.create_access_token(data= {"user_id": user.id, "user_verified":user.verified, "user_block":user.is_blocked})
#     # respone.set_cookie(key='token', value=access_token, httponly=True)
#     # return {"access_token": access_token, "token_type": "bearer"}




# @router.post("/disconnect", response_model=schemas.TokenResponse)
# def login(respone: Response, user_credentails: OAuth2PasswordRequestForm = Depends()):
#     pass
#     # TODO:
#     # 1. verify token
#     # 2. remove token from browser (close session)





# validate_user_credentials,
#     title="User Credentails", description="User credentails must be a verified email and password",
#     example={"email": "user@example.com", "password": "Password1!"})


@router.get("/test-get-user", status_code = status.HTTP_202_ACCEPTED)
async def test_get_user(request: Request,current_user = Depends(oauth2.get_current_user)
):
    print(current_user)