from __future__ import annotations

from app.models.schemas import FamilyBoardPostRequest
from app.services.family_board_service import FamilyBoardService
from app.services.family_board_store import FamilyBoardStore


def test_family_board_service_persists_and_orders_posts(tmp_path):
    store = FamilyBoardStore(str(tmp_path))
    service = FamilyBoardService(store)

    service.add_post(FamilyBoardPostRequest(title="둘째 숙제", author="엄마", content="오늘 숙제 확인"))
    service.add_post(FamilyBoardPostRequest(title="아침 공지", author="아빠", content="아침에 일찍 출발", pinned=True))

    state = service.snapshot_state()

    assert (tmp_path / "family_board.json").exists()
    assert [post.title for post in state.posts][0] == "아침 공지"
    assert state.posts[0].pinned is True
    assert state.posts[1].author == "엄마"


def test_family_board_service_remove_post(tmp_path):
    store = FamilyBoardStore(str(tmp_path))
    service = FamilyBoardService(store)
    post = service.add_post(FamilyBoardPostRequest(title="공지", author="kiwan", content="저녁 외식"))

    assert service.remove_post(post.board_post_id) is True
    assert service.remove_post(post.board_post_id) is False
    assert service.list_posts() == []
