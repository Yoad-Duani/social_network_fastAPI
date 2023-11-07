from fastapi import APIRouter, Depends, status, HTTPException, Response, Path, Body, Query, Request, BackgroundTasks
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy import schema
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import null
from .. import database, schemas, models, utils, oauth2
from app import constants as const
from pydantic import Required, SecretStr
from ..config import settings
from fastapi_keycloak.exceptions import KeycloakError, MandatoryActionException
from fastapi_keycloak.exceptions import HTTPException as Keycloak_HTTPException

# from ..main import idp
from typing import List, Optional
from fastapi_keycloak import FastAPIKeycloak, OIDCUser, UsernamePassword, HTTPMethod, KeycloakUser, KeycloakGroup
from fastapi.security import OAuth2PasswordBearer
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
from ..keycloak_config import get_keycloak
from app.log_config import init_loggers
from pydantic import BaseModel, EmailStr, validator, Field, Required
from ..email_config import send_mail_to_verify_email_address
from ..database import get_mongodb, get_db_collection,insert_one_to_collection
from ..models import users_serializer
from pymongo import MongoClient
from datetime import datetime
from bson import ObjectId
# from main import idp


router = APIRouter(
    prefix= "/auth",
    tags= ['Users']
    )

log = init_loggers(logger_name="auth_router-logger")
# idp = get_keycloak()



# TODO:
# 
@router.post("/user-registration", status_code = status.HTTP_201_CREATED)
async def create_user(request: Request, response: Response, 
        user_reg: schemas.UserRegistration, 
        background_tasks: BackgroundTasks, 
        idp: FastAPIKeycloak = Depends(get_keycloak),
        mongo_client: MongoClient =  Depends(get_mongodb)
):
    request_id = request.headers.get("X-Request-ID")
    try:
        keycloak_user = idp.create_user(
            first_name=user_reg.first_name,
            last_name=user_reg.last_name,
            username=user_reg.username,
            email=user_reg.email, 
            password=user_reg.password, 
            send_email_verification=False
        )
        log.info(f"User {keycloak_user.email} created in the system", extra={"request_id": request_id})
        # add to mongo
        try:
            user_mongo = schemas.UserMongo(user_id= keycloak_user.id, email= keycloak_user.email, name= keycloak_user.firstName)
            with mongo_client as client:
                _id = insert_one_to_collection(
                    request_id= request_id,
                    client= client,
                    db_name= settings.mongodb_db_name,
                    collection_name= settings.mongodb_collection_verify_email_address,
                    user_mongo= user_mongo
                )

                # mongo_collection = get_db_collection(
                #     client= client,
                #     db_name= settings.mongodb_db_name,
                #     collection_name= settings.mongodb_collection_verify_email_address
                # )
                # _id = mongo_collection.insert_one({"user_id": keycloak_user.id, "email": keycloak_user.email, "name": keycloak_user.firstName, "created_at": datetime.utcnow()})
                # log.info(f"User {keycloak_user.email} has been added to mongo for email verification.", extra={"request_id": request_id})
                # user = users_serializer(mongo_collection.find({"_id": ObjectId(_id.inserted_id)}))


                try:
                    log.info(f"Trying to send an email for verification", extra={"request_id": request_id})
                    user = schemas.UserEmail(email=keycloak_user.email, user_id= keycloak_user.id, name= keycloak_user.firstName)
                    background_tasks.add_task(send_mail_to_verify_email_address, request_id, user)
                except Exception as ex:
                    ex_status_code = getattr(ex, "status_code", 503)
                    log.error(f"An error occurred while send_email_verification: {ex}", extra={"request_id": request_id})
        except Exception as ex:
            log.error(f"An error occurred while add user to mongo: {ex}", extra={"request_id": request_id})
        # try:
        #     # idp.send_email_verification(user_id=user.id)
        #     # user = {"email": keycloak_user.email, "user_id": keycloak_user.id, "name": keycloak_user.firstName}
        #     log.info(f"Trying to send an email for verification", extra={"request_id": request_id})
        #     user = schemas.UserEmail(email=keycloak_user.email, user_id= keycloak_user.id, name= keycloak_user.firstName)
        #     background_tasks.add_task(send_mail_to_verify_email_address, request_id, user)
        # except Exception as ex:
        #     ex_status_code = getattr(ex, "status_code", 503)
        #     log.error(f"An error occurred while send_email_verification: {ex}", extra={"request_id": request_id})
    except Exception as ex:
        ex_status_code = getattr(ex, "status_code", 503)
        log.error(f"An error occurred while creating the user: {ex}", extra={"request_id": request_id})
        response.headers["X-Request-ID"] = request_id
        raise HTTPException(status_code=ex_status_code, detail= f"An error occurred while create a user: {ex}")
    return {
        "User": keycloak_user
    }




