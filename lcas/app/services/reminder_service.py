from __future__ import annotations

from datetime import datetime, timezone
from threading import Lock, Timer
from uuid import uuid4
from zoneinfo import ZoneInfo

from app.core.settings import get_settings
from app.models.schemas import ReminderItem, ReminderRequest, ReminderStatus
from app.services.power_service import power_service
from app.services.reminder_hub import reminder_hub
from app.services.reminder_store import reminder_store


class ReminderService:
    def __init__(self) -> None:
        self._lock = Lock()
        self._timers: dict[str, Timer] = {}

    def _timezone(self) -> ZoneInfo:
        settings = get_settings()
        return ZoneInfo(settings.default_timezone)

    def _parse_due_at(self, due_at: str) -> datetime:
        parsed = datetime.fromisoformat(due_at)
        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=self._timezone())
        return parsed

    def schedule_reminder(self, payload: ReminderRequest) -> ReminderItem:
        reminder_id = str(uuid4())
        due_at_dt = self._parse_due_at(payload.due_at)
        now = datetime.now(timezone.utc)
        delay = max(0.0, (due_at_dt.astimezone(timezone.utc) - now).total_seconds())
        reminder = ReminderItem(
            reminder_id=reminder_id,
            title=payload.title,
            due_at=due_at_dt.isoformat(),
            note=payload.note,
            created_at=now.isoformat(),
            status=ReminderStatus.scheduled,
            power_on=payload.power_on,
            wake_screen=payload.wake_screen,
        )
        reminder_store.upsert(reminder.model_dump())

        def run() -> None:
            try:
                self._fire_reminder(reminder_id)
            finally:
                with self._lock:
                    self._timers.pop(reminder_id, None)

        timer = Timer(delay, run)
        timer.daemon = True
        with self._lock:
            self._timers[reminder_id] = timer
        timer.start()
        return reminder

    def _fire_reminder(self, reminder_id: str) -> None:
        stored = reminder_store.get(reminder_id)
        if not stored or stored.get("status") != ReminderStatus.scheduled:
            return
        reminder = ReminderItem.model_validate(stored)
        reminder.status = ReminderStatus.fired
        reminder.fired_at = datetime.now(timezone.utc).isoformat()
        reminder_store.upsert(reminder.model_dump())

        if reminder.power_on:
            try:
                power_service.power_on_now()
            except Exception:
                pass
        if reminder.wake_screen:
            try:
                power_service.wake_screen_now()
            except Exception:
                pass

        reminder_hub.broadcast_from_thread({"type": "reminder-fired", "reminder": reminder.model_dump()})

    def list_reminders(self) -> list[ReminderItem]:
        reminders = [ReminderItem.model_validate(item) for item in reminder_store.snapshot()]
        return sorted(reminders, key=lambda item: (item.due_at, item.created_at))

    def cancel_reminder(self, reminder_id: str) -> bool:
        with self._lock:
            timer = self._timers.pop(reminder_id, None)
        if timer:
            timer.cancel()
        stored = reminder_store.get(reminder_id)
        if not stored:
            return False
        reminder = ReminderItem.model_validate(stored)
        reminder.status = ReminderStatus.canceled
        reminder_store.upsert(reminder.model_dump())
        return True

    def remove_reminder(self, reminder_id: str) -> bool:
        with self._lock:
            timer = self._timers.pop(reminder_id, None)
        if timer:
            timer.cancel()
        stored = reminder_store.get(reminder_id)
        if not stored:
            return False
        reminder_store.remove(reminder_id)
        return True


reminder_service = ReminderService()
