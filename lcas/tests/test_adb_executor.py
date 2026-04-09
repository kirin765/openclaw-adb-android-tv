from __future__ import annotations

from app.core import settings as settings_module
from app.executors import adb_executor as adb_executor_module
from app.executors.adb_executor import AdbExecutor
from app.models.schemas import IntentPayload


def test_adb_executor_uses_configured_android_tv_ip(monkeypatch):
    commands: list[list[str]] = []

    class FakeProcess:
        def __init__(self, cmd):
            self.cmd = cmd
            self.returncode = 0

        def poll(self):
            return 0

        def communicate(self):
            return "", ""

        def wait(self, timeout=None):
            return 0

        def terminate(self):
            return None

        def kill(self):
            return None

    def fake_popen(cmd, stdout=None, stderr=None, text=None):
        commands.append(cmd)
        return FakeProcess(cmd)

    monkeypatch.setenv("DEFAULT_ANDROID_TV_IP", "192.168.0.161")
    settings_module.get_settings.cache_clear()
    monkeypatch.setattr(adb_executor_module.subprocess, "Popen", fake_popen)

    executor = AdbExecutor()
    result = executor.execute(
        IntentPayload(
            intent="TV_KEYEVENT",
            parameters={"keycode": 3},
            target_device="android_tv",
        )
    )

    assert commands[0] == ["adb", "connect", "192.168.0.161"]
    assert commands[1] == ["adb", "shell", "input", "keyevent", "3"]
    assert result.device == "livingroom-tv"


def test_adb_executor_can_power_off_and_send_text(monkeypatch):
    commands: list[list[str]] = []

    class FakeProcess:
        def __init__(self, cmd):
            self.cmd = cmd
            self.returncode = 0

        def poll(self):
            return 0

        def communicate(self):
            return "", ""

        def wait(self, timeout=None):
            return 0

        def terminate(self):
            return None

        def kill(self):
            return None

    def fake_popen(cmd, stdout=None, stderr=None, text=None):
        commands.append(cmd)
        return FakeProcess(cmd)

    monkeypatch.setenv("DEFAULT_ANDROID_TV_IP", "192.168.0.161")
    settings_module.get_settings.cache_clear()
    monkeypatch.setattr(adb_executor_module.subprocess, "Popen", fake_popen)

    executor = AdbExecutor()
    power_result = executor.execute(
        IntentPayload(
            intent="TV_POWER_OFF",
            parameters={},
            target_device="android_tv",
        )
    )
    text_result = executor.execute(
        IntentPayload(
            intent="TV_INPUT_TEXT",
            parameters={"text": "hello world"},
            target_device="android_tv",
        )
    )

    assert commands[0] == ["adb", "connect", "192.168.0.161"]
    assert commands[1] == ["adb", "shell", "input", "keyevent", "26"]
    assert commands[-1] == ["adb", "shell", "input", "text", "hello%sworld"]
    assert power_result.device == "livingroom-tv"
    assert text_result.raw["text"] == "hello world"


def test_adb_executor_can_power_on_and_wake_screen(monkeypatch):
    commands: list[list[str]] = []

    class FakeProcess:
        def __init__(self, cmd):
            self.cmd = cmd
            self.returncode = 0

        def poll(self):
            return 0

        def communicate(self):
            return "", ""

        def wait(self, timeout=None):
            return 0

        def terminate(self):
            return None

        def kill(self):
            return None

    def fake_popen(cmd, stdout=None, stderr=None, text=None):
        commands.append(cmd)
        return FakeProcess(cmd)

    monkeypatch.setenv("DEFAULT_ANDROID_TV_IP", "192.168.0.161")
    settings_module.get_settings.cache_clear()
    monkeypatch.setattr(adb_executor_module.subprocess, "Popen", fake_popen)

    executor = AdbExecutor()
    power_on_result = executor.execute(
        IntentPayload(
            intent="TV_POWER_ON",
            parameters={},
            target_device="android_tv",
        )
    )
    wake_result = executor.execute(
        IntentPayload(
            intent="TV_WAKE_SCREEN",
            parameters={},
            target_device="android_tv",
        )
    )

    assert commands[1] == ["adb", "shell", "input", "keyevent", "224"]
    assert commands[-1] == ["adb", "shell", "input", "keyevent", "224"]
    assert power_on_result.message == "Turned power on"
    assert wake_result.message == "Woke screen"


