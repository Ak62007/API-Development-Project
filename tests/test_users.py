from app import schemas
from .database import client, session
    

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
    