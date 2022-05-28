from app import schemas
import pytest
from typing import List



####  Test get Groups  ####

def test_get_all_groups_authorized_client(authorized_client, test_posts, test_comments, test_groups, test_users_in_groups):
    res = authorized_client.get("/groups")
    assert res.status_code == 200
    assert len(res.json()) == len(test_groups)

def test_get_all_groups_unauthorized_client(client, test_posts, test_comments, test_groups, test_users_in_groups):
    res = client.get("/groups")
    assert res.status_code == 401
    
def test_get_one_group_authorized_client(authorized_client, test_posts, test_comments, test_groups, test_users_in_groups,test_user):
    res = authorized_client.get(f"/groups/{test_groups[0].groups_id}")
    group = schemas.GroupsResponse(**res.json())
    assert res.status_code == 200
    assert group.creator_id == test_user["id"]
    assert group.name == test_groups[0].name

def test_get_one_group_authorized_client_second_test(authorized_client, test_posts, test_comments, test_groups, test_users_in_groups,test_user,test_user_second):
    res = authorized_client.get(f"/groups/{test_groups[1].groups_id}")
    group = schemas.GroupsResponse(**res.json())
    assert res.status_code == 200
    assert group.creator_id == test_user_second["id"]
    assert group.name == test_groups[1].name

def test_get_one_group_unauthorized_client(client, test_posts, test_comments, test_groups, test_users_in_groups,test_user):
    res = client.get(f"/groups/{test_groups[0].groups_id}")
    assert res.status_code == 401

def test_get_one_group_authorized_client_non_exsit_group(authorized_client, test_posts, test_comments, test_groups, test_users_in_groups,test_user):
    res = authorized_client.get(f"/groups/88888")
    assert res.status_code == 404
    
def test_get_one_group_unauthorized_client_non_exsit_group(client, test_posts, test_comments, test_groups, test_users_in_groups,test_user):
    res = client.get(f"/groups/88888")
    assert res.status_code == 401



###  Test get users_in_group  ####

def test_get_all_users_in_group_authorized_client_owner_group(authorized_client, test_posts, test_comments, test_groups, test_users_in_groups,test_user):
    res = authorized_client.get(f"/groups/{test_groups[0].groups_id}/users-in-group")
    assert res.status_code == 200
    assert len(res.json()) == 5  # return only the rows with the same group_id

def test_get_all_users_in_group_unauthorized_client(client, test_posts, test_comments, test_groups, test_users_in_groups,test_user):
    res = client.get(f"/groups/{test_groups[0].groups_id}/users-in-group")
    assert res.status_code == 401

def test_get_all_users_in_group_authorized_client_not_owner_group(authorized_client_second, test_posts, test_comments, test_groups, test_users_in_groups,test_user):
    res = authorized_client_second.get(f"/groups/{test_groups[0].groups_id}/users-in-group")
    assert res.status_code == 200

def test_get_all_users_in_group_privte_group_not_member(authorized_client, test_posts, test_comments, test_groups, test_users_in_groups,test_user):
    res = authorized_client.get(f"/groups/{test_groups[2].groups_id}/users-in-group")
    assert res.status_code == 403

def test_get_all_users_in_group_privte_group(authorized_client_second, test_posts, test_comments, test_groups, test_users_in_groups,test_user):
    res = authorized_client_second.get(f"/groups/{test_groups[2].groups_id}/users-in-group")
    assert res.status_code == 200

def test_get_all_users_in_group_authorized_client_non_exsit_group(authorized_client, test_posts, test_comments, test_groups, test_users_in_groups,test_user):
    res = authorized_client.get(f"/groups/88888/users-in-group")
    assert res.status_code == 404

def test_get_user_in_group_by_id_authorized_client(authorized_client, test_posts, test_comments, test_groups, test_users_in_groups,test_user):
    res = authorized_client.get(f"groups/{test_groups[0].groups_id}/user-in-group/{test_user['id']}")
    assert res.status_code == 200
    user_in_group = schemas.UsersInGroupsResponse(**res.json())
    assert user_in_group.user_id == test_user['id']
    assert user_in_group.groups_id == test_groups[0].groups_id

def test_get_user_in_group_by_id_authorized_client_not_exist_group(authorized_client, test_posts, test_comments, test_groups, test_users_in_groups,test_user):
    res = authorized_client.get(f"groups/88888/user-in-group/{test_user['id']}")
    assert res.status_code == 404

