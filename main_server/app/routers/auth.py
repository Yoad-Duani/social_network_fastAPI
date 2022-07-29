from fastapi import APIRouter, Depends, status, HTTPException ,Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy import schema
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import null
from .. import database, schemas, models, utils, oauth2
from fastapi import Response


router = APIRouter(tags= ['Authentication'])

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