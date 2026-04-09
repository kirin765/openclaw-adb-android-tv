from __future__ import annotations

from dataclasses import dataclass
from threading import Lock

from app.models.schemas import MirrorState


@dataclass
class _MirrorRecord:
    active: bool = False
    source_label: str = ""
    frame_data_url: str | None = None
    started_at: str | None = None
    updated_at: str | None = None
    frame_count: int = 0


class MirrorStore:
    def __init__(self) -> None:
        self._lock = Lock()
        self._state = _MirrorRecord()

    def snapshot(self) -> MirrorState:
        with self._lock:
            return MirrorState(
                active=self._state.active,
                source_label=self._state.source_label,
                frame_data_url=self._state.frame_data_url,
                started_at=self._state.started_at,
                updated_at=self._state.updated_at,
                frame_count=self._state.frame_count,
            )

    def start(self, source_label: str, started_at: str | None = None) -> MirrorState:
        with self._lock:
            self._state.active = True
            self._state.source_label = source_label
            self._state.started_at = started_at
            self._state.updated_at = started_at
            self._state.frame_data_url = None
            self._state.frame_count = 0
            return MirrorState(
                active=self._state.active,
                source_label=self._state.source_label,
                frame_data_url=self._state.frame_data_url,
                started_at=self._state.started_at,
                updated_at=self._state.updated_at,
                frame_count=self._state.frame_count,
            )

    def upsert_frame(self, frame_data_url: str, source_label: str = "", started_at: str | None = None) -> MirrorState:
        with self._lock:
            self._state.active = True
            if source_label:
                self._state.source_label = source_label
            if started_at and not self._state.started_at:
                self._state.started_at = started_at
            self._state.frame_data_url = frame_data_url
            self._state.updated_at = started_at or self._state.updated_at
            self._state.frame_count += 1
            return MirrorState(
                active=self._state.active,
                source_label=self._state.source_label,
                frame_data_url=self._state.frame_data_url,
                started_at=self._state.started_at,
                updated_at=self._state.updated_at,
                frame_count=self._state.frame_count,
            )

    def stop(self) -> MirrorState:
        with self._lock:
            self._state.active = False
            self._state.frame_data_url = None
            return MirrorState(
                active=self._state.active,
                source_label=self._state.source_label,
                frame_data_url=self._state.frame_data_url,
                started_at=self._state.started_at,
                updated_at=self._state.updated_at,
                frame_count=self._state.frame_count,
            )


mirror_store = MirrorStore()