def test_get_user_in_group_by_id_authorized_client_not_exist_user(authorized_client, test_posts, test_comments, test_groups, test_users_in_groups,test_user):
    res = authorized_client.get(f"groups/{test_groups[0].groups_id}/user-in-group/88888")
    assert res.status_code == 404

def test_get_user_in_group_by_id_authorized_client_privte_not_member(authorized_client, test_posts, test_comments, test_groups, test_users_in_groups,test_user,test_user_second):
    res = authorized_client.get(f"groups/{test_groups[2].groups_id}/user-in-group/{test_user_second['id']}")
    assert res.status_code == 403

def test_get_user_in_group_by_id_authorized_client_privte_member(authorized_client_second, test_posts, test_comments, test_groups, test_users_in_groups,test_user,test_user_second):
    res = authorized_client_second.get(f"groups/{test_groups[2].groups_id}/user-in-group/{test_user_second['id']}")
    assert res.status_code == 200

def test_get_user_in_group_by_id_unauthorized_client(client, test_posts, test_comments, test_groups, test_users_in_groups,test_user):
    res = client.get(f"groups/{test_groups[0].groups_id}/user-in-group/{test_user['id']}")
    assert res.status_code == 401



###  Test get join requests to group ####

def test_get_all_requests_join_group_authorized_client_owner_group(authorized_client, test_posts, test_comments, test_groups, test_users_in_groups,test_user):
    res = authorized_client.get(f"/groups/{test_groups[0].groups_id}/join-requests")
    assert res.status_code == 200
    assert len(res.json()) == 0

def test_get_all_requests_join_group_authorized_client_non_exist_group(authorized_client, test_posts, test_comments, test_groups, test_users_in_groups,test_user):
    res = authorized_client.get(f"/groups/888888/join-requests")
    assert res.status_code == 404

def test_get_all_requests_join_group_unauthorized_client(client, test_posts, test_comments, test_groups, test_users_in_groups,test_user):
    res = client.get(f"/groups/{test_groups[0].groups_id}/join-requests")
    assert res.status_code == 401

def test_get_all_requests_join_group_authorized_client_non_owner_group(authorized_client_second, test_posts, test_comments, test_groups, test_users_in_groups,test_user):
    res = authorized_client_second.get(f"/groups/{test_groups[0].groups_id}/join-requests")
    assert res.status_code == 403



####  Test Create Groups  ####

@pytest.mark.parametrize("name, description, group_private, status_code",[
    ("new group 1", "new group description 1", False, 201),
    ("new group 2", None, False, 422),
    (None, "new group description 3", True, 422),
    ("new group  4", "new group description 3", None, 422),
    ("", "new group description 3", False, 422),
    ("new group  4", "", False, 422),
])
def test_create_group_authorized_client(authorized_client, test_posts, test_comments, test_groups, test_users_in_groups,test_user,name,description,group_private, status_code):
    res = authorized_client.post("/groups/", json = {"name": name, "description":description, "group_private":group_private})
    assert res.status_code == status_code
    if status_code == 201: 
        created_group = schemas.GroupCreateRespone(**res.json())
        assert created_group.name == name
        res_user_in_group = authorized_client.get(f"/groups/{created_group.groups_id}/user-in-group/{test_user['id']}")
        assert res_user_in_group.status_code == 200
        created_user_in_group = schemas.UsersInGroupsResponse(**res_user_in_group.json())
        assert created_user_in_group.user_id == test_user["id"]

def test_create_group_unauthorized_client(client, test_posts, test_comments, test_groups, test_users_in_groups,test_user):
    data = {
        "name": "new group 1",
        "description": "new group description 1",
        "group_private": False
    }
    res = client.post("/groups/",json = data)
    assert res.status_code == 401

def test_create_group_unauthorized_client_non_content(client, test_posts, test_comments, test_groups, test_users_in_groups,test_user):
    res = client.post("/groups/",json = None)
    assert res.status_code == 401



####  Test Update Groups  ####

