import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.main import app
from app.config import settings
from app.database import get_db, Base
from alembic import command
from app.oauth2 import create_access_token
from app import models

username = settings.pg_username
password = settings.pg_password
host = settings.pg_host
port = settings.pg_port
database = settings.pg_database
SQLALCHEMY_DATABASE_URL = f'postgresql://{username}:{password}@{host}:{port}/{database}_test'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# scope="function" - run fixtures every single test (function)
@pytest.fixture(scope="function")
def session():
    Base.metadata.drop_all(bind=engine) # drop the tables every time we end the tests
    Base.metadata.create_all(bind=engine) # create the tables every time we start the tests
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

# scope="function" - run fixtures every single test (function
@pytest.fixture(scope="function")
def client(session):
    # run this code before the tests
    # OPTION 1 - USING drop_all/create_all
    # Base.metadata.drop_all(bind=engine) # drop the tables every time we end the tests
    # Base.metadata.create_all(bind=engine) # create the tables every time we start the tests
    # OPTION 2
    # command.downgrade("base")
    # command.upgrade("head")
    # run the tests
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)

@pytest.fixture
def test_user(client):
    user_data = {"email": "test_user@test.com",
                 "password": "password123"}
    res = client.post("/users/", json=user_data)

    assert res.status_code == 201
    # print(res.json())
    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user

@pytest.fixture
def test_user2(client):
    user_data = {"email": "test_user2@test.com",
                 "password": "password123"}
    res = client.post("/users/", json=user_data)

    assert res.status_code == 201
    # print(res.json())
    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user

@pytest.fixture
def token(test_user):
    return create_access_token({"user_id": test_user['id']})

@pytest.fixture
def authorised_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }

    return client

@pytest.fixture
def test_posts(test_user, session, test_user2):
    posts_data = [{
        "title": "1st title",
        "content": "1st content",
        "user_id": test_user['id']
    }, {
        "title": "2nd title",
        "content": "2nd content",
        "user_id": test_user['id']
    }, {
        "title": "3rd title",
        "content": "3rd content",
        "user_id": test_user['id']
    }, {
        "title": "4rd title",
        "content": "4rd content",
        "user_id": test_user2['id']
    }]

    def create_post_model(post):
        return models.Post(**post)

    post_map = map(create_post_model, posts_data)
    posts = list(post_map)

    session.add_all(posts)
    session.commit()
    posts = session.query(models.Post).all()
    return posts