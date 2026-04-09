from __future__ import annotations

from app.models.schemas import FamilyTodoItemRequest
from app.services.family_todo_service import FamilyTodoService
from app.services.family_todo_store import FamilyTodoStore


def test_family_todo_service_persists_and_orders_items(tmp_path):
    store = FamilyTodoStore(str(tmp_path))
    service = FamilyTodoService(store)

    service.add_item(FamilyTodoItemRequest(title="세탁기 돌리기", owner="엄마"))
    service.add_item(FamilyTodoItemRequest(title="장보기", owner="아빠", due_at="2026-04-10T19:00"))
    service.add_item(FamilyTodoItemRequest(title="분리수거", owner="아이"))

    state = service.snapshot_state()

    assert (tmp_path / "family_todo.json").exists()
    assert state.items[0].title == "장보기"
    assert {item.title for item in state.items[1:]} == {"세탁기 돌리기", "분리수거"}
    assert all(item.done is False for item in state.items)


def test_family_todo_service_toggle_and_remove_item(tmp_path):
    store = FamilyTodoStore(str(tmp_path))
    service = FamilyTodoService(store)
    item = service.add_item(FamilyTodoItemRequest(title="청소", owner="가족"))

    assert service.set_done(item.todo_item_id, True) is True
    updated = next(entry for entry in service.list_items() if entry.todo_item_id == item.todo_item_id)
    assert updated.done is True

    assert service.remove_item(item.todo_item_id) is True
    assert service.remove_item(item.todo_item_id) is False
    assert service.list_items() == []