@pytest.mark.parametrize("name, description, group_private, status_code",[
    ('new name', "new description", True, 200),
    (None, "new description", True, 200),
    ('new name', None, True, 200),
    ('new name', "new description", None, 200),
    (None, None, None, 422),
])
def test_update_group_authorized_client_owner_group(authorized_client, test_posts, test_comments, test_groups, test_users_in_groups, test_user, name, description, group_private, status_code):
    data = {"name": name, "description": description, "group_private": group_private}
    res = authorized_client.put(f"/groups/{test_groups[0].groups_id}", json = data)
    assert res.status_code == status_code

def test_update_group_authorized_client_owner_group_second_test(authorized_client, test_posts, test_comments, test_groups, test_users_in_groups, test_user):
    data = {"name": "new name", "description": "new description", "group_private": True}
    res = authorized_client.put(f"/groups/{test_groups[0].groups_id}", json = data)
    assert res.status_code == 200
    updated_group = schemas.GroupsUpdateResponse(**res.json())
    assert updated_group.name == "new name"
    assert updated_group.description == "new description"
    assert updated_group.group_private == True
    assert updated_group.creator_id == test_user["id"]

def test_update_group_unauthorized_client(client, test_posts, test_comments, test_groups, test_users_in_groups, test_user):
    data = {"name": "new name", "description": "new description", "group_private": True}
    res = client.put(f"/groups/{test_groups[0].groups_id}", json = data)
    assert res.status_code == 401

def test_update_group_authorized_client_not_exist_group(authorized_client, test_posts, test_comments, test_groups, test_users_in_groups, test_user):
    data = {"name": "new name", "description": "new description", "group_private": True}
    res = authorized_client.put(f"/groups/88888", json = data)
    assert res.status_code == 404

def test_update_group_authorized_client_not_owner_group(authorized_client, test_posts, test_comments, test_groups, test_users_in_groups, test_user):
    data = {"name": "new name", "description": "new description", "group_private": True}
    res = authorized_client.put(f"/groups/{test_groups[2].groups_id}", json = data)
    assert res.status_code == 403



####  Test Delete Groups  ####

def test_authorized_user_delete_group_owner(authorized_client, test_posts, test_comments, test_groups, test_users_in_groups, test_user):
    post_id = test_posts[3].id
    res_group = authorized_client.get(f"/groups/{test_groups[0].groups_id}")
    assert res_group.status_code == 200
    res_users_in_group = authorized_client.get(f"/groups/{test_groups[0].groups_id}/users-in-group")
    assert res_users_in_group.status_code == 200
    res_posts = authorized_client.get(f"/group/{test_groups[0].groups_id}/posts")
    assert res_posts.status_code == 200
    res_comments = authorized_client.get(f"/posts/{post_id}/comments")
    assert res_comments.status_code == 200
    res_delete = authorized_client.delete(f"/groups/{test_groups[0].groups_id}")
    assert res_delete.status_code == 204
    res_group = authorized_client.get(f"/groups/{test_groups[0].groups_id}")
    assert res_group.status_code == 404
    res_users_in_group = authorized_client.get(f"/groups/{test_groups[0].groups_id}/users-in-group")
    assert res_users_in_group.status_code == 404
    res_posts = authorized_client.get(f"/group/{test_groups[0].groups_id}/posts")
    assert res_posts.status_code == 404
    res_comments = authorized_client.get(f"/posts/{post_id}/comments")
    assert res_comments.status_code == 404

def test_authorized_user_delete_group_not_owner(authorized_client, test_posts, test_comments, test_groups, test_users_in_groups, test_user):
    res = authorized_client.delete(f"/groups/{test_groups[2].groups_id}")
    assert res.status_code == 403

def test_authorized_user_delete_group_not_exist_group(authorized_client, test_posts, test_comments, test_groups, test_users_in_groups, test_user):
    res = authorized_client.delete(f"/groups/88888")
    assert res.status_code == 404

def test_unauthorized_user_delete_group(client, test_posts, test_comments, test_groups, test_users_in_groups, test_user):
    res = client.delete(f"/groups/{test_groups[2].groups_id}")
    assert res.status_code == 401



####  Test Get Join Requests  #### 

def test_get_join_requests_authorized_client_owner_group(authorized_client,test_groups,test_join_requests, test_posts, test_comments, test_user_second, test_users_in_groups):
    res = authorized_client.get(f"/groups/{test_groups[0].groups_id}/join-requests")
    assert res.status_code == 200
    join_request = res.json()
    assert join_request[0]['user_id'] == test_user_second['id']
    
