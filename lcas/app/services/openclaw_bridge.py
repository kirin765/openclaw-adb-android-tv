from __future__ import annotations

from typing import Any

import httpx

from app.models.schemas import IntentPayload


class OpenClawBridge:
    def __init__(self, endpoint: str):
        self.endpoint = endpoint

    async def classify(self, user_input: str) -> IntentPayload:
        payload = {
            "input": user_input,
            "expected_output_format": {
                "intent": "string",
                "parameters": {},
                "target_device": "string",
                "risk_level": "low|medium|high|blocked",
            },
        }
        async with httpx.AsyncClient(timeout=20.0) as client:
            response = await client.post(self.endpoint, json=payload)
            response.raise_for_status()
            data: dict[str, Any] = response.json()
        return IntentPayload(
            intent=data["intent"],
            parameters=data.get("parameters", {}),
            target_device=data.get("target_device", "android_tv"),
            risk_level=data.get("risk_level", "medium"),
            source="openclaw_bridge",
            requires_confirmation=data.get("risk_level") in {"high", "blocked"},
        )
