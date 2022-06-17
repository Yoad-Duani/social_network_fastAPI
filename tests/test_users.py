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
        "password": "A12345678!",
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
        "password": "A12345678!",
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
    ('A123456789!', 'new company', "new description", "new position", 200),
    (None, 'new company', "new description", "new position", 200),
    ('A12345678!', None, "new description", "new position", 200),
    ('A12345678!', 'new company', None, "new position", 200),
    ('A12345678!', 'new company', "new description", None, 200),
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
        "company_name": "company-name",
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
        "password": "A123456789!",
        "company_name": "company_name",
        "description": "description",
        "position": "position",
    }
    res = client.put("/users/update-user", json = data)
    assert res.status_code == 401



###  Test Get Join Requests  ###
def test_get_user_join_requests(authorized_client_second,test_groups,test_join_requests, test_posts, test_comments, test_user_second, test_users_in_groups):
    res = authorized_client_second.get("/users/my-join-requests/")
    assert res.status_code == 200
    assert res.json()[0]['group_name'] == 'group 1'

def test_get_user_join_requests_unauthorized_client(client,test_groups,test_join_requests, test_posts, test_comments, test_user_second, test_users_in_groups):
    res = client.get("/users/my-join-requests")
    assert res.status_code == 401



###  Test User Validation  ###

def test_get_user_id_0(client):
    res = client.get(f"users/0")
    assert res.status_code == 422

def test_get_user_id_not_int(client):
    res = client.get(f"users/fake-id")
    assert res.status_code == 422


# need update test for date
@pytest.mark.parametrize("email, password, name, birth_date, company_name, description, position, status_code",[
    ("test@gmail.com", 'A123456789!', "test name", "1997-12-26", 'new company', "new description", "new position", 201),
    ("testgmail.com", 'A123456789!', "test name", "1997-12-26", 'new company', "new description", "new position", 422), # test mail - no @
    ("test@gmailcom", 'A123456789!', "test name", "1997-12-26", 'new company', "new description", "new position", 422), # test mail - no .com
    ("test@gmail.com", '123456789!', "test name", "1997-12-26", 'new company', "new description", "new position", 422), # test password - no capital leter
    ("test@gmail.com", 'A123456789', "test name", "1997-12-26", 'new company', "new description", "new position", 422), # test password - no symbol
    ("test@gmail.com", 'Abcdefgdh!', "test name", "1997-12-26", 'new company', "new description", "new position", 422), # test password - no digit
    ("test@gmail.com", 'A!123', "test name", "1997-12-26", 'new company', "new description", "new position", 422), # test password - no 8 chars
    ("test@gmail.com", 'A123456789!', "a", "1997-12-26", 'new company', "new description", "new position", 422), # test name - no 2 chars
    ("test@gmail.com", 'A123456789!', "yosi()", "1997-12-26", 'new company', "new description", "new position", 422), # test name - symbol
    ("test@gmail.com", 'A123456789!', "test name", "fake date", 'new company', "new description", "new position", 422), # test date - str
    # ("test@gmail.com", 'A123456789!', "test name", "8888964", 'new company', "new description", "new position", 422), # test date - no date format
    ("test@gmail.com", 'A123456789!', "test name", "1997-12-26", 'select * from', "new description", "new position", 422), # test company name - symbol
    ("test@gmail.com", 'A123456789!', "test name", "1997-12-26", 'a', "new description", "new position", 422), # test company name - no 2 chars
    ("test@gmail.com", 'A123456789!', "test name", "1997-12-26", 'new company', "a", "new position", 422), # test description - no 2 chars
    ("test@gmail.com", 'A123456789!', "test name", "1997-12-26", 'new company', "new description", "a", 422), # test position - no 2 chars
    ("test@gmail.com", 'A123456789!', "test name", "1997-12-26", 'new company', "new description", "([#*])", 422), # test position - symbol
])
def test_create_user_unprocessable_entity(client, email, password, name, birth_date, company_name, description, position, status_code):
    res = client.post("/users/",json={
        "email": email,
        "password": password,
        "name": name,
        "birth_date": birth_date,
        "company_name": company_name,
        "description": description,
        "position": position
    })
    assert res.status_code == status_code



@pytest.mark.parametrize("password, company_name, description, position, status_code",[
    ('A123456789!', 'new company', "new description", "new position", 200),
    ('123456789!', 'new company', "new description", "new position", 422), # test password - no capital leter
    ('A123456789', 'new company', "new description", "new position", 422), # test password - no symbol
    ('Abcdefgdh!', 'new company', "new description", "new position", 422), # test password - no digit
    ('A!123', 'new company', "new description", "new position", 422), # test password - no 8 chars
    ('A123456789!', 'select * from', "new description", "new position", 422), # test company name - symbol
    ('A123456789!', 'a', "new description", "new position", 422), # test company name - no 2 chars
    ('A123456789!', 'new company', "a", "new position", 422), # test description - no 2 chars
    ('A123456789!', 'new company', "new description", "a", 422), # test position - no 2 chars
    ('A123456789!', 'new company', "new description", "([#*])", 422), # test position - symbol
])
def test_update_user_authorized_user_unprocessable_entity(authorized_client, password, company_name, description, position, status_code):
    data = {
        "password": password,
        "company_name": company_name,
        "description": description,
        "position": position,
    }
    res = authorized_client.put("/users/update-user", json = data)
    assert res.status_code == status_code