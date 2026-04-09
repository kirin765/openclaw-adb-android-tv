from __future__ import annotations

from app.models.schemas import TaskResult
from app.services import power_service as power_service_module
from app.services.power_service import PowerService


def test_power_service_schedule_executes_and_clears(monkeypatch):
    executed = []

    class FakeMapper:
        def execute(self, intent, cancel_requested=None):
            executed.append(intent.intent)
            return TaskResult(message="ok", device="livingroom-tv")

    class FakeTimer:
        def __init__(self, seconds, callback):
            self.seconds = seconds
            self.callback = callback
            self.daemon = False

        def start(self):
            self.callback()

        def cancel(self):
            executed.append("cancel")

    monkeypatch.setattr(power_service_module, "ActionMapper", lambda: FakeMapper())
    monkeypatch.setattr(power_service_module, "Timer", FakeTimer)

    service = PowerService()
    schedule = service.schedule_power_off(1)

    assert schedule.minutes == 1
    assert executed == ["TV_POWER_OFF"]
    assert service.list_schedules() == []


def test_reminder_service_fires_and_wakes(monkeypatch):
    from app.services import reminder_service as reminder_service_module
    from app.services.reminder_service import ReminderService
    from app.models.schemas import ReminderRequest, TaskResult

    fired = []

    class FakeTimer:
        def __init__(self, seconds, callback):
            self.seconds = seconds
            self.callback = callback
            self.daemon = False

        def start(self):
            self.callback()

        def cancel(self):
            fired.append("cancel")

    class FakePowerService:
        def power_on_now(self):
            fired.append("power_on")
            return TaskResult(message="power on", device="livingroom-tv")

        def wake_screen_now(self):
            fired.append("wake")
            return TaskResult(message="wake", device="livingroom-tv")

    reminder_events = []

    monkeypatch.setattr(reminder_service_module, "Timer", FakeTimer)
    monkeypatch.setattr(reminder_service_module, "power_service", FakePowerService())
    monkeypatch.setattr(reminder_service_module.reminder_hub, "broadcast_from_thread", lambda payload: reminder_events.append(payload))

    service = ReminderService()
    reminder = service.schedule_reminder(
        ReminderRequest(
            title="회의",
            due_at="2026-04-10T12:00",
            note="출발 준비",
            power_on=True,
            wake_screen=True,
        )
    )

    reminders = service.list_reminders()
    assert reminder.title == "회의"
    assert reminder.status.value == "scheduled"
    assert fired == ["power_on", "wake"]
    assert reminder_events and reminder_events[0]["type"] == "reminder-fired"
    assert reminders[0].status.value == "fired"
