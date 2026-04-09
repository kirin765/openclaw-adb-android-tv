from __future__ import annotations

from app.executors.browser_executor import BrowserExecutor
from app.executors.adb_executor import AdbExecutor
from app.executors.openclaw_executor import OpenClawExecutor
from app.executors.shell_executor import ShellExecutor
from app.models.schemas import IntentPayload, RiskLevel, TaskResult


class ActionMapper:
    def __init__(self) -> None:
        self.executors = [AdbExecutor(), BrowserExecutor(), ShellExecutor(), OpenClawExecutor()]

    def execute(self, intent: IntentPayload, cancel_requested=None) -> TaskResult:
        if intent.risk_level == RiskLevel.blocked:
            raise PermissionError("Blocked command")
        for executor in self.executors:
            if executor.supports(intent):
                return executor.execute(intent, cancel_requested=cancel_requested)
        raise ValueError(f"No executor found for target_device={intent.target_device}, intent={intent.intent}")
