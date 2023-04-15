# from hashlib import new
from sqlalchemy.sql.functions import user
from starlette.routing import Router
from app import oauth2
# from tests.conftest import session
from .. import models,schemas,utils
from fastapi import FastAPI , Response ,status , HTTPException, Depends, APIRouter, Path, Body
from sqlalchemy.orm import Session
# from ..database import get_db
from sqlalchemy.sql.expression import null
from jose import jwt
from app.config import settings
from fastapi.security import OAuth2PasswordBearer
from typing import List, Optional
from pydantic import Required
from app import constants as const



router = APIRouter(
    prefix= "/users",
    tags= ['Users']
    )

# oauth2_schema = OAuth2PasswordBearer(tokenUrl='login')
AUTH_SERVICE = f"http://{settings.auth_service_url}:{settings.auth_service_port}"
MAIN_SERVICE = f"http://{settings.main_service_url}:{settings.main_service_port}"




@router.post("/", status_code = status.HTTP_201_CREATED,response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate = Body(default= Required)):
    pass
    # TODO:
    # 1. call to auth server - create a user credentails
    # 2. call main server - create user info

    # try:
    #     user_email_exists = db.query(models.User).filter(models.User.email == user.email).first()
    # except Exception as error:
    #     print(error)
    #     raise HTTPException(status_code= status.HTTP_503_SERVICE_UNAVAILABLE, detail= f"An error occurred while creating the user")

    # if user_email_exists:
    #     raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail= f"User with this email is alerady exist")
    # hashed_password = utils.hash(user.password)
    # user.password = hashed_password
    # new_user = models.User(**user.dict())
    # try:
    #     db.add(new_user)
    #     db.commit()
    #     db.refresh(new_user)
    # except Exception as error:
    #     print(error)
    #     db.rollback()
    #     raise HTTPException(status_code= status.HTTP_503_SERVICE_UNAVAILABLE, detail= f"An error occurred while creating the user")
    # return new_user

@router.get("/{id}", response_model=schemas.UserResponse)
def get_user(
    id: int = Path(default= Required,title= "user id", description="The ID of the user to get",  ge=const.USER_ID_GE, example=const.EXAMPLE_USER_ID)
):
    pass
    # TODO:
    # 1. 
    # 2. call main server - pull user info


    # try:
    #     user = db.query(models.User).filter(models.User.id == id).first()
    # except Exception as error:
    #     print(error)
    #     raise HTTPException(status_code= status.HTTP_503_SERVICE_UNAVAILABLE, detail= f"An error occurred while trying get user")
    # if not user:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"User with id: {id} does not exist")
    # return user




@router.put("/update-user",response_model= schemas.UserResponse)
def update_user(update_user: schemas.UserUpdate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    pass
    # TODO:
    # 1. call to auth server - get current user
    # 2. call main server - sent updated details (need another key in the heder)
    # 3. 

    # try:
    #     user_query = db.query(models.User).filter(models.User.id == current_user.id)
    # except Exception as error:
    #     print(error)
    #     raise HTTPException(status_code= status.HTTP_503_SERVICE_UNAVAILABLE, detail= f"An error occurred while updating user")
    # if user_query.first() == None:
    #     raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f"user with id: {current_user.id} does not exist")
    # new_update_user = new_user_object(update_user)
    # try:
    #     user_query.update(new_update_user, synchronize_session= False)
    #     db.commit()
    # except Exception as error:
    #     print(error)
    #     db.rollback()
    #     raise HTTPException(status_code= status.HTTP_503_SERVICE_UNAVAILABLE, detail= f"An error occurred while updating user")
    # return user_query.first()