def test_get_join_requests_authorized_client_not_owner_group(authorized_client,test_groups,test_join_requests, test_posts, test_comments, test_user_second, test_users_in_groups):
    res = authorized_client.get(f"/groups/{test_groups[1].groups_id}/join-requests")
    assert res.status_code == 403

def test_get_join_requests_authorized_client_not_exist_group(authorized_client,test_groups,test_join_requests, test_posts, test_comments, test_user_second, test_users_in_groups):
    res = authorized_client.get(f"/groups/88888/join-requests")
    assert res.status_code == 404

def test_get_join_requests_unauthorized_client(client,test_groups,test_join_requests, test_posts, test_comments, test_user_second, test_users_in_groups):
    res = client.get(f"/groups/{test_groups[0].groups_id}/join-requests")
    assert res.status_code == 401



####  Test Send Join Requests  ####

def test_send_join_requests_authorized_client(authorized_client,test_groups,test_join_requests, test_posts, test_comments, test_user_second,test_user,test_users_in_groups):
    group_id = test_groups[1].groups_id
    res = authorized_client.post(f"/groups/{group_id}/join-request")
    assert res.status_code == 201
    join_request = schemas.JoinRequestGroupResponse(**res.json())
    assert join_request.groups_id == group_id
    assert join_request.user_id == test_user['id']

def test_send_join_requests_authorized_client_owner_group(authorized_client,test_groups,test_join_requests, test_posts, test_comments, test_user_second,test_user,test_users_in_groups):
    res = authorized_client.post(f"/groups/{test_groups[0].groups_id}/join-request")
    assert res.status_code == 409

def test_send_join_requests_authorized_client_alredy_sent(authorized_client_second,test_groups,test_join_requests, test_posts, test_comments, test_user_second,test_user,test_users_in_groups):
    res = authorized_client_second.post(f"/groups/{test_groups[0].groups_id}/join-request")
    assert res.status_code == 409

def test_send_join_requests_authorized_client_not_exist_group(authorized_client,test_groups,test_join_requests, test_posts, test_comments, test_user_second,test_user,test_users_in_groups):
    res = authorized_client.post(f"/groups/88888/join-request")
    assert res.status_code == 404

def test_send_join_requests_unauthorized_client(client,test_groups,test_join_requests, test_posts, test_comments, test_user_second,test_user,test_users_in_groups):
    res = client.post(f"/groups/{test_groups[0].groups_id}/join-request")
    assert res.status_code == 401



####  Test Approve Join Request  ####

def test_approve_join_request_authorized_client_owner_group(authorized_client,test_groups,test_join_requests, test_posts, test_comments, test_user_second,test_user,test_users_in_groups):
    group_id = test_groups[0].groups_id
    res = authorized_client.put(f"/groups/{group_id}/management-user/{test_user_second['id']}/approve-join-request")
    assert res.status_code == 201
    new_member = schemas.UsersInGroupsResponse(**res.json())
    assert new_member.groups_id == group_id
    assert new_member.user_id == test_user_second['id']
    res_join_request = authorized_client.get(f"/groups/{group_id}/join-requests")
    assert res_join_request.status_code == 200
    join_request = res_join_request.json()
    assert join_request == []  # check that request deleted from the list

def test_approve_join_request_authorized_client_not_exist_group(authorized_client,test_groups,test_join_requests, test_posts, test_comments, test_user_second,test_user,test_users_in_groups):
    res = authorized_client.put(f"/groups/88888/management-user/{test_user_second['id']}/approve-join-request")
    assert res.status_code == 404

def test_approve_join_request_authorized_client_not_exist_user(authorized_client,test_groups,test_join_requests, test_posts, test_comments, test_user_second,test_user,test_users_in_groups):
    res = authorized_client.put(f"/groups/{test_groups[0].groups_id}/management-user/888888/approve-join-request")
    assert res.status_code == 404

def test_approve_join_request_authorized_client_not_owner_group(authorized_client_second,test_groups,test_join_requests, test_posts, test_comments, test_user_second,test_user,test_users_in_groups):
    res = authorized_client_second.put(f"/groups/{test_groups[0].groups_id}/management-user/{test_user_second['id']}/approve-join-request")
    assert res.status_code == 403

