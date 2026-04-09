from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from app.models.schemas import IntentPayload, RiskLevel


STOPWORDS = {
    "열어줘",
    "열어",
    "켜줘",
    "켜",
    "꺼줘",
    "꺼",
    "틀어줘",
    "틀어",
    "재생해줘",
    "재생",
    "보여줘",
    "보여",
    "실행해줘",
    "실행",
    "해줘",
    "해주세요",
    "해주세요",
    "해주세요.",
    "해",
    "please",
    "open",
    "launch",
    "start",
}

COMMON_SUFFIXES = ("에서", "으로", "로", "을", "를", "이", "가", "은", "는", "에", "와", "과", "도", "만", "부터", "까지", "에게", "께")


class LearnedRuleService:
    def __init__(self, rules_path: str):
        self.rules_path = Path(rules_path)
        self.rules_path.parent.mkdir(parents=True, exist_ok=True)

    def _load(self) -> dict[str, Any]:
        if not self.rules_path.exists():
            return {"rules": []}
        with self.rules_path.open("r", encoding="utf-8") as file:
            return yaml.safe_load(file) or {"rules": []}

    def _write(self, data: dict[str, Any]) -> None:
        with self.rules_path.open("w", encoding="utf-8") as file:
            yaml.safe_dump(data, file, allow_unicode=True, sort_keys=False)

    def _strip_suffix(self, token: str) -> str:
        for suffix in COMMON_SUFFIXES:
            if token.endswith(suffix) and len(token) > len(suffix) + 1:
                return token[: -len(suffix)]
        return token

    def _normalize_tokens(self, command: str) -> list[str]:
        cleaned = (
            command.lower()
            .replace("?", " ")
            .replace("!", " ")
            .replace(",", " ")
            .replace(".", " ")
            .replace("·", " ")
            .replace("/", " ")
            .replace("\\", " ")
            .replace(":", " ")
            .replace(";", " ")
            .replace('"', " ")
            .replace("'", " ")
        )
        tokens: list[str] = []
        for raw_token in cleaned.split():
            token = self._strip_suffix(raw_token.strip())
            if not token:
                continue
            if token in STOPWORDS:
                continue
            if len(token) < 2 and not any("\uac00" <= ch <= "\ud7a3" for ch in token):
                continue
            tokens.append(token)
        return tokens

    def _build_patterns(self, command: str) -> list[str]:
        tokens = self._normalize_tokens(command)
        if not tokens:
            return [command.strip()]
        patterns = [" ".join(tokens)]
        if len(tokens) > 1:
            patterns.append(" ".join(tokens[:2]))
        if len(tokens) > 2:
            patterns.append(" ".join(tokens[:3]))
        if len(tokens) == 1:
            patterns.append(tokens[0])
        deduped: list[str] = []
        seen: set[str] = set()
        for pattern in patterns:
            pattern = pattern.strip()
            if len(pattern) < 2 or pattern in seen:
                continue
            seen.add(pattern)
            deduped.append(pattern)
        return deduped

    def learn(self, command: str, intent: IntentPayload) -> dict[str, Any] | None:
        if intent.risk_level in {RiskLevel.high, RiskLevel.blocked}:
            return None

        patterns = self._build_patterns(command)
        if not patterns:
            return None

        data = self._load()
        rules = data.setdefault("rules", [])
        if any(
            rule.get("intent") == intent.intent
            and rule.get("target_device", "android_tv") == intent.target_device
            and set(rule.get("patterns", [])) & set(patterns)
            for rule in rules
        ):
            return None

        learned_rule = {
            "patterns": patterns,
            "intent": intent.intent,
            "parameters": intent.parameters,
            "target_device": intent.target_device,
            "risk_level": intent.risk_level.value if hasattr(intent.risk_level, "value") else str(intent.risk_level),
            "source": "learned",
        }
        rules.append(learned_rule)
        self._write(data)
        return learned_rule


learned_rule_service = LearnedRuleService("storage/learned_rules.yaml")
