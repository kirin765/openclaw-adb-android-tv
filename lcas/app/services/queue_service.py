from __future__ import annotations

from typing import Callable

from fastapi import BackgroundTasks
from redis import Redis
from rq import Queue

from app.core.settings import get_settings
from app.workers.tasks import execute_task


class QueueService:
    def __init__(self) -> None:
        self.settings = get_settings()

    def enqueue(self, task_id: str, intent_data: dict, background_tasks: BackgroundTasks | None = None) -> None:
        try:
            redis = Redis.from_url(self.settings.redis_url)
            queue = Queue("lcas", connection=redis)
            queue.enqueue(execute_task, task_id, intent_data, job_id=task_id)
        except Exception:
            if background_tasks is None:
                raise
            background_tasks.add_task(execute_task, task_id, intent_data)

    def cancel(self, task_id: str) -> bool:
        try:
            redis = Redis.from_url(self.settings.redis_url)
            queue = Queue("lcas", connection=redis)
            job = queue.fetch_job(task_id)
            if job:
                job.cancel()
                return True
        except Exception:
            return False
        return False
