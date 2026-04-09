from __future__ import annotations

from app.models.schemas import MirrorState
from app.services.mirror_store import mirror_store


class MirrorService:
    def get_state(self) -> MirrorState:
        return mirror_store.snapshot()

    def start(self, source_label: str, started_at: str | None = None) -> MirrorState:
        return mirror_store.start(source_label, started_at)

    def update_frame(self, frame_data_url: str, source_label: str = "", started_at: str | None = None) -> MirrorState:
        return mirror_store.upsert_frame(frame_data_url, source_label, started_at)

    def stop(self) -> MirrorState:
        return mirror_store.stop()


mirror_service = MirrorService()
