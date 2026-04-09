from __future__ import annotations

from datetime import datetime
from uuid import uuid4

from app.models.schemas import FamilyTodoItem, FamilyTodoItemRequest, FamilyTodoStateResponse
from app.services.family_todo_store import FamilyTodoStore


class FamilyTodoService:
    def __init__(self, store: FamilyTodoStore):
        self._store = store

    def list_items(self) -> list[FamilyTodoItem]:
        return self._store.list_items()

    def snapshot_state(self) -> FamilyTodoStateResponse:
        return FamilyTodoStateResponse(items=self.list_items(), checked_at=self._now_iso())

    def add_item(self, payload: FamilyTodoItemRequest) -> FamilyTodoItem:
        title = payload.title.strip()
        if not title:
            raise ValueError("할 일 제목을 입력하세요.")
        now = self._now_iso()

        item = FamilyTodoItem(
            todo_item_id=str(uuid4()),
            title=title,
            owner=payload.owner.strip(),
            due_at=payload.due_at.strip(),
            note=payload.note.strip(),
            done=False,
            created_at=now,
            updated_at=now,
        )
        self._store.upsert_item(item)
        return item

    def set_done(self, todo_item_id: str, done: bool) -> bool:
        items = self.list_items()
        for item in items:
            if item.todo_item_id == todo_item_id:
                updated = item.model_copy(update={"done": done, "updated_at": self._now_iso()})
                self._store.upsert_item(updated)
                return True
        return False

    def remove_item(self, todo_item_id: str) -> bool:
        return self._store.remove_item(todo_item_id)

    def _now_iso(self) -> str:
        return datetime.now().isoformat(timespec="seconds")


def build_family_todo_service(store: FamilyTodoStore) -> FamilyTodoService:
    return FamilyTodoService(store)
