from fastapi import APIRouter, Depends, status, HTTPException ,Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy import schema
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import null
# from .. import database, schemas, models, utils, oauth2
from app.config import settings
from fastapi import Response
from fastapi import FastAPI, HTTPException, status, Request, Body
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from pydantic import Required
# from app.main import log
from pydantic import EmailStr
import requests
import traceback
from .. import schemas

log = ""

router = APIRouter(tags= ['Authentication'])


AUTH_SERVICE = f"http://{settings.auth_service_url}:{settings.auth_service_port}"
MAIN_SERVICE = f"http://{settings.main_service_url}:{settings.main_service_port}"

router = APIRouter(
    prefix= "/auth",
    tags= ['Users']
    )


# TODO:
# create a schema for login, all the relevant values for keycloak should be included
# create a call to auth service, output logs
# return the token is got 200
# 
@router.get("/login", response_model=schemas.LoginResponse)
def login(request: Request, respone: Response,
    user_credentails: OAuth2PasswordRequestForm = Depends(Body(default=Required,
    title="User Credentails", description="User credentails must be a verified email and password",
    example={"email": "user@example.com", "password": "Password1!"})),
):
    email = EmailStr.validate(user_credentails.username)
    if email is None:
        log.debug(f"UNPROCESSABLE_ENTITY: This is not a valid email", extra={"request_id": request.state.request_id})
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, detail= f"This is not a valid email")
    try:
        log.debug(f"Try to login for user {email}", extra={"request_id": request.state.request_id})
        headers = {'X-Request-ID': request.state.request_id}
        response_auth = requests.get(f'{AUTH_SERVICE}/login',headers= headers, json= {
            "email": email,
            "password": user_credentails.password
        })
    except:
        log.error(f"An error occurred while try to login: {traceback.format_exc()} ", extra={"request_id": request.state.request_id})
    
    if response_auth.status_code != 200:
        log.debug(f"Invalid credentials or unauthorized", extra={"request_id": request.state.request_id})
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail= f"Invalid credentials or unauthorized")
    response_auth_json = response_auth.json()
    token = response_auth_json.get('token')
    respone.set_cookie(key='token', value=token, httponly=True)
    log.debug(f"Login was successful", extra={"request_id": request.state.request_id})
    return {"access_token": token, "token_type": "bearer"}



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