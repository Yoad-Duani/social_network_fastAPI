# from fastapi import FastAPI, BackgroundTasks, UploadFile, File, Form, status, HTTPException, Depends
# from fastapi_mail import FastMail, MessageSchema,ConnectionConfig
# from .config import settings
# from . import models,schemas,utils
# from jose import JWTError, jwt





# conf = ConnectionConfig(
#     MAIL_USERNAME = settings.email_username,
#     MAIL_PASSWORD = settings.email_password,
#     MAIL_FROM = settings.email_from,
#     MAIL_PORT = 587,
#     MAIL_SERVER = "smpt.gmail.com",
#     MAIL_TLS = True,
#     MAIL_SSL = False,
#     USE_CREDENTIALS = True,
#     #VALIDATE_CERTS = True
# )


# async def send_email(email: schemas.EmailSchema, user: models.User):

#     token_data = {
#         "id": user.id,
#         "user_name": user
#     }

#     token = jwt.encode(token_data,settings.secret_key)

