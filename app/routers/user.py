from starlette.routing import Router
from .. import models,schemas,utils
from fastapi import FastAPI , Response ,status , HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import get_db
from sqlalchemy.sql.expression import null

router = APIRouter(
    prefix= "/users",
    tags= ['Users']
    )



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