def test_approve_join_request_authorized_client_owner_group_not_request(authorized_client,test_groups,test_join_requests, test_posts, test_comments,test_user_third,test_users_in_groups):
    res = authorized_client.put(f"/groups/{test_groups[0].groups_id}/management-user/{test_user_third['id']}/approve-join-request")
    assert res.status_code == 404

def test_approve_join_request_unauthorized_client(client,test_groups,test_join_requests, test_posts, test_comments, test_user_second,test_user,test_users_in_groups):
    res = client.put(f"/groups/{test_groups[0].groups_id}/management-user/{test_user_second['id']}/approve-join-request")
    assert res.status_code == 401



####  Test Replace Manager  ####

def test_replace_manager_authorized_client_owner_group(authorized_client,test_groups,test_join_requests, test_posts, test_comments, test_user_second,test_user,test_user_4,test_users_in_groups):
    res = authorized_client.put(f"/groups/{test_groups[0].groups_id}/management-user/replace-manager", json = {"new_manager_id":test_user_4.id})
    assert res.status_code == 200

def test_replace_manager_unauthorized_client(client,test_groups,test_join_requests, test_posts, test_comments, test_user_second,test_user,test_user_4,test_users_in_groups):
    res = client.put(f"/groups/{test_groups[0].groups_id}/management-user/replace-manager", json = {"new_manager_id":test_user_4.id})
    assert res.status_code == 401

def test_replace_manager_authorized_client_not_exist_group(authorized_client,test_groups,test_join_requests, test_posts, test_comments, test_user_second,test_user,test_user_4,test_users_in_groups):
    res = authorized_client.put(f"/groups/88888/management-user/replace-manager", json = {"new_manager_id":test_user_4.id})
    assert res.status_code == 404

def test_replace_manager_authorized_client_not_exist_user(authorized_client,test_groups,test_join_requests, test_posts, test_comments, test_user_second,test_user,test_user_4,test_users_in_groups):
    res = authorized_client.put(f"/groups/{test_groups[0].groups_id}/management-user/replace-manager", json = {"new_manager_id":88888})
    assert res.status_code == 404

def test_replace_manager_authorized_client_not_owner_group(authorized_client,test_groups,test_join_requests, test_posts, test_comments, test_user_second,test_user,test_user_4,test_users_in_groups):
    res = authorized_client.put(f"/groups/{test_groups[1].groups_id}/management-user/replace-manager", json = {"new_manager_id":test_user_4.id})
    assert res.status_code == 403

def test_replace_manager_authorized_client_not_verified(authorized_client,test_groups,test_join_requests, test_posts, test_comments, test_user_second,test_user,test_user_4,test_users_in_groups,test_user_third):
    res = authorized_client.put(f"/groups/{test_groups[0].groups_id}/management-user/replace-manager", json = {"new_manager_id":test_user_third['id']})
    assert res.status_code == 406

def test_replace_manager_authorized_client_user_is_block(authorized_client,test_groups,test_join_requests, test_posts, test_comments, test_user_second,test_user,test_user_4,test_users_in_groups,test_user_5):
    res = authorized_client.put(f"/groups/{test_groups[0].groups_id}/management-user/replace-manager", json = {"new_manager_id":test_user_5.id})
    assert res.status_code == 406

def test_replace_manager_authorized_client_user_not_member_in_group(authorized_client,test_groups,test_join_requests, test_posts, test_comments, test_user_second,test_user,test_user_4,test_user_6,test_users_in_groups):
    res = authorized_client.put(f"/groups/{test_groups[0].groups_id}/management-user/replace-manager", json = {"new_manager_id":test_user_6.id})
    assert res.status_code == 404

def test_replace_manager_authorized_client_owner_group(authorized_client,test_groups,test_join_requests, test_posts, test_comments, test_user_second,test_user,test_user_7,test_users_in_groups):
    res = authorized_client.put(f"/groups/{test_groups[0].groups_id}/management-user/replace-manager", json = {"new_manager_id":test_user_7.id})
    assert res.status_code == 406



####  Test Remove User From Group  ####

def test_remove_user_from_group_authorized_client_owner_group(authorized_client,test_groups,test_join_requests, test_posts, test_comments, test_user_second,test_user,test_user_third,test_users_in_groups):
    group_id = test_groups[0].groups_id
    res = authorized_client.delete(f"/groups/{group_id}/management-user/delete-user/{test_user_third['id']}")
    assert res.status_code == 204
    res_user_group = authorized_client.get(f"/groups/{group_id}/user-in-group/{test_user_third['id']}")
    assert res_user_group.status_code == 404
    assert res_user_group.json()['detail'] == f"user with id: {test_user_third['id']} does not exist"

