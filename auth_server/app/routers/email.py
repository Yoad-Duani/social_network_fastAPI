from fastapi import APIRouter, Depends, status, HTTPException, Response, Path, Body, Query, BackgroundTasks, Request
# from fastapi.security.oauth2 import OAuth2PasswordRequestForm
# from sqlalchemy import schema
# from sqlalchemy.orm import Session
# from sqlalchemy.sql.expression import null
# from .. import database, schemas, models, utils, oauth2
# from app import constants as const
# from pydantic import Required, SecretStr
# from ..email_config import send_mail_to_verify_email_address
from ..html_response import email_verification_response
from ..keycloak_config import get_keycloak
# from fastapi.responses import JSONResponse
from fastapi_keycloak import FastAPIKeycloak
from pymongo import MongoClient
# import ast
from ..config import settings
from ..database import get_mongodb, delete_user_by_user_id
from .. import custom_exceptions as c_ex
# from app.log_config import init_loggers
from app.log_config import init_loggers
from pydantic import BaseModel

log = init_loggers(logger_name= "email_router-logger")



# log = init_loggers()

class Message(BaseModel):
    message: str

router = APIRouter(
    prefix= "/email",
    tags= ['email']
    )



# @router.post('/send-verify-email-address')
# async def email_verification_mail(user: schemas.User, request: Request, background_tasks: BackgroundTasks)-> JSONResponse:
#     request_id = request.headers.get("X-Request-ID")
#     print("before background_tasks")
#     background_tasks.add_task(send_mail_to_verify_email_address, request_id, user)


    # response_model= schemas.ResponseKeycloakUser

@router.post('/verify-email-address',
    status_code = status.HTTP_202_ACCEPTED,
    responses= {
        404: {"model": Message, "description": "The item was not found"},
        401: {"model": Message, "description": "Invalid Token entered: Incorrect or expired."},
    }
    # responses={
    #     401: {"model": Message(message="Invalid Token entered: Incorrect or expired."), "description": "Invalid Token entered: Incorrect or expired."},
    #     208: {"model": Message(message="The email address has already been verified."), "description": "The email address has already been verified."},
    #     500: {"model": Message(message="Server error during authentication token."), "description": "Server error during authentication token."}}
    )
async def email_verification_address(
    request: Request, 
    action_token: str, 
    idp: FastAPIKeycloak = Depends(get_keycloak),
    mongo_client: MongoClient =  Depends(get_mongodb)
):
    request_id = request.headers.get("X-Request-ID")
    try:
        user = await email_verification_response(request, action_token, request_id)
    except c_ex.UnverifiedTokenException as ex:
        log.info(f"Invalid Token entered. Incorrect or expired: {ex}", extra={"request_id": request_id})
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail= f"Invalid Token entered: Incorrect or expired.")
    except c_ex.EmailAlreadyVerifiedException as ex:
        log.info(f"The user has already verified the email: {ex}", extra={"request_id": request_id})
        raise HTTPException(status_code=status.HTTP_208_ALREADY_REPORTED, detail= f"The email address has already been verified.")
    except Exception as ex:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail= f"Server error during authentication.")
    keycloak_user = idp.get_user(user_id=user.get("id"))
    keycloak_user.emailVerified = True
    keycloak_user = idp.update_user(user=keycloak_user)
    try:
        with mongo_client as client:
            delete_user_by_user_id(
                request_id= request_id,
                mongo_client= client,
                collection_name= settings.mongodb_collection_verify_email_address,
                user_id= user.get("id")
            )
    except Exception as ex:
        log.warning(f"Error during user {user.get('id')} deletion from mongo: {ex}", extra={"request_id": request_id})
        log.warning(f"The verification link has not been canceled.", extra={"request_id": request_id})
    return keycloak_user


