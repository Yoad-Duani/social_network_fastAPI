
from fastapi import FastAPI, HTTPException, status, Request, Depends, Response, Header
import time

from fastapi.security import OAuth2PasswordBearer
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
# import sys, os, io

# from app.models import Comment, Groups
# from . import models
# from .database import engine
# from .routers import auth
from fastapi.middleware.cors import CORSMiddleware
import datetime
# from fastapi.exceptions import RequestValidationError, ValidationError
from fastapi.responses import JSONResponse, RedirectResponse
# import json
from app import constants as const
# from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from .config import settings
import os
from fastapi.responses import FileResponse

from typing import List, Optional, Annotated, Union

from fastapi import Query, Body
from pydantic import SecretStr, Required
from app.log_config import init_loggers
from fastapi_keycloak import FastAPIKeycloak, OIDCUser, UsernamePassword, HTTPMethod, KeycloakUser, KeycloakGroup

import uvicorn



favicon_path = os.path.join(os.path.dirname(__file__), 'assets', 'favicon.ico')
log = init_loggers(logger_name="main-logger")

app = FastAPI(
    title= const.FASTAPI_METADATA_TITLE,
    version= const.FASTAPI_METADATA_VERSION,
    description= const.FASTAPI_METADATA_DESCRIPTION,
    contact= {
        "name": f"{const.FASTAPI_METADATA_CONTACT_NAME}",
        "url": "https://www.linkedin.com/in/yoad-duani/",
    },
)

time.sleep(30)

idp = FastAPIKeycloak(
    server_url=f"http://{settings.keycloak_hostname}:{settings.keycloak_port}/auth",
    client_id=settings.client_id,
    client_secret=settings.client_secret,
    admin_client_secret=settings.admin_client_secret,
    realm=settings.realm,
    callback_uri=f"http://{settings.auth_server_url}:{settings.keycloak_port_callback}/callback"
)
idp.login_uri = f"http://{settings.auth_server_url}:8002/docs"
idp.add_swagger_config(app)

app.add_middleware(
    CORSMiddleware,
    # allow_origins= const.ALLOW_ORIGINS,
    allow_origins= ["*"],
    allow_credentials= True,
    allow_methods= const.ALLOW_METHODS,
    allow_headers=["*"],
)

# app.add_middleware(HTTPSRedirectMiddleware)

# app.include_router(auth.router)


@app.get("/")
async def root(request: Request, my_header: str = Header(default= Required)):
    # print(request.client.host)
    print(request.state.request_id)
    print("this is in auth service")
    now = datetime.datetime.now()
    now = now.strftime("%Y-%b-%d, %A %I:%M:%S")
    return {
        "API Name": "Social Network fastAPI auth_server",
        "API Documentation": f"{request.url._url}docs",
        "GitHub Repo": "https://github.com/Yoad-Duani/social_network_fastAPI",
        "Host": f"{request.client.host}",
        "Date": f"{now}",
        "My-Header": f"{my_header}"
    }

@app.get("/reconnect")
async def reconnect():
    try:
        idp.add_swagger_config(app)
    except Exception as error:
        print(error)
    return {
        "reconnect": "reconnect",
    }



# @app.exception_handler(RequestValidationError)
# @app.exception_handler(ValidationError)
# def validation_exception_handler(request, exc):
#     print(f"The client sent invalid data: {exc}")
#     exc_json = json.loads(exc.json())
#     response = {"error type": "validation error" ,"message": [], "data": None}
#     for error in exc_json:
#         response['message'].append(error['loc'][-1]+f": {error['msg']}")
#     return JSONResponse(response, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)


@app.get("/login")
def login(email: str, password: SecretStr, respone: Response,):
    token = idp.user_login(username=email, password=password.get_secret_value())
    respone.set_cookie(key='token', value=token, httponly=True)
    return {"access_token": token, "token_type": "bearer"}


@app.get("/callback")
def callback(session_state: str, code: str):
    return idp.exchange_authorization_code(session_state=session_state, code=code)  # This will return an access token


@app.post("/users", tags=["user-management"])
def create_user(first_name: str, last_name: str, email: str, password: SecretStr):
    return idp.create_user(first_name=first_name, last_name=last_name, username=email, email=email, password=password.get_secret_value(), send_email_verification= False)

@app.get("/user-safe")  # Requires logged in
def current_users(token: str = Depends(oauth2_scheme),
    user: OIDCUser = Depends(idp.get_current_user())
):
    return user
# TODO:
# add check for header if is Bearer, if not return error

# if __name__ == '__main__':
#     uvicorn.run('app:app', host="127.0.0.1", port=8081)



@app.get("/test")
async def test(request: Request):
    # print(request.client.host)
    request_id = request.headers.get("X-Request-ID")
    print("this is log in the auth service - start")
    print(request_id)
    print("this is log in the auth service - end")
    now = datetime.datetime.now()
    now = now.strftime("%Y-%b-%d, %A %I:%M:%S")
    return {
        "API Name": "Social Network fastAPI auth_server"
    }




##################################################################################################################
##################################################################################################################
##################################################################################################################
##################################################################################################################



# from fastapi import FastAPI, Depends
# from fastapi.responses import RedirectResponse
# from fastapi_keycloak import FastAPIKeycloak, OIDCUser




# @app.get("/")  # Unprotected
# def root():
#     return 'Hello World'


# @app.get("/user")  # Requires logged in
# def current_users(user: OIDCUser = Depends(idp.get_current_user())):
#     return user


# @app.get("/admin")  # Requires the admin role
# def company_admin(user: OIDCUser = Depends(idp.get_current_user(required_roles=["admin"]))):
#     return f'Hi admin {user}'


# @app.get("/login")
# def login_redirect():
#     return RedirectResponse(idp.login_uri)


# @app.get("/callback")
# def callback(session_state: str, code: str):
#     return idp.exchange_authorization_code(session_state=session_state, code=code)  # This will return an access token


@app.get('/favicon.ico', include_in_schema=False)
async def favicon():
    return FileResponse(path=favicon_path, filename=favicon_path)

if __name__ == '__main__':
    uvicorn.run('app:app', host="0.0.0.0", port=8002)