@router.post("/login", status_code = status.HTTP_201_CREATED)
def login(username: str,
    request: Request,
    password: SecretStr = Required,
    respone: Response = Required,
    idp: FastAPIKeycloak = Depends(get_keycloak),
):
    request_id = request.headers.get("X-Request-ID")
    try:
        token = idp.user_login(username=username, password=password.get_secret_value())
        log.info(f"User login to the system", extra={"request_id": request_id})
    except MandatoryActionException as ex:
        ex_status_code = getattr(ex, "status_code", 400)
        log.warning(f"The login is not possible due to mandatory actions: {ex}", extra={"request_id": request_id})
        raise HTTPException(status_code=ex_status_code, detail= f"The login is not possible due to mandatory actions: {ex}")
    except Keycloak_HTTPException as ex:
        ex_status_code = getattr(ex, "status_code", 401)
        log.warning(f"The credentials did not match any user: {ex}", extra={"request_id": request_id})
        raise HTTPException(status_code=ex_status_code, detail= f"The credentials did not match any user: {ex}")
    except KeycloakError as ex:
        ex_status_code = getattr(ex, "status_code", 503)
        log.error(f"An error occurred while try to login: {ex}", extra={"request_id": request_id})
        raise HTTPException(status_code=ex_status_code, detail= f"An error occurred while try to login: {ex}")
    respone.set_cookie(key='token', value=token, httponly=True)
    return {"access_token": token, "token_type": "bearer"}




# @router.get("/get_current_users")
# async def get_current_users(token: str = Depends(oauth2_scheme),
#                             idp: FastAPIKeycloak = Depends(get_keycloak),
#                             user: OIDCUser = Depends(idp.get_current_user())):
#     print(user)
#     return user
    


# @app.get("/user-safe")  # Requires logged in
# async def current_users(token: str = Depends(oauth2_scheme),
#     user: OIDCUser = Depends(idp.get_current_user())
# ):
#     print(user)
#     return user


@router.get("/user-registration-test-mongo", status_code = status.HTTP_201_CREATED)
async def create_user_test(request: Request, response: Response, 
    mongo_client: MongoClient =  Depends(get_mongodb)
):
    with get_mongodb() as mongo_client:
        print(mongo_client.server_info())
        aaa = mongo_client.server_info()
    return aaa

































# TODO:
# add test

# router = APIRouter(tags= ['Auth-Flow'])

# @router.get("/user-safe")  # Requires logged in
# async def current_users(token: str = Depends(oauth2_scheme),
#     user: OIDCUser = Depends(idp.get_current_user())
# ):
#     return user

# FIXME:
# update the funcation - acording to auth_user table

# @router.post("/login", response_model=schemas.TokenResponse)
# def login(respone: Response, user_credentails: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
#     try:
#         user = db.query(models.User).filter(models.User.email == user_credentails.username).first()
#     except:
#         raise HTTPException(status.HTTP_503_SERVICE_UNAVAILABLE, detail= f"An error occurred while connecting to the database")
#     if not user:
#         raise HTTPException(status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")
#     if not utils.verify(user_credentails.password, user.password):
#         raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")
        
#     access_token = oauth2.create_access_token(data= {"user_id": user.id, "user_verified":user.verified, "user_block":user.is_blocked})
#     respone.set_cookie(key='token', value=access_token, httponly=True)
#     return {"access_token": access_token, "token_type": "bearer"}


