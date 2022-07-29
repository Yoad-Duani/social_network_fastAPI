import pytest
import pytest
from app import schemas




####  Test get posts  ####

def test_get_all_posts(authorized_client, test_posts):
    res = authorized_client.get("/posts/")
    assert len(res.json()) == len(test_posts)
    assert res.status_code == 200

def test_unauthorized_user_get_all_posts(client,test_posts):
    res = client.get("/posts/")
    assert res.status_code == 401

def test_unauthorized_user_get_one_post(client,test_posts):
    res = client.get(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401

def test_get_one_post_not_exist(authorized_client,test_posts):
    res = authorized_client.get(f"/posts/88888")
    assert res.status_code == 404

def test_get_one_post(authorized_client,test_posts):
    res = authorized_client.get(f"/posts/{test_posts[0].id}")
    assert res.status_code == 200
    post = schemas.PostOut(**res.json())
    assert post.Post.id == test_posts[0].id
    assert post.Post.title == test_posts[0].title
    assert post.Post.content == test_posts[0].content

def test_get_one_post_member_in_group(authorized_client, test_posts, test_comments, test_groups, test_users_in_groups, test_user):
    res = authorized_client.get(f"posts/{test_posts[3].id}")
    assert res.status_code == 200

def test_get_one_post_not_member_in_group(authorized_client_second, test_posts, test_comments, test_groups, test_users_in_groups, test_user):
    res = authorized_client_second.get(f"posts/{test_posts[3].id}")
    assert res.status_code == 403

def test_get_posts_by_group_authorized_user_member_in_group(authorized_client, test_posts, test_comments, test_groups, test_users_in_groups, test_user):
    res = authorized_client.get(f"/group/{test_groups[0].groups_id}/posts")
    assert res.status_code == 200
    assert len(res.json()) == 1    # One post in this group in conftest

def test_get_post_by_group_authorized_user_member_not_exist_group(authorized_client, test_posts, test_comments, test_groups, test_users_in_groups, test_user):
    res = authorized_client.get(f"/group/88888/posts")
    assert res.status_code == 404

def test_get_post_by_group_authorized_user_not_member_in_group(authorized_client, test_posts, test_comments, test_groups, test_users_in_groups, test_user):
    res = authorized_client.get(f"/group/{test_groups[2].groups_id}/posts")
    assert res.status_code == 403

def test_get_post_by_group_unauthorized_user(client, test_posts, test_comments, test_groups, test_users_in_groups, test_user):
    res = client.get(f"/group/{test_groups[0].groups_id}/posts")
    assert res.status_code == 401



####  Tests create posts  ####

@pytest.mark.parametrize("title, content, published, status_code",[
    ("new title 1", "new content 1", True, 201),
    ("", "new content 2", False, 422),
    (None, "new content 3", True, 422),
    ("new content", None, True, 422),
    ("new content 3", "", True, 422)
])
def test_create_post(authorized_client,test_user, test_posts, title, content, published, status_code):
    res = authorized_client.post("/posts/",json={"title": title, "content": content, "published": published})
    assert res.status_code == status_code
    if res.status_code == 201:
        created_post = schemas.PostResponse(**res.json())
        assert created_post.title == title
        assert created_post.content == content
        assert created_post.published == published
        assert created_post.owner_id == test_user['id']
        assert created_post.group_id == 0

def test_create_post_default_published(authorized_client,test_user,test_posts):
    res = authorized_client.post("/posts/",json={"title": "test title", "content": "test content"})
    created_post = schemas.PostResponse(**res.json())
    assert res.status_code == 201
    assert created_post.title == "test title"
    assert created_post.content == "test content"
    assert created_post.published == True
    assert created_post.owner_id == test_user['id']
    assert created_post.group_id == 0

def test_unauthorized_user_create_post(client,test_user,test_posts):
    res = client.post("/posts/",json={"title": "test title", "content": "test content"})
    assert res.status_code == 401

def test_authorized_user_create_post_in_group_membber_in_group(authorized_client, test_posts, test_comments, test_groups, test_users_in_groups, test_user):
    data = {"title": "test title", "content": "test content"}
    group_id = test_groups[0].groups_id
    res = authorized_client.post(f"/group/{group_id}/post", json = data)
    created_post = schemas.PostResponse(**res.json())
    assert res.status_code == 201
    assert created_post.title == "test title"
    assert created_post.group_id == group_id

@pytest.mark.parametrize("title, content, published, status_code",[
    ("", "new content 2", False, 422),
    (None, "new content 3", True, 422),
    ("new content", None, True, 422),
    ("new content 3", "", True, 422)
])
def test_authorized_user_create_post_in_group_membber_in_group_no_content(authorized_client, test_posts, test_comments, test_groups, test_users_in_groups, test_user,title,content,published,status_code):
    data = {"title": title, "content": content, "published":published}
    res = authorized_client.post(f"/group/{test_groups[0].groups_id}/post", json = data)
    assert res.status_code == status_code

def test_unauthorized_user_create_post_in_group(client, test_posts, test_comments, test_groups, test_users_in_groups, test_user):
    data = {"title": "test title", "content": "test content"}
    res = client.post(f"/group/{test_groups[0].groups_id}/post", json = data)
    assert res.status_code == 401

def test_authorized_user_create_post_in_group_not_exist_group(authorized_client, test_posts, test_comments, test_groups, test_users_in_groups, test_user):
    data = {"title": "test title", "content": "test content"}
    res = authorized_client.post(f"/group/88888/post", json = data)
    assert res.status_code == 404

def test_authorized_user_create_post_in_group_not_member_in_group(authorized_client, test_posts, test_comments, test_groups, test_users_in_groups, test_user):
    data = {"title": "test title", "content": "test content"}
    res = authorized_client.post(f"/group/{test_groups[2].groups_id}/post", json = data)
    assert res.status_code == 403



####  Tests delete posts  ####

def test_unauthorized_user_delete_post(client,test_user,test_posts):
    res = client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401

def test_authorized_user_delete_post(authorized_client, test_posts, test_comments, test_groups, test_users_in_groups, test_user):
    comment_id = test_comments[0].comment_id
    post_id = test_posts[0].id
    res = authorized_client.delete(f"/posts/{post_id}")
    assert res.status_code == 204
    res_comments = authorized_client.get(f"/posts/{post_id}/comments/{comment_id}/test")
    assert res_comments.status_code == 404
    res_post = authorized_client.get(f"/posts/{post_id}")
    assert res_post.status_code == 404


def test_unauthorized_user_delete_post_non_exist(client,test_user,test_posts):
    res = client.delete(f"/posts/88888")
    assert res.status_code == 401

def test_authorized_user_delete_post_non_exist(authorized_client,test_user,test_posts):
    res = authorized_client.delete(f"/posts/88888")
    assert res.status_code == 404

def test_authorized_user_delete_post_no_create_the_post(authorized_client_second,test_user_second,test_posts):
    res = authorized_client_second.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == 403



####  Tests update posts  ####

def test_update_post_authorized_user(authorized_client,test_user,test_posts):
    data = {
        "title": "update title",
        "content": "updated content",
    }
    res = authorized_client.put(f"/posts/{test_posts[0].id}", json = data)
    updated_post = schemas.PostResponse(**res.json())
    assert res.status_code == 200
    assert updated_post.title == data['title']
    assert updated_post.content == data['content']

def test_update_post_authorized_user_other_user_post(authorized_client_second,test_user_second,test_posts):
    data = {
        "title": "update title",
        "content": "updated content",
    }
    res = authorized_client_second.put(f"/posts/{test_posts[0].id}", json = data)
    assert res.status_code == 403

def test_unauthorized_user_update_post(client,test_user,test_posts):
    data = {
        "title": "update title",
        "content": "updated content",
    }
    res = client.put(f"/posts/{test_posts[0].id}", json = data)
    assert res.status_code == 401

def test_update_post_authorized_user_non_exist_post(authorized_client,test_user,test_posts):
    data = {
        "title": "update title",
        "content": "updated content",
    }
    res = authorized_client.put(f"/posts/88888", json = data)
    assert res.status_code == 404



 ###  Test Post Validation  ###

def test_get_one_post_id_0(authorized_client,test_posts):
    res = authorized_client.get(f"/posts/0")
    assert res.status_code == 422


def test_get_one_post_id_not_int(authorized_client,test_posts):
    res = authorized_client.get(f"/posts/fake-id", )
    assert res.status_code == 422


@pytest.mark.parametrize("limit, skip, search, status_code",[
    (20 ,0, "work", 200),
    ("not-int" ,0, "work", 422),
    (0, 0, "work", 422),
    (300, 0, "work", 422),
    (20, "not-int", "work", 422),
    (20, 20, "work", 422),
    (20 ,0, "t", 422),
    (20 ,0, "12345678912345678912345", 422),
])
def test_get_all_posts_unprocessable_entity(authorized_client, test_posts, limit, skip, search, status_code):
    params = {
        "limit": limit,
        "skip": skip,
        "search": search
    }
    res = authorized_client.get("/posts/", params= params)
    assert res.status_code == status_code


@pytest.mark.parametrize("limit, skip, search, status_code",[
    (20 ,0, "work", 200),
    ("not-int" ,0, "work", 422),
    (0, 0, "work", 422),
    (300, 0, "work", 422),
    (20, "not-int", "work", 422),
    (20, 20, "work", 422),
    (20 ,0, "t", 422),
    (20 ,0, "12345678912345678912345", 422),
])
def test_get_posts_by_group_authorized_user_member_in_group_unprocessable_entity(authorized_client, test_posts, test_comments, test_groups, test_users_in_groups, test_user, limit, skip, search, status_code):
    parameters = {
         "limit": limit,
         "skip": skip,
         "search": search
     }
    res = authorized_client.get(f"/group/{test_groups[0].groups_id}/posts", params= parameters)
    assert res.status_code == status_code


def test_get_posts_by_group_authorized_user_member_in_group_group_id_0(authorized_client, test_posts, test_comments, test_groups, test_users_in_groups, test_user):
    res = authorized_client.get(f"/group/0/posts")
    assert res.status_code == 422

def test_get_posts_by_group_authorized_user_member_in_group_group_id_not_int(authorized_client, test_posts, test_comments, test_groups, test_users_in_groups, test_user):
    res = authorized_client.get(f"/group/no-id/posts")
    assert res.status_code == 422


@pytest.mark.parametrize("title, content, published, status_code",[
    ("new title 1", "new content 1", True, 201),
    ("a", "new content 2", False, 422),
    ("a12345678901234567890", "new content 2", False, 422),
    ("new title 1", "n", True, 422),
    ("new title 1", "", True, 422),
    ("new title 1", "n", "fghhfg", 422),
])
def test_create_post_unprocessable_entity(authorized_client,test_user, test_posts, title, content, published, status_code):
    res = authorized_client.post("/posts/",json={"title": title, "content": content, "published": published})
    assert res.status_code == status_code



@pytest.mark.parametrize("title, content, published, status_code",[
    ("new title 1", "new content 1", True, 200),
    ("a", "new content 2", False, 422),
    ("a12345678901234567890", "new content 2", False, 422),
    ("new title 1", "n", True, 422),
    ("new title 1", "", True, 422),
    ("new title 1", "n", "fghhfg", 422),
])
def test_update_post_authorized_user_unprocessable_entity(authorized_client,test_user,test_posts, title, content, published, status_code):
    data = {
        "title": title,
        "content": content,
        "published":published
    }
    res = authorized_client.put(f"/posts/{test_posts[0].id}", json = data)
    assert res.status_code == status_code


@pytest.mark.parametrize("title, content, published, status_code",[
    ("new title 1", "new content 1", True, 201),
    ("a", "new content 2", False, 422),
    ("a12345678901234567890", "new content 2", False, 422),
    ("new title 1", "n", True, 422),
    ("new title 1", "", True, 422),
    ("new title 1", "n", "fghhfg", 422),
])
def test_authorized_user_create_post_in_group_membber_in_group_unprocessable_entity(authorized_client, test_posts, test_comments, test_groups, test_users_in_groups, test_user, title, content, published, status_code):
    data = {"title": title, "content": content, "published": published}
    res = authorized_client.post(f"/group/{test_groups[0].groups_id}/post", json = data)
    assert res.status_code == status_code


def test_authorized_user_create_post_in_group_membber_in_group_group_id_0(authorized_client, test_posts, test_comments, test_groups, test_users_in_groups, test_user):
    res = authorized_client.post(f"/group/0/post", json = {"title": "test title", "content": "test content"})
    assert res.status_code == 422

def test_authorized_user_create_post_in_group_membber_in_group_group_id_not_int(authorized_client, test_posts, test_comments, test_groups, test_users_in_groups, test_user):
    res = authorized_client.post(f"/group/no-id/post", json = {"title": "test title", "content": "test content"})
    assert res.status_code == 422