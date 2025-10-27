from fastapi.testclient import TestClient


def test_root_returns_hello_world():
    from app import app
    client = TestClient(app)
    response = client.get("/")
    assert response.status_code == 200
    assert "Hello World" in response.text
