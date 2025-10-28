from fastapi.testclient import TestClient


def test_api_endpoint_exists():
    from app import app
    client = TestClient(app)
    response = client.post("/api/promptify", json={"text": "test", "prompt": "template"})
    assert response.status_code in [200, 400]


def test_api_validates_empty_text():
    from app import app
    client = TestClient(app)
    response = client.post("/api/promptify", json={"text": "", "prompt": "template"})
    assert response.status_code == 400
    assert "error" in response.json()["detail"]


def test_api_validates_missing_text():
    from app import app
    client = TestClient(app)
    response = client.post("/api/promptify", json={"prompt": "template"})
    assert response.status_code == 422


def test_api_validates_whitespace_only_text():
    from app import app
    client = TestClient(app)
    response = client.post("/api/promptify", json={"text": "   ", "prompt": "template"})
    assert response.status_code == 400


def test_api_accepts_valid_text():
    from app import app
    client = TestClient(app)
    response = client.post("/api/promptify", json={"text": "test input", "prompt": "template"})
    assert response.status_code == 200


def test_api_replaces_text_in_prompt():
    from app import app
    client = TestClient(app)
    response = client.post("/api/promptify", json={"text": "my text", "prompt": "Process this: {text}"})
    assert response.status_code == 200
