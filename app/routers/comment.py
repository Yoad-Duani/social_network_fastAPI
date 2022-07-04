from requests import post
from sqlalchemy.sql.functions import current_user
from .. import models,schemas,oauth2
from fastapi import Body, FastAPI, Path, Query , Response ,status , HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import get_db
from sqlalchemy.sql.expression import null
from sqlalchemy import func
from typing import List, Optional
from pydantic import Required
from app import constants as const

router = APIRouter(
    prefix= "/posts/{id}/comments",
    tags= ['Comments']
    )

## I need to add check if user is verified and not block
## if post is in group check user is not block
##


@router.get("/",response_model= List[schemas.CommentResponse])
def get_comments(id: int = Path(default= Required, title="post id", description= "The ID of the post to get comments", ge= const.POST_ID_GE),
    db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user),
    limit: Optional[int] = Query(default= const.DEFAULT_LIMIT_GET_COMMENTS, title= "limit comments", description= "limit on the number of comments to get from the DB",ge= const.MIN_LIMIT_GET_COMMENTS, le= const.MAX_LIMIT_GET_COMMENTS),
    skip: Optional[int] = Query(default= const.DEFAULT_SKIP_GET_COMMENTS, title= "skip on comments", description= "skipping comments by offset", ge= const.MIN_SKIP_GET_COMMENTS, le= const.MAX_SKIP_GET_COMMENTS)
):
    try:
        post = db.query(models.Post).filter(models.Post.id == id).first()
    except Exception as error:
        print(error)
        raise HTTPException(status_code= status.HTTP_503_SERVICE_UNAVAILABLE, detail= f"An error occurred while getting comments")
    if not post:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f"post with id: {id} was not found")
    if post.group_id != 0:
        try:
            group = db.query(models.Groups).filter(models.Groups.groups_id ==  post.group_id).first()
        except Exception as error:
            print(error)
            raise HTTPException(status_code= status.HTTP_503_SERVICE_UNAVAILABLE, detail= f"An error occurred while getting comments")
        if group.group_private == True:
            try:
                user_in_group = db.query(models.UserInGroups).filter(models.UserInGroups.groups_id == post.group_id).filter(models.UserInGroups.user_id == current_user.id).first()
            except Exception as error:
                print(error)
                raise HTTPException(status_code= status.HTTP_503_SERVICE_UNAVAILABLE, detail= f"An error occurred while getting comments")
            if not user_in_group:
                raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail= f"user with id: {current_user.id} not member in the group and the group is privte")
            if user_in_group.is_blocked == True:
                raise HTTPException(status.HTTP_406_NOT_ACCEPTABLE, detail= f"the user has blocked from this group")
            if current_user.verified == False or current_user.is_blocked == True:
                raise HTTPException(status.HTTP_406_NOT_ACCEPTABLE, detail= f"the user have to be verified and not block")
    try:
        comments = db.query(models.Comment).filter(models.Comment.post_id == id).limit(limit).offset(skip).all()
    except Exception as error:
        print(error)
        raise HTTPException(status_code= status.HTTP_503_SERVICE_UNAVAILABLE, detail= f"An error occurred while getting comments")
    return  comments


# add check if the post is in group - like get all comments
@router.get("/{comment_id}",response_model=schemas.CommentResponse)
def get_comments(id: int = Path(default= Required, title="post id", description= "The ID of the post to get comments", ge= const.POST_ID_GE), 
    comment_id: int =  Path(default= Required, title="comment id", description= "The ID of the comment to get comments", ge= const.COMMENT_ID_GE),
    db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)
):
    try:
        post = db.query(models.Post).filter(models.Post.id == id).first()
    except Exception as error:
        print(error)
        raise HTTPException(status_code= status.HTTP_503_SERVICE_UNAVAILABLE, detail= f"An error occurred while getting comment")
    if not post:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f"post with id: {id} was not found")
    try:
        comment = db.query(models.Comment).filter(models.Comment.post_id == id).filter(models.Comment.comment_id == comment_id).first()
    except Exception as error:
        print(error)
        raise HTTPException(status_code= status.HTTP_503_SERVICE_UNAVAILABLE, detail= f"An error occurred while getting comment")
    if not comment:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f"comment with id: {comment_id} was not found")
    return  comment



