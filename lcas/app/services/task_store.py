from __future__ import annotations

from threading import Lock
from typing import Dict

from app.models.schemas import TaskRecord, TaskResult, TaskStatus


class InMemoryTaskStore:
    def __init__(self) -> None:
        self._tasks: Dict[str, TaskRecord] = {}
        self._lock = Lock()

    def create(self, record: TaskRecord) -> TaskRecord:
        with self._lock:
            self._tasks[record.task_id] = record
        return record

    def get(self, task_id: str) -> TaskRecord | None:
        return self._tasks.get(task_id)

    def set_running(self, task_id: str) -> None:
        with self._lock:
            self._tasks[task_id].status = TaskStatus.running
            self._tasks[task_id].progress = "실행 중"

    def set_done(self, task_id: str, result: TaskResult) -> None:
        with self._lock:
            task = self._tasks[task_id]
            task.status = TaskStatus.done
            task.result = result
            task.error = None
            task.progress = result.message

    def set_failed(self, task_id: str, error: str) -> None:
        with self._lock:
            task = self._tasks[task_id]
            task.status = TaskStatus.failed
            task.error = error
            task.progress = "실패"

    def request_cancel(self, task_id: str) -> TaskRecord:
        with self._lock:
            task = self._tasks[task_id]
            if task.status in {TaskStatus.pending, TaskStatus.running}:
                task.cancel_requested = True
                if task.status == TaskStatus.pending:
                    task.status = TaskStatus.canceled
                    task.progress = "취소됨"
            return task

    def is_cancel_requested(self, task_id: str) -> bool:
        with self._lock:
            task = self._tasks.get(task_id)
            return bool(task and task.cancel_requested)

    def set_canceled(self, task_id: str) -> None:
        with self._lock:
            task = self._tasks[task_id]
            task.status = TaskStatus.canceled
            task.error = None
            task.progress = "취소됨"

    def set_progress(self, task_id: str, progress: str) -> None:
        with self._lock:
            task = self._tasks[task_id]
            task.progress = progress


task_store = InMemoryTaskStore()
