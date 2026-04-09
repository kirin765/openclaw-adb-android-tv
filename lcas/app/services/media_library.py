from __future__ import annotations

import base64
import json
from pathlib import Path
from threading import Lock
from typing import Any
from uuid import uuid4

from app.models.schemas import FavoriteVideoLink, MediaItem, MediaKind


class MediaLibrary:
    def __init__(self, storage_dir: str):
        self.storage_dir = Path(storage_dir)
        self.upload_dir = self.storage_dir / "uploads"
        self.index_path = self.storage_dir / "media_library.json"
        self.upload_dir.mkdir(parents=True, exist_ok=True)
        self._lock = Lock()
        self._data = self._load()

    def _default_data(self) -> dict[str, Any]:
        return {"uploads": [], "favorites": []}

    def _load(self) -> dict[str, Any]:
        if not self.index_path.exists():
            return self._default_data()
        try:
            return json.loads(self.index_path.read_text(encoding="utf-8"))
        except Exception:
            return self._default_data()

    def _save(self) -> None:
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        self.index_path.write_text(json.dumps(self._data, ensure_ascii=False, indent=2), encoding="utf-8")

    def _kind_for_content_type(self, content_type: str, filename: str) -> MediaKind:
        ext = filename.lower().rsplit(".", 1)[-1] if "." in filename else ""
        if content_type.startswith("video/") or ext in {"mp4", "webm", "mov", "mkv", "avi"}:
            return MediaKind.video
        if content_type.startswith("audio/") or ext in {"mp3", "wav", "ogg", "m4a", "flac"}:
            return MediaKind.audio
        if content_type.startswith("image/") or ext in {"jpg", "jpeg", "png", "gif", "webp", "bmp"}:
            return MediaKind.image
        return MediaKind.file

    def list_uploads(self) -> list[MediaItem]:
        return [MediaItem.model_validate(item) for item in self._data.get("uploads", [])]

    def list_favorites(self) -> list[FavoriteVideoLink]:
        return [FavoriteVideoLink.model_validate(item) for item in self._data.get("favorites", [])]

    def add_favorite(self, title: str, url: str) -> FavoriteVideoLink:
        with self._lock:
            item = FavoriteVideoLink(title=title, url=url, created_at=self._now_iso())
            self._data.setdefault("favorites", []).append(item.model_dump())
            self._save()
            return item

    def remove_favorite(self, favorite_id: str) -> bool:
        with self._lock:
            favorites = self._data.setdefault("favorites", [])
            before = len(favorites)
            self._data["favorites"] = [item for item in favorites if item.get("favorite_id") != favorite_id]
            changed = len(self._data["favorites"]) != before
            if changed:
                self._save()
            return changed

    def add_upload(self, filename: str, content_type: str, data_base64: str) -> MediaItem:
        with self._lock:
            raw = base64.b64decode(data_base64)
            stored_name = f"{uuid4()}-{Path(filename).name}"
            target = self.upload_dir / stored_name
            target.write_bytes(raw)
            item = MediaItem(
                original_name=Path(filename).name,
                stored_name=stored_name,
                content_type=content_type or "application/octet-stream",
                kind=self._kind_for_content_type(content_type or "application/octet-stream", filename),
                size_bytes=len(raw),
                url=f"/media-files/{stored_name}",
                created_at=self._now_iso(),
            )
            self._data.setdefault("uploads", []).append(item.model_dump())
            self._save()
            return item

    def get_upload(self, media_id: str) -> MediaItem | None:
        for item in self.list_uploads():
            if item.media_id == media_id:
                return item
        return None

    def _now_iso(self) -> str:
        from datetime import datetime, timezone

        return datetime.now(timezone.utc).isoformat()


def build_media_library(storage_dir: str) -> MediaLibrary:
    return MediaLibrary(storage_dir)
