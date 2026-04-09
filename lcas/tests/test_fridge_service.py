from __future__ import annotations

from app.models.schemas import FridgeItemCategory, FridgeItemRequest
from app.services.fridge_service import FridgeService


def test_fridge_service_persists_items_and_recommends(tmp_path):
    service = FridgeService(str(tmp_path))

    service.add_item(FridgeItemRequest(name="밥", category=FridgeItemCategory.ingredient, quantity="1공기"))
    service.add_item(FridgeItemRequest(name="계란", category=FridgeItemCategory.ingredient, quantity="2개"))
    service.add_item(FridgeItemRequest(name="간장", category=FridgeItemCategory.ingredient))
    service.add_item(FridgeItemRequest(name="멸치볶음", category=FridgeItemCategory.side_dish))

    state = service.snapshot_state()

    assert (tmp_path / "fridge_inventory.json").exists()
    assert any(item.name == "멸치볶음" for item in state.items)
    assert any(recipe.title == "간장계란밥" for recipe in state.recommendations)
    assert any(recipe.title == "남은 반찬 한상차림" for recipe in state.recommendations)


def test_fridge_service_remove_item(tmp_path):
    service = FridgeService(str(tmp_path))
    item = service.add_item(FridgeItemRequest(name="두부", category=FridgeItemCategory.ingredient))

    assert service.remove_item(item.fridge_item_id) is True
    assert service.remove_item(item.fridge_item_id) is False
    assert service.list_items() == []
