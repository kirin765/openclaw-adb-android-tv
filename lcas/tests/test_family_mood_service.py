from __future__ import annotations

from app.models.schemas import FamilyMoodRecordRequest
from app.services.family_mood_service import FamilyMoodService
from app.services.family_mood_store import FamilyMoodStore


def test_family_mood_service_persists_and_builds_series(tmp_path):
    store = FamilyMoodStore(str(tmp_path))
    service = FamilyMoodService(store)

    service.add_record(FamilyMoodRecordRequest(member="엄마", mood=4, note="기분 좋음"))
    service.add_record(FamilyMoodRecordRequest(member="아빠", mood=2))
    service.add_record(FamilyMoodRecordRequest(member="엄마", mood=5))

    state = service.snapshot_state()

    assert (tmp_path / "family_mood.json").exists()
    assert state.members == ["아빠", "엄마"]
    assert len(state.records) == 3
    assert any(series.member == "엄마" for series in state.series)
    assert any(series.member == "아빠" for series in state.series)
    assert any(point.count >= 1 for series in state.series for point in series.points)


def test_family_mood_service_remove_record(tmp_path):
    store = FamilyMoodStore(str(tmp_path))
    service = FamilyMoodService(store)
    record = service.add_record(FamilyMoodRecordRequest(member="아이", mood=3))

    assert service.remove_record(record.mood_record_id) is True
    assert service.remove_record(record.mood_record_id) is False
    assert service.list_records() == []
