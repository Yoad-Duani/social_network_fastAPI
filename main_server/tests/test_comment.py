from app import schemas
# from .database import client, session
import pytest
from jose import jwt
from app.config import settings



####  Test get comments  ####
# I need add test to check if unverified or block user can get comment, also check if grouop is prive I got error

def test_get_all_comments_authorized_client(authorized_client, test_posts, test_comments):
    res = authorized_client.get(f"/posts/{test_posts[0].id}/comments")
    assert res.status_code == 200
    assert len(res.json()) == len(test_comments) -1 # there is 4 comment and 3 for this post

def test_get_all_comments_authorized_client_in_group( test_posts, test_comments,test_groups,test_users_in_groups,authorized_client_4):
    res = authorized_client_4.get(f"/posts/{test_posts[4].id}/comments")
    assert res.status_code == 200
    assert len(res.json()) == 0 # there is 4 comment and 0 for this post

def test_get_all_comments_unauthorized_client(client, test_posts, test_comments):
    res = client.get(f"/posts/{test_posts[0].id}/comments")
    assert res.status_code == 401

def test_get_all_comments_authorized_client_privte_group_no_member(authorized_client, test_posts, test_comments):
    res = authorized_client.get(f"/posts/{test_posts[4].id}/comments")
    assert res.status_code == 403
    
def test_get_one_comment_authorized_client(authorized_client, test_posts, test_comments):
    res = authorized_client.get(f"/posts/{test_posts[0].id}/comments/{test_comments[0].comment_id}")
    assert res.status_code == 200
    comment = schemas.CommentResponse(**res.json())
    assert comment.comment_id == test_comments[0].comment_id
    assert comment.created_at == test_comments[0].created_at
    assert comment.content == test_comments[0].content

def test_get_one_comment_unauthorized_client(client, test_posts, test_comments):
    res = client.get(f"/posts/{test_posts[0].id}/comments/{test_comments[0].comment_id}")
    assert res.status_code == 401

def test_get_one_comment_non_exist_comment_authorized_client(authorized_client, test_posts, test_comments):
    res = authorized_client.get(f"/posts/{test_posts[0].id}/comments/88888")
    assert res.status_code == 404

def test_get_one_comment_non_exist_comment_unauthorized_client(client, test_posts, test_comments):
    res = client.get(f"/posts/{test_posts[0].id}/comments/88888")
    assert res.status_code == 401

def test_get_one_comment_non_exist_post_authorized_client(authorized_client, test_posts, test_comments):
    res = authorized_client.get(f"/posts/88888/comments/{test_comments[0].comment_id}")
    assert res.status_code == 404

def test_get_one_comment_non_exist_post_unauthorized_client(client, test_posts, test_comments):
    res = client.get(f"/posts/88888/comments/{test_comments[0].comment_id}")
    assert res.status_code == 401

def test_get_one_comment_non_exist_post_non_exist_comment_authorized(authorized_client, test_posts, test_comments):
    res = authorized_client.get(f"/posts/88888/comments/88888")
    assert res.status_code == 404

def test_get_one_comment_non_exist_post_non_exist_comment_unauthorized(client, test_posts, test_comments):
    res = client.get(f"/posts/88888/comments/88888")
    assert res.status_code == 401


 
####  Test create comment  ####

def test_create_comment_authorized_client(authorized_client, test_posts, test_comments, test_user):
    post_id = test_posts[0].id
    res = authorized_client.post(f"/posts/{post_id}/comments/",json = {"content": "test content"})
    created_comment = schemas.CommentResponse(**res.json())
    assert res.status_code == 201
    assert created_comment.post_id == post_id
    assert created_comment.user_id == test_user["id"]
    assert created_comment.content == "test content"

def test_create_comment_authorized_client_no_content(authorized_client, test_posts, test_comments, test_user):
    res = authorized_client.post(f"/posts/{test_posts[0].id}/comments/",json = {"content": ""})
    assert res.status_code == 422

def test_create_comment_authorized_client_none_content(authorized_client, test_posts, test_comments, test_user):
    res = authorized_client.post(f"/posts/{test_posts[0].id}/comments/",json = None)
    assert res.status_code == 422

def test_create_comment_authorized_client_non_exsit_post(authorized_client, test_posts, test_comments, test_user):
    res = authorized_client.post("/posts/88888/comments/",json = {"content": "test content"})
    assert res.status_code == 404

def test_create_comment_unauthorized_client_non_exsit_post(client, test_posts, test_comments, test_user):
    res = client.post("/posts/88888/comments/",json = {"content": "test content"})
    assert res.status_code == 401

