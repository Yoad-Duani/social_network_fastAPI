from re import DEBUG
from tokenize import group
from sqlalchemy.sql.functions import current_user, user
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
@router.get("/", response_model= List[schemas.GroupsResponse])
def get_groups(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user),
limit: Optional[int] = 10, search: Optional[str] = ""):
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
        new_object_v.append({"groups_id": object.Groups.groups_id, "creator_id":object.Groups.creator_id, "name": object.Groups.name, "group_private":object.Groups.group_private, "created_at": object.Groups.created_at, "update_at": object.Groups.update_at, "members":object.members, "description": object.Groups.description})
    return new_object_v



@router.get("/{groups_id}")
def get_group(groups_id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    group = db.query(models.Groups, func.count(models.UserInGroups.groups_id).label("members")).join(models.UserInGroups, models.UserInGroups.groups_id == models.Groups.groups_id,isouter=True).group_by(models.Groups.groups_id).filter(models.Groups.groups_id == groups_id).first()
    if not group:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f"group with id: {groups_id} was not found")
    new_group = new_group_object_for_get(group)
    return new_group

def new_group_object_for_get(object):
    new_object_v = ({"groups_id": object.Groups.groups_id, "creator_id":object.Groups.creator_id, "name": object.Groups.name, "group_private":object.Groups.group_private, "created_at": object.Groups.created_at, "update_at": object.Groups.update_at, "members":object.members, "description": object.Groups.description})
    return new_object_v



@router.post("/", status_code= status.HTTP_201_CREATED, response_model= schemas.GroupCreateRespone)
def create_group(group: schemas.GroupCreate, db:Session = Depends(get_db),currect_user:int = Depends(oauth2.get_current_user)):
    if not group.name != "" and group.name != None:
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY,detail= f"the name of the group have contains context")
    if not group.description != "" and group.description != None:
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY,detail= f"the description of the group have contains context")
    if not group.group_private != None:
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY,detail= f"the description of the group have contains context")
    new_group = models.Groups(creator_id = currect_user.id,**group.dict())
    try:
        db.add(new_group)
        db.commit()
        db.refresh(new_group)
    except:
        raise HTTPException(status.HTTP_503_SERVICE_UNAVAILABLE, detail= f"An error occurred while creating the group")
    try:
        new_creator_object_group_v = models.UserInGroups(user_id = currect_user.id, groups_id = new_group.groups_id, is_blocked = False)
        db.add(new_creator_object_group_v)
        db.commit()
        db.refresh(new_creator_object_group_v)
    except:
        raise HTTPException(status.HTTP_503_SERVICE_UNAVAILABLE, detail= f"An error occurred while creating the group")
    return new_group
    ## open for issue


# def add_currect_user(group, currect_user):
#     return {"name": group.name, "description": group.description, "group_private": group.group_private, "creator_id": currect_user.id}
#def creator_object_group(currect_user, group_id):
#   return {"user_id": currect_user.id, "groups_id": group_id, "request_accepted": True}





#response_model= schemas.CommentResponse
@router.put("/{group_id}", response_model= schemas.GroupsUpdateResponse)
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
    if object.name != None and object.name != "":
        new_group_object_v["name"] = object.name
    if object.description!= None and object.description != "":
        new_group_object_v["description"] = object.description
    if object.group_private!= None:
        new_group_object_v["group_private"] = object.group_private
    if new_group_object_v != {}:
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
    posts_query = db.query(models.Post).filter(models.Post.group_id == group_id)
    users_in_group_query = db.query(models.UserInGroups).filter(models.UserInGroups.groups_id == group_id)
    try:
        users_in_group_query.delete(synchronize_session= False)
        posts_query.delete(synchronize_session= False)
        group_query.delete(synchronize_session= False)
        db.commit()
    except:
        raise HTTPException(status_code= status.HTTP_503_SERVICE_UNAVAILABLE, detail= f"An error occurred while deleting the group")
    return Response(status_code= status.HTTP_204_NO_CONTENT)


#############################################
#############################################
#############################################


@router.get("/{group_id}/users-in-group",status_code= status.HTTP_200_OK, response_model= List[schemas.UsersInGroupsResponse])
def get_users_in_groups(group_id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    group = db.query(models.Groups).filter(models.Groups.groups_id == group_id).first()
    if not group:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f"group with id: {group_id} does not exist")
    # if not group.creator_id == current_user.id:
    #     raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail= "Not authhorized to perform requested action")
    if group.group_private == True:
        if not db.query(models.UserInGroups).filter(models.UserInGroups.groups_id == group_id).filter(models.UserInGroups.user_id == current_user.id).first():
            raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail= "This group is private")
    users_in_group = db.query(models.UserInGroups).filter(models.UserInGroups.groups_id == group_id).all()
    return users_in_group

