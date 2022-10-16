# from email import message
# from re import M
from datetime import datetime, timedelta
from fastapi import BackgroundTasks, UploadFile, File, Form, Depends, HTTPException, status, Path, Body
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
# from fastapi_mail import MessageType
from .config import settings
from pydantic import Required
from . import schemas
from app import constants as const
import jwt
from . import oauth2

from pathlib import Path

from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")

conf = ConnectionConfig(
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

async def send_email(user: schemas.User):
    token = oauth2.create_verification_token(user)
    message = MessageSchema(
        subject= "Social-Network-FastAPI Verification Email",
        recipients= [user["email"]],
        template_body={"name": user["name"], "token": token},
        subtype= "html",
    )
    fm = FastMail(conf)
    await fm.send_message(message= message, template_name="verification_mail.html")