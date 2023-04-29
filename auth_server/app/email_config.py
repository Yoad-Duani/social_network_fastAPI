from fastapi import BackgroundTasks, UploadFile, File, Form, Depends, HTTPException, status, Path, Body
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from .config import settings
from . import schemas
from . import oauth2
from pathlib import Path
from fastapi.templating import Jinja2Templates
from app.log_config import init_loggers

templates = Jinja2Templates(directory="templates")
log = init_loggers(logger_name="email-logger")

conf_mail = ConnectionConfig(
    MAIL_USERNAME= settings.mail_username,
    MAIL_PASSWORD=settings.mail_password,
    MAIL_FROM=settings.mail_username,
    MAIL_PORT=settings.mail_port,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_TLS= True,
    MAIL_SSL= False,
    USE_CREDENTIALS=True,
    TEMPLATE_FOLDER=Path(__file__).parent / 'templates'
)

async def send_mail_to_verify_email_address(request_id: str, user: schemas.User):
    token = oauth2.create_verification_token(user)
    message = MessageSchema(
        subject= "Social-Network-FastAPI Verification Email",
        recipients= [user.email],
        template_body={"name": user.name, "token": token},
        subtype= "html",
    )
    fm = FastMail(conf_mail)
    log.info(f"Sending email to verify email address {user.name}", extra={"request_id": request_id})
    try:
        await fm.send_message(message= message, template_name="verification_mail.html")
    except Exception as ex:
        log.error(f"An error occurred while sending a verification email to {user.email}: {ex}", extra={"request_id": request_id})
        raise Exception(f"An error occurred while sending a verification email to {user.email}: {ex}")
    log.info(f"The verification email to {user.email} has been sent", extra={"request_id": request_id})