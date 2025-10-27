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


def test_hero_message_exists():
    from app import app
    client = TestClient(app)
    response = client.get("/")
    assert "turn your ramblings into perfectly structured prompts" in response.text.lower()


def test_panels_grid_exists():
    from app import app
    client = TestClient(app)
    response = client.get("/")
    assert 'class="panels-grid"' in response.text or 'grid' in response.text.lower()


def test_two_panel_cards_exist():
    from app import app
    client = TestClient(app)
    response = client.get("/")
    assert response.text.count('class="panel-card"') >= 2


def test_input_panel_has_title():
    from app import app
    client = TestClient(app)
    response = client.get("/")
    assert "your ramblings" in response.text.lower()


def test_input_panel_has_textarea():
    from app import app
    client = TestClient(app)
    response = client.get("/")
    assert '<textarea' in response.text.lower()


def test_input_textarea_has_placeholder():
    from app import app
    client = TestClient(app)
    response = client.get("/")
    assert "paste or dictate your ramblings here" in response.text.lower()


def test_output_panel_has_title():
    from app import app
    client = TestClient(app)
    response = client.get("/")
    assert "structured prompt" in response.text.lower()


def test_output_panel_has_textarea():
    from app import app
    client = TestClient(app)
    response = client.get("/")
    assert response.text.count('<textarea') >= 2


def test_output_textarea_has_placeholder():
    from app import app
    client = TestClient(app)
    response = client.get("/")
    assert "your structured prompt will appear here" in response.text.lower()