def test_adb_executor_can_open_tv_url(monkeypatch):
    commands: list[list[str]] = []

    class FakeProcess:
        def __init__(self, cmd):
            self.cmd = cmd
            self.returncode = 0

        def poll(self):
            return 0

        def communicate(self):
            return "", ""

        def wait(self, timeout=None):
            return 0

        def terminate(self):
            return None

        def kill(self):
            return None

    def fake_popen(cmd, stdout=None, stderr=None, text=None):
        commands.append(cmd)
        return FakeProcess(cmd)

    monkeypatch.setenv("DEFAULT_ANDROID_TV_IP", "192.168.0.161")
    settings_module.get_settings.cache_clear()
    monkeypatch.setattr(adb_executor_module.subprocess, "Popen", fake_popen)

    executor = AdbExecutor()
    result = executor.execute(
        IntentPayload(
            intent="TV_OPEN_URL",
            parameters={"url": "http://192.168.0.172:8000/?mode=tv&view=standby"},
            target_device="android_tv",
        )
    )

    assert commands[1] == [
        "adb",
        "shell",
        "am",
        "start",
        "-a",
        "android.intent.action.VIEW",
        "-d",
        "http://192.168.0.172:8000/?mode=tv&view=standby",
    ]
    assert result.raw["url"].endswith("view=standby")


def test_adb_executor_lists_and_launches_apps(monkeypatch):
    commands: list[list[str]] = []

    class FakeProcess:
        def __init__(self, cmd, stdout_text=""):
            self.cmd = cmd
            self.returncode = 0
            self._stdout_text = stdout_text

        def poll(self):
            return 0

        def communicate(self):
            return self._stdout_text, ""

        def wait(self, timeout=None):
            return 0

        def terminate(self):
            return None

        def kill(self):
            return None

    def fake_popen(cmd, stdout=None, stderr=None, text=None):
        command_tuple = tuple(cmd)
        commands.append(cmd)
        if command_tuple[:5] == ("adb", "shell", "cmd", "package", "query-intent-activities"):
            stdout_text = "ResolveInfo{123 com.netflix.ninja/.MainActivity}\nResolveInfo{456 com.google.android.youtube.tv/.HomeActivity}\n"
        elif command_tuple[:4] == ("adb", "shell", "pm", "list"):
            stdout_text = "package:com.netflix.ninja\npackage:com.google.android.youtube.tv\n"
        else:
            stdout_text = ""
        return FakeProcess(cmd, stdout_text)

    monkeypatch.setenv("DEFAULT_ANDROID_TV_IP", "192.168.0.161")
    settings_module.get_settings.cache_clear()
    monkeypatch.setattr(adb_executor_module.subprocess, "Popen", fake_popen)

    executor = AdbExecutor()
    apps = executor.list_launchable_apps()
    launch_result = executor.launch_app("com.netflix.ninja", ".MainActivity")

    assert commands[0] == ["adb", "connect", "192.168.0.161"]
    assert apps[0].package_name in {"com.google.android.youtube.tv", "com.netflix.ninja"}
    assert any(app.label for app in apps)
    assert commands[-1] == ["adb", "shell", "am", "start", "-n", "com.netflix.ninja/.MainActivity"]
    assert launch_result.raw["package"] == "com.netflix.ninja"


def test_adb_executor_falls_back_when_query_intent_fails(monkeypatch):
    commands: list[list[str]] = []

    class FakeProcess:
        def __init__(self, cmd, stdout_text="", returncode=0):
            self.cmd = cmd
            self.returncode = returncode
            self._stdout_text = stdout_text

        def poll(self):
            return 0 if self.returncode == 0 else self.returncode

        def communicate(self):
            return self._stdout_text, "boom"

        def wait(self, timeout=None):
            return 0

        def terminate(self):
            return None

        def kill(self):
            return None

    def fake_popen(cmd, stdout=None, stderr=None, text=None):
        command_tuple = tuple(cmd)
        commands.append(cmd)
        if command_tuple[:5] == ("adb", "shell", "cmd", "package", "query-intent-activities"):
            return FakeProcess(cmd, "", returncode=255)
        if command_tuple[:4] == ("adb", "shell", "pm", "list"):
            return FakeProcess(cmd, "package:com.netflix.ninja\n")
        return FakeProcess(cmd, "")

    monkeypatch.setenv("DEFAULT_ANDROID_TV_IP", "192.168.0.161")
    settings_module.get_settings.cache_clear()
    monkeypatch.setattr(adb_executor_module.subprocess, "Popen", fake_popen)

    executor = AdbExecutor()
    apps = executor.list_launchable_apps()

    assert commands[0] == ["adb", "connect", "192.168.0.161"]
    assert ["adb", "shell", "cmd", "package", "query-intent-activities", "-a", "android.intent.action.MAIN", "-c", "android.intent.category.LAUNCHER"] in commands
    assert ["adb", "shell", "pm", "list", "packages", "-3"] in commands or ["adb", "shell", "pm", "list", "packages"] in commands
    assert apps[0].package_name == "com.netflix.ninja"