@router.get("/{group_id}/user-in-group/{user_id}",status_code= status.HTTP_200_OK, response_model= schemas.UsersInGroupsResponse)
def get_users_in_groups(group_id: int, user_id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    group = db.query(models.Groups).filter(models.Groups.groups_id == group_id).first()
    # if not group.creator_id == current_user.id:
    #     raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail= "Not authhorized to perform requested action")
    if not group:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f"group with id: {group_id} does not exist")
    user_in_group = db.query(models.UserInGroups).filter(models.UserInGroups.groups_id == group_id).filter(models.UserInGroups.user_id == user_id).first()
    if not user_in_group:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f"user with id: {user_id} does not exist")
    if group.group_private == True:
        if not db.query(models.UserInGroups).filter(models.UserInGroups.groups_id == group_id).filter(models.UserInGroups.user_id == current_user.id).first():
            raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail= "This group is private")
    return user_in_group



# @router.get("/{group_id}/user-in-group/{user_id}",status_code= status.HTTP_200_OK, response_model= schemas.UsersInGroupsResponse)
# def get_user_in_group(group_id: int, user_id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
#     group = db.query(models.Groups).filter(models.Groups.groups_id == group_id).first()
#     # if not group.creator_id == current_user.id:
#     #     raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail= "Not authhorized to perform requested action")
#     if not group:
#         raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f"group with id: {group_id} does not exist")
#     user = db.query(models.User).filter(models.User.id == user_id).first()
#     if not user:
#         raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f"user with id: {user_id} does not exist")
#     user_in_group = db.query(models.UserInGroups).filter(models.UserInGroups.groups_id == group_id).first()
#     if not user_in_group:
#         raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f"user with id: {user_id} does not related to group with id: {group.groups_id}")
#     return user_in_group

@router.get("/{group_id}/join-requests",status_code= status.HTTP_200_OK,response_model= List[schemas.JoinRequestGroupResponse])
def get_join_requests(group_id: int, db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    group = db.query(models.Groups).filter(models.Groups.groups_id == group_id).first()
    if not group:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f"group with id: {group_id} does not exist")
    if not group.creator_id == current_user.id:
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail= "Not authhorized to perform requested action")
    join_requests = db.query(models.JoinRequestGroups).filter(models.JoinRequestGroups.groups_id == group_id).all()
    return join_requests




@router.post("/{group_id}/join-request",status_code= status.HTTP_201_CREATED, response_model=schemas.JoinRequestGroupResponse)
def join_request_group(group_id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    if not db.query(models.Groups).filter(models.Groups.groups_id == group_id).first():
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f"group with id: {group_id} was not found")
    if db.query(models.UserInGroups).filter(models.UserInGroups.groups_id == group_id).filter(models.UserInGroups.user_id == current_user.id).first():
        raise HTTPException(status_code= status.HTTP_409_CONFLICT, detail=f"the user is already member it this group")
    if db.query(models.JoinRequestGroups).filter(models.JoinRequestGroups.user_id == current_user.id).filter(models.JoinRequestGroups.groups_id == group_id).first():
        raise HTTPException(status_code= status.HTTP_409_CONFLICT, detail= f"the user is alredy sent request join to this group")
    join_request = join_request_helper(group_id,current_user.id, current_user.name)
    new_request = models.JoinRequestGroups(**join_request)
    try:
        db.add(new_request)
        db.commit()
        db.refresh(new_request)
    except:
        raise HTTPException(status_code= status.HTTP_503_SERVICE_UNAVAILABLE, detail= f"An error occurred send join request group")
    return new_request

def join_request_helper(group_id,user_id,name):
    return {"user_id": user_id, "groups_id": group_id, "name":name}





