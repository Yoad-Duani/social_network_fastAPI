from fastapi import Body, FastAPI, Form, Cookie, status, Query, Header, HTTPException, Request, BackgroundTasks, HTTPException, Depends
from fastapi.templating import Jinja2Templates
from .oauth2 import verify_token
from app.log_config import init_loggers
from pathlib import Path
from pymongo import MongoClient
from .database import get_mongodb, find_user_by_user_id
from . import schemas, custom_exceptions as c_ex
from .config import settings

# templates = Jinja2Templates(directory="templates")
templates = Jinja2Templates(directory= Path(__file__).parent / 'templates')
log = init_loggers(logger_name="responses-logger")

with get_mongodb() as mongo_client:
    pass


async def email_verification_response(
        request: Request, 
        action_token: str, 
        request_id: str,
):
    # log.info(f"Trying to verify an email address", extra={"request_id": request_id})
    try:
        user = await verify_token(action_token= action_token, request_id= request_id)
    except c_ex.UnverifiedTokenException as ex:
        raise c_ex.UnverifiedTokenException(f"Invalid_token: {ex}")
    except Exception as ex:
        # return templates.TemplateResponse("invalid_token.html", {"request": request, "exceptionDetail": ex.detail})
        raise Exception(f"invalid_token: {ex}")
        # return {"message": "invalid_token"}
    if user.get("id"):
        print(f"user: {user}")
        try:
            print("**********  TEST ***************")
            mongo_user = find_user_by_user_id(
                request_id= request_id,
                mongo_client= mongo_client,
                collection_name= settings.mongodb_collection_verify_email_address,
                user_id= user.get("id")
            )
        except Exception as ex:
            print ("error - 111")
            log.error(f"Failed to search for user in mongo: {ex}", extra={"request_id": request_id})
            raise Exception(f"Failed to search for user in mongo: {ex}") 
        if mongo_user is not None:
            log.info(f"User {user.get('id')} has been verified", extra={"request_id": request_id})
            return user
        else:
            print ("error - 222")
            log.info(f"The user: {user.get('id')} has already verified the email", extra={"request_id": request_id})
            print ("error - 333")
            # log.info(f"The user: {user.get('id')} has already verified the email: {ex}", extra={"request_id": request_id})
            print ("error - 444")
            raise c_ex.EmailAlreadyVerifiedException(f"The email address has already been verified.")
        # return templates.TemplateResponse("verified_mail.html", {"request": request, "name": user.get("name")}, status_code=HTTPException(status_code= status.HTTP_202_ACCEPTED))
    else:
        # return templates.TemplateResponse("invalid_token.html", {"request": request})
        return {"message": "invalid_token"}









# @router.get('/verify-test')
# async def email_verification(request: Request, token: str):
#     user = await verify_token(token)

#     if user.get("id"):
#         #send a request to update user
#         print("sccuess verify user mail!")
#         return templates.TemplateResponse("verified_mail.html", {"request": request, "name": user.get("name")})
#         pass


# async def send_mail_to_verify_email_address(user: schemas.User):
#     token = oauth2.create_verification_token(user)
#     message = MessageSchema(
#         subject= "Social-Network-FastAPI Verification Email",
#         recipients= [user["email"]],
#         template_body={"name": user["name"], "token": token},
#         subtype= "html",
#     )
#     fm = FastMail(conf_mail)
#     await fm.send_message(message= message, template_name="verification_mail.html")