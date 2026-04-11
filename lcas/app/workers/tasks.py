from __future__ import annotations

from app.models.schemas import IntentPayload
from app.services.cancellation import TaskCancelled
from app.services.action_mapper import ActionMapper
from app.services.task_store import task_store


def execute_task(task_id: str, intent_data: dict) -> dict:
    if task_store.is_cancel_requested(task_id):
        task_store.set_canceled(task_id)
        return {"status": "canceled"}
    task_store.set_running(task_id)
    task_store.set_progress(task_id, "명령 해석 완료")
    if task_store.is_cancel_requested(task_id):
        task_store.set_canceled(task_id)
        return {"status": "canceled"}
    mapper = ActionMapper()
    intent = IntentPayload(**intent_data)
    try:
        task_store.set_progress(task_id, "실행기 선택 중")
        result = mapper.execute(
            intent,
            cancel_requested=lambda: task_store.is_cancel_requested(task_id),
            progress_callback=lambda message: task_store.set_progress(task_id, message),
        )
        task_store.set_done(task_id, result)
        return result.model_dump()
    except TaskCancelled:
        task_store.set_canceled(task_id)
        return {"status": "canceled"}
    except Exception as exc:
        task_store.set_failed(task_id, str(exc))
        raise