# @router.post("/create-user-credentials", response_model=schemas.ResponseUserCredentials, status_code = status.HTTP_201_CREATED)
# def create_credentials_user(user: schemas.CreateUserCredentials = Body(default= Required),db: Session = Depends(database.get_db)):
#     try:
#         user_email_exists = db.query(models.User).filter(models.User.email == user.email).first()
#     except Exception as error:
#         print(error)
#         raise HTTPException(status_code= status.HTTP_503_SERVICE_UNAVAILABLE, detail= f"An error occurred while creating the user")
#     if user_email_exists:
#         raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail= f"User with this email is alerady exist")
#     hashed_password = utils.hash(user.password)
#     user.password = hashed_password
#     new_user = models.User(**user.dict())
#     try:
#         db.add(new_user)
#         db.commit()
#         db.refresh(new_user)
#     except Exception as error:
#         print(error)
#         db.rollback()
#         raise HTTPException(status_code= status.HTTP_503_SERVICE_UNAVAILABLE, detail= f"An error occurred while creating the user")
#     return new_user


# @router.put("/update-user-credentials", response_model=schemas.ResponseUserCredentials, status_code = status.HTTP_200_OK)
# def update_credentials_user(user_credentials: schemas.UpdateUserCredentials, db: Session = Depends(database.get_db), current_user: int = Depends(oauth2.get_current_user)):
#     try:
#         user_query = db.query(models.User).filter(models.User.id == current_user.id)
#     except Exception as error:
#         print(error)
#         raise HTTPException(status_code= status.HTTP_503_SERVICE_UNAVAILABLE, detail= f"An error occurred while updating user")
#     if user_query.first() == None:
#         raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f"user with id: {current_user.id} does not exist")
#     password = utils.hash(user_credentials.password)   
#     try:
#         user_query.update({"password": password, "password_update_at": "now()"}, synchronize_session= False)
#         db.commit()
#     except Exception as error:
#         print(error)
#         db.rollback()
#         raise HTTPException(status_code= status.HTTP_503_SERVICE_UNAVAILABLE, detail= f"An error occurred while updating user")
#     return user_query.first()


# TODO:
# create funcation for remove credentials



# FIXME:
# fix the current user to secret key / token

# @router.put("/verify-user", status_code = status.HTTP_200_OK)
# def update_verify_user(user_id: int = Path(default= Required,title= "user id", description="The ID of the user to get",  ge=const.USER_ID_GE, example=const.EXAMPLE_USER_ID), 
#     db: Session = Depends(database.get_db), current_user: int = Depends(oauth2.get_current_user)
# ):
#     user_query = db.query(models.User).filter(models.User.id == current_user.id)
#     try:
#         user = user_query.first()
#     except Exception as error:
#         print(error)
#         raise HTTPException(status_code= status.HTTP_503_SERVICE_UNAVAILABLE, detail= f"An error occurred while verify user")
#     if user == None:
#         raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f"user with id: {current_user.id} does not exist")
#     if user.verified == True:
#         raise HTTPException(status_code= status.HTTP_409_CONFLICT, detail= f"user with id: {current_user.id} already verified")
#     try:
#         user_query.update({"verified": True}, synchronize_session= False)
#         db.commit()
#     except Exception as error:
#         print(error)
#         db.rollback()
#         raise HTTPException(status_code= status.HTTP_503_SERVICE_UNAVAILABLE, detail= f"An error occurred while verify user")
#     return {"status": "succeeded - user authenticated"}



# TODO:
# create funcation for block user - scope admin

# TODO:
# create funcation for unblock user - scop admin







# Admin

# @router.post("/proxy", tags=["admin-cli"])
# def proxy_admin_request(relative_path: str, method: HTTPMethod, additional_headers: dict = Body(None), payload: dict = Body(None)):
#     return idp.proxy(
#         additional_headers=additional_headers,
#         relative_path=relative_path,
#         method=method,
#         payload=payload
#     )


# @router.get("/identity-providers", tags=["admin-cli"])
# def get_identity_providers():
#     return idp.get_identity_providers()


# @router.get("/idp-configuration", tags=["admin-cli"])
# def get_idp_config():
#     return idp.open_id_configuration