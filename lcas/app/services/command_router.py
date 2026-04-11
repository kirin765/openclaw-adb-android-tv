from __future__ import annotations

import asyncio
import json
from dataclasses import dataclass
from typing import Any
from urllib import error, request as urllib_request

from app.models.schemas import CommandRequest, IntentPayload


@dataclass(frozen=True)
class CommandRouter:
    rules_path: str
    learned_rules_path: str
    openclaw_bridge_url: str

    async def route(self, request: CommandRequest) -> IntentPayload:
        return await asyncio.to_thread(self._route_sync, request)

    def _route_sync(self, request: CommandRequest) -> IntentPayload:
        payload = {
            "command": request.command,
            "user_id": request.user_id,
            "source": request.source,
        }
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        req = urllib_request.Request(
            self.openclaw_bridge_url,
            data=body,
            headers={"Content-Type": "application/json"},
            method="POST",
        )

        try:
            with urllib_request.urlopen(req, timeout=30) as response:
                response_data = json.loads(response.read().decode("utf-8"))
        except error.HTTPError as exc:
            message = exc.read().decode("utf-8", errors="ignore") if exc.fp else exc.reason
            raise RuntimeError(f"OpenClaw bridge returned HTTP {exc.code}: {message}") from exc
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
