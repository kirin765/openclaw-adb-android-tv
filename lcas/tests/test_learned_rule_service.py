from __future__ import annotations

from pathlib import Path

from app.models.schemas import IntentPayload, RiskLevel
from app.services.learned_rule_service import LearnedRuleService
from app.services.rule_engine import RuleEngine


def test_learned_rule_service_persists_heuristic_rule(tmp_path):
    learned_rules_path = tmp_path / "learned_rules.yaml"
    service = LearnedRuleService(str(learned_rules_path))

    learned = service.learn(
        "아침 뉴스 틀어줘",
        IntentPayload(
            intent="OPEN_URL",
            parameters={"url": "https://example.com/news"},
            target_device="pc",
            risk_level=RiskLevel.low,
            source="openclaw_bridge",
        ),
    )

    assert learned is not None
    assert learned_rules_path.exists()
    engine = RuleEngine("config/rules.yaml", str(learned_rules_path))
    matched = engine.match("아침 뉴스 틀어줘")
    assert matched is not None
    assert matched.intent == "OPEN_URL"
    assert matched.parameters["url"] == "https://example.com/news"


def test_learned_rule_service_skips_high_risk(tmp_path):
    learned_rules_path = tmp_path / "learned_rules.yaml"
    service = LearnedRuleService(str(learned_rules_path))

    learned = service.learn(
        "은행 앱 열어줘",
        IntentPayload(
            intent="OPEN_URL",
            parameters={"url": "https://bank.example"},
            target_device="pc",
            risk_level=RiskLevel.high,
            source="openclaw_bridge",
        ),
    )

    assert learned is None
    assert not learned_rules_path.exists() or learned_rules_path.read_text(encoding="utf-8").strip() in {"", "rules: []"}
