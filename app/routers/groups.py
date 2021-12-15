from sqlalchemy.sql.functions import current_user
from .. import models,schemas,oauth2
from fastapi import FastAPI , Response ,status , HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import get_db
from sqlalchemy.sql.expression import join, null, true, update
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
    new_group = new_group_object_for_get(group)
    return new_group

def new_group_object_for_get(object):
    new_object_v = ({"groups_id": object.Groups.creator_id, "name": object.Groups.name, "group_private":object.Groups.group_private, "created_at": object.Groups.created_at, "update_at": object.Groups.update_at, "members":object.members, "description": object.Groups.description})
    return new_object_v



@router.post("/", status_code= status.HTTP_201_CREATED, response_model= schemas.GroupCreateRespone)
def create_group(group: schemas.GroupCreate, db:Session = Depends(get_db),currect_user:int = Depends(oauth2.get_current_user)):
    if not group.name != "":
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY,detail= f"the name of the group have contains context")
    if not group.description != "":
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY,detail= f"the description of the group have contains context")
    new_group = models.Groups(creator_id = currect_user.id,**group.dict())
    db.add(new_group)
    db.commit()
    db.refresh(new_group)
    new_creator_object_group_v = models.UserInGroups(user_id = currect_user.id, groups_id = new_group.groups_id, request_accepted = True)
    db.add(new_creator_object_group_v)
    db.commit()
    db.refresh(new_creator_object_group_v)
    return new_group

# def add_currect_user(group, currect_user):
#     return {"name": group.name, "description": group.description, "group_private": group.group_private, "creator_id": currect_user.id}
#def creator_object_group(currect_user, group_id):
#   return {"user_id": currect_user.id, "groups_id": group_id, "request_accepted": True}





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
    if new_group_object_v != None:
        new_group_object_v["update_at"] = "now()"
        return new_group_object_v
    raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY,detail= f"you didnt update any field")
    # return {"name": object.name, "description": object.description, "group_private": object.group_private, "update_at": "now()"}






#
@router.delete("/{group_id}",status_code= status.HTTP_204_NO_CONTENT)
def delete_group(group_id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    group_query = db.query(models.Groups).filter(models.Groups.groups_id == group_id)
    group = group_query.first()
    if group == None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f"group with id: {group_id} does not exist")
    if group.creator_id != current_user.id:
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail= f"Not authhorized to perform requested action")
    group_query.delete(synchronize_session= False)
    db.commit()
    return Response(status_code= status.HTTP_204_NO_CONTENT)


#####
@router.post("/{group_id}/JoinRequest",status_code= status.HTTP_201_CREATED)
def join_request_group(group_id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    if not db.query(models.Groups).filter(models.Groups.groups_id == group_id).first():
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f"group with id: {group_id} was not found")
    if db.query(models.UserInGroups).filter(models.UserInGroups.user_id == current_user.id).filter(models.UserInGroups.groups_id == group_id).first():
                raise HTTPException(status_code= status.HTTP_409_CONFLICT, detail= f"the user is alredy sent request join to this group")
    join_request = join_request_helper(group_id,current_user.id)
    new_request = models.UserInGroups(**join_request)
    db.add(new_request)
    db.commit()
    db.refresh(new_request)
    return new_request

def join_request_helper(group_id,user_id):
    return {"user_id": user_id, "groups_id": group_id}



@router.put("/{group_id}/management-user/{user_id}")
def Approve_or_block(group_id: int, user_id:int,  updatedStatus: schemas.UsersInGroupsUpdate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    if not db.query(models.Groups).filter(models.Groups.groups_id == group_id).filter(models.Groups.creator_id == current_user.id).first():
        raise HTTPException(status_code= status.HTTP_401_UNAUTHORIZED, detail= f"Not authhorized to perform requested action")
    if not db.query(models.Groups).filter(models.Groups.groups_id == group_id).first():
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f"group with id: {group_id} not found")
    userInGroup_query = db.query(models.UserInGroups).filter(models.UserInGroups.user_id == user_id).filter(models.UserInGroups.groups_id == group_id)
    userInG = userInGroup_query.first()
    if userInG == None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f"user with id: {current_user.id} not found in this group")
    if(userInG.request_accepted == True and updatedStatus.request_accepted == True):
            raise HTTPException(status_code= status.HTTP_422_UNPROCESSABLE_ENTITY, detail= f"user alredy accepted to the group - you can block him if you want or remove him from the group")
    new_usersInGroups = new_Approve_or_block(updatedStatus)
    userInGroup_query.update(new_usersInGroups, synchronize_session= False)
    db.commit()
    return userInGroup_query.first()

def new_Approve_or_block(updatedStatus):
    new_UsersInGroups_object = {}
    if updatedStatus.is_blocked != None and updatedStatus.is_blocked != "":
        new_UsersInGroups_object["is_blocked"] = updatedStatus.is_blocked
    if updatedStatus.request_accepted != None and updatedStatus.request_accepted != "":
        new_UsersInGroups_object["request_accepted"] = updatedStatus.request_accepted
    # need add colum for update date and membership date
    if new_UsersInGroups_object != None:
        new_UsersInGroups_object["update_at"] = "now()"
        new_UsersInGroups_object["join_group_date"] = "now()"
        return new_UsersInGroups_object
    raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY,detail= f"you didnt update any field")





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