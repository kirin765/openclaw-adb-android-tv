from __future__ import annotations

from abc import ABC, abstractmethod

from app.models.schemas import IntentPayload, TaskResult


class Executor(ABC):
    @abstractmethod
    def supports(self, intent: IntentPayload) -> bool:
        raise NotImplementedError

    @abstractmethod
    def execute(self, intent: IntentPayload, cancel_requested=None, progress_callback=None) -> TaskResult:
        raise NotImplementedError
