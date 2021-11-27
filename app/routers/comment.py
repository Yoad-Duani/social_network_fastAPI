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


# @router.get("/", response_model= List[schemas.PostOut])
# def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user),
# limit: int = 10, skip: int = 0, search: Optional[str] = ""):
#     # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
#     posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes"), func.count(models.Comment.post_id).label("comments")).join(models.Vote, models.Vote.post_id == models.Post.id,
#         isouter=True).join(models.Comment,models.Comment.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
#     return  posts