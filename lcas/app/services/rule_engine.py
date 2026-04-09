from __future__ import annotations

from pathlib import Path
from typing import Any
import re

import yaml

from app.models.schemas import IntentPayload, RiskLevel


class RuleEngine:
    def __init__(self, rules_path: str, learned_rules_path: str | None = None):
        self.rules_path = Path(rules_path)
        self.learned_rules_path = Path(learned_rules_path) if learned_rules_path else None
        self.rules = self._load_rules()

    def _load_rules(self) -> list[dict[str, Any]]:
        rules = []
        for path in [self.rules_path, self.learned_rules_path]:
            if not path or not path.exists():
                continue
            with path.open("r", encoding="utf-8") as file:
                data = yaml.safe_load(file) or {}
            rules.extend(data.get("rules", []))
        return rules

    def match(self, command: str) -> IntentPayload | None:
        normalized = command.strip().lower()
        if self._looks_like_url(command):
            return IntentPayload(
                intent="OPEN_URL",
                parameters={"url": command.strip()},
                target_device="pc",
                risk_level=RiskLevel.low,
                source="rule_engine",
                requires_confirmation=False,
            )
        for rule in self.rules:
            for pattern in rule.get("patterns", []):
                if pattern.lower() in normalized:
                    return IntentPayload(
                        intent=rule["intent"],
                        parameters=rule.get("parameters", {}),
                        target_device=rule.get("target_device", "android_tv"),
                        risk_level=RiskLevel(rule.get("risk_level", "low")),
                        source="rule_engine",
                        requires_confirmation=rule.get("risk_level") in {"high", "blocked"},
                    )
        return None

    def _looks_like_url(self, command: str) -> bool:
        return bool(re.match(r"^https?://\S+$", command.strip(), re.IGNORECASE))
