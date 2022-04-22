from app import schemas




####  Test get Groups  ####

# def test_get_all_groups_authorized_client(authorized_client, test_posts, test_comments, test_groups, test_users_in_groups):
#     res = authorized_client.get("/groups")
#     assert res.status_code == 200
#     assert len(res.json()) == len(test_groups)

# def test_get_all_groups_unauthorized_client(client, test_posts, test_comments, test_groups, test_users_in_groups):
#     res = client.get("/groups")
#     assert res.status_code == 401
    
# def test_get_one_group_authorized_client(authorized_client, test_posts, test_comments, test_groups, test_users_in_groups,test_user):
#     res = authorized_client.get(f"/groups/{test_groups[0].groups_id}")
#     group = schemas.GroupsResponse(**res.json())
#     assert res.status_code == 200
#     assert group.creator_id == test_user["id"]
#     assert group.name == test_groups[0].name

# def test_get_one_group_authorized_client_second_test(authorized_client, test_posts, test_comments, test_groups, test_users_in_groups,test_user,test_user_second):
#     res = authorized_client.get(f"/groups/{test_groups[1].groups_id}")
#     group = schemas.GroupsResponse(**res.json())
#     assert res.status_code == 200
#     assert group.creator_id == test_user_second["id"]
#     assert group.name == test_groups[1].name

# def test_get_one_group_unauthorized_client(client, test_posts, test_comments, test_groups, test_users_in_groups,test_user):
#     res = client.get(f"/groups/{test_groups[0].groups_id}")
#     assert res.status_code == 401

# def test_get_one_group_authorized_client_non_exsit_group(authorized_client, test_posts, test_comments, test_groups, test_users_in_groups,test_user):
#     res = authorized_client.get(f"/groups/88888")
#     assert res.status_code == 404
    
# def test_get_one_group_unauthorized_client_non_exsit_group(client, test_posts, test_comments, test_groups, test_users_in_groups,test_user):
#     res = client.get(f"/groups/88888")
#     assert res.status_code == 401



def test_get_all_join_request_group_authorized_client_owner_group(authorized_client, test_posts, test_comments, test_groups, test_users_in_groups,test_user):
    res = authorized_client.get(f"/groups/{test_groups[0].groups_id}/JoinRequest")
    assert res.status_code == 200
    assert len(res.json()) == 1  # return only the rows with the same group_id

def test_get_all_join_request_group_unauthorized_client(client, test_posts, test_comments, test_groups, test_users_in_groups,test_user):
    res = client.get(f"/groups/{test_groups[0].groups_id}/JoinRequest")
    assert res.status_code == 401

def test_get_all_join_request_group_authorized_client_not_owner_group(authorized_client_second, test_posts, test_comments, test_groups, test_users_in_groups,test_user):
    res = authorized_client_second.get(f"/groups/{test_groups[0].groups_id}/JoinRequest")
    assert res.status_code == 403

def test_get_all_join_request_group_authorized_client_non_exsit_group(authorized_client, test_posts, test_comments, test_groups, test_users_in_groups,test_user):
    res = authorized_client.get(f"/groups/88888/JoinRequest")
    assert res.status_code == 404