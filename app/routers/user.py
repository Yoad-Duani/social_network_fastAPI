# from hashlib import new
from sqlalchemy.sql.functions import user
from starlette.routing import Router
from app import oauth2
# from tests.conftest import session
from .. import models,schemas,utils
from fastapi import FastAPI , Response ,status , HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import get_db
from sqlalchemy.sql.expression import null
from jose import jwt
from app.config import settings
from fastapi.security import OAuth2PasswordBearer


router = APIRouter(
    prefix= "/users",
    tags= ['Users']
    )

oauth2_schema = OAuth2PasswordBearer(tokenUrl='login')




@router.post("/", status_code = status.HTTP_201_CREATED,response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate ,db: Session = Depends(get_db)):

    user_email_exists = db.query(models.User).filter(models.User.email == user.email).first()
    if user_email_exists:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail= f"User with this email is alerady exist")
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/{id}", response_model=schemas.UserResponse)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"User with id: {id} does not exist")
    return user

#respone
@router.put("/update-user",response_model= schemas.UserResponse)
def update_user(update_user: schemas.UserUpdate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    user_query = db.query(models.User).filter(models.User.id == current_user.id)
    if user_query.first() == None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f"user with id: {current_user.id} does not exist")
    new_update_user = new_user_object(update_user)
    user_query.update(new_update_user, synchronize_session= False)
    db.commit()
    return user_query.first()


def new_user_object(user_object):
    hsa_conntent : bool = False
    new_user_update_object = {}
    if user_object.password != None and user_object.password != "":
        new_user_update_object["password"] = utils.hash(user_object.password)
        hsa_conntent = True
    if user_object.company_name != None and user_object.company_name != "":
        new_user_update_object["company_name"] = user_object.company_name
        hsa_conntent = True
    if user_object.description != None and user_object.description != "":
        new_user_update_object["description"] = user_object.description
        hsa_conntent = True
    if user_object.position != None and user_object.position != "":
        new_user_update_object["position"] = user_object.position
        hsa_conntent = True
    if hsa_conntent == True:
        new_user_update_object["update_at"] = "now()"
        return new_user_update_object
    raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, detail= f"you didnt update any field")


