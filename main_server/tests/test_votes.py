


def test_vote_on_post_authorized_user(authorized_client,test_user,test_posts):
    res = authorized_client.post("/vote/", json = {"post_id":test_posts[0].id, "dir":1})
    assert res.status_code == 201

def test_vote_twice_post_authorized_user(authorized_client,test_user,test_posts, test_vote):
    res = authorized_client.post("/vote/", json = {"post_id":test_posts[0].id, "dir": 1})
    assert res.status_code == 409

def test_remove_vote_authorized_user(authorized_client,test_user,test_posts, test_vote):
    res = authorized_client.post("/vote/", json = {"post_id":test_posts[0].id, "dir": 0})
    assert res.status_code == 201

def test_remove_vote_unauthorized_user(client,test_user,test_posts, test_vote):
    res = client.post("/vote/", json = {"post_id":test_posts[0].id, "dir": 0})
    assert res.status_code == 401

def test_remove_vote_non_exist_vote_authorized_user(authorized_client,test_user,test_posts):
    res = authorized_client.post("/vote/", json = {"post_id":test_posts[0].id, "dir": 0})
    assert res.status_code == 404

def test_vote_non_exist_post_authorized_user(authorized_client,test_user,test_posts):
    res = authorized_client.post("/vote/", json = {"post_id": 88888, "dir": 1})
    assert res.status_code == 404

def test_vote_unauthorized_user(client,test_user,test_posts):
    res = client.post("/vote/", json = {"post_id":test_posts[0].id, "dir": 1})
    assert res.status_code == 401




###  Test Vote Validation  ###

def test_vote_on_post_authorized_user_post_id_0(authorized_client,test_user,test_posts):
    res = authorized_client.post("/vote/", json = {"post_id": 0, "dir":1})
    assert res.status_code == 422

def test_vote_on_post_authorized_user_dir_99(authorized_client,test_user,test_posts):
    res = authorized_client.post("/vote/", json = {"post_id": test_posts[0].id, "dir":99})
    assert res.status_code == 422

def test_vote_on_post_authorized_user_dir_minus_91(authorized_client,test_user,test_posts):
    res = authorized_client.post("/vote/", json = {"post_id":test_posts[0].id, "dir":-91})
    assert res.status_code == 422

def test_vote_on_post_authorized_user_post_id_minus_99(authorized_client,test_user,test_posts):
    res = authorized_client.post("/vote/", json = {"post_id":-99, "dir":1})
    assert res.status_code == 422