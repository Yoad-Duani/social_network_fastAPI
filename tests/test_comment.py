from app import schemas
# from .database import client, session
import pytest
from jose import jwt
from app.config import settings



####  Test get comments  ####

def test_get_all_comments_authorized_client(authorized_client, test_posts, test_comments):
    res = authorized_client.get(f"/posts/{test_posts[0].id}/comments")
    assert res.status_code == 200
    assert len(res.json()) == len(test_comments)

def test_get_all_comments_unauthorized_client(client, test_posts, test_comments):
    res = client.get(f"/posts/{test_posts[0].id}/comments")
    assert res.status_code == 401
    
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

def test_get_non_exist_comment_authorized_client(authorized_client, test_posts, test_comments):
    res = authorized_client.get(f"/posts/{test_posts[0].id}/comments/88888")
    assert res.status_code == 404

def test_get_non_exist_comment_unauthorized_client(client, test_posts, test_comments):
    res = client.get(f"/posts/{test_posts[0].id}/comments/88888")
    assert res.status_code == 401

def test_get_one_comment_non_exist_post_authorized_client(authorized_client, test_posts, test_comments):
    res = authorized_client.get(f"/posts/88888/comments/{test_comments[0].comment_id}")
    assert res.status_code == 404

def test_get_one_comment_non_exist_post_unauthorized_client(client, test_posts, test_comments):
    res = client.get(f"/posts/88888/comments/{test_comments[0].comment_id}")
    assert res.status_code == 401




####  Test create comment  ####