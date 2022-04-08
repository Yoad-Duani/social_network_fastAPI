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
    post = schemas.PostOut(**res.json())
    assert post.Post.id == test_posts[0].id
    assert post.Post.title == test_posts[0].title
    assert post.Post.content == test_posts[0].content
    assert res.status_code == 200



####  Tests create posts  ####

# need to add chcek with group
@pytest.mark.parametrize("title, content, published",[
    ("new title 1", "new content 1", True),
    ("new title 2", "new content 2", False),
    ("new title 3", "new content 3", True)
])
def test_create_post(authorized_client,test_user, test_posts, title, content, published):
    res = authorized_client.post("/posts/",json={"title": title, "content": content, "published": published})
    created_post = schemas.PostResponse(**res.json())
    assert res.status_code == 201
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



####  Tests delete posts  ####

def test_unauthorized_user_delete_post(client,test_user,test_posts):
    res = client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401

def test_authorized_user_delete_post(authorized_client,test_user,test_posts):
    res = authorized_client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == 204

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