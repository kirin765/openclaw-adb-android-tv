from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from threading import Lock, Timer
from uuid import uuid4

from app.models.schemas import IntentPayload, TaskResult
from app.services.action_mapper import ActionMapper


@dataclass
class PowerSchedule:
    timer_id: str
    due_at: str
    minutes: int


class PowerService:
    def __init__(self) -> None:
        self._lock = Lock()
        self._timers: dict[str, Timer] = {}
        self._schedules: dict[str, PowerSchedule] = {}

    def power_off_now(self) -> TaskResult:
        mapper = ActionMapper()
        intent = IntentPayload(intent="TV_POWER_OFF", target_device="android_tv")
        return mapper.execute(intent)

    def power_on_now(self) -> TaskResult:
        mapper = ActionMapper()
        intent = IntentPayload(intent="TV_POWER_ON", target_device="android_tv")
        return mapper.execute(intent)

    def wake_screen_now(self) -> TaskResult:
        mapper = ActionMapper()
        intent = IntentPayload(intent="TV_WAKE_SCREEN", target_device="android_tv")
        return mapper.execute(intent)

    def schedule_power_off(self, minutes: int) -> PowerSchedule:
        timer_id = str(uuid4())
        due_at_dt = datetime.now(timezone.utc) + timedelta(minutes=minutes)
        schedule = PowerSchedule(timer_id=timer_id, due_at=due_at_dt.isoformat(), minutes=minutes)

        def run() -> None:
            try:
                self.power_off_now()
            finally:
                with self._lock:
                    self._timers.pop(timer_id, None)
                    self._schedules.pop(timer_id, None)

        timer = Timer(minutes * 60, run)
        timer.daemon = True
        with self._lock:
            self._timers[timer_id] = timer
            self._schedules[timer_id] = schedule
        timer.start()
        return schedule

    def list_schedules(self) -> list[PowerSchedule]:
        with self._lock:
            return list(self._schedules.values())

    def cancel_schedule(self, timer_id: str) -> bool:
        with self._lock:
            timer = self._timers.pop(timer_id, None)
            self._schedules.pop(timer_id, None)
        if timer:
            timer.cancel()
            return True
        return False


power_service = PowerService()
