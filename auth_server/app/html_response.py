from fastapi import Body, FastAPI, Form, Cookie, status, Query, Header, HTTPException, Request, BackgroundTasks, HTTPException
from fastapi.templating import Jinja2Templates
from .oauth2 import verify_token
from app.log_config import init_loggers
from pathlib import Path

# templates = Jinja2Templates(directory="templates")
templates = Jinja2Templates(directory= Path(__file__).parent / 'templates')
log = init_loggers(logger_name= "responses-logger")


async def email_verification_response(request: Request, action_token: str, request_id: str):
    # log.info(f"Trying to verify an email address", extra={"request_id": request_id})
    try:
        user = await verify_token(action_token= action_token, request_id= request_id)
    except Exception as ex:
        # return templates.TemplateResponse("invalid_token.html", {"request": request, "exceptionDetail": ex.detail})
        return {"message": "invalid_token"}
    if user.get("id"):
        log.info(f"Email address -yoad@test- has been verified", extra={"request_id": request_id})
        return user
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