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



#response_model= schemas.CommentResponse
@router.put("/{group_id}",)
def update_groups(group_id: int, update_group: schemas.GroupUpdate,db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    new_object = new_group_object(update_group)
    group_query = db.query(models.Groups).filter(models.Groups.groups_id == group_id)
    group = group_query.first()
    if group == None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f"group with id: {group_id} does not exist")
    if group.creator_id != current_user.id:
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail= f"Not authhorized to perform requested action")
    group_query.update(new_object, synchronize_session= False)
    db.commit()
    return group_query.first()

def new_group_object(object):
    new_group_object_v = {}
    if object.name != None and  object.name != "":
        new_group_object_v["name"] = object.name
    if object.description!= None and object.description != "":
        new_group_object_v["description"] = object.description
    if object.group_private!= None:
        new_group_object_v["group_private"] = object.group_private
    new_group_object_v["update_at"] = "now()"
    return new_group_object_v
    # return {"name": object.name, "description": object.description, "group_private": object.group_private, "update_at": "now()"}

    #
    #


# @router.put("/{comment_id}",response_model= schemas.CommentResponse)
# def update_comment(comment_id: int, update_comment: schemas.CommentUpdate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
#     new_object = new_comment_object(update_comment)
#     comment_query = db.query(models.Comment).filter(models.Comment.comment_id == comment_id)
#     comment = comment_query.first()
#     if comment == None:
#         raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f"comment with id: {comment_id} does not exist")
#     if comment.user_id != current_user.id:
#         raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail= f"Not authhorized to perform requested action")
#     comment_query.update(new_object, synchronize_session=False)
#     db.commit()
#     return comment_query.first()

# #create a new key with datetime to update the curect time of the update
# def new_comment_object(object):
#     return {"content": object.content, "update_at": "now()"}
     
