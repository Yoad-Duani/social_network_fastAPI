from fastapi import APIRouter, Depends, status, HTTPException, Response, Path, Body, Query
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy import schema
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import null
from .. import database, schemas, models, utils, oauth2
from app import constants as const
from pydantic import Required, SecretStr

from ..main import idp
from typing import List, Optional
from fastapi_keycloak import FastAPIKeycloak, OIDCUser, UsernamePassword, HTTPMethod, KeycloakUser, KeycloakGroup


# TODO:
# add test

router = APIRouter(tags= ['Authentication'])

# FIXME:
# update the funcation - acording to auth_user table

@router.post("/login", response_model=schemas.TokenResponse)
def login(respone: Response, user_credentails: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    try:
        user = db.query(models.User).filter(models.User.email == user_credentails.username).first()
    except:
        raise HTTPException(status.HTTP_503_SERVICE_UNAVAILABLE, detail= f"An error occurred while connecting to the database")
    if not user:
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")
    if not utils.verify(user_credentails.password, user.password):
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")
        
    access_token = oauth2.create_access_token(data= {"user_id": user.id, "user_verified":user.verified, "user_block":user.is_blocked})
    respone.set_cookie(key='token', value=access_token, httponly=True)
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/create-user-credentials", response_model=schemas.ResponseUserCredentials, status_code = status.HTTP_201_CREATED)
def create_credentials_user(user: schemas.CreateUserCredentials = Body(default= Required),db: Session = Depends(database.get_db)):
    try:
        user_email_exists = db.query(models.User).filter(models.User.email == user.email).first()
    except Exception as error:
        print(error)
        raise HTTPException(status_code= status.HTTP_503_SERVICE_UNAVAILABLE, detail= f"An error occurred while creating the user")
    if user_email_exists:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail= f"User with this email is alerady exist")
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    new_user = models.User(**user.dict())
    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    except Exception as error:
        print(error)
        db.rollback()
        raise HTTPException(status_code= status.HTTP_503_SERVICE_UNAVAILABLE, detail= f"An error occurred while creating the user")
    return new_user


@router.put("/update-user-credentials", response_model=schemas.ResponseUserCredentials, status_code = status.HTTP_200_OK)
def update_credentials_user(user_credentials: schemas.UpdateUserCredentials, db: Session = Depends(database.get_db), current_user: int = Depends(oauth2.get_current_user)):
    try:
        user_query = db.query(models.User).filter(models.User.id == current_user.id)
    except Exception as error:
        print(error)
        raise HTTPException(status_code= status.HTTP_503_SERVICE_UNAVAILABLE, detail= f"An error occurred while updating user")
    if user_query.first() == None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f"user with id: {current_user.id} does not exist")
    password = utils.hash(user_credentials.password)   
    try:
        user_query.update({"password": password, "password_update_at": "now()"}, synchronize_session= False)
        db.commit()
    except Exception as error:
        print(error)
        db.rollback()
        raise HTTPException(status_code= status.HTTP_503_SERVICE_UNAVAILABLE, detail= f"An error occurred while updating user")
    return user_query.first()


# TODO:
# create funcation for remove credentials



# FIXME:
# fix the current user to secret key / token

@router.put("/verify-user", status_code = status.HTTP_200_OK)
def update_verify_user(user_id: int = Path(default= Required,title= "user id", description="The ID of the user to get",  ge=const.USER_ID_GE, example=const.EXAMPLE_USER_ID), 
    db: Session = Depends(database.get_db), current_user: int = Depends(oauth2.get_current_user)
):
    user_query = db.query(models.User).filter(models.User.id == current_user.id)
    try:
        user = user_query.first()
    except Exception as error:
        print(error)
        raise HTTPException(status_code= status.HTTP_503_SERVICE_UNAVAILABLE, detail= f"An error occurred while verify user")
    if user == None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f"user with id: {current_user.id} does not exist")
    if user.verified == True:
        raise HTTPException(status_code= status.HTTP_409_CONFLICT, detail= f"user with id: {current_user.id} already verified")
    try:
        user_query.update({"verified": True}, synchronize_session= False)
        db.commit()
    except Exception as error:
        print(error)
        db.rollback()
        raise HTTPException(status_code= status.HTTP_503_SERVICE_UNAVAILABLE, detail= f"An error occurred while verify user")
    return {"status": "succeeded - user authenticated"}



# TODO:
# create funcation for block user - scope admin

# TODO:
# create funcation for unblock user - scop admin







# Admin

@router.post("/proxy", tags=["admin-cli"])
def proxy_admin_request(relative_path: str, method: HTTPMethod, additional_headers: dict = Body(None), payload: dict = Body(None)):
    return idp.proxy(
        additional_headers=additional_headers,
        relative_path=relative_path,
        method=method,
        payload=payload
    )


@router.get("/identity-providers", tags=["admin-cli"])
def get_identity_providers():
    return idp.get_identity_providers()


@router.get("/idp-configuration", tags=["admin-cli"])
def get_idp_config():
    return idp.open_id_configuration