from datetime import datetime
from fastapi.testclient import TestClient
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
        "password": "12345678",
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
        "password": "12345678",
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


# token test 
@pytest.fixture
def token(test_user):
    return create_access_token({"user_id":test_user['id']})


# token test second
@pytest.fixture
def token_second(test_user_second):
    return create_access_token({"user_id":test_user_second['id']})


# posts test
@pytest.fixture
def test_posts(test_user, session):
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
def test_groups(test_user, test_user_second, session):
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
def test_users_in_groups(test_user, test_user_second, test_groups, session):
    group_1_id = test_groups[0].groups_id
    group_2_id = test_groups[1].groups_id
    print(test_groups)
    users_in_groups_data = [{
        "user_id": test_user["id"],
        "groups_id": group_1_id,
        "is_blocked": False,
        "request_accepted":True,
        "update_at": datetime.now(),
        "join_group_date": datetime.now()
        },
        {
        "user_id": test_user_second["id"],
        "groups_id": group_2_id,
        "is_blocked": False,
        "request_accepted":True,
        "update_at": datetime.now(),
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
    