@router.put("/{group_id}/management-user/{user_id}/approve-join-request",status_code= status.HTTP_201_CREATED, response_model=schemas.UsersInGroupsResponse)
def Approve_join_request(group_id: int, user_id:int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    if not db.query(models.Groups).filter(models.Groups.groups_id == group_id).first():
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f"group with id: {group_id} not exist")
    if not db.query(models.User).filter(models.User.id == user_id).first():
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f"user with id: {user_id} not exist")
    if not db.query(models.Groups).filter(models.Groups.groups_id == group_id).filter(models.Groups.creator_id == current_user.id).first():
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail= f"Not authhorized to perform requested action")
    join_request_query = db.query(models.JoinRequestGroups).filter(models.JoinRequestGroups.groups_id == group_id).filter(models.JoinRequestGroups.user_id == user_id)
    if not join_request_query.first():
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f"user with id: {user_id} not asked to join to this group")
    new_usr_in_group = models.UserInGroups(user_id = user_id, groups_id = group_id)
    try:
        db.add(new_usr_in_group)
        join_request_query.delete(synchronize_session= False)
        db.commit()
        db.refresh(new_usr_in_group)
    except:
        raise HTTPException(status.HTTP_503_SERVICE_UNAVAILABLE, detail= f"An error occurred while approve the join_request")
    return new_usr_in_group



@router.put("/{group_id}/management-user/replace-manager", response_model=schemas.GroupsUpdateResponse)
def replace_manager(group_id: int, new_manager: schemas.ReplaceManager, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    group_query = db.query(models.Groups).filter(models.Groups.groups_id == group_id)
    group = group_query.first()
    if not group:
        raise HTTPException(status.HTTP_404_NOT_FOUND,detail= f"Group with id: {group_id} was not found")
    user_query = db.query(models.User).filter(models.User.id == new_manager.new_manager_id)
    user = user_query.first()
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND,detail= f"User with id: {new_manager.new_manager_id} was not found")
    if not group.creator_id == current_user.id:
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail= f"Not authhorized to perform requested action")
    if user.verified == False or user.is_blocked == True:
        raise HTTPException(status.HTTP_406_NOT_ACCEPTABLE, detail= f"the user have to be verified and not block")
    user_in_group = db.query(models.UserInGroups).filter(models.UserInGroups.groups_id == group_id).filter(models.UserInGroups.user_id == new_manager.new_manager_id).first()
    if not user_in_group:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f"the user must be a member in this group")
    if user_in_group.is_blocked == True:
        raise HTTPException(status.HTTP_406_NOT_ACCEPTABLE, detail= f"the user has blocked from this group")
    try:
        group_query.update({"creator_id": new_manager.new_manager_id})
        db.commit
    except:
        raise HTTPException(status.HTTP_503_SERVICE_UNAVAILABLE, detail= f"An error occurred while approve the join_request")
    return group_query.first()



@router.delete("{group_id}/management-user/{user_id}",status_code= status.HTTP_204_NO_CONTENT)
def delete_user_from_group(group_id: int, user_id:int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    if not db.query(models.Groups).filter(models.Groups.creator_id == current_user.id).first:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail= f"Not authhorized to perform requested action")
    if not current_user.id == user_id:
        raise HTTPException(status.HTTP_405_METHOD_NOT_ALLOWED, detail= f"You cant remove yourself from the group before you change manager")
    userInGroup_query = db.query(models.UserInGroups).filter(models.UserInGroups.user_id == user_id)
    if not userInGroup_query.first():
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f"user with id: {user_id} does not exist")
    try:
        userInGroup_query.delete(synchronize_session= False)
        db.commit()
    except:
        raise HTTPException(status.HTTP_503_SERVICE_UNAVAILABLE, detail= f"An error occurred while approve the join_request")
    return Response(status_code= status.HTTP_204_NO_CONTENT)


@router.delete("{group_id}/leave-group", status_code= status.HTTP_204_NO_CONTENT)
def leave_group(group_id: int, db: Session = Depends(get_db), current_user:int = Depends(oauth2.get_current_user)):
    query_userInGroup = db.query(models.UserInGroups).filter(models.UserInGroups.user_id == current_user.id).filter(models.UserInGroups.groups_id == group_id)
    if not query_userInGroup.first():
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail= f"you are not memeber in group with id: {group_id}")
    current_group = db.query(models.Groups).filter(models.Groups.groups_id == group_id).first()
    if current_user.id == current_group.creator_id:
        raise HTTPException(status.HTTP_405_METHOD_NOT_ALLOWED, detail= f"you cant leave the group while you manage the group")
    query_userInGroup.delete(synchronize_session= False)
    db.commit()
    return Response(status_code= status.HTTP_204_NO_CONTENT )


#respone models
@router.get("{group_id}/posts")
def get_posts_by_group(group_id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user),
limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes"), func.count(models.Comment.post_id).label("comments")).join(models.Vote, models.Vote.post_id == models.Post.id,
        isouter=True).join(models.Comment,models.Comment.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.group_id == group_id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    return  posts







#
# need to check before posts if there is a id for group
# need to delete all posts in the group before delete group
#