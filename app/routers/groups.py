from sqlalchemy.sql.functions import current_user
from .. import models,schemas,oauth2
from fastapi import FastAPI , Response ,status , HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import get_db
from sqlalchemy.sql.expression import null
from sqlalchemy import func, desc
from typing import List, Optional

router = APIRouter(
    prefix= "/groups",
    tags= ['Groups']
    )

#response_model= List[schemas.groupsResponse]
@router.get("/")
def get_groups(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user),
limit:int = 10, search: str = ""):
    groups_query = db.query(models.Groups, func.count(models.UserInGroups.groups_id).label("members")).join(models.UserInGroups, models.UserInGroups.groups_id == models.Groups.groups_id,isouter=True).group_by(models.Groups.groups_id)
    if search == "":
        groups= groups_query.filter().order_by(desc("members")).limit(limit).all()
        #groups = db.query(models.Groups, func.count(models.UserInGroups.groups_id).label("members")).join(models.UserInGroups, models.UserInGroups.groups_id == models.Groups.groups_id,isouter=True).group_by(models.Groups.groups_id).filter().order_by(desc("members")).limit(limit).all()
    else:
        groups= groups_query.filter(models.Groups.name.contains(search)).limit(limit).all()
        #groups = db.query(models.Groups, func.count(models.UserInGroups.groups_id).label("members")).join(models.UserInGroups, models.UserInGroups.groups_id == models.Groups.groups_id,isouter=True).group_by(models.Groups.groups_id).filter(models.Groups.name.contains(search)).limit(limit).all()
    new_groups = new_groups_objects(groups)
    return new_groups

#create a new List objects with members field inside
def new_groups_objects(objects):
    new_object_v=[]
    for object in objects:
        new_object_v.append({"groups_id": object.Groups.creator_id, "name": object.Groups.name, "group_private":object.Groups.group_private, "created_at": object.Groups.created_at, "update_at": object.Groups.update_at, "members":object.members, "description": object.Groups.description})
    return new_object_v



@router.get("/{groups_id}")
def get_group(groups_id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    group = db.query(models.Groups, func.count(models.UserInGroups.groups_id).label("members")).join(models.UserInGroups, models.UserInGroups.groups_id == models.Groups.groups_id,isouter=True).group_by(models.Groups.groups_id).filter(models.Groups.groups_id == groups_id).first()
    if not group:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f"group with id: {groups_id} was not found")
    new_group = new_group_object(group)
    return new_group

def new_group_object(object):
    new_object_v = ({"groups_id": object.Groups.creator_id, "name": object.Groups.name, "group_private":object.Groups.group_private, "created_at": object.Groups.created_at, "update_at": object.Groups.update_at, "members":object.members, "description": object.Groups.description})
    return new_object_v



#response_model=schemas.CommentResponse
@router.post("/", status_code= status.HTTP_201_CREATED)
def create_group(group: schemas.GroupCreate, db:Session = Depends(get_db),currect_user:int = Depends(oauth2.get_current_user)):
    if not group.name != "":
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY,detail= f"the name of the group have contains context")
    if not group.description != "":
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY,detail= f"the description of the group have contains context")
    group_with_ceatorID = add_currect_user(group, currect_user)
    new_group = models.Groups(**group_with_ceatorID)
    db.add(new_group)
    db.commit()
    db.refresh(new_group)
    return new_group

def add_currect_user(group, currect_user):
    return {"name": group.name, "description": group.description, "group_private": group.group_private, "creator_id": currect_user.id}






# @router.post("/", status_code= status.HTTP_201_CREATED,response_model=schemas.CommentResponse)
# def create_comment(comment: schemas.CommentCreate, db:Session = Depends(get_db),currect_user:int = Depends(oauth2.get_current_user)):
#         new_comment = models.Comment(**comment.dict())
#         if not db.query(models.User).filter(models.User.id == new_comment.user_id).first():
#             raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f"user with id: {new_comment.user_id} was not found")
#         if not db.query(models.Post).filter(models.Post.id == new_comment.post_id).first():
#             raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f"post with id: {new_comment.post_id} was not found")
#         if not new_comment.content != "":
#             raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY,detail= f"the content of comment have contains context")
#         db.add(new_comment)
#         db.commit()
#         db.refresh(new_comment)
#         return new_comment