def test_create_comment_unauthorized_client(client, test_posts, test_comments, test_user):
    res = client.post(f"/posts/{test_posts[0].id}/comments/",json = {"content": "test content"})
    assert res.status_code == 401

def test_create_comment_unauthorized_client_none_content(client, test_posts, test_comments, test_user):
    res = client.post(f"/posts/{test_posts[0].id}/comments/",json = {"content": ""})
    assert res.status_code == 401



####  Tests delete comments  ####

def test_authorized_client_delete_comment(authorized_client, test_posts, test_comments, test_user):
    res = authorized_client.delete(f"/posts/{test_posts[0].id}/comments/{test_comments[0].comment_id}")
    assert res.status_code == 204

def test_authorized_client_delete_comment_non_exsit_post(authorized_client, test_posts, test_comments, test_user):
    res = authorized_client.delete(f"/posts/88888/comments/{test_comments[0].comment_id}")
    assert res.status_code == 404

def test_authorized_client_delete_comment_non_exsit_comment(authorized_client, test_posts, test_comments, test_user):
    res = authorized_client.delete(f"/posts/{test_posts[0].id}/comments/88888")
    assert res.status_code == 404

def test_authorized_client_delete_comment_non_exsit_comment_and_post(authorized_client, test_posts, test_comments, test_user):
    res = authorized_client.delete("/posts/88888/comments/88888")
    assert res.status_code == 404

def test_authorized_client_delete_comment_other_user(authorized_client_second, test_posts, test_comments, test_user):
    res = authorized_client_second.delete(f"/posts/{test_posts[0].id}/comments/{test_comments[0].comment_id}")
    assert res.status_code == 403

def test_unauthorized_client_delete_comment(client, test_posts, test_comments, test_user):
    res = client.delete(f"/posts/{test_posts[0].id}/comments/{test_comments[0].comment_id}")
    assert res.status_code == 401

def test_unauthorized_client_delete_comment_non_exsit_post(client, test_posts, test_comments, test_user):
    res = client.delete(f"/posts/88888/comments/{test_comments[0].comment_id}")
    assert res.status_code == 401

def test_unauthorized_client_delete_comment_non_exsit_comment(client, test_posts, test_comments, test_user):
    res = client.delete(f"/posts/{test_posts[0].id}/comments/88888")
    assert res.status_code == 401



####  Tests update comments  ####

def test_update_comment_authorized_client(authorized_client, test_posts, test_comments, test_user):
    post_id = test_posts[0].id
    data = {"content": "updated content",}
    res = authorized_client.put(f"/posts/{post_id}/comments/{test_comments[0].comment_id}",json = data)
    updated_comment = schemas.CommentResponse(**res.json())
    assert res.status_code == 200
    assert updated_comment.content == data['content']
    assert updated_comment.user_id == test_user['id']
    assert updated_comment.post_id == post_id

def test_update_comment_authorized_client_no_content(authorized_client, test_posts, test_comments, test_user):
    data = {"content": "",}
    res = authorized_client.put(f"/posts/{test_posts[0].id}/comments/{test_comments[0].comment_id}",json = data)
    assert res.status_code == 422

def test_update_comment_authorized_client_none_content(authorized_client, test_posts, test_comments, test_user):
    res = authorized_client.put(f"/posts/{test_posts[0].id}/comments/{test_comments[0].comment_id}",json = None)
    assert res.status_code == 422
    
def test_update_comment_authorized_client_non_exsit_post(authorized_client, test_posts, test_comments, test_user):
    data = {"content": "updated content",}
    res = authorized_client.put(f"/posts/88888/comments/{test_comments[0].comment_id}",json = data)
    assert res.status_code == 404

def test_update_comment_authorized_client_non_exsit_comment(authorized_client, test_posts, test_comments, test_user):
    data = {"content": "updated content",}
    res = authorized_client.put(f"/posts/{test_posts[0].id}/comments/88888",json = data)
    assert res.status_code == 404

def test_update_comment_authorized_client_non_exsit_comment_post_and_comment(authorized_client, test_posts, test_comments, test_user):
    data = {"content": "updated content",}
    res = authorized_client.put(f"/posts/88888/comments/88888",json = data)
    assert res.status_code == 404

def test_update_comment_authorized_client_other_user(authorized_client_second, test_posts, test_comments, test_user):
    data = {"content": "updated content",}
    res = authorized_client_second.put(f"/posts/{test_posts[0].id}/comments/{test_comments[0].comment_id}",json = data)
    assert res.status_code == 403