def test_remove_user_from_group_authorized_client_group_not_exist(authorized_client,test_groups,test_join_requests, test_posts, test_comments, test_user_second,test_user,test_user_third,test_users_in_groups):
    res = authorized_client.delete(f"/groups/88888/management-user/delete-user/{test_user_third['id']}")
    assert res.status_code == 404

def test_remove_user_from_group_authorized_client_user_not_exist(authorized_client,test_groups,test_join_requests, test_posts, test_comments, test_user_second,test_user,test_user_third,test_users_in_groups):
    res = authorized_client.delete(f"/groups/{test_groups[0].groups_id}/management-user/delete-user/88888")
    assert res.status_code == 404

def test_remove_user_from_group_authorized_client_not_owner_group(authorized_client_second,test_groups,test_join_requests, test_posts, test_comments, test_user_second,test_user,test_user_third,test_users_in_groups):
    res = authorized_client_second.delete(f"/groups/{test_groups[0].groups_id}/management-user/delete-user/{test_user_third['id']}")
    assert res.status_code == 403

def test_remove_user_from_group_authorized_client_owner_group_remove_manager(authorized_client,test_groups,test_join_requests, test_posts, test_comments, test_user_second,test_user,test_user_third,test_users_in_groups):
    res = authorized_client.delete(f"/groups/{test_groups[0].groups_id}/management-user/delete-user/{test_user['id']}")
    assert res.status_code == 403

def test_remove_user_from_group_authorized_client_owner_group_remove_manager(authorized_client,test_groups,test_join_requests, test_posts, test_comments, test_user_second,test_user,test_user_third,test_users_in_groups):
    res = authorized_client.delete(f"/groups/{test_groups[0].groups_id}/management-user/delete-user/{test_user_second['id']}")
    assert res.status_code == 404

def test_remove_user_from_group_unauthorized_client_owner_group(client,test_groups,test_join_requests, test_posts, test_comments, test_user_second,test_user,test_user_third,test_users_in_groups):
    res = client.delete(f"/groups/{test_groups[0].groups_id}/management-user/delete-user/{test_user_third['id']}")
    assert res.status_code == 401



####  Test Leave Group  ####

def test_leave_group_authorized_client_member_in_group(authorized_client_third,test_groups,test_users_in_groups,test_join_requests, test_posts, test_comments, test_user_second,test_user,test_user_third):
    res_members_in_group = authorized_client_third.get(f"/groups/{test_groups[0].groups_id}/users-in-group")
    assert len(res_members_in_group.json()) == 5 ## the numbers of memeber in conftest.py
    group_id = test_groups[0].groups_id
    res = authorized_client_third.delete(f"/groups/{group_id}/leave-group")
    assert res.status_code == 204
    res_members_in_group = authorized_client_third.get(f"/groups/{test_groups[0].groups_id}/users-in-group")
    assert len(res_members_in_group.json()) == 4

def test_leave_group_authorized_client_not_exist_group(authorized_client_third,test_groups,test_users_in_groups,test_join_requests, test_posts, test_comments, test_user_second,test_user,test_user_third):
    res = authorized_client_third.delete(f"/groups/88888/leave-group")
    assert res.status_code == 404

def test_leave_group_authorized_client_not_member_in_group(authorized_client_third,test_groups,test_users_in_groups,test_join_requests, test_posts, test_comments, test_user_second,test_user,test_user_third):
    res = authorized_client_third.delete(f"/groups/{test_groups[1].groups_id}/leave-group")
    assert res.status_code == 404

def test_leave_group_authorized_client_manager_of_group(authorized_client,test_groups,test_users_in_groups,test_join_requests, test_posts, test_comments, test_user_second,test_user,test_user_third):
    res = authorized_client.delete(f"/groups/{test_groups[0].groups_id}/leave-group")
    assert res.status_code == 403

def test_leave_group_unauthorized_client(client,test_groups,test_users_in_groups,test_join_requests, test_posts, test_comments, test_user_second,test_user,test_user_third):
    res = client.delete(f"/groups/{test_groups[0].groups_id}/leave-group")
    assert res.status_code == 401