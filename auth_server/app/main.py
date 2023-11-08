
from typing import List
from fastapi import FastAPI, HTTPException, status, Request, Depends, Response, Header, BackgroundTasks
import time

# import sys, os, io

# from app.models import Comment, Groups
# from . import models
# from .database import engine
# from .routers import auth
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import datetime
# from fastapi.exceptions import RequestValidationError, ValidationError
# from fastapi.responses import JSONResponse, RedirectResponse
# import json
from app import constants as const
# from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from .config import settings
import os
from fastapi.responses import FileResponse
from .keycloak_config import get_keycloak
# from typing import List, Optional, Annotated, Union
print("test 111")
from .routers import email, auth
# from routers import 
print("test 222")
from fastapi import Query, Body
print("test 333")
from pydantic import SecretStr, Required
print("test 444")
from app.log_config import init_loggers
from fastapi_keycloak import FastAPIKeycloak, OIDCUser, UsernamePassword, HTTPMethod, KeycloakUser, KeycloakGroup
# import contextvars
# import traceback

import uvicorn
from .email_config import send_mail_to_verify_email_address
from .database import get_mongodb, check_or_create_collections, create_index_created_at, create_index_user_id
from fastapi.templating import Jinja2Templates
# from pathlib import Path
from fastapi import FastAPI, HTTPException, Request
from pymongo.errors import ConnectionFailure
# from fastapi.responses import PlainTextResponse
# from starlette.exceptions import HTTPException as StarletteHTTPException
# from starlette.background import BackgroundTask
# import asyncio
from fastapi.security import OAuth2PasswordBearer
# from .email_config import *
# import asyncio


# startup_complete = asyncio.Event()

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


app.add_middleware(
    CORSMiddleware,
    # allow_origins= const.ALLOW_ORIGINS,
    allow_origins= ["*"],
    allow_credentials= True,
    allow_methods= const.ALLOW_METHODS,
    allow_headers=["*"],
)

log.info(f"Initializing auth service.")
log.info(f"Waiting for keycloak service.")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth")





# def check_or_create_collections(mongo_client, db_name, collection_names):
#     db = mongo_client[db_name]
#     existing_collection_names = db.list_collection_names()
#     collections = []
#     for collection_name in collection_names:
#         if collection_name in existing_collection_names:
#             collections.append(db[collection_name])
#         else:
#             db.create_collection(collection_name)
#             collections.append(db[collection_name])
#     return collections



try:
    time.sleep(30)
    idp = get_keycloak()
except Exception as ex:
    log.warning(f"Failed to connect to Keycloak. watting 30 seconeds before try again.")
    try:
        time.sleep(30)
        idp = get_keycloak()
    except Exception as ex:
        log.error(f"Failed to connect to Keycloak after 30 seconds. ConnectionError.")
        log.warning(f"Shutting down the app.")
        raise Exception(f"Failed to connect to Keycloak. Shuts down the service: {ex}")
log.info(f"Waiting for mongodb service.")
try:
    with get_mongodb() as mongo_client:
        mongo_client.server_info()
        db_names = mongo_client.list_database_names()
        if settings.mongodb_db_name in db_names:
            log.info(f"Database {settings.mongodb_db_name} already exists.")
        else:
            mongo_client[settings.mongodb_db_name]
            log.info(f"Database {settings.mongodb_db_name} created.")
        collections_names = [settings.mongodb_collection_verify_email_address,settings.mongodb_collection_reset_password]
        check_or_create_collections(mongo_client= mongo_client, 
                                    db_name= settings.mongodb_db_name, 
                                    collection_names= collections_names
        )
        create_index_created_at(mongo_client= mongo_client, 
                                db_name= settings.mongodb_db_name, 
                                collection_name= settings.mongodb_collection_verify_email_address, 
                                time_in_seconds=settings.mongodb_index_created_at_expired_seconds
        )
        create_index_user_id(mongo_client= mongo_client, 
                                db_name= settings.mongodb_db_name, 
                                collection_name= settings.mongodb_collection_verify_email_address, 
        )
except ConnectionFailure as ex:
    log.warning(f"Shutting down the app...")
    raise Exception(f"Failed to connect to Mongo. Shuts down the service: {ex}")

# TODO:
# improve the check connction flollow




# templates = Jinja2Templates(directory= Path(__file__).parent / 'templates')



# app.include_router(auth.router)
app.include_router(email.router)
app.include_router(auth.router)




@app.post('/verify-test')
async def email_verification_mail(background_tasks: BackgroundTasks)-> JSONResponse:
    background_tasks.add_task(send_mail_to_verify_email_address, {"email": "yoad787@gmail.com", "user_id": 999, "name": "Yoad"})



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


