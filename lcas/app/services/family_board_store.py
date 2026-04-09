from __future__ import annotations

import json
from pathlib import Path
from threading import Lock
from typing import Any

from app.models.schemas import FamilyBoardPost


class FamilyBoardStore:
    def __init__(self, storage_dir: str):
        self.storage_dir = Path(storage_dir)
        self.index_path = self.storage_dir / "family_board.json"
        self._lock = Lock()
        self._data = self._load()

    def _default_data(self) -> dict[str, Any]:
        return {"posts": []}

    def _load(self) -> dict[str, Any]:
        if not self.index_path.exists():
            return self._default_data()
        try:
            data = json.loads(self.index_path.read_text(encoding="utf-8"))
            if isinstance(data, dict):
                data.setdefault("posts", [])
                return data
        except Exception:
            pass
        return self._default_data()

    def _save(self) -> None:
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        self.index_path.write_text(json.dumps(self._data, ensure_ascii=False, indent=2), encoding="utf-8")

    def list_posts(self) -> list[FamilyBoardPost]:
        with self._lock:
            posts = [FamilyBoardPost.model_validate(item) for item in self._data.get("posts", [])]
        return sorted(posts, key=lambda post: (not post.pinned, post.created_at, post.title))

    def upsert_post(self, post: FamilyBoardPost) -> None:
        with self._lock:
            posts = [item for item in self._data.setdefault("posts", []) if item.get("board_post_id") != post.board_post_id]
            posts.append(post.model_dump(mode="json"))
            self._data["posts"] = posts
            self._save()

    def remove_post(self, board_post_id: str) -> bool:
        with self._lock:
            posts = self._data.setdefault("posts", [])
            before = len(posts)
            self._data["posts"] = [item for item in posts if item.get("board_post_id") != board_post_id]
            changed = len(self._data["posts"]) != before
            if changed:
                self._save()
            return changed


def build_family_board_store(storage_dir: str) -> FamilyBoardStore:
    return FamilyBoardStore(storage_dir)
