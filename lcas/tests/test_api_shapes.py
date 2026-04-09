from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_index_page():
    response = client.get("/")
    assert response.status_code == 200
    assert "LCAS Control Panel" in response.text


def test_mirror_state():
    response = client.get("/mirror/state")
    assert response.status_code == 200
    assert response.json()["active"] is False


def test_fridge_state():
    response = client.get("/fridge/state")
    assert response.status_code == 200
    body = response.json()
    assert "items" in body
    assert "recommendations" in body


def test_family_calendar_state():
    response = client.get("/family-calendar/state")
    assert response.status_code == 200
    body = response.json()
    assert "events" in body
    assert "today_events" in body


def test_family_board_state():
    response = client.get("/family-board/state")
    assert response.status_code == 200
    body = response.json()
    assert "posts" in body


def test_family_mood_state():
    response = client.get("/family-mood/state")
    assert response.status_code == 200
    body = response.json()
    assert "records" in body
    assert "series" in body


def test_family_todo_state():
    response = client.get("/family-todo/state")
    assert response.status_code == 200
    body = response.json()
    assert "items" in body
