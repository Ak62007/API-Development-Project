from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

response = client.get("/")
print(response.status_code)
print(response.json().get("message"))

def test_root():
    response = client.get("/")
    print(response.status_code)
    print(response.json().get("message"))
    assert response.status_code == 200
    assert response.json().get("message") == "hello world!!!!!!!!!!"