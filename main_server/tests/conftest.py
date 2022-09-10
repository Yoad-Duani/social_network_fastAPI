from datetime import datetime
from fastapi.testclient import TestClient
# from itsdangerous import json
import pytest
from app.main import app
from app.config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import get_db
from app.database import Base
from app.oauth2 import create_access_token
from app import models
from colorama import init, Fore

###
### All the class on the tests module will automatically import all the fixture from this conftest file
###




# Test data Base configuration

init(autoreset=True)

SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit = False, autoflush = False, bind = engine)


@pytest.fixture
def session():
    # Base.metadata.
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    except Exception as error:
        print(Fore.RED + "Eror:")
        print(Fore.RED + str(error))
    finally:
        db.close()


@pytest.fixture
def client(session):
    def override_get_db():
        try:
            yield session
        except Exception as error:
            print(Fore.RED + "Eror:")
            print(Fore.RED + str(error))
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)

# End test data Base configuration




# User test
@pytest.fixture
def test_user(client):
    user_data = {
        "email": "test@gmail.com",
        "password": "A12345678!",
        "name": "test test",
        "birth_date": "1997-12-26",
        "company_name": "NSO",
        "description": "some description",
        "position": "Backend Eng."}
    res = client.post("/users/",json = user_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user

@pytest.fixture
def test_user_second(client):
    user_data = {
        "email": "test2@gmail.com",
        "password": "A12345678!",
        "name": "test test",
        "birth_date": "1997-12-26",
        "company_name": "NSO",
        "description": "some description",
        "position": "Backend Eng."}
    res = client.post("/users/",json = user_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user

@pytest.fixture
def test_user_third(client):
    user_data = {
        "email": "test3@gmail.com",
        "password": "A12345678!",
        "name": "test test",
        "birth_date": "1997-12-26",
        "company_name": "NSO",
        "description": "some description",
        "position": "Backend Eng."}
    res = client.post("/users/",json = user_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user

@pytest.fixture
def test_user_4(session):
    user_data = [{
        "email": "test4@gmail.com",
        "password": "A12345678!",
        "name": "test test",
        "birth_date": "1997-12-26",
        "company_name": "NSO",
        "description": "some description",
        "position": "Backend Eng.",
        "verified": True,}]

    def create_test_user_4(test_user):
        return models.User(**test_user)
    user_map = map(create_test_user_4,user_data)
    user = list(user_map)
    session.add_all(user)
    session.commit()
    session.refresh(user[0])
    return user[0]


# This user is for check the replace manager
@pytest.fixture
def test_user_5(session):
    user_data = [{
        "email": "test5@gmail.com",
        "password": "A12345678!",
        "name": "test test",
        "birth_date": "1997-12-26",
        "company_name": "NSO",
        "description": "some description",
        "position": "Backend Eng.",
        "verified": True,
        "is_blocked":True}]
    def create_test_user_5(test_user):
        return models.User(**test_user)
    user_map = map(create_test_user_5,user_data)
    user = list(user_map)
    session.add_all(user)
    session.commit()
    session.refresh(user[0])
    return user[0]

# This user is for check the replace manager
@pytest.fixture 
def test_user_6(session):
    user_data = [{
        "email": "test6@gmail.com",
        "password": "A12345678!",
        "name": "test test",
        "birth_date": "1997-12-26",
        "company_name": "NSO",
        "description": "some description",
        "position": "Backend Eng.",
        "verified": True,
        "is_blocked":False}]
    def create_test_user_6(test_user):
        return models.User(**test_user)
    user_map = map(create_test_user_6,user_data)
    user = list(user_map)
    session.add_all(user)
    session.commit()
    session.refresh(user[0])
    return user[0]

# This user is for check the replace manager
@pytest.fixture 
def test_user_7(session):
    user_data = [{
        "email": "test7@gmail.com",
        "password": "A12345678!",
        "name": "test test",
        "birth_date": "1997-12-26",
        "company_name": "NSO",
        "description": "some description",
        "position": "Backend Eng.",
        "verified": True,
        "is_blocked":False}]
    def create_test_user_7(test_user):
        return models.User(**test_user)
    user_map = map(create_test_user_7,user_data)
    user = list(user_map)
    session.add_all(user)
    session.commit()
    session.refresh(user[0])
    return user[0]




# authorized user test
@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }
    return client


# authorized second user test
@pytest.fixture
def authorized_client_second(client, token_second):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token_second}"
    }
    return client

# authorized third user test
@pytest.fixture
def authorized_client_third(client, token_third):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token_third}"
    }
    return client

# authorized 4 user test
@pytest.fixture
def authorized_client_4(client, token_4):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token_4}"
    }
    return client


# token test 
@pytest.fixture
def token(test_user):
    return create_access_token({"user_id":test_user['id']})

# token test second
@pytest.fixture
def token_second(test_user_second):
    return create_access_token({"user_id":test_user_second['id']})

# token test third
@pytest.fixture
def token_third(test_user_third):
    return create_access_token({"user_id":test_user_third['id']})

# token test 4
@pytest.fixture
def token_4(test_user_4):
    return create_access_token({"user_id":test_user_4.id,"user_verified":test_user_4.verified,"user_block":test_user_4.is_blocked})

