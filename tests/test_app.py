from fastapi.testclient import TestClient


def test_page_includes_picocss():
    from app import app
    client = TestClient(app)
    response = client.get("/promptify")
    assert response.status_code == 200
    assert "picocss" in response.text.lower()


def test_page_includes_inter_font():
    from app import app
    client = TestClient(app)
    response = client.get("/promptify")
    assert response.status_code == 200
    assert "inter" in response.text.lower()


def test_page_has_html_structure():
    from app import app
    client = TestClient(app)
    response = client.get("/promptify")
    assert response.status_code == 200
    assert "<html" in response.text.lower()
    assert "<head" in response.text.lower()
    assert "<body" in response.text.lower()


def test_header_exists():
    from app import app
    client = TestClient(app)
    response = client.get("/promptify")
    assert response.status_code == 200
    assert "<header" in response.text.lower()


def test_header_contains_logo():
    from app import app
    client = TestClient(app)
    response = client.get("/promptify")
    assert response.status_code == 200
    assert "promptify_logo.png" in response.text.lower()
    assert "<img" in response.text.lower()


def test_header_contains_title():
    from app import app
    client = TestClient(app)
    response = client.get("/promptify")
    assert response.status_code == 200
    html = response.text.lower()
    assert "<header" in html
    assert "promptify" in html


def test_hero_message_exists():
    from app import app
    client = TestClient(app)
    response = client.get("/promptify")
    assert response.status_code == 200
    assert "turn your ramblings into perfectly structured prompts" in response.text.lower()


def test_panels_grid_exists():
    from app import app
    client = TestClient(app)
    response = client.get("/promptify")
    assert response.status_code == 200
    assert 'class="panels-grid"' in response.text or 'grid' in response.text.lower()


def test_two_panel_cards_exist():
    from app import app
    client = TestClient(app)
    response = client.get("/promptify")
    assert response.status_code == 200
    assert response.text.count('class="panel-card"') >= 2


def test_input_panel_has_title():
    from app import app
    client = TestClient(app)
    response = client.get("/promptify")
    assert response.status_code == 200
    assert "your ramblings" in response.text.lower()


def test_input_panel_has_textarea():
    from app import app
    client = TestClient(app)
    response = client.get("/promptify")
    assert response.status_code == 200
    assert '<textarea' in response.text.lower()


def test_input_textarea_has_placeholder():
    from app import app
    client = TestClient(app)
    response = client.get("/promptify")
    assert response.status_code == 200
    assert "paste or dictate your ramblings here" in response.text.lower()


def test_output_panel_has_title():
    from app import app
    client = TestClient(app)
    response = client.get("/promptify")
    assert response.status_code == 200
    assert "structured prompt" in response.text.lower()


def test_output_panel_has_textarea():
    from app import app
    client = TestClient(app)
    response = client.get("/promptify")
    assert response.status_code == 200
    assert response.text.count('<textarea') >= 2


def test_output_textarea_has_placeholder():
    from app import app
    client = TestClient(app)
    response = client.get("/promptify")
    assert response.status_code == 200
    assert "your structured prompt will appear here" in response.text.lower()


def test_promptify_button_exists():
    from app import app
    client = TestClient(app)
    response = client.get("/promptify")
    assert response.status_code == 200
    assert "<button" in response.text.lower()
    assert "promptify" in response.text.lower()


def test_copy_button_exists():
    from app import app
    client = TestClient(app)
    response = client.get("/promptify")
    assert response.status_code == 200
    assert response.text.count("<button") >= 2
    assert "copy" in response.text.lower()


def test_root_redirects_to_promptify():
    from app import app
    client = TestClient(app, follow_redirects=False)
    response = client.get("/")
    assert response.status_code == 307
    assert response.headers["location"] == "/promptify"


def test_promptify_path_serves_app():
    from app import app
    client = TestClient(app)
    response = client.get("/promptify")
    assert response.status_code == 200
    assert "promptify" in response.text.lower()
