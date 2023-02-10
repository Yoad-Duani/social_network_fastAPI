from fastapi import Depends,status,HTTPException
from jose import JWTError, jwt
from datetime import datetime, timedelta
from functools import lru_cache

from sqlalchemy.orm import Session
from . import schemas, database, models
from fastapi.security import OAuth2PasswordBearer
from .config import settings
from colorama import init, Fore


@lru_cache()
def get_settings():
    return settings()


init(autoreset=True)
oauth2_schema = OAuth2PasswordBearer(tokenUrl='login')

SECRET_KEY = f"{settings.secret_key}" 
ALGORITHM = f"{settings.algorithm}"
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes = ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encode_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm= ALGORITHM)
    return encode_jwt
    
def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms= [ALGORITHM])
        id: str = payload.get("user_id")
        if id is None:
            raise credentials_exception
        token_data = schemas.TokenData(id = id)
    except JWTError:
        raise credentials_exception
    return token_data

def get_current_user(token: str = Depends(oauth2_schema),db: Session = Depends(database.get_db)):
    try:
        credentials_exception = HTTPException(status_code= status.HTTP_401_UNAUTHORIZED, detail= "Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"})
        token = verify_access_token(token, credentials_exception)
        user = db.query(models.User).filter(models.User.id == token.id).first()
        return user
    except Exception as error:
        print(Fore.RED + "Eror:")
        print(Fore.RED + str(error))
        raise HTTPException(status.HTTP_503_SERVICE_UNAVAILABLE, detail= f"An error occurred while connecting to the database")
#verify_access_token(token, credentials_exception)