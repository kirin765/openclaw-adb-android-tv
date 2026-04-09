from __future__ import annotations

from fastapi.testclient import TestClient

from app.main import app
from app.models.schemas import IntentPayload, TaskRecord, TaskStatus
from app.services.task_store import InMemoryTaskStore
from app.services.task_store import task_store


def test_task_store_request_cancel_marks_pending_task_canceled():
    store = InMemoryTaskStore()
    record = TaskRecord(command="유튜브 열어줘", intent=IntentPayload(intent="TV_LAUNCH_APP"))
    store.create(record)

    updated = store.request_cancel(record.task_id)

    assert updated.cancel_requested is True
    assert updated.status == TaskStatus.canceled
    assert store.is_cancel_requested(record.task_id) is True


def test_cancel_api_marks_task_canceled():
    client = TestClient(app)
    record = TaskRecord(command="유튜브 열어줘", intent=IntentPayload(intent="TV_LAUNCH_APP"))
    task_store.create(record)

    response = client.post(f"/cancel/{record.task_id}", headers={"X-API-Token": "change-me"})

    assert response.status_code == 200
    assert response.json()["status"] == "canceled"
    assert response.json()["cancel_requested"] is True
