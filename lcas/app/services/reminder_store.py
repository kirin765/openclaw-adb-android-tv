from __future__ import annotations

from dataclasses import dataclass, field
from threading import Lock
from typing import Any


@dataclass
class ReminderState:
    reminders: dict[str, dict[str, Any]] = field(default_factory=dict)


class ReminderStore:
    def __init__(self) -> None:
        self._lock = Lock()
        self._state = ReminderState()

    def snapshot(self) -> list[dict[str, Any]]:
        with self._lock:
            return [dict(item) for item in self._state.reminders.values()]

    def upsert(self, reminder: dict[str, Any]) -> None:
        with self._lock:
            self._state.reminders[str(reminder["reminder_id"])] = dict(reminder)

    def get(self, reminder_id: str) -> dict[str, Any] | None:
        with self._lock:
            reminder = self._state.reminders.get(reminder_id)
            return dict(reminder) if reminder else None

    def remove(self, reminder_id: str) -> None:
        with self._lock:
            self._state.reminders.pop(reminder_id, None)


reminder_store = ReminderStore()
