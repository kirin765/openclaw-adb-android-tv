from __future__ import annotations

import shlex
import subprocess
import time
from typing import Any

from app.core.settings import get_settings
from app.executors.base import Executor
from app.models.schemas import IntentPayload, TaskResult
from app.services.cancellation import TaskCancelled


class AdbExecutor(Executor):
    def __init__(self) -> None:
        self.settings = get_settings()

    def supports(self, intent: IntentPayload) -> bool:
        return intent.target_device == "android_tv"

    def execute(self, intent: IntentPayload, cancel_requested=None) -> TaskResult:
        self._check_cancel(cancel_requested)
        ip = self.settings.default_android_tv_ip
        adb = self.settings.adb_path
        self._run([adb, "connect", ip], cancel_requested)

        if intent.intent == "TV_KEYEVENT":
            self._check_cancel(cancel_requested)
            keycode = str(intent.parameters["keycode"])
            cmd = [adb, "shell", "input", "keyevent", keycode]
            self._run(cmd, cancel_requested)
            return TaskResult(message=f"Sent keyevent {keycode}", executed_command=shlex.join(cmd), device=self.settings.default_android_tv_id)

        if intent.intent == "TV_LAUNCH_APP":
            self._check_cancel(cancel_requested)
            package = intent.parameters["package"]
            cmd = [adb, "shell", "monkey", "-p", package, "1"]
            self._run(cmd, cancel_requested)
            return TaskResult(message=f"Launched {package}", executed_command=shlex.join(cmd), device=self.settings.default_android_tv_id)

        if intent.intent == "PLAY_PLAYLIST":
            self._check_cancel(cancel_requested)
            query = intent.parameters.get("query", "lofi chill music").replace(" ", "+")
            url = f"https://www.youtube.com/results?search_query={query}"
            cmd = [adb, "shell", "am", "start", "-a", "android.intent.action.VIEW", "-d", url]
            self._run(cmd, cancel_requested)
            return TaskResult(message="Opened playlist search", executed_command=shlex.join(cmd), device=self.settings.default_android_tv_id, raw={"url": url})

        if intent.intent == "TV_INPUT_TEXT":
            self._check_cancel(cancel_requested)
            text = self._encode_input_text(str(intent.parameters["text"]))
            cmd = [adb, "shell", "input", "text", text]
            self._run(cmd, cancel_requested)
            return TaskResult(message="Sent text input", executed_command=shlex.join(cmd), device=self.settings.default_android_tv_id, raw={"text": intent.parameters["text"]})

        if intent.intent == "TV_POWER_OFF":
            self._check_cancel(cancel_requested)
            cmd = [adb, "shell", "input", "keyevent", "26"]
            self._run(cmd, cancel_requested)
            return TaskResult(message="Turned power off", executed_command=shlex.join(cmd), device=self.settings.default_android_tv_id)

        if intent.intent == "TV_POWER_ON":
            self._check_cancel(cancel_requested)
            cmd = [adb, "shell", "input", "keyevent", "224"]
            self._run(cmd, cancel_requested)
            return TaskResult(message="Turned power on", executed_command=shlex.join(cmd), device=self.settings.default_android_tv_id)

        if intent.intent == "TV_WAKE_SCREEN":
            self._check_cancel(cancel_requested)
            cmd = [adb, "shell", "input", "keyevent", "224"]
            self._run(cmd, cancel_requested)
            return TaskResult(message="Woke screen", executed_command=shlex.join(cmd), device=self.settings.default_android_tv_id)

        if intent.intent == "TV_POWER_TOGGLE":
            self._check_cancel(cancel_requested)
            cmd = [adb, "shell", "input", "keyevent", "26"]
            self._run(cmd, cancel_requested)
            return TaskResult(message="Toggled power", executed_command=shlex.join(cmd), device=self.settings.default_android_tv_id)

        raise ValueError(f"Unsupported android_tv intent: {intent.intent}")

    def _run(self, cmd: list[str], cancel_requested=None) -> None:
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        try:
            while True:
                if cancel_requested and cancel_requested():
                    process.terminate()
                    try:
                        process.wait(timeout=2)
                    except subprocess.TimeoutExpired:
                        process.kill()
                        process.wait(timeout=2)
                    raise TaskCancelled("Task cancelled")
                if process.poll() is not None:
                    break
                time.sleep(0.1)
            stdout, stderr = process.communicate()
            if process.returncode:
                raise subprocess.CalledProcessError(process.returncode, cmd, output=stdout, stderr=stderr)
        finally:
            if process.poll() is None:
                process.kill()

    def _check_cancel(self, cancel_requested=None) -> None:
        if cancel_requested and cancel_requested():
            raise TaskCancelled("Task cancelled")

    def _encode_input_text(self, text: str) -> str:
        return text.replace(" ", "%s")
