from __future__ import annotations

import shlex
import subprocess
from shutil import which

from app.executors.base import Executor
from app.models.schemas import IntentPayload, TaskResult
from app.services.cancellation import TaskCancelled


class BrowserExecutor(Executor):
    def supports(self, intent: IntentPayload) -> bool:
        return intent.intent in {"OPEN_BROWSER", "OPEN_URL"}

    def execute(self, intent: IntentPayload, cancel_requested=None) -> TaskResult:
        if cancel_requested and cancel_requested():
            raise TaskCancelled("Task cancelled")

        url = intent.parameters.get("url", "about:blank")
        command = self._resolve_command(url)
        subprocess.Popen(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return TaskResult(message=f"Opened browser for {url}", executed_command=shlex.join(command), device="local-pc", raw={"url": url})

    def _resolve_command(self, url: str) -> list[str]:
        for candidate in (["xdg-open", url], ["google-chrome", url], ["chromium", url], ["firefox", url]):
            if which(candidate[0]):
                return candidate
        return ["xdg-open", url]
