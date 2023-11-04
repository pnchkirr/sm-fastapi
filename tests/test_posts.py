import pytest
from app import schemas
# from .database import client, session # no need to import anymore after we introduced tests/conftest.py file
from jose import jwt
from app.config import settings
from typing import List


def test_get_all_posts(authorised_client, test_posts):
    res = authorised_client.get("/posts/")

    def validate(post):
        return schemas.PostOut(**post)
    posts_map = map(validate, res.json())
    posts_list = list(posts_map)
    # print(posts_list)

    # print(res.json())
    assert len(res.json()) == len(test_posts)
    assert res.status_code == 200
    # assert posts_list[0].Post.id == test_posts[0].id # TO FIX: add ordering to make sure we compare consistently ordered sets

def test_unauthorised_user_get_all_posts(client, test_posts):
    res = client.get("/posts/")
    assert res.status_code == 401

def test_unauthorised_user_get_one_post(client, test_posts):
    res = client.get(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401

def test_get_one_post_not_exists(authorised_client, test_posts):
    res = authorised_client.get("/posts/88888")
    assert res.status_code == 404

def test_get_one_post(authorised_client, test_posts):
    res = authorised_client.get(f"/posts/{test_posts[0].id}")
    # print(res.json())
    post = schemas.PostOut(**res.json())
    # print(post)
    assert post.Post.id == test_posts[0].id
    assert post.Post.content == test_posts[0].content
    assert post.Post.title == test_posts[0].title

@pytest.mark.parametrize("title, content, published", [
    ("Test create post 1", "Test random content 1", True),
    ("Test create post 2", "Test random content 2", False),
    ("Test 3", "test content 3", True)
])
def test_create_post(authorised_client, test_user, test_posts, title, content, published):
    res = authorised_client.post("/posts/", json={"title": title,
                                                  "content": content,
                                                  "published": published})
    # print(res)
    new_post = schemas.Post(**res.json())
    assert new_post.title == title
    assert new_post.content == content
    assert new_post.published == published
    assert new_post.user_id == test_user['id']
    assert res.status_code == 201

def test_create_post_default_published_true(authorised_client, test_user, test_posts):
    res = authorised_client.post("/posts/", json={"title": "Test create post default published true",
                                                  "content": "Test post content"})
    # print(res)
    new_post = schemas.Post(**res.json())
    assert new_post.title == "Test create post default published true"
    assert new_post.content == "Test post content"
    assert new_post.published == True
    assert new_post.user_id == test_user['id']
    assert res.status_code == 201

def test_unauthorised_user_create_post(client, test_user, test_posts):
    res = client.post("/posts/", json={"title": "Test create post unauthorised user",
                                                "content": "This should never get into db"})
    assert res.status_code == 401

def test_unauthorised_user_delete_post(client, test_user, test_posts):
    res = client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401

def test_delete_post_success(authorised_client, test_user, test_posts):
    res = authorised_client.delete(f"/posts/{test_posts[0].id}")
    # TO DO: Add len() check
    assert res.status_code == 204

def test_delete_post_not_exists(authorised_client, test_posts):
    res = authorised_client.delete("/posts/88888")
    assert res.status_code == 404

def test_delete_other_user_post(authorised_client, test_user, test_posts):
    res = authorised_client.delete(f"/posts/{test_posts[3].id}")
    assert res.status_code == 403

def test_update_post_success(authorised_client, test_user, test_posts):
    data = {
        "title": "Test updated title",
        "content": "Test updated content",
        "id": test_posts[0].id
    }
    res = authorised_client.put(f"/posts/{data['id']}", json={"title": data["title"],
                                                              "content": data["content"]})
    updated_post = schemas.Post(**res.json())
    assert updated_post.title == data["title"]
    assert updated_post.content == data["content"]
    assert res.status_code == 200

def test_update_other_user_post(authorised_client, test_user, test_user2, test_posts):
    data = {
        "title": "Test updated title other user",
        "content": "Test updated content other user",
        "id": test_posts[3].id
    }
    res = authorised_client.put(f"/posts/{data['id']}", json={"title": data["title"],
                                                              "content": data["content"]})
    assert res.status_code == 403

def test_unauthorised_user_update_post(client, test_user, test_posts):
    data = {
        "title": "Test updated title unauthorised user",
        "content": "Test updated content unauthorised user",
        "id": test_posts[0].id
    }
    res = client.put(f"/posts/{data['id']}", json={"title": data["title"],
                                                   "content": data["content"]})
    assert res.status_code == 401

def test_update_post_not_exists(authorised_client, test_user, test_posts):
    data = {
        "title": "Test updated title not exists",
        "content": "Test updated content not exists",
        "id": "88888"
    }
    res = authorised_client.put(f"/posts/{data['id']}", json={"title": data["title"],
                                                              "content": data["content"]})
    assert res.status_code == 404
