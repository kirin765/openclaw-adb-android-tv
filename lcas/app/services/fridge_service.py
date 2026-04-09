from __future__ import annotations

import json
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from threading import Lock
from typing import Any
from uuid import uuid4

from app.models.schemas import (
    FridgeItem,
    FridgeItemCategory,
    FridgeItemRequest,
    FridgeStateResponse,
    RecipeRecommendation,
)


@dataclass(frozen=True)
class RecipeRule:
    recipe_id: str
    title: str
    description: str
    required_terms: tuple[str, ...]
    optional_terms: tuple[str, ...] = ()
    steps: tuple[str, ...] = ()
    requires_side_dish: bool = False


class FridgeService:
    def __init__(self, storage_dir: str):
        self.storage_dir = Path(storage_dir)
        self.index_path = self.storage_dir / "fridge_inventory.json"
        self._lock = Lock()
        self._data = self._load()

    def _default_data(self) -> dict[str, Any]:
        return {"items": []}

    def _load(self) -> dict[str, Any]:
        if not self.index_path.exists():
            return self._default_data()
        try:
            data = json.loads(self.index_path.read_text(encoding="utf-8"))
            if isinstance(data, dict):
                data.setdefault("items", [])
                return data
        except Exception:
            pass
        return self._default_data()

    def _save(self) -> None:
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        self.index_path.write_text(json.dumps(self._data, ensure_ascii=False, indent=2), encoding="utf-8")

    def list_items(self) -> list[FridgeItem]:
        with self._lock:
            items = [FridgeItem.model_validate(item) for item in self._data.get("items", [])]
        return sorted(
            items,
            key=lambda item: (
                0 if item.category == FridgeItemCategory.ingredient else 1,
                item.created_at,
                item.name,
            ),
        )

    def add_item(self, request: FridgeItemRequest) -> FridgeItem:
        with self._lock:
            name = request.name.strip()
            if not name:
                raise ValueError("이름을 입력하세요.")
            now = self._now_iso()
            item = FridgeItem(
                fridge_item_id=str(uuid4()),
                name=name,
                category=request.category,
                quantity=request.quantity.strip(),
                note=request.note.strip(),
                created_at=now,
                updated_at=now,
            )
            self._data.setdefault("items", []).append(item.model_dump(mode="json"))
            self._save()
            return item

    def remove_item(self, fridge_item_id: str) -> bool:
        with self._lock:
            items = self._data.setdefault("items", [])
            before = len(items)
            self._data["items"] = [item for item in items if item.get("fridge_item_id") != fridge_item_id]
            changed = len(self._data["items"]) != before
            if changed:
                self._save()
            return changed

    def snapshot_state(self) -> FridgeStateResponse:
        items = self.list_items()
        recommendations = self.recommend_recipes(items)
        return FridgeStateResponse(items=items, recommendations=recommendations, checked_at=self._now_iso())

    def recommend_recipes(self, items: list[FridgeItem] | None = None, limit: int = 5) -> list[RecipeRecommendation]:
        inventory = items if items is not None else self.list_items()
        if not inventory:
            return []

        rules = self._recipe_rules()
        recommendations: list[RecipeRecommendation] = []
        for rule in rules:
            recommendation = self._score_rule(rule, inventory)
            if recommendation is not None:
                recommendations.append(recommendation)

        recommendations.sort(key=lambda item: (-item.score, -len(item.matched_items), len(item.missing_items), item.title))
        return recommendations[:limit]

    def _score_rule(self, rule: RecipeRule, inventory: list[FridgeItem]) -> RecipeRecommendation | None:
        side_dish_items = [item for item in inventory if item.category == FridgeItemCategory.side_dish]
        if rule.requires_side_dish and not side_dish_items:
            return None

        matched_items: list[str] = []
        used_ids: set[str] = set()
        missing_items: list[str] = []

        for term in rule.required_terms:
            match = self._find_match(term, inventory, used_ids)
            if match:
                used_ids.add(match.fridge_item_id)
                matched_items.append(match.name)
            else:
                missing_items.append(term)

        optional_matches = 0
        for term in rule.optional_terms:
            match = self._find_match(term, inventory, used_ids)
            if match:
                used_ids.add(match.fridge_item_id)
                matched_items.append(match.name)
                optional_matches += 1

        if rule.requires_side_dish:
            for item in side_dish_items:
                if item.fridge_item_id not in used_ids:
                    matched_items.append(item.name)
                    used_ids.add(item.fridge_item_id)

        if not matched_items:
            return None

        required_ratio = len(rule.required_terms)
        required_score = 100 if required_ratio == 0 else int(round((len(rule.required_terms) - len(missing_items)) / required_ratio * 100))
        score = required_score + optional_matches * 8 + (15 if rule.requires_side_dish and side_dish_items else 0)
        score = max(1, min(100, score))

        return RecipeRecommendation(
            recipe_id=rule.recipe_id,
            title=rule.title,
            description=rule.description,
            score=score,
            matched_items=matched_items[:6],
            missing_items=missing_items,
            steps=list(rule.steps),
        )

    def _find_match(self, term: str, inventory: list[FridgeItem], used_ids: set[str]) -> FridgeItem | None:
        aliases = self._aliases_for(term)
        for item in inventory:
            if item.fridge_item_id in used_ids:
                continue
            if self._matches_any(item.name, (term, *aliases)):
                return item
        return None

    def _matches_any(self, value: str, terms: tuple[str, ...]) -> bool:
        normalized_value = self._normalize(value)
        for term in terms:
            normalized_term = self._normalize(term)
            if not normalized_term:
                continue
            if normalized_term in normalized_value or normalized_value in normalized_term:
                return True
        return False

    def _normalize(self, value: str) -> str:
        return re.sub(r"\s+", "", value).lower()

    def _aliases_for(self, term: str) -> tuple[str, ...]:
        aliases = {
            "계란": ("달걀", "알"),
            "달걀": ("계란", "알"),
            "밥": ("쌀밥", "즉석밥"),
            "김치": ("배추김치", "신김치"),
            "두부": ("순두부",),
            "참치": ("참치캔",),
            "돼지고기": ("삼겹살", "목살"),
            "소고기": ("우삼겹", "불고기용"),
            "부침가루": ("전가루", "튀김가루"),
            "간장": ("진간장",),
            "마요네즈": ("마요",),
            "된장": ("집된장",),
        }
        return aliases.get(term, ())

    def _recipe_rules(self) -> list[RecipeRule]:
        return [
            RecipeRule(
                recipe_id="soy_egg_rice",
                title="간장계란밥",
                description="가장 빠르게 한 그릇으로 먹기 좋은 기본 조합입니다.",
                required_terms=("밥", "계란", "간장"),
                optional_terms=("버터", "참기름", "대파"),
                steps=(
                    "밥을 그릇에 담는다.",
                    "계란을 익혀 올리고 간장을 살짝 둘러 먹는다.",
                    "버터나 참기름이 있으면 마지막에 더한다.",
                ),
            ),
            RecipeRule(
                recipe_id="kimchi_fried_rice",
                title="김치볶음밥",
                description="냉장고 김치와 밥이 있을 때 가장 안정적으로 잘 맞는 메뉴입니다.",
                required_terms=("김치", "밥", "계란"),
                optional_terms=("햄", "대파", "참기름"),
                steps=(
                    "김치를 잘게 썬다.",
                    "밥과 함께 볶고 계란을 얹는다.",
                    "참기름으로 마무리한다.",
                ),
            ),
            RecipeRule(
                recipe_id="egg_fried_rice",
                title="계란볶음밥",
                description="재료가 적어도 바로 만들 수 있는 편한 한 끼입니다.",
                required_terms=("밥", "계란"),
                optional_terms=("대파", "버터", "간장"),
                steps=(
                    "계란을 먼저 볶아 부드럽게 익힌다.",
                    "밥을 넣고 함께 볶는다.",
                    "간장으로 간을 맞춘다.",
                ),
            ),
            RecipeRule(
                recipe_id="tuna_mayo_bowl",
                title="참치마요덮밥",
                description="반찬이 애매할 때 간단하게 해결하기 좋은 덮밥입니다.",
                required_terms=("밥", "참치", "마요네즈"),
                optional_terms=("계란", "김"),
                steps=(
                    "참치에 마요네즈를 섞는다.",
                    "따뜻한 밥 위에 올린다.",
                    "계란이나 김을 더하면 더 든든해진다.",
                ),
            ),
            RecipeRule(
                recipe_id="tofu_pan_fry",
                title="두부부침",
                description="반찬이나 안주로도 잘 맞는 담백한 메뉴입니다.",
                required_terms=("두부", "간장"),
                optional_terms=("대파", "깨", "고춧가루"),
                steps=(
                    "두부를 먹기 좋은 크기로 자른다.",
                    "노릇하게 굽는다.",
                    "간장 양념을 곁들인다.",
                ),
            ),
            RecipeRule(
                recipe_id="kimchi_pancake",
                title="김치전",
                description="김치와 가루 재료가 있으면 빠르게 만들 수 있습니다.",
                required_terms=("김치", "부침가루"),
                optional_terms=("계란", "대파", "오징어"),
                steps=(
                    "김치를 잘게 썰어 반죽에 섞는다.",
                    "팬에 넓게 부친다.",
                    "간장 초간장과 함께 먹는다.",
                ),
            ),
            RecipeRule(
                recipe_id="doenjang_stew",
                title="된장찌개",
                description="두부와 채소가 남아 있을 때 가장 먼저 떠올리기 좋은 국물 메뉴입니다.",
                required_terms=("된장", "두부"),
                optional_terms=("애호박", "양파", "감자", "대파"),
                steps=(
                    "물에 된장을 풀어 끓인다.",
                    "두부와 채소를 넣는다.",
                    "간을 보고 한소끔 더 끓인다.",
                ),
            ),
            RecipeRule(
                recipe_id="leftover_side_dish_plate",
                title="남은 반찬 한상차림",
                description="반찬이 여러 개 있을 때 밥과 곁들여 한 끼로 정리하기 좋습니다.",
                required_terms=(),
                optional_terms=("밥", "계란", "김"),
                steps=(
                    "남은 반찬을 접시에 보기 좋게 담는다.",
                    "밥과 함께 곁들여 먹는다.",
                    "계란후라이가 있으면 더 든든하다.",
                ),
                requires_side_dish=True,
            ),
        ]

    def _now_iso(self) -> str:
        return datetime.now(timezone.utc).isoformat()


def build_fridge_service(storage_dir: str) -> FridgeService:
    return FridgeService(storage_dir)
