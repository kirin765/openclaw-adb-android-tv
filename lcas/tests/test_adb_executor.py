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
