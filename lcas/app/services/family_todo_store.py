from __future__ import annotations

import json
from pathlib import Path
from threading import Lock
from typing import Any

from app.models.schemas import FamilyTodoItem


class FamilyTodoStore:
    def __init__(self, storage_dir: str):
        self.storage_dir = Path(storage_dir)
        self.index_path = self.storage_dir / "family_todo.json"
        self._lock = Lock()
        self._data = self._load()

    def _default_data(self) -> dict[str, Any]:
        return {"items": []}

    def _load(self) -> dict[str, Any]:
        if not self.index_path.exists():
            return self._default_data()
        try:
            data = json.loads(self.index_path.read_text(encoding="utf-8"))
            if isinstance(data, dict):
                data.setdefault("items", [])
                return data
        except Exception:
            pass
        return self._default_data()

    def _save(self) -> None:
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        self.index_path.write_text(json.dumps(self._data, ensure_ascii=False, indent=2), encoding="utf-8")

    def list_items(self) -> list[FamilyTodoItem]:
        with self._lock:
            items = [FamilyTodoItem.model_validate(item) for item in self._data.get("items", [])]
        return sorted(
            items,
            key=lambda item: (
                item.done,
                self._sort_due_at(item.due_at),
                item.created_at,
                item.title,
            ),
        )

    def upsert_item(self, item: FamilyTodoItem) -> None:
        with self._lock:
            items = [existing for existing in self._data.setdefault("items", []) if existing.get("todo_item_id") != item.todo_item_id]
            items.append(item.model_dump(mode="json"))
            self._data["items"] = items
            self._save()

    def remove_item(self, todo_item_id: str) -> bool:
        with self._lock:
            items = self._data.setdefault("items", [])
            before = len(items)
            self._data["items"] = [item for item in items if item.get("todo_item_id") != todo_item_id]
            changed = len(self._data["items"]) != before
            if changed:
                self._save()
            return changed

    def _sort_due_at(self, value: str) -> str:
        return value or "9999-12-31T23:59:59"


def build_family_todo_store(storage_dir: str) -> FamilyTodoStore:
    return FamilyTodoStore(storage_dir)
