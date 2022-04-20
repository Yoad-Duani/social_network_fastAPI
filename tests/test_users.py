# from itsdangerous import json
from app import schemas
# from .database import client, session
import pytest
from jose import jwt
from app.config import settings



# def test_root(client):
#     res = client.get("/")
#     assert res.json().get('message') == 'Hello World'
#     assert res.status_code == 200




def test_create_user(client):
    res = client.post("/users/",json={
        "email": "test@gmail.com",
        "password": "12345678",
        "name": "test test",
        "birth_date": "1997-12-26",
        "company_name": "NSO",
        "description": "some description",
        "position": "Backend Eng."
    })
    new_user = schemas.UserResponse(**res.json())
    assert new_user.email == "test@gmail.com"
    assert res.status_code == 201


def test_create_user_with_exsits_email(client,test_user):
    res = client.post("/users/",json={
        "email": "test@gmail.com",
        "password": "12345678",
        "name": "test test",
        "birth_date": "1997-12-26",
        "company_name": "NSO",
        "description": "some description",
        "position": "Backend Eng."
    })
    assert res.status_code == 409


def test_get_user(client,test_user):
    id = test_user["id"]
    res = client.get(f"users/{id}")
    user = schemas.UserResponse(**res.json())
    assert user.email == "test@gmail.com"
    assert res.status_code == 200


# Test Login
def test_login_user(client,test_user):
    res = client.post("/login",data={
        "username": test_user["email"],
        "password": test_user["password"]
    })
    login_res = schemas.TokenResponse(**res.json())
    payload = jwt.decode(login_res.access_token, settings.secret_key, algorithms= [settings.algorithm])
    id = payload.get("user_id")
    assert id == test_user["id"]
    assert login_res.token_type == "bearer"
    assert res.status_code == 200



# Test Incorrect Login
@pytest.mark.parametrize("email, password, status_code",[
    ('wrongemail@gmail.com', '12345678', 403),
    ('test@gmail.com', 'wrongPassword', 403),
    ('wrongemail@gmail.com', 'wrongPassword', 403),
    (None, '12345678', 422),
    ('wrongemail@gmail.com', None, 422),
])
def test_incorrect_login(test_user, client, email, password, status_code):
    res = client.post("/login", data={
        "username": email,
        "password": password
    })
    assert res.status_code == status_code



@pytest.mark.parametrize("password, company_name, description, position, status_code",[
    ('123456789', 'new company', "new description", "new position", 200),
    (None, 'new company', "new description", "new position", 200),
    ('12345678', None, "new description", "new position", 200),
    ('12345678', 'new company', None, "new position", 200),
    ('12345678', 'new company', "new description", None, 200),
    (None, None, None, None, 422),
])
def test_update_user_authorized_user(authorized_client, password, company_name, description, position, status_code):
    data = {
        "password": password,
        "company_name": company_name,
        "description": description,
        "position": position,
    }
    res = authorized_client.put("/users/update-user", json = data)
    assert res.status_code == status_code

def test_update_user_authorized_user_secondTest(authorized_client):
    data = {
        "company_name": "company_name",
        "description": "description",
        "position": "position",
    }
    res = authorized_client.put("/users/update-user", json = data)
    assert res.status_code == 200
    updated_user = schemas.UserResponse(**res.json())
    assert updated_user.company_name == data['company_name']
    assert updated_user.description == data['description']
    assert updated_user.position == data['position']


def test_update_user_unauthorized_user(client,test_user):
    data = {
        "password": "123456789",
        "company_name": "company_name",
        "description": "description",
        "position": "position",
    }
    res = client.put("/users/update-user", json = data)
    assert res.status_code == 401