async def get_current_user_dependency():
    user = idp.get_current_user()
    try:
        yield user
    except Exception as ex:
        print("error")
        print(ex)
    finally:
        (print("finally"))

    # try:
    #     print("test get_current_user")
    #     user =  idp.get_current_user()
    #     print (user)
    #     user = user()
    #     print (user)
    #     return user
    # except Exception as ex:
    #     print("errorrrrrrrrr")
    #     print("errorrrrrrrrr")
    #     print(ex)

    # try:
    #     user: OIDCUser = idp.get_current_user()
    #     return user
    # except Exception as ex:
    #     print("errorrrrrrrrr")
    #     print("errorrrrrrrrr")
    

@app.get("/auth/get_current_user")  # Requires logged in
async def current_user(
    user: OIDCUser = Depends(idp.get_current_user())
):
     print("test")
     print(user)
     return user
    # try:
    #     get_user = idp.get_current_user()
    #     user = get_user()
    #     print(user)
    # except Exception as ex:
    #     print("errorrrrrrrrr")
    #     print(ex)
    # try:
    #     user_result = user()
    #     print(user_result)
    #     return user_result
    # except Exception as ex:
    #     print("errorrrrrrrrr")
    #     print("errorrrrrrrrr")





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
def login(username: str, password: SecretStr, respone: Response,):
    token = idp.user_login(username=username, password=password.get_secret_value())
    respone.set_cookie(key='token', value=token, httponly=True)
    return {"access_token": token, "token_type": "bearer"}


@app.get("/callback")
def callback(session_state: str, code: str):
    return idp.exchange_authorization_code(session_state=session_state, code=code)  # This will return an access token


@app.post("/users", tags=["user-management"])
def create_user(first_name: str, last_name: str, email: str, password: SecretStr):
    return idp.create_user(first_name=first_name, last_name=last_name, username=email, email=email, password=password.get_secret_value(), send_email_verification= False)



# @app.get("/user-safe-new")  # Requires logged in
# async def current_users_new(token: str = Depends(oauth2_scheme)):
#     user = idp.get_current_user()
#     print(user)
#     return user
# TODO:
# add check for header if is Bearer, if not return error

# if __name__ == '__main__':
#     uvicorn.run('app:app', host="127.0.0.1", port=8081)



@app.get("/test")
async def test(request: Request, response: Response):
    # print(request.client.host)
    request_id = request.headers.get("X-Request-ID")
    request.state.request_id = request_id
    print("this is log in the auth service - start")
    print(request_id)
    print("this is log in the auth service - end")
    now = datetime.datetime.now()
    now = now.strftime("%Y-%b-%d, %A %I:%M:%S")
    response.headers["X-Request-ID"] = request_id
    return {
        "API Name": "Social Network fastAPI auth_server"
    }



@app.post("/test-reg")
async def test(request: Request, response: Response):
    request_id = request.headers.get("X-Request-ID")
    try:
        user = idp.create_user(first_name="Yosi", last_name="Choen", username="yoad787@gmail.com", email="yoad787@gmail.com", password="12345678", send_email_verification=False)
        log.info(f"User {user.email} created in the system", extra={"request_id": request_id})
        try:
            idp.send_email_verification(user_id=user.id)
            
        except Exception as ex:
            ex_status_code = getattr(ex, "status_code", 503)
            log.error(f"An error occurred while send_email_verification: {ex}", extra={"request_id": request_id})
    except Exception as ex:
        ex_status_code = getattr(ex, "status_code", 503)
        log.error(f"An error occurred while creating the user: {ex}", extra={"request_id": request_id})
        response.headers["X-Request-ID"] = request_id
        raise HTTPException(status_code=ex_status_code, detail= f"An error occurred while create a user: {ex}")
    return {
        "User": user
    }

@app.post("/test-actiontoken")
async def test(request: Request, response: Response, user_id: str, action_token: str):
    request_id = request.headers.get("X-Request-ID")
    try:
        log.info(f"Try verify email", extra={"request_id": request_id})
        action_response = idp.execute_actions_email_validation(user_id=user_id, action_token=action_token)
    except Exception as ex:
        ex_status_code = getattr(ex, "status_code", 503)
        log.error(f"An error occurred while verify email: {ex}", extra={"request_id": request_id})
        raise HTTPException(status_code=ex_status_code, detail= f"An error occurred while verify email: {ex}")
    return {"action_response": action_response}



# @app.post('/verify-test')
# async def email_verification_mail(background_tasks: BackgroundTasks)-> JSONResponse:
#     background_tasks.add_task(send_mail_to_verify_email_address, {"email": "yoad787@gmail.com", "user_id": 999, "name": "Yoad"})


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
    # asyncio.run(startup_complete.wait())
    uvicorn.run('app:app', host="0.0.0.0", port=8002)