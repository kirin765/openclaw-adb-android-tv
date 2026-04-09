from fastapi.testclient import TestClient

from app.main import app
from app.models.schemas import TvApp


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


def test_tv_apps_state(monkeypatch):
    monkeypatch.setattr(
        "app.api.routes.AdbExecutor.list_launchable_apps",
        lambda self, cancel_requested=None: [TvApp(package_name="com.netflix.ninja", label="Netflix", activity_name=".MainActivity")],
    )
    response = client.get("/tv/apps")
    assert response.status_code == 200
    body = response.json()
    assert body["apps"][0]["label"] == "Netflix"


def test_tv_standby_open(monkeypatch):
    captured = {}

    def fake_enqueue(self, task_id, intent_data, background_tasks=None):
        captured["task_id"] = task_id
        captured["intent_data"] = intent_data
        return None

    monkeypatch.setattr("app.api.routes.QueueService.enqueue", fake_enqueue)
    response = client.post("/tv/standby/open", headers={"X-API-Token": "change-me"})
    assert response.status_code == 200
    body = response.json()
    assert body["task_id"]
    assert captured["intent_data"]["intent"] == "TV_OPEN_URL"
    assert captured["intent_data"]["parameters"]["url"].endswith("/?mode=tv&view=standby")
