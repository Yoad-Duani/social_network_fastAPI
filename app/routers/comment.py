from sqlalchemy.sql.functions import current_user
from .. import models,schemas,oauth2
from fastapi import FastAPI , Response ,status , HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import get_db
from sqlalchemy.sql.expression import null
from sqlalchemy import func
from typing import List, Optional

router = APIRouter(
    prefix= "/posts/{id}/comments",
    tags= ['Comments']
    )


@router.get("/",response_model=    List[schemas.CommentResponse])
def get_comments(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user),
limit: int = 10, skip: int = 0):
    comments = db.query(models.Comment).filter(models.Comment.post_id == id).limit(limit).offset(skip).all()
    return  comments

@router.get("/{comment_id}",response_model=schemas.CommentResponse)
def get_comments(id: int, comment_id: int,   db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    comment = db.query(models.Comment).filter(models.Comment.post_id == id).filter(models.Comment.comment_id == comment_id).first()
    if not comment:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f"comment with id: {comment_id} was not found")
    return  comment


@router.post("/", status_code= status.HTTP_201_CREATED,response_model=schemas.CommentResponse)
def create_comment(comment: schemas.CommentCreate, db:Session = Depends(get_db),currect_user:int = Depends(oauth2.get_current_user)):
        new_comment = models.Comment(**comment.dict())
        if not db.query(models.User).filter(models.User.id == new_comment.user_id).first():
            raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f"user with id: {new_comment.user_id} was not found")
        if not db.query(models.Post).filter(models.Post.id == new_comment.post_id).first():
            raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f"post with id: {new_comment.post_id} was not found")
        if not new_comment.content != "":
            raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY,detail= f"the content of comment have contains context")
        db.add(new_comment)
        db.commit()
        db.refresh(new_comment)
        return new_comment


@router.put("/{comment_id}",response_model= schemas.CommentResponse)
def update_comment(comment_id: int, update_comment: schemas.CommentUpdate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    new_object = new_comment_object(update_comment)
    comment_query = db.query(models.Comment).filter(models.Comment.comment_id == comment_id)
    comment = comment_query.first()
    if comment == None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f"comment with id: {comment_id} does not exist")
    if comment.user_id != current_user.id:
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail= f"Not authhorized to perform requested action")
    comment_query.update(new_object, synchronize_session=False)
    db.commit()
    return comment_query.first()

#create a new key with datetime to update the curect time of the update
def new_comment_object(object):
    new_object_v = {"content": object.content, "update_at": "now()"}
    return new_object_v


@router.delete("/{comment_id}", status_code= status.HTTP_204_NO_CONTENT)
def delete_comment(comment_id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    comment_query = db.query(models.Comment).filter(models.Comment.comment_id == comment_id)
    comment = comment_query.first()
    if comment == None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f"comment with id: {comment_id} does not exist")
    if comment.user_id != current_user.id:
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail= f"Not authhorized to perform requested action")
    comment_query.delete(synchronize_session= False)
    db.commit()
    return Response(status_code= status.HTTP_204_NO_CONTENT)