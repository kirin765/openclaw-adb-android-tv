from __future__ import annotations

import hashlib
from collections import defaultdict
from datetime import date, datetime, timedelta, timezone

from app.models.schemas import (
    FamilyMoodChartPoint,
    FamilyMoodRecord,
    FamilyMoodRecordRequest,
    FamilyMoodSeries,
    FamilyMoodStateResponse,
)
from app.services.family_mood_store import FamilyMoodStore


class FamilyMoodService:
    def __init__(self, store: FamilyMoodStore):
        self._store = store
        self._palette = [
            "#c084fc",
            "#60a5fa",
            "#34d399",
            "#f59e0b",
            "#f472b6",
            "#f87171",
        ]

    def list_records(self) -> list[FamilyMoodRecord]:
        return self._store.list_records()

    def snapshot_state(self) -> FamilyMoodStateResponse:
        records = self.list_records()
        return FamilyMoodStateResponse(
            records=records,
            series=self._build_series(records),
            members=self._unique_members(records),
            checked_at=self._now_iso(),
        )

    def add_record(self, payload: FamilyMoodRecordRequest) -> FamilyMoodRecord:
        member = payload.member.strip()
        if not member:
            raise ValueError("가족 구성원 이름을 입력하세요.")
        note = payload.note.strip()
        record = FamilyMoodRecord(
            mood_record_id=self._new_id(),
            member=member,
            mood=payload.mood,
            note=note,
            created_at=self._now_iso(),
        )
        self._store.upsert_record(record)
        return record

    def remove_record(self, mood_record_id: str) -> bool:
        return self._store.remove_record(mood_record_id)

    def _build_series(self, records: list[FamilyMoodRecord], days: int = 14) -> list[FamilyMoodSeries]:
        cutoff = date.today() - timedelta(days=days - 1)
        daily: dict[str, dict[str, list[int]]] = defaultdict(lambda: defaultdict(list))
        for record in records:
            created = self._parse_date(record.created_at)
            if created is None or created < cutoff:
                continue
            daily[record.member][created.isoformat()].append(record.mood)

        series: list[FamilyMoodSeries] = []
        for member in sorted(daily.keys()):
            points: list[FamilyMoodChartPoint] = []
            member_days = daily[member]
            for offset in range(days):
                current_day = cutoff + timedelta(days=offset)
                moods = member_days.get(current_day.isoformat())
                if not moods:
                    continue
                points.append(
                    FamilyMoodChartPoint(
                        date=current_day.isoformat(),
                        mood=sum(moods) / len(moods),
                        count=len(moods),
                    )
                )
            series.append(FamilyMoodSeries(member=member, color=self._color_for(member), points=points))
        return series

    def _unique_members(self, records: list[FamilyMoodRecord]) -> list[str]:
        members = sorted({record.member for record in records})
        return members

    def _color_for(self, member: str) -> str:
        digest = hashlib.sha1(member.encode("utf-8")).hexdigest()
        index = int(digest[:8], 16) % len(self._palette)
        return self._palette[index]

    def _parse_date(self, value: str) -> date | None:
        try:
            return datetime.fromisoformat(value).date()
        except ValueError:
            return None

    def _new_id(self) -> str:
        from uuid import uuid4

        return str(uuid4())

    def _now_iso(self) -> str:
        return datetime.now(timezone.utc).isoformat(timespec="seconds")


def build_family_mood_service(store: FamilyMoodStore) -> FamilyMoodService:
    return FamilyMoodService(store)
