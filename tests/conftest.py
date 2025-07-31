from fastapi.testclient import TestClient
import pytest
from app.main import app
from app import models
from app.database import get_db, Base
from app.oauth2 import create_access_token
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config import settings
# from alembic import command

SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture()
def session():
    # Run our code before tests
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    # if using alembic (after setting up the revisions)
    # command.downgrade("base")
    # command.upgrade("head")
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture()
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    # Run our code after tests

@pytest.fixture
def test_user(client):
    user = {"email": "kkadi8434367970@gmail.com", "password": "adi827193"}
    res = client.post("/users/", json=user)
    assert res.status_code == 201
    new_user = res.json()
    new_user["password"] = user["password"]
    return new_user

@pytest.fixture
def test_user2(client):
    user = {"email": "kkkadi8434@gmail.com", "password": "adi827193"}
    res = client.post("/users/", json=user)
    assert res.status_code == 201
    new_user = res.json()
    new_user["password"] = user["password"]
    return new_user

@pytest.fixture
def token(test_user):
    return create_access_token({"user_id": test_user["id"]})

@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }
    return client

@pytest.fixture
def test_posts(test_user, session, test_user2):
    posts_data = [{
        "title": "1st Title",
        "content": "1st Content",
        "owner_id": test_user["id"],
    },{
        "title": "2nd Title",
        "content": "2nd Content",
        "owner_id": test_user["id"],
    },{
        "title": "3rd Title",
        "content": "3rd Content",
        "owner_id": test_user["id"],
    },{
        "title": "4rd Title",
        "content": "4rd Content",
        "owner_id": test_user2["id"],
    }]
    
    def create_post_models(post_data: list[dict]):
        return models.Posts(**post_data)
    
    posts_map = map(create_post_models, posts_data)
    posts = list(posts_map)
    
    session.add_all(posts)
    session.commit()
    posts = session.query(models.Posts).all()
    
    return posts