def test_update_comment_unauthorized_client(client, test_posts, test_comments, test_user):
    data = {"content": "updated content",}
    res = client.put(f"/posts/{test_posts[0].id}/comments/{test_comments[0].comment_id}",json = data)
    assert res.status_code == 401



###  Test comment Validation  ###

def test_get_all_comments_authorized_client_post_id_0(authorized_client, test_posts, test_comments):
    res = authorized_client.get(f"/posts/0/comments")
    assert res.status_code == 422


@pytest.mark.parametrize("limit, skip, status_code",[
    (5 ,0, 200),
    (0 ,0, 422),
    (40 ,0, 422),
    ("not-int" ,0, 422),
    (5 ,10, 422),
    (5 ,-1, 422),
    (5 ,"not-int", 422),
])
def test_get_all_comments_authorized_client_unprocessable_entity(authorized_client, test_posts, test_comments,limit,skip,status_code):
    params = {
        "limit": limit,
        "skip": skip,
    }
    res = authorized_client.get(f"/posts/{test_posts[0].id}/comments", params= params)
    assert res.status_code == status_code


def test_get_one_comment_authorized_client_post_id_0(authorized_client, test_posts, test_comments):
    res = authorized_client.get(f"/posts/0/comments/{test_comments[0].comment_id}")
    assert res.status_code == 422

def test_get_one_comment_authorized_client_post_id_not_int(authorized_client, test_posts, test_comments):
    res = authorized_client.get(f"/posts/noid/comments/{test_comments[0].comment_id}")
    assert res.status_code == 422

def test_get_one_comment_authorized_client_comment_id_0(authorized_client, test_posts, test_comments):
    res = authorized_client.get(f"/posts/{test_posts[0].id}/comments/0")
    assert res.status_code == 422

def test_get_one_comment_authorized_client_comment_id_no_int(authorized_client, test_posts, test_comments):
    res = authorized_client.get(f"/posts/{test_posts[0].id}/comments/noid")
    assert res.status_code == 422


def test_create_comment_authorized_client_unprocessable_entity(authorized_client, test_posts, test_comments, test_user):
    post_id = test_posts[0].id
    res = authorized_client.post(f"/posts/{post_id}/comments/",json = {"content": "t"})
    assert res.status_code == 422
    
def test_update_comment_authorized_client_unprocessable_entity(authorized_client, test_posts, test_comments, test_user):
    post_id = test_posts[0].id
    data = {"content": "u",}
    res = authorized_client.put(f"/posts/{post_id}/comments/{test_comments[0].comment_id}",json = data)
    assert res.status_code == 422


def test_create_comment_authorized_client_post_id_0(authorized_client, test_posts, test_comments, test_user):
    res = authorized_client.post(f"/posts/0/comments/",json = {"content": "test content"})
    assert res.status_code == 422

def test_create_comment_authorized_client_post_id_not_int(authorized_client, test_posts, test_comments, test_user):
    res = authorized_client.post(f"/posts/noid/comments/",json = {"content": "test content"})
    assert res.status_code == 422


def test_update_comment_authorized_client_post_id_0(authorized_client, test_posts, test_comments, test_user):
    data = {"content": "updated content",}
    res = authorized_client.put(f"/posts/0/comments/{test_comments[0].comment_id}",json = data)
    assert res.status_code == 422

def test_update_comment_authorized_client_post_id_not_int(authorized_client, test_posts, test_comments, test_user):
    data = {"content": "updated content",}
    res = authorized_client.put(f"/posts/noid/comments/{test_comments[0].comment_id}",json = data)
    assert res.status_code == 422


def test_authorized_client_delete_comment_post_id_0(authorized_client, test_posts, test_comments, test_user):
    res = authorized_client.delete(f"/posts/0/comments/{test_comments[0].comment_id}")
    assert res.status_code == 422

def test_authorized_client_delete_comment_podt_id_not_int(authorized_client, test_posts, test_comments, test_user):
    res = authorized_client.delete(f"/posts/id/comments/{test_comments[0].comment_id}")
    assert res.status_code == 422

def test_authorized_client_delete_comment_comment_id_0(authorized_client, test_posts, test_comments, test_user):
    res = authorized_client.delete(f"/posts/{test_posts[0].id}/comments/0")
    assert res.status_code == 422

def test_authorized_client_delete_comment_comment_id_not_int(authorized_client, test_posts, test_comments, test_user):
    res = authorized_client.delete(f"/posts/{test_posts[0].id}/comments/noid")
    assert res.status_code == 422