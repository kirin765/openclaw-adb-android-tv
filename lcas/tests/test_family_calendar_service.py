from __future__ import annotations

from app.models.schemas import FamilyCalendarEventRequest
from app.services.family_calendar_service import FamilyCalendarService


def test_family_calendar_service_persists_and_sorts(tmp_path):
    service = FamilyCalendarService(str(tmp_path))

    service.add_event(
        FamilyCalendarEventRequest(
            title="저녁 약속",
            start_at="2026-04-10T19:00",
            end_at="2026-04-10T21:00",
            attendees="엄마, 아빠",
            tag="김은영똥",
            location="집",
            note="외식",
        )
    )
    service.add_event(
        FamilyCalendarEventRequest(
            title="아침 등원",
            start_at="2026-04-10T08:30",
            attendees="아이",
        )
    )

    state = service.snapshot_state()

    assert (tmp_path / "family_calendar.json").exists()
    assert [event.title for event in state.events] == ["아침 등원", "저녁 약속"]
    assert state.events[0].tag == "김은영똥"
    assert len(state.today_events) == 2
    assert len(state.upcoming_events) == 2


def test_family_calendar_service_remove_event(tmp_path):
    service = FamilyCalendarService(str(tmp_path))
    event = service.add_event(FamilyCalendarEventRequest(title="회의", start_at="2026-04-10T10:00"))

    assert service.remove_event(event.calendar_event_id) is True
    assert service.remove_event(event.calendar_event_id) is False
    assert service.list_events() == []
