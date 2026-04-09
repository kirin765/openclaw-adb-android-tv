from __future__ import annotations

from app.executors.browser_executor import BrowserExecutor
from app.models.schemas import IntentPayload


def test_browser_executor_opens_default_browser(monkeypatch):
    launched = []

    def fake_popen(cmd, stdout=None, stderr=None):
        launched.append(cmd)

        class Proc:
            pass

        return Proc()

    monkeypatch.setattr("app.executors.browser_executor.which", lambda _: "/usr/bin/xdg-open")
    monkeypatch.setattr("app.executors.browser_executor.subprocess.Popen", fake_popen)

    result = BrowserExecutor().execute(
        IntentPayload(
            intent="OPEN_BROWSER",
            parameters={"url": "about:blank"},
            target_device="pc",
        )
    )

    assert launched[0] == ["xdg-open", "about:blank"]
    assert result.device == "local-pc"


def test_browser_executor_opens_specific_url(monkeypatch):
    launched = []

    def fake_popen(cmd, stdout=None, stderr=None):
        launched.append(cmd)

        class Proc:
            pass

        return Proc()

    monkeypatch.setattr("app.executors.browser_executor.which", lambda _: "/usr/bin/firefox")
    monkeypatch.setattr("app.executors.browser_executor.subprocess.Popen", fake_popen)

    result = BrowserExecutor().execute(
        IntentPayload(
            intent="OPEN_URL",
            parameters={"url": "https://example.com"},
            target_device="pc",
        )
    )

    assert launched[0] == ["xdg-open", "https://example.com"]
    assert result.raw["url"] == "https://example.com"
