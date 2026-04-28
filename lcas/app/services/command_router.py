from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import httpx

from app.models.schemas import CommandRequest, IntentPayload


@dataclass(frozen=True)
class CommandRouter:
    rules_path: str
    learned_rules_path: str
    openclaw_bridge_url: str

    async def route(self, request: CommandRequest) -> IntentPayload:
        payload = {
            "command": request.command,
            "user_id": request.user_id,
            "source": request.source,
        }
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    self.openclaw_bridge_url,
                    json=payload,
                )
                response.raise_for_status()
                response_data = response.json()
        except httpx.HTTPStatusError as exc:
            raise RuntimeError(f"OpenClaw bridge returned HTTP {exc.response.status_code}: {exc.response.text}") from exc
        except Exception as exc:
            raise RuntimeError(f"OpenClaw bridge request failed: {exc}") from exc

        intent_data = self._extract_intent_data(response_data)
        if "source" not in intent_data:
            intent_data["source"] = "openclaw_bridge"
        return IntentPayload.model_validate(intent_data)

    def _extract_intent_data(self, response_data: Any) -> dict[str, Any]:
        if isinstance(response_data, dict):
            if "intent_data" in response_data and isinstance(response_data["intent_data"], dict):
                return dict(response_data["intent_data"])
            if "intent" in response_data:
                return dict(response_data)
            if "data" in response_data and isinstance(response_data["data"], dict):
                inner = response_data["data"]
                if "intent" in inner:
                    return dict(inner)
                if "intent_data" in inner and isinstance(inner["intent_data"], dict):
                    return dict(inner["intent_data"])
        raise RuntimeError("OpenClaw bridge returned an unexpected response format")
