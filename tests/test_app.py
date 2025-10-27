from fastapi.testclient import TestClient


def test_root_returns_hello_world():
    from app import app
    client = TestClient(app)
    response = client.get("/")
    assert response.status_code == 200
    assert "Hello World" in response.text


def test_page_includes_picocss():
    from app import app
    client = TestClient(app)
    response = client.get("/")
    assert "picocss" in response.text.lower()


def test_page_includes_inter_font():
    from app import app
    client = TestClient(app)
    response = client.get("/")
    assert "inter" in response.text.lower()


def test_page_has_html_structure():
    from app import app
    client = TestClient(app)
    response = client.get("/")
    assert "<html" in response.text.lower()
    assert "<head" in response.text.lower()
    assert "<body" in response.text.lower()


def test_header_exists():
    from app import app
    client = TestClient(app)
    response = client.get("/")
    assert "<header" in response.text.lower()


def test_header_contains_logo():
    from app import app
    client = TestClient(app)
    response = client.get("/")
    assert "promptify_logo.png" in response.text.lower()
    assert "<img" in response.text.lower()


def test_header_contains_title():
    from app import app
    client = TestClient(app)
    response = client.get("/")
    html = response.text.lower()
    assert "<header" in html
    assert "promptify" in html
