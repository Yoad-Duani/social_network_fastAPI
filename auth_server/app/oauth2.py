from fastapi import Depends,status,HTTPException
from jose import JWTError, jwt
from datetime import datetime, timedelta

from sqlalchemy.orm import Session
from . import schemas, database, models
from fastapi.security import OAuth2PasswordBearer
from .config import settings
from colorama import init, Fore
from app.log_config import init_loggers
from . import schemas, custom_exceptions as c_ex

log = init_loggers(logger_name="oauth2-logger")


# # TODO:
# # create a check for verify user 

# init(autoreset=True)
# oauth2_schema = OAuth2PasswordBearer(tokenUrl='login')

# SECRET_KEY = f"{settings.secret_key}" 
# ALGORITHM = f"{settings.algorithm}"
# ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

# def create_access_token(data: dict):
#     to_encode = data.copy()
#     expire = datetime.utcnow() + timedelta(minutes = ACCESS_TOKEN_EXPIRE_MINUTES)
#     to_encode.update({"exp": expire})
#     encode_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm= ALGORITHM)
#     return encode_jwt
    
# def verify_access_token(token: str, credentials_exception):
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms= [ALGORITHM])
#         id: str = payload.get("user_id")
#         if id is None:
#             raise credentials_exception
#         token_data = schemas.TokenData(id = id)
#     except JWTError:
#         raise credentials_exception
#     return token_data

# def get_current_user(token: str = Depends(oauth2_schema),db: Session = Depends(database.get_db)):
#     try:
#         credentials_exception = HTTPException(status_code= status.HTTP_401_UNAUTHORIZED, detail= "Could not validate credentials",
#         headers={"WWW-Authenticate": "Bearer"})
#         token = verify_access_token(token, credentials_exception)
#         user = db.query(models.User).filter(models.User.id == token.id).first()
#         return user
#     except Exception as error:
#         print(Fore.RED + "Eror:")
#         print(Fore.RED + str(error))
#         raise HTTPException(status.HTTP_503_SERVICE_UNAVAILABLE, detail= f"An error occurred while connecting to the database")
# #verify_access_token(token, credentials_exception)


# Auth Token Mail
SECRET_KEY = f"{settings.mail_auth_token_key}" 
ALGORITHM = f"{settings.mail_token_algorithm}"
MAIL_TOKEN_EXPIRE_HOURS = settings.mail_token_expire_hours



def create_verification_token(user: schemas.User):
    token_data = {
        "id": user.user_id,
        "email": user.email,
        "name": user.name,
    }
    to_encode = token_data.copy()
    expire = datetime.utcnow() + timedelta(hours= MAIL_TOKEN_EXPIRE_HOURS)
    to_encode.update({"exp": expire})
    token = jwt.encode(to_encode, SECRET_KEY, algorithm= ALGORITHM)
    return token


async def verify_token(action_token: str, request_id: str):
    try:
        log.info(f"Trying to verify token action", extra={"request_id": request_id})
        payload = jwt.decode(action_token, SECRET_KEY, algorithms= [ALGORITHM])
        # user_id: str = payload.get("id")
    except:
        log.warning(f"Invalid action-token has been sent from user -id-", extra={"request_id": request_id})
        raise c_ex.UnverifiedTokenException()
    log.info(f"The token is verified for  -email-", extra={"request_id": request_id})
    return payload