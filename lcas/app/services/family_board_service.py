from __future__ import annotations

from datetime import datetime
from uuid import uuid4

from app.models.schemas import FamilyBoardPost, FamilyBoardPostRequest, FamilyBoardStateResponse
from app.services.family_board_store import FamilyBoardStore


class FamilyBoardService:
    def __init__(self, store: FamilyBoardStore):
        self._store = store

    def list_posts(self) -> list[FamilyBoardPost]:
        return self._store.list_posts()

    def snapshot_state(self) -> FamilyBoardStateResponse:
        return FamilyBoardStateResponse(posts=self.list_posts(), checked_at=self._now_iso())

    def add_post(self, payload: FamilyBoardPostRequest) -> FamilyBoardPost:
        title = payload.title.strip()
        author = payload.author.strip()
        content = payload.content.strip()
        if not title:
            raise ValueError("제목을 입력하세요.")
        if not author:
            raise ValueError("작성자를 입력하세요.")
        if not content:
            raise ValueError("내용을 입력하세요.")

        now = self._now_iso()
        post = FamilyBoardPost(
            board_post_id=str(uuid4()),
            title=title,
            author=author,
            content=content,
            pinned=payload.pinned,
            created_at=now,
            updated_at=now,
        )
        self._store.upsert_post(post)
        return post

    def remove_post(self, board_post_id: str) -> bool:
        return self._store.remove_post(board_post_id)

    def _now_iso(self) -> str:
        return datetime.now().isoformat(timespec="seconds")


def build_family_board_service(store: FamilyBoardStore) -> FamilyBoardService:
    return FamilyBoardService(store)
