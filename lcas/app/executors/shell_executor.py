from __future__ import annotations

import shlex
import subprocess

from app.core.settings import get_settings
from app.executors.base import Executor
from app.models.schemas import IntentPayload, TaskResult


class ShellExecutor(Executor):
    def __init__(self) -> None:
        self.settings = get_settings()

    def supports(self, intent: IntentPayload) -> bool:
        return intent.target_device == "pc" and self.settings.allow_shell_executor

    def execute(self, intent: IntentPayload, cancel_requested=None, progress_callback=None) -> TaskResult:
        command = intent.parameters.get("command")
        if not command:
            raise ValueError("Missing shell command")
        if progress_callback:
            progress_callback("쉘 명령 실행 중")
        completed = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        return TaskResult(message="Shell command executed", executed_command=command, device="local-pc", raw={"stdout": completed.stdout, "stderr": completed.stderr})
