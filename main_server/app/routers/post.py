#from sqlalchemy.sql.functions import user
#from starlette.routing import Router
# from _typeshed import Self
# import re
from .. import models,schemas,oauth2
from fastapi import FastAPI , Response ,status , HTTPException, Depends, APIRouter, Body, Path, Query
from sqlalchemy.orm import Session
from ..database import get_db
from sqlalchemy.sql.expression import null
from sqlalchemy import func
from typing import List, Optional, Union
from app import constants as const
from pydantic import Required


router = APIRouter(
    prefix= "/posts",
    tags= ['Posts']
    )
router_group = APIRouter(
    prefix= "/group",
    tags= ['Posts']
    )



@router.get("/", response_model= List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user),
    limit: int = Query(default= const.DEFAULT_LIMIT_GET_POSTS, ge= const.MIN_LIMIT_GET_POSTS, le= const.MAX_LIMIT_GET_POSTS, title="limit post", description= "limit on the number of posts when get from the DB",example= const.EXAMPLE_LIMIT_GET_POSTS), 
    skip: int = Query(default= const.DEFAULT_SKIP_GET_POSTS, ge= const.MIN_SKIP_GET_POSTS, le= const.MAX_SKIP_GET_POSTS, title="skip on posts", description= "skipping posts by offset",example= const.EXAMPLE_SKIP_GET_POSTS),
    search: Optional[str] = Query(default= const.DEFAULT_VALUE_SEARCH_KEY_GET_POSTS, min_length= const.MIN_LENGTH_SEARCH_KEY_GET_POSTS, max_length= const.MAX_LENGTH_SEARCH_KEY_GET_POSTS, title= "key word", description="search for posts by keyword", example= "work")
):
    try:
        posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes"), func.count(models.Comment.post_id).label("comments")).join(models.Vote, models.Vote.post_id == models.Post.id,
            isouter=True).join(models.Comment,models.Comment.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    except Exception as error:
        print(error)
        raise HTTPException(status_code= status.HTTP_503_SERVICE_UNAVAILABLE, detail= f"An error occurred while getting posts")
    return  posts


@router_group.get("/{group_id}/posts", response_model= List[schemas.PostOut], status_code = status.HTTP_200_OK)
def get_posts_by_group(group_id: int = Path(default= Required, title= "group id", description="The ID of the group to get user", ge=const.GROUPS_ID_GE, example=const.EXAMPLE_GROUPS_ID), 
    db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user),
    limit: int = Query(default= const.DEFAULT_LIMIT_GET_POSTS, ge= const.MIN_LIMIT_GET_POSTS, le= const.MAX_LIMIT_GET_POSTS, title="limit post", description= "limit on the number of posts when get from the DB",example= const.EXAMPLE_LIMIT_GET_POSTS), 
    skip: int = Query(default= const.DEFAULT_SKIP_GET_POSTS, ge= const.MIN_SKIP_GET_POSTS, le= const.MAX_SKIP_GET_POSTS, title="skip on posts", description= "skipping posts by offset",example= const.EXAMPLE_SKIP_GET_POSTS), 
    search: Optional[str] = Query(default= const.DEFAULT_VALUE_SEARCH_KEY_GET_POSTS, min_length= const.MIN_LENGTH_SEARCH_KEY_GET_POSTS, max_length= const.MAX_LENGTH_SEARCH_KEY_GET_POSTS, title= "key word", description="search for posts by keyword", example= "work"),
):
    try:
        group = db.query(models.Groups).filter(models.Groups.groups_id == group_id).first()
    except Exception as error:
        print(error)
        raise HTTPException(status_code= status.HTTP_503_SERVICE_UNAVAILABLE, detail= f"An error occurred while getting posts")
    if not group:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail= f"group with id {group_id} was not found")
    try:
        member_in_group = db.query(models.UserInGroups).filter(models.UserInGroups.groups_id == group_id).filter(models.UserInGroups.user_id == current_user.id).first()
    except Exception as error:
        print(error)
        raise HTTPException(status_code= status.HTTP_503_SERVICE_UNAVAILABLE, detail= f"An error occurred while getting posts")
    if not member_in_group:
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail= f"Not authhorized to perform requested action, you are not member in this group")
    try:
        posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes"), func.count(models.Comment.post_id).label("comments")).join(models.Vote, models.Vote.post_id == models.Post.id,
            isouter=True).join(models.Comment,models.Comment.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.group_id == group_id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    except Exception as error:
        print(error)
        raise HTTPException(status_code= status.HTTP_503_SERVICE_UNAVAILABLE, detail= f"An error occurred while getting posts")
    return posts


@router.post("/", status_code = status.HTTP_201_CREATED, response_model= schemas.PostResponse)
def create_posts(post: schemas.PostCreate = Body(default= Required), db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    new_post = models.Post(owner_id = current_user.id, **post.dict())
    if new_post.title == "" or new_post.content == "":
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY,detail= f"the post must contains context and title")
    try:
        db.add(new_post)
        db.commit()
        db.refresh(new_post)
    except Exception as error:
        print(error)
        db.rollback()
        raise HTTPException(status_code= status.HTTP_503_SERVICE_UNAVAILABLE, detail= f"An error occurred while creating the post")
    return  new_post


@router_group.post("/{group_id}/post", status_code= status.HTTP_201_CREATED, response_model= schemas.PostResponse)
def create_post_in_group(post: schemas.PostCreate = Body(default= Required), 
    group_id: int = Path(default= Required, title= "group id", description="The ID of the group to get user", ge=const.GROUPS_ID_GE, example=const.EXAMPLE_GROUPS_ID), 
    db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)
):
    try:
        group = db.query(models.Groups).filter(models.Groups.groups_id == group_id).first()
    except Exception as error:
        print(error)
        raise HTTPException(status_code= status.HTTP_503_SERVICE_UNAVAILABLE, detail= f"An error occurred while creating the post")
    if not group:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail= f"group with id {group_id} was not found")
    try:
        member_in_group = db.query(models.UserInGroups).filter(models.UserInGroups.groups_id == group_id).filter(models.UserInGroups.user_id == current_user.id).first()
    except Exception as error:
        print(error)
        raise HTTPException(status_code= status.HTTP_503_SERVICE_UNAVAILABLE, detail= f"An error occurred while creating the post")
    if not member_in_group:
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail= f"Not authhorized to perform requested action, you are not member in this group")
    if post.title == "" or post.content == "":
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY,detail= f"the post must contains context and title")
    new_post = models.Post(owner_id = current_user.id, group_id = group_id ,**post.dict())
    try:
        db.add(new_post)
        db.commit()
        db.refresh(new_post)
    except Exception as error:
        db.rollback()
        print(error)
        raise HTTPException(status_code= status.HTTP_503_SERVICE_UNAVAILABLE, detail= f"An error occurred while creating the post")
    return  new_post


