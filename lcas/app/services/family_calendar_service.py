from __future__ import annotations

import json
from datetime import datetime, timedelta
from pathlib import Path
from threading import Lock
from typing import Any
from uuid import uuid4

from app.models.schemas import (
    FamilyCalendarEvent,
    FamilyCalendarEventRequest,
    FamilyCalendarStateResponse,
)


class FamilyCalendarService:
    def __init__(self, storage_dir: str):
        self.storage_dir = Path(storage_dir)
        self.index_path = self.storage_dir / "family_calendar.json"
        self._lock = Lock()
        self._data = self._load()

    def _default_data(self) -> dict[str, Any]:
        return {"events": []}

    def _load(self) -> dict[str, Any]:
        if not self.index_path.exists():
            return self._default_data()
        try:
            data = json.loads(self.index_path.read_text(encoding="utf-8"))
            if isinstance(data, dict):
                data.setdefault("events", [])
                return data
        except Exception:
            pass
        return self._default_data()

    def _save(self) -> None:
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        self.index_path.write_text(json.dumps(self._data, ensure_ascii=False, indent=2), encoding="utf-8")

    def list_events(self) -> list[FamilyCalendarEvent]:
        with self._lock:
            events = [FamilyCalendarEvent.model_validate(item) for item in self._data.get("events", [])]
        return sorted(events, key=lambda event: (event.start_at, event.title))

    def add_event(self, request: FamilyCalendarEventRequest) -> FamilyCalendarEvent:
        title = request.title.strip()
        if not title:
            raise ValueError("제목을 입력하세요.")
        start_at = request.start_at.strip()
        if not start_at:
            raise ValueError("시작 시간을 입력하세요.")

        attendees = [part.strip() for part in request.attendees.split(",") if part.strip()]
        now = self._now_iso()
        event = FamilyCalendarEvent(
            calendar_event_id=str(uuid4()),
            title=title,
            start_at=start_at,
            end_at=request.end_at.strip(),
            location=request.location.strip(),
            attendees=attendees,
            tag=request.tag,
            note=request.note.strip(),
            all_day=request.all_day,
            created_at=now,
            updated_at=now,
        )
        with self._lock:
            self._data.setdefault("events", []).append(event.model_dump(mode="json"))
            self._save()
        return event

    def remove_event(self, calendar_event_id: str) -> bool:
        with self._lock:
            events = self._data.setdefault("events", [])
            before = len(events)
            self._data["events"] = [item for item in events if item.get("calendar_event_id") != calendar_event_id]
            changed = len(self._data["events"]) != before
            if changed:
                self._save()
            return changed

    def snapshot_state(self) -> FamilyCalendarStateResponse:
        events = self.list_events()
        today_events = self._today_events(events)
        upcoming_events = self._upcoming_events(events)
        return FamilyCalendarStateResponse(
            events=events,
            today_events=today_events,
            upcoming_events=upcoming_events,
            checked_at=self._now_iso(),
        )

    def _today_events(self, events: list[FamilyCalendarEvent]) -> list[FamilyCalendarEvent]:
        today_prefix = datetime.now().strftime("%Y-%m-%d")
        return [event for event in events if event.start_at.startswith(today_prefix)]

    def _upcoming_events(self, events: list[FamilyCalendarEvent], days: int = 7) -> list[FamilyCalendarEvent]:
        now = datetime.now()
        start_of_today = now.replace(hour=0, minute=0, second=0, microsecond=0)
        cutoff = start_of_today + timedelta(days=days)
        upcoming: list[FamilyCalendarEvent] = []
        for event in events:
            start = self._parse_datetime(event.start_at)
            if start is None:
                continue
            if start_of_today <= start <= cutoff:
                upcoming.append(event)
        return upcoming[:10]

    def _parse_datetime(self, value: str) -> datetime | None:
        try:
            return datetime.fromisoformat(value)
        except ValueError:
            return None

    def _now_iso(self) -> str:
        return datetime.now().isoformat(timespec="seconds")


def build_family_calendar_service(storage_dir: str) -> FamilyCalendarService:
    return FamilyCalendarService(storage_dir)