@router.post("/", status_code= status.HTTP_201_CREATED,response_model=schemas.CommentResponse)
def create_comment(comment: schemas.CommentCreate = Body( default= Required), 
    id: int = Path(default= Required, title="post id", description= "The ID of the post to get comments", ge= const.POST_ID_GE), 
    db:Session = Depends(get_db),currect_user:int = Depends(oauth2.get_current_user)
):
    try:
        post = db.query(models.Post).filter(models.Post.id == id).first()
    except Exception as error:
        print(error)
        raise HTTPException(status_code= status.HTTP_503_SERVICE_UNAVAILABLE, detail= f"An error occurred while creating comment")
    if not post:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f"post with id: {id} was not found")
    if post.group_id != 0:
        try:
            user_in_group = db.query(models.UserInGroups).filter(models.UserInGroups.groups_id == post.group_id).filter(models.UserInGroups.user_id == currect_user.id).first()
        except Exception as error:
            print(error)
            raise HTTPException(status_code= status.HTTP_503_SERVICE_UNAVAILABLE, detail= f"An error occurred while creating comment")
        if not user_in_group:
            raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail= f"you are not member in the post's group")
    new_comment = models.Comment(user_id = currect_user.id, post_id = id, **comment.dict())
    if not new_comment.content != "":
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY,detail= f"the content of comment have contains context")
    try:
        db.add(new_comment)
        db.commit()
        db.refresh(new_comment)
    except Exception as error:
        print(error)
        db.rollback()
        raise HTTPException(status_code= status.HTTP_503_SERVICE_UNAVAILABLE, detail= f"An error occurred while creating comment")
    return new_comment



@router.put("/{comment_id}",response_model= schemas.CommentResponse)
def update_comment(comment_id: int = Path(default= Required, title="comment id", description= "The ID of the comment to get comments", ge= const.COMMENT_ID_GE), 
    id: int = Path(default= Required, title="post id", description= "The ID of the post to get comments", ge= const.POST_ID_GE), 
    update_comment: schemas.CommentUpdate = Body(default= Required), 
    db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)
):
    try:
        post = db.query(models.Post).filter(models.Post.id == id).first()
    except Exception as error:
        print(error)
        raise HTTPException(status_code= status.HTTP_503_SERVICE_UNAVAILABLE, detail= f"An error occurred while updating comment")
    if not post:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f"post with id: {id} was not found")
    comment_query = db.query(models.Comment).filter(models.Comment.comment_id == comment_id)
    try:
        comment = comment_query.first()
    except Exception as error:
        print(error)
        raise HTTPException(status_code= status.HTTP_503_SERVICE_UNAVAILABLE, detail= f"An error occurred while updating comment")
    if comment == None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f"comment with id: {comment_id} does not exist")
    if comment.user_id != current_user.id:
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail= f"Not authhorized to perform requested action")
    new_object = new_comment_object(update_comment)
    try:
        comment_query.update(new_object, synchronize_session=False)
        db.commit()
    except Exception as error:
        print(error)
        db.rollback()
        raise HTTPException(status_code= status.HTTP_503_SERVICE_UNAVAILABLE, detail= f"An error occurred while updating comment")
    return comment_query.first()

#create a new key with datetime to update the curect time of the update
def new_comment_object(object):
    if object.content == "" or object.content == None:
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY,detail= f"the content of comment have contains context")
    return {"content": object.content, "update_at": "now()"}
    


@router.delete("/{comment_id}", status_code= status.HTTP_204_NO_CONTENT)
def delete_comment(comment_id: int = Path(default= Required, title="comment id", description= "The ID of the comment to get comments", ge= const.COMMENT_ID_GE), 
    id: int = Path(default= Required, title="post id", description= "The ID of the post to get comments", ge= const.POST_ID_GE), 
    db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)
):
    try:
        post = db.query(models.Post).filter(models.Post.id == id).first()
    except Exception as error:
        print(error)
        raise HTTPException(status_code= status.HTTP_503_SERVICE_UNAVAILABLE, detail= f"An error occurred while deletting comment")
    if not post:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f"post with id: {id} was not found")
    comment_query = db.query(models.Comment).filter(models.Comment.comment_id == comment_id)
    try:
        comment = comment_query.first()
    except Exception as error:
        print(error)
        raise HTTPException(status_code= status.HTTP_503_SERVICE_UNAVAILABLE, detail= f"An error occurred while deletting comment")
    if comment == None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f"comment with id: {comment_id} does not exist")
    if comment.user_id != current_user.id:
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail= f"Not authhorized to perform requested action")
    try:
        comment_query.delete(synchronize_session= False)
        db.commit()
    except Exception as error:
        print(error)
        db.rollback()
        raise HTTPException(status_code= status.HTTP_503_SERVICE_UNAVAILABLE, detail= f"An error occurred while deletting comment")
    return Response(status_code= status.HTTP_204_NO_CONTENT)
