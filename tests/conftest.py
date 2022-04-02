from datetime import datetime
from pyexpat import model
from fastapi.testclient import TestClient
import pytest
from app.main import app
from app.config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
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


# authorized user test
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



@pytest.fixture()
def test_vote(test_posts, session, test_user):
    new_vote = models.Vote(post_id = test_posts[0].id, user_id = test_user['id'])
    session.add(new_vote)
    session.commit()
