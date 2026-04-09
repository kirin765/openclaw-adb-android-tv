from __future__ import annotations

from app.executors.base import Executor
from app.models.schemas import IntentPayload, TaskResult


class OpenClawExecutor(Executor):
    def supports(self, intent: IntentPayload) -> bool:
        return intent.target_device == "openclaw"

    def execute(self, intent: IntentPayload, cancel_requested=None) -> TaskResult:
        return TaskResult(message="OpenClaw delegated task prepared", device="openclaw", raw={"intent": intent.model_dump()})
