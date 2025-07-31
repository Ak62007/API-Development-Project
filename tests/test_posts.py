from app import schemas
from app import models
import pytest

def test_all_posts(authorized_client, test_posts):
    res = authorized_client.get("/posts/")
    
    def map_schema(post):
        return schemas.PostOut(**post)
    
    posts_map = map(map_schema, res.json())
    posts = list(posts_map)
    print(posts)
    assert res.status_code == 200
    assert len(res.json()) == len(test_posts)
    
def test_unauth_user_get_all_posts(client, test_posts):
    res = client.get("/posts/")
    assert res.status_code == 401
    
def test_unauth_user_get_one_posts(client, test_posts):
    res = client.get(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401
    
def test_get_one_post_not_exist(authorized_client, test_posts):
    res = authorized_client.get("/posts/288946")
    assert res.status_code == 404
    
def test_get_one_post(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/{test_posts[0].id}")
    print(res.json())
    assert res.status_code == 200
    assert res.json().get("Posts")["title"] == test_posts[0].title
    assert res.json().get("Posts")["content"] == test_posts[0].content

@pytest.mark.parametrize("title, content, published", [
    ("oyee post", "oyee content", True),
    ("nahi", "kuch", True),
    ("kya", "ho", False)
])    
def test_create_post(authorized_client, test_user, test_posts, title, content, published):
    res = authorized_client.post("/posts/", json={"title": title, "content": content, "published": published})
    
    created_post = schemas.Post(**res.json())
    assert res.status_code == 201
    assert created_post.title == title
    assert created_post.content == content
    assert created_post.published == published
    assert created_post.owner_id == test_user["id"]
    
def test_create_post_default_publish_case(authorized_client):
    res = authorized_client.post("/posts/", json={"title": "kam", "content": "bol"})
    
    print(res.json())
    assert res.status_code == 201
    assert res.json().get("published") == True
    
def test_unauthorized_user_create_post(client):
    res = client.post("/posts/", json={"title": "what title!!?", "content": "IDK", "published": True})
    assert res.status_code == 401
    
def test_unauthorized_user_delete_post(client, test_user, test_posts):
    res = client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401
    
def test_delete_post(authorized_client, test_user, test_posts, session):
    res = authorized_client.delete(f"/posts/{test_posts[0].id}")
    # deleted_post = session.query(models.Posts).filter(models.Posts.id == test_posts[0].id).first()
    assert res.status_code == 204
    
def test_delete_non_exixting_post(authorized_client):
    res = authorized_client.delete(f"/posts/{87298}")
    assert res.status_code == 404
    
def test_delete_post_created_by_different_user(authorized_client, test_posts):
    res = authorized_client.delete(f"/posts/{test_posts[3].id}")
    assert res.status_code == 403

def test_update_post(authorized_client, test_user, test_posts):
    data = {
        "title": "updated_post",
        "content": "updated content",
        "published": False
    }
    res = authorized_client.put(f"/posts/{test_posts[0].id}", json=data)
    data_return = schemas.Post(**res.json())
    assert res.status_code == 202
    assert data_return.title == data["title"]
    assert data_return.content == data["content"]
    
def test_update_post_of_different_user(authorized_client, test_user, test_user2, test_posts):
    data = {
        "title": "updated_title",
        "content": "updated content",
    }
    res = authorized_client.put(f"/posts/{test_posts[3].id}", json=data)
    assert res.status_code == 403
    
def test_update_post_that_does_not_exist(authorized_client, test_user, test_posts):
    data = {
        "title": "updated_title",
        "content": "updated content",
    }
    res = authorized_client.put("/posts/542652", json=data)
    assert res.status_code == 404
    
def test_update_post_by_unauth_user(client, test_user, test_posts):
    data = {
        "title": "updated_title",
        "content": "updated content",
    }
    res = client.put(f"/posts/{test_posts[0].id}", json=data)
    assert res.status_code == 401