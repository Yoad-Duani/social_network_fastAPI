from fastapi import HTTPException
import jwt
from .config import settings
from fastapi import status
from datetime import datetime, timedelta
# from jose import JWTError, jwt
 
SECRET_KEY = f"{settings.mail_auth_token_key}" 
ALGORITHM = f"{settings.mail_token_algorithm}"
MAIL_TOKEN_EXPIRE_HOURS = settings.mail_token_expire_hours


def create_verification_token(user: dict):
    token_data = {
        "id": user["user_id"],
        "email": user["email"],
        "name": user["name"],
    }
    to_encode = token_data.copy()
    expire = datetime.utcnow() + timedelta(hours= MAIL_TOKEN_EXPIRE_HOURS)
    to_encode.update({"exp": expire})
    token = jwt.encode(to_encode, SECRET_KEY, algorithm= ALGORITHM)
    return token


async def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms= [ALGORITHM])
        user_id: str = payload.get("id")
    except:
        raise HTTPException(status_code= status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Token",
            headers={"WWW-Authenticate": "Bearer"}
        )
    return payload