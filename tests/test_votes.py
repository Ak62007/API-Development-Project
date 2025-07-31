import pytest
from app import models

@pytest.fixture
def test_vote(test_user, test_posts, session):
    new_vote=models.Votes(post_id=test_posts[3].id, user_id=test_user["id"])
    session.add(new_vote)
    session.commit()

def test_vote_a_post(authorized_client, test_user, test_posts):
    res = authorized_client.post("/vote/", json={"post_id": test_posts[0].id, "dir": 1})
    assert res.status_code == 201
    
def test_vote_to_other_user_post(authorized_client, test_posts):
    res = authorized_client.post("/vote/", json={"post_id": test_posts[3].id, "dir": 1})
    assert res.status_code == 201
    
def test_vote_unauth_user(client, test_posts):
    res = client.post("/vote/", json={"post_id": test_posts[0].id, "dir": 1})
    assert res.status_code == 401
    
def test_vote_non_existing_post(authorized_client, test_posts):
    res = authorized_client.post("/vote/", json={"post_id": 4624, "dir": 1})
    assert res.status_code == 404
    
def test_double_vote_a_post(authorized_client, test_user, test_posts, test_vote):
    res = authorized_client.post("/vote/", json={"post_id": test_posts[3].id, "dir": 1})
    assert res.status_code == 409
    # res = authorized_client.post("/vote/", json={"post_id": test_posts[0].id, "dir": 1})
    # res2 = authorized_client.post("/vote/", json={"post_id": test_posts[0].id, "dir": 1})
    # assert res.status_code == 201
    # assert res2.status_code == 409
    
def test_down_vote_a_post(authorized_client, test_posts, test_vote):
    res = authorized_client.post("/vote/", json={"post_id": test_posts[3].id, "dir": 0})
    assert res.status_code == 201
    
def test_delete_vote_which_is_not_voted(authorized_client, test_posts):
    res = authorized_client.post("/vote/", json={"post_id": test_posts[0].id, "dir": 0})
    assert res.status_code == 404
    
