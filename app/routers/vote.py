from .. import models,schemas,oauth2,database
from fastapi import FastAPI , Response ,status , HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import get_db
from sqlalchemy.sql.expression import null
from typing import List, Optional
from app import constants as const


router = APIRouter(
    prefix="/vote",
    tags=['Vote']
)

@router.post("/", status_code= status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id)
    try:
        post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    except Exception as error:
        print(error)
        raise HTTPException(status_code= status.HTTP_503_SERVICE_UNAVAILABLE, detail= f"An error occurred while votting the post")
    if not post :
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f"Post with id: {vote.post_id}  does not exist")
    try:
        found_vote = vote_query.first()
    except Exception as error:
        print(error)
        raise HTTPException(status_code= status.HTTP_503_SERVICE_UNAVAILABLE, detail= f"An error occurred while votting the post")
    if(vote.dir == const.VOTE_MAX_VALUE):
        if found_vote:
            raise HTTPException(status_code= status.HTTP_409_CONFLICT, detail=f"user {current_user.id} has alredy voted on post {vote.post_id}")
        new_vote = models.Vote(post_id = vote.post_id, user_id = current_user.id)
        try:
            db.add(new_vote)
            db.commit()
        except Exception as error:
            print(error)
            db.rollback()
            raise HTTPException(status_code= status.HTTP_503_SERVICE_UNAVAILABLE, detail= f"An error occurred while votting the post")
        return {"message": "successfuly added vote"}
    else:
        if not found_vote:
            raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail="Vote does not exist")
        try:
            vote_query.delete(synchronize_session=False)
            db.commit()
        except Exception as error:
            print(error)
            db.rollback()
            raise HTTPException(status_code= status.HTTP_503_SERVICE_UNAVAILABLE, detail= f"An error occurred while votting the post")
        return {"message": "successfuly deleted vote"}