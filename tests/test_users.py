import pytest
from app import schemas
from app.config import settings
from jose import JWTError, jwt
    

def test_root(client):
    response = client.get("/")
    print(response.status_code)
    print(response.json().get("message"))
    assert response.status_code == 200
    assert response.json().get("message") == "hello world!!!!!!!!!!"
    
def test_create_user(client):
    res = client.post("/users/", json={"email": "kkadi8434367970@gmail.com", "password": "adi827193"})
    user = schemas.UserRes(**res.json())
    print(user)
    assert res.status_code == 201
    
def test_login_user(client, test_user):
    res = client.post(
        "/login", data={"username": test_user["email"], "password": test_user["password"]}
    )
    token = schemas.Token(**res.json())
    payload = jwt.decode(token.access_token, settings.secret_key, algorithms=[settings.algorithm])
    id: str = payload.get("user_id")
    assert id == test_user["id"]
    assert token.type == "bearer"
    assert res.status_code == 200
    

@pytest.mark.parametrize("email, password, status_code",[
    ("kkadi8434367970@gmail.com", "oyeee", 403),
    ("oyeee", "adi827193", 403),
    ("kkadi8434367970@gmail.com", None, 403),
    (None, "adi827193", 403)
])
def test_inc_login(test_user, client, email, password, status_code):
    res = client.post("/login", data = {"username": email, "password": password})
    
    assert res.status_code == status_code
    # assert res.json().get("detail") == "Invalid Credentials"