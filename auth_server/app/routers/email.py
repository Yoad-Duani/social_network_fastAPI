from fastapi import APIRouter, Depends, status, HTTPException, Response, Path, Body, Query, BackgroundTasks, Request
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy import schema
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import null
from .. import database, schemas, models, utils, oauth2
from app import constants as const
from pydantic import Required, SecretStr
from ..email_config import send_mail_to_verify_email_address
from ..html_response import email_verification_response
from ..keycloak_config import get_keycloak
from fastapi.responses import JSONResponse
from fastapi_keycloak import FastAPIKeycloak
import ast
# from app.log_config import init_loggers


# log = init_loggers()

router = APIRouter(
    prefix= "/email",
    tags= ['email']
    )



@router.post('/send-verify-email-address')
async def email_verification_mail(user: schemas.User, request: Request, background_tasks: BackgroundTasks)-> JSONResponse:
    request_id = request.headers.get("X-Request-ID")
    print("before background_tasks")
    background_tasks.add_task(send_mail_to_verify_email_address, request_id, user)


@router.post('/verify-email-address', status_code = status.HTTP_202_ACCEPTED)
async def email_verification_address(request: Request, action_token: str, idp: FastAPIKeycloak = Depends(get_keycloak)):
    # request_id = request.headers.get("X-Request-ID")
    request_id = request.headers.get("X-Request-ID")
    # background_tasks.add_task(email_verification_response, request, action_token, request_id)
    try:
        user = await email_verification_response(request, action_token, request_id)
    except Exception as ex:
        pass
    keycloak_user = idp.get_user(user_id=user.get("id"))
    keycloak_user.emailVerified = True
    # keycloak_user_dict = ast.literal_eval(keycloak_user[0])
    # keycloak_user_dict['User']['emailVerified'] = True
    # keycloak_user[0] = str(keycloak_user_dict)
    keycloak_user = idp.update_user(user=keycloak_user)
    return keycloak_user


    # (request: Request, token: str):
    # user = await verify_token(token)

    # if user.get("id"):
    #     #send a request to update user
    #     print("sccuess verify user mail!")
    #     return templates.TemplateResponse("verified_mail.html", {"request": request, "name": user.get("name")})
        # pass