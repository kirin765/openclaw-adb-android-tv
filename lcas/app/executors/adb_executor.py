from __future__ import annotations

import shlex
import subprocess
import re
import time
from typing import Any, Callable

from app.core.settings import get_settings
from app.executors.base import Executor
from app.models.schemas import IntentPayload, TaskResult, TvApp
from app.services.cancellation import TaskCancelled


class AdbExecutor(Executor):
    def __init__(self) -> None:
        self.settings = get_settings()
        self._screen_size: tuple[int, int] | None = None
        # dispatch 테이블 초기화
        self._intent_handlers: dict[str, Callable[..., TaskResult]] = {
            "TV_KEYEVENT": self._handle_keyevent,
            "TV_LAUNCH_APP": self._handle_launch_app,
            "PLAY_PLAYLIST": self._handle_play_playlist,
            "TV_INPUT_TEXT": self._handle_input_text,
            "TV_TRACKPAD": self._handle_trackpad,
            "TV_OPEN_URL": self._handle_open_url,
            "TV_POWER_OFF": self._handle_power_off,
            "TV_POWER_ON": self._handle_power_on,
            "TV_WAKE_SCREEN": self._handle_wake_screen,
            "TV_POWER_TOGGLE": self._handle_power_toggle,
        }

    def supports(self, intent: IntentPayload) -> bool:
        return intent.target_device == "android_tv"

    def execute(self, intent: IntentPayload, cancel_requested=None, progress_callback=None) -> TaskResult:
        self._check_cancel(cancel_requested)
        ip = self.settings.default_android_tv_ip
        adb = self.settings.adb_path
        if progress_callback:
            progress_callback(f"ADB {ip} 연결 중")
        self._connect(adb, ip, cancel_requested)

        handler = self._intent_handlers.get(intent.intent)
        if handler is None:
            raise ValueError(f"Unsupported android_tv intent: {intent.intent}")
        return handler(intent, adb=adb, cancel_requested=cancel_requested, progress_callback=progress_callback)

    def _handle_keyevent(self, intent: IntentPayload, *, adb: str, cancel_requested, progress_callback) -> TaskResult:
        self._check_cancel(cancel_requested)
        keycode = str(intent.parameters["keycode"])
        if progress_callback:
            progress_callback(f"TV 키 입력 전송 중: {keycode}")
        cmd = [adb, "shell", "input", "keyevent", keycode]
        self._run(cmd, cancel_requested)
        return TaskResult(message=f"Sent keyevent {keycode}", executed_command=shlex.join(cmd), device=self.settings.default_android_tv_id)

    def _handle_launch_app(self, intent: IntentPayload, *, adb: str, cancel_requested, progress_callback) -> TaskResult:
        self._check_cancel(cancel_requested)
        package = intent.parameters["package"]
        activity = intent.parameters.get("activity")
        if progress_callback:
            progress_callback(f"TV 앱 실행 중: {package}")
        return self.launch_app(package, activity, cancel_requested, progress_callback)

    def _handle_play_playlist(self, intent: IntentPayload, *, adb: str, cancel_requested, progress_callback) -> TaskResult:
        self._check_cancel(cancel_requested)
        query = intent.parameters.get("query", "lofi chill music").replace(" ", "+")
        url = f"https://www.youtube.com/results?search_query={query}"
        if progress_callback:
            progress_callback("유튜브 음악 검색 열기")
        cmd = [adb, "shell", "am", "start", "-a", "android.intent.action.VIEW", "-d", url]
        self._run(cmd, cancel_requested)
        return TaskResult(message="Opened playlist search", executed_command=shlex.join(cmd), device=self.settings.default_android_tv_id, raw={"url": url})

    def _handle_input_text(self, intent: IntentPayload, *, adb: str, cancel_requested, progress_callback) -> TaskResult:
        self._check_cancel(cancel_requested)
        text = self._encode_input_text(str(intent.parameters["text"]))
        if progress_callback:
            progress_callback("TV 글자 입력 중")
        cmd = [adb, "shell", "input", "text", text]
        self._run(cmd, cancel_requested)
        return TaskResult(message="Sent text input", executed_command=shlex.join(cmd), device=self.settings.default_android_tv_id, raw={"text": intent.parameters["text"]})

    def _handle_trackpad(self, intent: IntentPayload, *, adb: str, cancel_requested, progress_callback) -> TaskResult:
        self._check_cancel(cancel_requested)
        action = str(intent.parameters.get("action", "drag")).lower()
        if action == "tap":
            if progress_callback:
                progress_callback("트랙패드 탭 전송 중")
            cmd = [adb, "shell", "input", "keyevent", "23"]
            self._run(cmd, cancel_requested)
            return TaskResult(
                message="Tapped TV selection",
                executed_command=shlex.join(cmd),
                device=self.settings.default_android_tv_id,
                raw={"action": "tap"},
            )

        if action == "back":
            if progress_callback:
                progress_callback("트랙패드 뒤로 전송 중")
            cmd = [adb, "shell", "input", "keyevent", "4"]
            self._run(cmd, cancel_requested)
            return TaskResult(
                message="Sent back",
                executed_command=shlex.join(cmd),
                device=self.settings.default_android_tv_id,
                raw={"action": "back"},
            )

        if action == "home":
            if progress_callback:
                progress_callback("트랙패드 홈 전송 중")
            cmd = [adb, "shell", "input", "keyevent", "3"]
            self._run(cmd, cancel_requested)
            return TaskResult(
                message="Sent home",
                executed_command=shlex.join(cmd),
                device=self.settings.default_android_tv_id,
                raw={"action": "home"},
            )

        delta_x = float(intent.parameters.get("delta_x", 0.0))
        delta_y = float(intent.parameters.get("delta_y", 0.0))
        duration_ms = int(intent.parameters.get("duration_ms", 220))
        if abs(delta_x) < 0.01 and abs(delta_y) < 0.01:
            if progress_callback:
                progress_callback("트랙패드 탭 전송 중")
            cmd = [adb, "shell", "input", "keyevent", "23"]
            self._run(cmd, cancel_requested)
            return TaskResult(
                message="Tapped TV selection",
                executed_command=shlex.join(cmd),
                device=self.settings.default_android_tv_id,
                raw={"action": "tap"},
            )

        width, height = self._get_screen_size(adb, cancel_requested)
        if progress_callback:
            progress_callback("TV 화면 크기 확인 중")
        center_x = width // 2
        center_y = height // 2
        scale = float(intent.parameters.get("scale", 0.35))
        scale = max(0.1, min(scale, 0.5))
        end_x = self._clamp_int(center_x + int(delta_x * width * scale), 0, max(0, width - 1))
        end_y = self._clamp_int(center_y + int(delta_y * height * scale), 0, max(0, height - 1))
        duration_ms = max(50, min(duration_ms, 2000))
        if progress_callback:
            progress_callback("트랙패드 드래그 전송 중")
        cmd = [
            adb,
            "shell",
            "input",
            "swipe",
            str(center_x),
            str(center_y),
            str(end_x),
            str(end_y),
            str(duration_ms),
        ]
        self._run(cmd, cancel_requested)
        return TaskResult(
            message="Sent trackpad swipe",
            executed_command=shlex.join(cmd),
            device=self.settings.default_android_tv_id,
            raw={
                "action": "drag",
                "delta_x": delta_x,
                "delta_y": delta_y,
                "duration_ms": duration_ms,
                "screen_width": width,
                "screen_height": height,
            },
        )

    def _handle_open_url(self, intent: IntentPayload, *, adb: str, cancel_requested, progress_callback) -> TaskResult:
        self._check_cancel(cancel_requested)
        url = str(intent.parameters["url"])
        if progress_callback:
            progress_callback("TV 브라우저 열기")
        cmd = [adb, "shell", "am", "start", "-a", "android.intent.action.VIEW", "-d", url]
        self._run(cmd, cancel_requested)
        return TaskResult(message=f"Opened TV browser for {url}", executed_command=shlex.join(cmd), device=self.settings.default_android_tv_id, raw={"url": url})

    def _handle_power_off(self, intent: IntentPayload, *, adb: str, cancel_requested, progress_callback) -> TaskResult:
        self._check_cancel(cancel_requested)
        if progress_callback:
            progress_callback("TV 전원 끄는 중")
        cmd = [adb, "shell", "input", "keyevent", "26"]
        self._run(cmd, cancel_requested)
        return TaskResult(message="Turned power off", executed_command=shlex.join(cmd), device=self.settings.default_android_tv_id)

    def _handle_power_on(self, intent: IntentPayload, *, adb: str, cancel_requested, progress_callback) -> TaskResult:
        self._check_cancel(cancel_requested)
        if progress_callback:
            progress_callback("TV 전원 켜는 중")
        cmd = [adb, "shell", "input", "keyevent", "224"]
        self._run(cmd, cancel_requested)
        return TaskResult(message="Turned power on", executed_command=shlex.join(cmd), device=self.settings.default_android_tv_id)

    def _handle_wake_screen(self, intent: IntentPayload, *, adb: str, cancel_requested, progress_callback) -> TaskResult:
        self._check_cancel(cancel_requested)
        if progress_callback:
            progress_callback("TV 화면 깨우는 중")
        cmd = [adb, "shell", "input", "keyevent", "224"]
        self._run(cmd, cancel_requested)
        return TaskResult(message="Woke screen", executed_command=shlex.join(cmd), device=self.settings.default_android_tv_id)

    def _handle_power_toggle(self, intent: IntentPayload, *, adb: str, cancel_requested, progress_callback) -> TaskResult:
        self._check_cancel(cancel_requested)
        if progress_callback:
            progress_callback("TV 전원 토글 중")
        cmd = [adb, "shell", "input", "keyevent", "26"]
        self._run(cmd, cancel_requested)
        return TaskResult(message="Toggled power", executed_command=shlex.join(cmd), device=self.settings.default_android_tv_id)

    def list_launchable_apps(self, cancel_requested=None) -> list[TvApp]:
        ip = self.settings.default_android_tv_ip
        adb = self.settings.adb_path
        self._connect(adb, ip, cancel_requested)

        apps: list[TvApp] = []
        try:
            output = self._run_capture(
                [adb, "shell", "cmd", "package", "query-intent-activities", "-a", "android.intent.action.MAIN", "-c", "android.intent.category.LAUNCHER"],
                cancel_requested,
            )
            apps = self._parse_launchable_apps(output)
        except subprocess.CalledProcessError:
            apps = []
        if not apps:
            try:
                output = self._run_capture([adb, "shell", "pm", "list", "packages", "-3"], cancel_requested)
                apps = self._parse_package_list(output)
            except subprocess.CalledProcessError:
                apps = []
        if not apps:
            try:
                output = self._run_capture([adb, "shell", "pm", "list", "packages"], cancel_requested)
                apps = self._parse_package_list(output)
            except subprocess.CalledProcessError:
                apps = []
        return sorted(apps, key=lambda item: (item.label.lower(), item.package_name.lower()))

    def launch_app(self, package: str, activity: str | None = None, cancel_requested=None, progress_callback=None) -> TaskResult:
        self._check_cancel(cancel_requested)
        ip = self.settings.default_android_tv_ip
        adb = self.settings.adb_path
        self._connect(adb, ip, cancel_requested)

        if activity:
            component = f"{package}/{activity}"
            cmd = [adb, "shell", "am", "start", "-n", component]
        else:
            cmd = [adb, "shell", "monkey", "-p", package, "1"]
        if progress_callback:
            progress_callback(f"앱 실행 중: {package}")
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

    def _get_screen_size(self, adb: str, cancel_requested=None) -> tuple[int, int]:
        if self._screen_size:
            return self._screen_size
        output = self._run_capture([adb, "shell", "wm", "size"], cancel_requested)
        match = re.search(r"(\d+)\s*x\s*(\d+)", output)
        if match:
            width = max(1, int(match.group(1)))
            height = max(1, int(match.group(2)))
            self._screen_size = (width, height)
            return self._screen_size
        self._screen_size = (1920, 1080)
        return self._screen_size

    def _clamp_int(self, value: int, minimum: int, maximum: int) -> int:
        return max(minimum, min(value, maximum))

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