@router.get("/{id}",response_model= schemas.PostOut)
def get_post(id: int = Path(default= Required,title= "post id", description="The ID of the post to get",  ge=const.POST_ID_GE, example=const.EXAMPLE_POST_ID),
    db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)
):
    try:
        post = db.query(models.Post, func.count(models.Vote.post_id).label("votes"), func.count(models.Comment.post_id).label("comments")).join(models.Vote,
            models.Vote.post_id == models.Post.id,
            isouter=True).join(models.Comment,models.Comment.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
    except Exception as error:
        print(error)
        raise HTTPException(status_code= status.HTTP_503_SERVICE_UNAVAILABLE, detail= f"An error occurred while getting the post")
    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"post with id: {id} was not found")
    if post["Post"].group_id != 0:
        try:
            post_in_group = db.query(models.UserInGroups).filter(models.UserInGroups.groups_id == post["Post"].group_id).filter(models.UserInGroups.user_id == current_user.id).first()
        except Exception as error:
            print(error)
            raise HTTPException(status_code= status.HTTP_503_SERVICE_UNAVAILABLE, detail= f"An error occurred while getting the post")
        if not post_in_group:
            raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail= f"Not authhorized to perform requested action, not member in this group")
    return post
    


@router.delete("/{id}", status_code = status.HTTP_204_NO_CONTENT)
def delete_post(id: int = Path(default= Required,title= "post id", description="The ID of the post to delete",  ge=const.POST_ID_GE, example=const.EXAMPLE_POST_ID), 
    db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)
):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    try:
        post = post_query.first()
    except Exception as error:
        print(error)
        raise HTTPException(status_code= status.HTTP_503_SERVICE_UNAVAILABLE, detail= f"An error occurred while deleting the post")
    if post == None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f"post with id: {id} does not exist")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail= f"Not authhorized to perform requested action")
    try:
        post_query.delete(synchronize_session= False)
        db.commit()
    except Exception as error:
        db.rollback()
        print(error)
        raise HTTPException(status_code= status.HTTP_503_SERVICE_UNAVAILABLE, detail= f"An error occurred while deleting the post")
    return Response(status_code= status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model= schemas.PostResponse)
def update_post(updated_post: schemas.PostCreate,
    id: int = Path(default= Required,title= "post id", description="The ID of the post to update", ge=const.POST_ID_GE, example=const.EXAMPLE_POST_ID), 
    db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)
):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    try:
        post = post_query.first()
    except Exception as error:
        print(error)
        raise HTTPException(status_code= status.HTTP_503_SERVICE_UNAVAILABLE, detail= f"An error occurred while updating the post")
    if post == None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f"post with id: {id} does not exist")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail= f"Not authhorized to perform requested action")
    try:
        post_query.update(updated_post.dict(), synchronize_session= False)
        db.commit()
    except Exception as error:
        print(error)
        db.rollback()
        raise HTTPException(status_code= status.HTTP_503_SERVICE_UNAVAILABLE, detail= f"An error occurred while updating the post")
    return post_query.first()  