from __future__ import annotations

import json
from pathlib import Path
from threading import Lock
from typing import Any

from app.models.schemas import FamilyMoodRecord


class FamilyMoodStore:
    def __init__(self, storage_dir: str):
        self.storage_dir = Path(storage_dir)
        self.index_path = self.storage_dir / "family_mood.json"
        self._lock = Lock()
        self._data = self._load()

    def _default_data(self) -> dict[str, Any]:
        return {"records": []}

    def _load(self) -> dict[str, Any]:
        if not self.index_path.exists():
            return self._default_data()
        try:
            data = json.loads(self.index_path.read_text(encoding="utf-8"))
            if isinstance(data, dict):
                data.setdefault("records", [])
                return data
        except Exception:
            pass
        return self._default_data()

    def _save(self) -> None:
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        self.index_path.write_text(json.dumps(self._data, ensure_ascii=False, indent=2), encoding="utf-8")

    def list_records(self) -> list[FamilyMoodRecord]:
        with self._lock:
            records = [FamilyMoodRecord.model_validate(item) for item in self._data.get("records", [])]
        return sorted(records, key=lambda record: (record.created_at, record.member), reverse=True)

    def upsert_record(self, record: FamilyMoodRecord) -> None:
        with self._lock:
            records = [item for item in self._data.setdefault("records", []) if item.get("mood_record_id") != record.mood_record_id]
            records.append(record.model_dump(mode="json"))
            self._data["records"] = records
            self._save()

    def remove_record(self, mood_record_id: str) -> bool:
        with self._lock:
            records = self._data.setdefault("records", [])
            before = len(records)
            self._data["records"] = [item for item in records if item.get("mood_record_id") != mood_record_id]
            changed = len(self._data["records"]) != before
            if changed:
                self._save()
            return changed


def build_family_mood_store(storage_dir: str) -> FamilyMoodStore:
    return FamilyMoodStore(storage_dir)
