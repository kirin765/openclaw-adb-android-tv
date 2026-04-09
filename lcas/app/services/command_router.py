from __future__ import annotations

from app.models.schemas import CommandRequest, IntentPayload
from app.services.openclaw_bridge import OpenClawBridge
from app.services.rule_engine import RuleEngine


class CommandRouter:
    def __init__(self, rules_path: str, learned_rules_path: str, openclaw_bridge_url: str):
        self.rule_engine = RuleEngine(rules_path, learned_rules_path)
        self.bridge = OpenClawBridge(openclaw_bridge_url)

    async def route(self, request: CommandRequest) -> IntentPayload:
        matched = self.rule_engine.match(request.command)
        if matched:
            return matched
        return await self.bridge.classify(request.command)
