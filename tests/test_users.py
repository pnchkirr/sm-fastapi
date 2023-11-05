import pytest
from app import schemas
# from .database import client, session # no need to import anymore after we introduced tests/conftest.py file
from jose import jwt
from app.config import settings


def test_root(client):
    res = client.get("/")
    print(res.json().get('message')) # res: <Response [200 OK]> / json(): {'message': "Welcome to Kirill's API!"} / get: Welcome to Kirill's API!
    assert res.json().get('message') == "Welcome to Kirill's API - successfully deployed by GitHub Actions"
    assert res.status_code == 200

def test_create_user(client):
    res = client.post("/users/", json={"email": "pnchkireg@gmail.com",
                                       "password": "password123"})
    new_user = schemas.UserOut(**res.json())
    assert new_user.email == "pnchkireg@gmail.com"
    assert res.status_code == 201

def test_login_user(client, test_user):
    res = client.post("/login", data={"username": test_user['email'],
                                      "password": test_user['password']})
    # print(res.json())
    login_res = schemas.Token(**res.json())
    payload = jwt.decode(login_res.access_token, settings.secret_key, algorithms=[settings.algorithm])
    id = payload.get("user_id")
    assert id == test_user['id']
    assert login_res.token_type == "bearer"
    assert res.status_code == 200
    # response_model=schemas.Token
    # {"access_token": access_token, "token_type": "bearer"}

@pytest.mark.parametrize("email, password, status_code", [
    ('wrongemail@gmail.com', 'password123', 403),
    ('test_user@test.com', 'wrongpassword', 403),
    ('wrongemail@gmail.com', 'wrongpassword', 403),
    (None, 'password123', 422),
    ('test_user@test.com', None, 422)
])
def test_incorrect_login(client, email, password, status_code):
    res = client.post("/login", data={"username": email,
                                      "password": password})

    assert res.status_code == status_code
    # assert res.json().get('detail') == "Invalid Credentials"
