from fastapi.testclient import TestClient
import pytest
from app.main import app
from app.database import get_db, Base
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
    print(res.json())
    new_user = res.json()
    new_user["password"] = user["password"]
    return new_user