# posts test
@pytest.fixture
def test_posts(test_user,test_user_second, session ,test_groups):
    posts_data = [{
        "title": "first title",
        "content": "first content",
        "published":  True,
        "created_at": datetime.now(),
        "owner_id": test_user['id'],
        "group_id": 0
        },
        {
        "title": "2nd title",
        "content": "2nd content",
        "published":  True,
        "created_at": datetime.now(),
        "owner_id": test_user['id'],
        "group_id": 0
        },
        {
        "title": "3nd title",
        "content": "3nd content",
        "published":  True,
        "created_at": datetime.now(),
        "owner_id": test_user['id'],
        "group_id": 0
        },
        {
        "title": "4nd title",
        "content": "4nd content",
        "published":  True,
        "created_at": datetime.now(),
        "owner_id": test_user['id'],
        "group_id": test_groups[0].groups_id
        },
        {
        "title": "5nd title",
        "content": "5nd content",
        "published":  True,
        "created_at": datetime.now(),
        "owner_id": test_user_second['id'],
        "group_id": test_groups[2].groups_id
        }]

    def create_posts_model(post):
        return models.Post(**post)
    post_map = map(create_posts_model, posts_data)
    posts = list(post_map)
    session.add_all(posts)
    session.commit()
    posts = session.query(models.Post).all()
    return posts


# comments test
@pytest.fixture
def test_comments(test_posts, test_user, session):
    comments_data = [{
        "user_id": test_user["id"],
        "post_id": test_posts[0].id,
        "content": "first comment",
        "created_at": datetime.now(),
        "update_at": datetime.now()
        },
        {
        "user_id": test_user["id"],
        "post_id": test_posts[0].id,
        "content": "second comment",
        "created_at": datetime.now(),
        "update_at": datetime.now()
        },
        {
        "user_id": test_user["id"],
        "post_id": test_posts[0].id,
        "content": "third comment",
        "created_at": datetime.now(),
        "update_at": datetime.now()
        },
        {
        "user_id": test_user["id"],
        "post_id": test_posts[3].id,
        "content": "4 comment",
        "created_at": datetime.now(),
        "update_at": datetime.now()
        }]
    def create_comments_model(comment):
        return models.Comment(**comment)
    comment_map = map(create_comments_model,comments_data)
    comments = list(comment_map)
    session.add_all(comments)
    session.commit()
    comments = session.query(models.Comment).all()
    return comments
    


# vote test
@pytest.fixture
def test_vote(test_posts, session, test_user):
    new_vote = models.Vote(post_id = test_posts[0].id, user_id = test_user['id'])
    session.add(new_vote)
    session.commit()





@pytest.fixture
def test_groups(test_user, test_user_second,test_user_third,test_user_4, session):
    groups_data = [{
        "creator_id": test_user["id"],
        "name": "group 1",
        "description": "description group 1",
        "group_private":False,
        "created_at": datetime.now(),
        "update_at": datetime.now()
        },
        {
        "creator_id": test_user_second["id"],
        "name": "group 2",
        "description": "description group 2",
        "group_private":False,
        "created_at": datetime.now(),
        "update_at": datetime.now()
        },
        {
        "creator_id": test_user_second["id"],
        "name": "group 3",
        "description": "description group 3",
        "group_private":True,
        "created_at": datetime.now(),
        "update_at": datetime.now()
        }]
    
    def create_groups_model(group):
        return models.Groups(**group)
    group_map = map(create_groups_model,groups_data)
    groups = list(group_map)
    session.add_all(groups)
    session.commit()
    groups = session.query(models.Groups).all()
    return groups
   

@pytest.fixture
def test_users_in_groups(test_user, test_user_second,test_user_third,test_user_4,test_user_5,test_user_7, test_groups, session):
    group_1_id = test_groups[0].groups_id
    group_2_id = test_groups[1].groups_id
    group_3_id = test_groups[2].groups_id
    print(test_groups)
    users_in_groups_data = [{
        "user_id": test_user["id"],
        "groups_id": group_1_id,
        "is_blocked": False,
        "join_group_date": datetime.now()
        },
        {
        "user_id": test_user_second["id"],
        "groups_id": group_2_id,
        "is_blocked": False,
        "join_group_date": datetime.now()
        },
        {
        "user_id": test_user_second["id"],
        "groups_id": group_3_id,
        "is_blocked": False,
        "join_group_date": datetime.now()
        },
        {
        "user_id": test_user_4.id,
        "groups_id": group_3_id,
        "is_blocked": False,
        "join_group_date": datetime.now()
        },
        {
        "user_id": test_user_third["id"],
        "groups_id": group_1_id,
        "is_blocked": False,
        "join_group_date": datetime.now()
        },
        {
        "user_id": test_user_5.id,
        "groups_id": group_1_id,
        "is_blocked": False,
        "join_group_date": datetime.now()
        },
        {
        "user_id": test_user_7.id,
        "groups_id": group_1_id,
        "is_blocked": True,
        "join_group_date": datetime.now()
        },
        {
        "user_id": test_user_4.id,
        "groups_id": group_1_id,
        "is_blocked": False,
        "join_group_date": datetime.now()
        }]
    def create_users_in_groups_model(user_in_group):
        return models.UserInGroups(**user_in_group)
    user_in_group_map = map(create_users_in_groups_model,users_in_groups_data)
    users_in_groups = list(user_in_group_map)
    session.add_all(users_in_groups)
    session.commit()
    users_in_groups = session.query(models.UserInGroups).all()
    return users_in_groups
    
@pytest.fixture
def test_join_requests(session, test_user_second, test_groups):
    data = [{
        "user_id":test_user_second['id'],
        "groups_id": test_groups[0].groups_id,
        "name": test_user_second['name'],
        "group_name":test_groups[0].name
    }]
    def create_join_requests(join_request):
        return models.JoinRequestGroups(**join_request)
    join_requests_map = map(create_join_requests,data)
    join_requests = list(join_requests_map)
    session.add_all(join_requests)
    session.commit()
    join_requests = session.query(models.JoinRequestGroups).all()
    return join_requests
    # group_id = test_groups[0].groups_id
    # res = authorized_client_second.post(f"/groups{group_id}/join-request")
    # assert res.status_code == 201
    # new_join_request = res.json()
    # return new_join_request
