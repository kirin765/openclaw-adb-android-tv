from __future__ import annotations

import shlex
import subprocess
import re
import time
from typing import Any

from app.core.settings import get_settings
from app.executors.base import Executor
from app.models.schemas import IntentPayload, TaskResult, TvApp
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
        self._connect(adb, ip, cancel_requested)

        if intent.intent == "TV_KEYEVENT":
            self._check_cancel(cancel_requested)
            keycode = str(intent.parameters["keycode"])
            cmd = [adb, "shell", "input", "keyevent", keycode]
            self._run(cmd, cancel_requested)
            return TaskResult(message=f"Sent keyevent {keycode}", executed_command=shlex.join(cmd), device=self.settings.default_android_tv_id)

        if intent.intent == "TV_LAUNCH_APP":
            self._check_cancel(cancel_requested)
            package = intent.parameters["package"]
            activity = intent.parameters.get("activity")
            return self.launch_app(package, activity, cancel_requested)

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

    def list_launchable_apps(self, cancel_requested=None) -> list[TvApp]:
        ip = self.settings.default_android_tv_ip
        adb = self.settings.adb_path
        self._connect(adb, ip, cancel_requested)

        output = self._run_capture(
            [adb, "shell", "cmd", "package", "query-intent-activities", "-a", "android.intent.action.MAIN", "-c", "android.intent.category.LAUNCHER"],
            cancel_requested,
        )
        apps = self._parse_launchable_apps(output)
        if not apps:
            output = self._run_capture([adb, "shell", "pm", "list", "packages", "-3"], cancel_requested)
            apps = self._parse_package_list(output)
        return sorted(apps, key=lambda item: (item.label.lower(), item.package_name.lower()))

    def launch_app(self, package: str, activity: str | None = None, cancel_requested=None) -> TaskResult:
        self._check_cancel(cancel_requested)
        ip = self.settings.default_android_tv_ip
        adb = self.settings.adb_path
        self._connect(adb, ip, cancel_requested)

        if activity:
            component = f"{package}/{activity}"
            cmd = [adb, "shell", "am", "start", "-n", component]
        else:
            cmd = [adb, "shell", "monkey", "-p", package, "1"]
        self._run(cmd, cancel_requested)
        return TaskResult(
            message=f"Launched {package}",
            executed_command=shlex.join(cmd),
            device=self.settings.default_android_tv_id,
            raw={"package": package, "activity": activity or ""},
        )

    def _connect(self, adb: str, ip: str, cancel_requested=None) -> None:
        self._run([adb, "connect", ip], cancel_requested)

    def _run(self, cmd: list[str], cancel_requested=None) -> None:
        self._run_command(cmd, cancel_requested)

    def _run_capture(self, cmd: list[str], cancel_requested=None) -> str:
        stdout, _ = self._run_command(cmd, cancel_requested)
        return stdout.strip()

    def _run_command(self, cmd: list[str], cancel_requested=None) -> tuple[str, str]:
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
            return stdout, stderr
        finally:
            if process.poll() is None:
                process.kill()

    def _check_cancel(self, cancel_requested=None) -> None:
        if cancel_requested and cancel_requested():
            raise TaskCancelled("Task cancelled")

    def _encode_input_text(self, text: str) -> str:
        return text.replace(" ", "%s")

    def _parse_launchable_apps(self, output: str) -> list[TvApp]:
        apps: dict[str, TvApp] = {}
        for raw_line in output.splitlines():
            line = raw_line.strip()
            if not line:
                continue
            package, activity = self._extract_component(line)
            if not package:
                continue
            label = self._label_from_component(package, activity)
            if package not in apps:
                apps[package] = TvApp(package_name=package, label=label, activity_name=activity or "")
            elif label and (not apps[package].label or apps[package].label == self._label_from_component(package)):
                apps[package] = apps[package].model_copy(update={"label": label, "activity_name": activity or apps[package].activity_name})
        return list(apps.values())

    def _parse_package_list(self, output: str) -> list[TvApp]:
        apps: list[TvApp] = []
        for raw_line in output.splitlines():
            line = raw_line.strip()
            if not line.startswith("package:"):
                continue
            package = line.split(":", 1)[1].strip()
            if not package:
                continue
            apps.append(TvApp(package_name=package, label=self._label_from_component(package), activity_name=""))
        return apps

    def _extract_component(self, line: str) -> tuple[str, str]:
        match = re.search(r"([A-Za-z0-9_.]+)\/([A-Za-z0-9_.$]+)", line)
        if match:
            return match.group(1), match.group(2)
        package_match = re.search(r"package[:=]([A-Za-z0-9_.]+)", line)
        if package_match:
            return package_match.group(1), ""
        return "", ""

    def _label_from_component(self, package: str, activity: str | None = None) -> str:
        if activity:
            name = activity.rsplit("/", 1)[-1]
            if name.startswith("."):
                name = name[1:]
            name = name.rsplit(".", 1)[-1]
            name = re.sub(r"(?<!^)(?=[A-Z])", " ", name).replace("_", " ").strip()
            if name:
                return name
        tail = package.rsplit(".", 1)[-1]
        return tail.replace("_", " ").title() if tail else package
