from __future__ import annotations

import base64
from datetime import datetime

from fastapi import APIRouter, BackgroundTasks, Depends, Header, HTTPException, WebSocket, WebSocketDisconnect

from app.core.settings import Settings, get_settings
from app.models.schemas import (
    CommandAcceptedResponse,
    CommandRequest,
    FavoriteVideoLink,
    FavoriteVideoRequest,
    FridgeItem,
    FridgeItemRequest,
    FridgeStateResponse,
    FamilyBoardPost,
    FamilyBoardPostRequest,
    FamilyBoardStateResponse,
    FamilyCalendarEvent,
    FamilyCalendarEventRequest,
    FamilyCalendarStateResponse,
    FamilyMoodRecord,
    FamilyMoodRecordRequest,
    FamilyMoodStateResponse,
    FamilyTodoItem,
    FamilyTodoItemRequest,
    FamilyTodoStateResponse,
    MediaLibraryResponse,
    MediaUploadRequest,
    MediaUploadResponse,
    MirrorState,
    NewsFeedResponse,
    ReminderItem,
    ReminderRequest,
    PowerTimerRequest,
    PowerTimerResponse,
    RiskLevel,
    TvAppLaunchRequest,
    TvAppListResponse,
    TaskRecord,
    TaskStatusResponse,
    IntentPayload,
    TextInputRequest,
    WeatherResponse,
)
from app.services.command_router import CommandRouter
from app.executors.adb_executor import AdbExecutor
from app.services.family_board_hub import family_board_hub
from app.services.family_board_service import build_family_board_service
from app.services.family_board_store import build_family_board_store
from app.services.family_mood_hub import family_mood_hub
from app.services.family_mood_service import build_family_mood_service
from app.services.family_mood_store import build_family_mood_store
from app.services.family_todo_hub import family_todo_hub
from app.services.family_todo_service import build_family_todo_service
from app.services.family_todo_store import build_family_todo_store
from app.services.family_calendar_service import build_family_calendar_service
from app.services.fridge_service import build_fridge_service
from app.services.learned_rule_service import LearnedRuleService
from app.services.media_library import build_media_library
from app.services.mirror_hub import mirror_hub
from app.services.mirror_service import mirror_service
from app.services.news_service import NewsService
from app.services.power_service import power_service
from app.services.reminder_hub import reminder_hub
from app.services.reminder_service import reminder_service
from app.services.queue_service import QueueService
from app.services.task_store import task_store
from app.services.whiteboard import whiteboard_store
from app.services.whiteboard_hub import whiteboard_hub
from app.services.weather_service import WeatherService

router = APIRouter()


@router.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@router.post("/command", response_model=CommandAcceptedResponse)
async def submit_command(
    request: CommandRequest,
    background_tasks: BackgroundTasks,
    x_api_token: str | None = Header(default=None),
    settings: Settings = Depends(get_settings),
) -> CommandAcceptedResponse:
    if x_api_token != settings.api_token:
        raise HTTPException(status_code=401, detail="Invalid API token")

    router_service = CommandRouter(settings.rules_path, settings.learned_rules_path, settings.openclaw_bridge_url)
    intent = await router_service.route(request)
    if intent.source == "openclaw_bridge":
        LearnedRuleService(settings.learned_rules_path).learn(request.command, intent)
    record = TaskRecord(command=request.command, intent=intent)
    task_store.create(record)

    QueueService().enqueue(record.task_id, intent.model_dump(), background_tasks)
    return CommandAcceptedResponse(task_id=record.task_id)


@router.get("/status/{task_id}", response_model=TaskStatusResponse)
def get_status(task_id: str) -> TaskStatusResponse:
    record = task_store.get(task_id)
    if not record:
        raise HTTPException(status_code=404, detail="Task not found")
    return TaskStatusResponse(task_id=record.task_id, status=record.status, result=record.result, error=record.error, cancel_requested=record.cancel_requested)


@router.post("/cancel/{task_id}", response_model=TaskStatusResponse)
def cancel_task(
    task_id: str,
    x_api_token: str | None = Header(default=None),
    settings: Settings = Depends(get_settings),
) -> TaskStatusResponse:
    if x_api_token != settings.api_token:
        raise HTTPException(status_code=401, detail="Invalid API token")

    record = task_store.get(task_id)
    if not record:
        raise HTTPException(status_code=404, detail="Task not found")

    task_store.request_cancel(task_id)
    QueueService().cancel(task_id)
    record = task_store.get(task_id)
    return TaskStatusResponse(task_id=record.task_id, status=record.status, result=record.result, error=record.error, cancel_requested=record.cancel_requested)


@router.get("/media/library", response_model=MediaLibraryResponse)
def get_media_library(settings: Settings = Depends(get_settings)) -> MediaLibraryResponse:
    library = build_media_library(settings.storage_dir)
    return MediaLibraryResponse(uploads=library.list_uploads(), favorites=library.list_favorites())


@router.post("/media/upload", response_model=MediaUploadResponse)
def upload_media(
    payload: MediaUploadRequest,
    x_api_token: str | None = Header(default=None),
    settings: Settings = Depends(get_settings),
) -> MediaUploadResponse:
    if x_api_token != settings.api_token:
        raise HTTPException(status_code=401, detail="Invalid API token")

    library = build_media_library(settings.storage_dir)
    try:
        base64.b64decode(payload.data_base64)
    except Exception as exc:
        raise HTTPException(status_code=400, detail="Invalid base64 media payload") from exc
    item = library.add_upload(payload.filename, payload.content_type, payload.data_base64)
    return MediaUploadResponse(item=item)


@router.get("/favorites/videos", response_model=list[FavoriteVideoLink])
def list_favorite_videos(settings: Settings = Depends(get_settings)) -> list[FavoriteVideoLink]:
    library = build_media_library(settings.storage_dir)
    return library.list_favorites()


@router.post("/favorites/videos", response_model=FavoriteVideoLink)
def add_favorite_video(
    payload: FavoriteVideoRequest,
    x_api_token: str | None = Header(default=None),
    settings: Settings = Depends(get_settings),
) -> FavoriteVideoLink:
    if x_api_token != settings.api_token:
        raise HTTPException(status_code=401, detail="Invalid API token")
    library = build_media_library(settings.storage_dir)
    return library.add_favorite(payload.title, payload.url)


@router.delete("/favorites/videos/{favorite_id}", response_model=dict[str, bool])
def remove_favorite_video(
    favorite_id: str,
    x_api_token: str | None = Header(default=None),
    settings: Settings = Depends(get_settings),
) -> dict[str, bool]:
    if x_api_token != settings.api_token:
        raise HTTPException(status_code=401, detail="Invalid API token")
    library = build_media_library(settings.storage_dir)
    return {"removed": library.remove_favorite(favorite_id)}


@router.get("/fridge/state", response_model=FridgeStateResponse)
def fridge_state(settings: Settings = Depends(get_settings)) -> FridgeStateResponse:
    return build_fridge_service(settings.storage_dir).snapshot_state()


@router.post("/fridge/items", response_model=FridgeItem)
def add_fridge_item(
    payload: FridgeItemRequest,
    x_api_token: str | None = Header(default=None),
    settings: Settings = Depends(get_settings),
) -> FridgeItem:
    if x_api_token != settings.api_token:
        raise HTTPException(status_code=401, detail="Invalid API token")
    try:
        return build_fridge_service(settings.storage_dir).add_item(payload)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.delete("/fridge/items/{fridge_item_id}", response_model=dict[str, bool])
def delete_fridge_item(
    fridge_item_id: str,
    x_api_token: str | None = Header(default=None),
    settings: Settings = Depends(get_settings),
) -> dict[str, bool]:
    if x_api_token != settings.api_token:
        raise HTTPException(status_code=401, detail="Invalid API token")
    removed = build_fridge_service(settings.storage_dir).remove_item(fridge_item_id)
    return {"removed": removed}


@router.get("/family-calendar/state", response_model=FamilyCalendarStateResponse)
def family_calendar_state(settings: Settings = Depends(get_settings)) -> FamilyCalendarStateResponse:
    return build_family_calendar_service(settings.storage_dir).snapshot_state()


@router.post("/family-calendar/events", response_model=FamilyCalendarEvent)
def add_family_calendar_event(
    payload: FamilyCalendarEventRequest,
    x_api_token: str | None = Header(default=None),
    settings: Settings = Depends(get_settings),
) -> FamilyCalendarEvent:
    if x_api_token != settings.api_token:
        raise HTTPException(status_code=401, detail="Invalid API token")
    try:
        return build_family_calendar_service(settings.storage_dir).add_event(payload)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.delete("/family-calendar/events/{calendar_event_id}", response_model=dict[str, bool])
def delete_family_calendar_event(
    calendar_event_id: str,
    x_api_token: str | None = Header(default=None),
    settings: Settings = Depends(get_settings),
) -> dict[str, bool]:
    if x_api_token != settings.api_token:
        raise HTTPException(status_code=401, detail="Invalid API token")
    removed = build_family_calendar_service(settings.storage_dir).remove_event(calendar_event_id)
    return {"removed": removed}


@router.get("/family-mood/state", response_model=FamilyMoodStateResponse)
def family_mood_state(settings: Settings = Depends(get_settings)) -> FamilyMoodStateResponse:
    store = build_family_mood_store(settings.storage_dir)
    family_mood_hub.set_store(store)
    return build_family_mood_service(store).snapshot_state()


@router.post("/family-mood/records", response_model=FamilyMoodRecord)
async def add_family_mood_record(
    payload: FamilyMoodRecordRequest,
    x_api_token: str | None = Header(default=None),
    settings: Settings = Depends(get_settings),
) -> FamilyMoodRecord:
    if x_api_token != settings.api_token:
        raise HTTPException(status_code=401, detail="Invalid API token")
    store = build_family_mood_store(settings.storage_dir)
    family_mood_hub.set_store(store)
    service = build_family_mood_service(store)
    try:
        record = service.add_record(payload)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    snapshot = service.snapshot_state()
    await family_mood_hub.broadcast({
        "type": "snapshot",
        "records": [item.model_dump() for item in snapshot.records],
        "checked_at": snapshot.checked_at,
    })
    return record


@router.delete("/family-mood/records/{mood_record_id}", response_model=dict[str, bool])
async def delete_family_mood_record(
    mood_record_id: str,
    x_api_token: str | None = Header(default=None),
    settings: Settings = Depends(get_settings),
) -> dict[str, bool]:
    if x_api_token != settings.api_token:
        raise HTTPException(status_code=401, detail="Invalid API token")
    store = build_family_mood_store(settings.storage_dir)
    family_mood_hub.set_store(store)
    service = build_family_mood_service(store)
    removed = service.remove_record(mood_record_id)
    if removed:
        snapshot = service.snapshot_state()
        await family_mood_hub.broadcast({
            "type": "snapshot",
            "records": [item.model_dump() for item in snapshot.records],
            "checked_at": snapshot.checked_at,
        })
    return {"removed": removed}


@router.websocket("/ws/family-mood")
async def family_mood_socket(websocket: WebSocket) -> None:
    await family_mood_hub.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        family_mood_hub.disconnect(websocket)


@router.get("/family-todo/state", response_model=FamilyTodoStateResponse)
def family_todo_state(settings: Settings = Depends(get_settings)) -> FamilyTodoStateResponse:
    store = build_family_todo_store(settings.storage_dir)
    family_todo_hub.set_store(store)
    return build_family_todo_service(store).snapshot_state()


@router.post("/family-todo/items", response_model=FamilyTodoItem)
async def add_family_todo_item(
    payload: FamilyTodoItemRequest,
    x_api_token: str | None = Header(default=None),
    settings: Settings = Depends(get_settings),
) -> FamilyTodoItem:
    if x_api_token != settings.api_token:
        raise HTTPException(status_code=401, detail="Invalid API token")
    store = build_family_todo_store(settings.storage_dir)
    family_todo_hub.set_store(store)
    service = build_family_todo_service(store)
    try:
        item = service.add_item(payload)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    snapshot = service.snapshot_state()
    await family_todo_hub.broadcast({
        "type": "snapshot",
        "items": [entry.model_dump() for entry in snapshot.items],
        "checked_at": snapshot.checked_at,
    })
    return item


@router.patch("/family-todo/items/{todo_item_id}", response_model=dict[str, bool])
async def update_family_todo_item(
    todo_item_id: str,
    payload: dict[str, bool],
    x_api_token: str | None = Header(default=None),
    settings: Settings = Depends(get_settings),
) -> dict[str, bool]:
    if x_api_token != settings.api_token:
        raise HTTPException(status_code=401, detail="Invalid API token")
    store = build_family_todo_store(settings.storage_dir)
    family_todo_hub.set_store(store)
    service = build_family_todo_service(store)
    done = bool(payload.get("done", False))
    updated = service.set_done(todo_item_id, done)
    if updated:
        snapshot = service.snapshot_state()
        await family_todo_hub.broadcast({
            "type": "snapshot",
            "items": [entry.model_dump() for entry in snapshot.items],
            "checked_at": snapshot.checked_at,
        })
    return {"updated": updated}


@router.delete("/family-todo/items/{todo_item_id}", response_model=dict[str, bool])
async def delete_family_todo_item(
    todo_item_id: str,
    x_api_token: str | None = Header(default=None),
    settings: Settings = Depends(get_settings),
) -> dict[str, bool]:
    if x_api_token != settings.api_token:
        raise HTTPException(status_code=401, detail="Invalid API token")
    store = build_family_todo_store(settings.storage_dir)
    family_todo_hub.set_store(store)
    service = build_family_todo_service(store)
    removed = service.remove_item(todo_item_id)
    if removed:
        snapshot = service.snapshot_state()
        await family_todo_hub.broadcast({
            "type": "snapshot",
            "items": [entry.model_dump() for entry in snapshot.items],
            "checked_at": snapshot.checked_at,
        })
    return {"removed": removed}


@router.websocket("/ws/family-todo")
async def family_todo_socket(websocket: WebSocket) -> None:
    await family_todo_hub.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        family_todo_hub.disconnect(websocket)


@router.get("/family-board/state", response_model=FamilyBoardStateResponse)
def family_board_state(settings: Settings = Depends(get_settings)) -> FamilyBoardStateResponse:
    store = build_family_board_store(settings.storage_dir)
    return build_family_board_service(store).snapshot_state()


@router.post("/family-board/posts", response_model=FamilyBoardPost)
async def add_family_board_post(
    payload: FamilyBoardPostRequest,
    x_api_token: str | None = Header(default=None),
    settings: Settings = Depends(get_settings),
) -> FamilyBoardPost:
    if x_api_token != settings.api_token:
        raise HTTPException(status_code=401, detail="Invalid API token")
    store = build_family_board_store(settings.storage_dir)
    family_board_hub.set_store(store)
    service = build_family_board_service(store)
    try:
        post = service.add_post(payload)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    snapshot = service.snapshot_state()
    await family_board_hub.broadcast({"type": "snapshot", "posts": [item.model_dump() for item in snapshot.posts], "checked_at": snapshot.checked_at})
    return post


@router.delete("/family-board/posts/{board_post_id}", response_model=dict[str, bool])
async def delete_family_board_post(
    board_post_id: str,
    x_api_token: str | None = Header(default=None),
    settings: Settings = Depends(get_settings),
) -> dict[str, bool]:
    if x_api_token != settings.api_token:
        raise HTTPException(status_code=401, detail="Invalid API token")
    store = build_family_board_store(settings.storage_dir)
    family_board_hub.set_store(store)
    service = build_family_board_service(store)
    removed = service.remove_post(board_post_id)
    if removed:
        snapshot = service.snapshot_state()
        await family_board_hub.broadcast({"type": "snapshot", "posts": [item.model_dump() for item in snapshot.posts], "checked_at": snapshot.checked_at})
    return {"removed": removed}


@router.websocket("/ws/family-board")
async def family_board_socket(websocket: WebSocket) -> None:
    await family_board_hub.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        family_board_hub.disconnect(websocket)


@router.get("/weather/current", response_model=WeatherResponse)
async def current_weather(settings: Settings = Depends(get_settings)) -> WeatherResponse:
    service = WeatherService(settings.weather_latitude, settings.weather_longitude, settings.weather_label, settings.weather_units)
    return await service.get_current()


@router.get("/news/yonhap", response_model=NewsFeedResponse)
async def yonhap_news(settings: Settings = Depends(get_settings)) -> NewsFeedResponse:
    service = NewsService(settings.yonhap_rss_url)
    try:
        return await service.get_yonhap_feed()
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"연합뉴스 피드를 불러오지 못했습니다: {exc}") from exc


@router.get("/mirror/state", response_model=MirrorState)
def mirror_state() -> MirrorState:
    return mirror_service.get_state()


@router.post("/tv/text", response_model=CommandAcceptedResponse)
def tv_text_input(
    payload: TextInputRequest,
    background_tasks: BackgroundTasks,
    x_api_token: str | None = Header(default=None),
    settings: Settings = Depends(get_settings),
) -> TaskStatusResponse:
    if x_api_token != settings.api_token:
        raise HTTPException(status_code=401, detail="Invalid API token")

    intent = IntentPayload(
        intent="TV_INPUT_TEXT",
        parameters={"text": payload.text},
        target_device="android_tv",
        risk_level=RiskLevel.low,
        source="web_ui",
        requires_confirmation=False,
    )
    record = TaskRecord(command=payload.text, intent=intent)
    task_store.create(record)
    QueueService().enqueue(record.task_id, intent.model_dump(), background_tasks)
    return CommandAcceptedResponse(task_id=record.task_id)


@router.get("/tv/apps", response_model=TvAppListResponse)
def tv_apps(settings: Settings = Depends(get_settings)) -> TvAppListResponse:
    executor = AdbExecutor()
    try:
        apps = executor.list_launchable_apps()
        return TvAppListResponse(apps=apps, checked_at=datetime.now().isoformat(timespec="seconds"))
    except Exception as exc:
        return TvAppListResponse(apps=[], checked_at=datetime.now().isoformat(timespec="seconds"), error=str(exc))


@router.post("/tv/apps/launch", response_model=dict[str, str])
def tv_launch_app(
    payload: TvAppLaunchRequest,
    x_api_token: str | None = Header(default=None),
    settings: Settings = Depends(get_settings),
) -> dict[str, str]:
    if x_api_token != settings.api_token:
        raise HTTPException(status_code=401, detail="Invalid API token")
    executor = AdbExecutor()
    try:
        result = executor.launch_app(payload.package_name, payload.activity_name or None)
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"TV 앱 실행에 실패했습니다: {exc}") from exc
    return {"message": result.message, "executed_command": result.executed_command or "", "device": result.device or ""}


@router.post("/tv/power/off", response_model=dict[str, str])
def tv_power_off(
    x_api_token: str | None = Header(default=None),
    settings: Settings = Depends(get_settings),
) -> dict[str, str]:
    if x_api_token != settings.api_token:
        raise HTTPException(status_code=401, detail="Invalid API token")
    result = power_service.power_off_now()
    return {"message": result.message}


@router.post("/tv/power/on", response_model=dict[str, str])
def tv_power_on(
    x_api_token: str | None = Header(default=None),
    settings: Settings = Depends(get_settings),
) -> dict[str, str]:
    if x_api_token != settings.api_token:
        raise HTTPException(status_code=401, detail="Invalid API token")
    result = power_service.power_on_now()
    return {"message": result.message}


@router.post("/tv/screen/wake", response_model=dict[str, str])
def tv_wake_screen(
    x_api_token: str | None = Header(default=None),
    settings: Settings = Depends(get_settings),
) -> dict[str, str]:
    if x_api_token != settings.api_token:
        raise HTTPException(status_code=401, detail="Invalid API token")
    result = power_service.wake_screen_now()
    return {"message": result.message}


@router.post("/tv/power/schedule", response_model=PowerTimerResponse)
def schedule_tv_power_off(
    payload: PowerTimerRequest,
    x_api_token: str | None = Header(default=None),
    settings: Settings = Depends(get_settings),
) -> PowerTimerResponse:
    if x_api_token != settings.api_token:
        raise HTTPException(status_code=401, detail="Invalid API token")
    schedule = power_service.schedule_power_off(payload.minutes)
    return PowerTimerResponse(timer_id=schedule.timer_id, minutes=schedule.minutes, due_at=schedule.due_at)


@router.get("/tv/power/schedule", response_model=list[PowerTimerResponse])
def list_tv_power_schedules() -> list[PowerTimerResponse]:
    schedules = power_service.list_schedules()
    return [PowerTimerResponse(timer_id=item.timer_id, minutes=item.minutes, due_at=item.due_at) for item in schedules]


@router.delete("/tv/power/schedule/{timer_id}", response_model=dict[str, bool])
def cancel_tv_power_schedule(
    timer_id: str,
    x_api_token: str | None = Header(default=None),
    settings: Settings = Depends(get_settings),
) -> dict[str, bool]:
    if x_api_token != settings.api_token:
        raise HTTPException(status_code=401, detail="Invalid API token")
    return {"removed": power_service.cancel_schedule(timer_id)}


@router.get("/reminders", response_model=list[ReminderItem])
def list_reminders() -> list[ReminderItem]:
    return reminder_service.list_reminders()


@router.post("/reminders", response_model=ReminderItem)
def create_reminder(
    payload: ReminderRequest,
    x_api_token: str | None = Header(default=None),
    settings: Settings = Depends(get_settings),
) -> ReminderItem:
    if x_api_token != settings.api_token:
        raise HTTPException(status_code=401, detail="Invalid API token")
    try:
        return reminder_service.schedule_reminder(payload)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.delete("/reminders/{reminder_id}", response_model=dict[str, bool])
def delete_reminder(
    reminder_id: str,
    x_api_token: str | None = Header(default=None),
    settings: Settings = Depends(get_settings),
) -> dict[str, bool]:
    if x_api_token != settings.api_token:
        raise HTTPException(status_code=401, detail="Invalid API token")
    return {"removed": reminder_service.remove_reminder(reminder_id)}


@router.websocket("/ws/whiteboard")
async def whiteboard_socket(websocket: WebSocket) -> None:
    await whiteboard_hub.connect(websocket)
    try:
        while True:
            data = await websocket.receive_json()
            event_type = data.get("type")
            if event_type in {"stroke", "stroke-point"}:
                stroke = {
                    "id": data.get("id"),
                    "points": data.get("points", []),
                    "color": data.get("color", "#7dd3fc"),
                    "size": data.get("size", 4),
                    "tool": data.get("tool", "pen"),
                }
                whiteboard_store.upsert_stroke(stroke)
                await whiteboard_hub.broadcast({"type": "stroke-point", "stroke": stroke, "clientId": data.get("clientId")})
            elif event_type == "clear":
                whiteboard_store.clear()
                await whiteboard_hub.broadcast({"type": "clear", "clientId": data.get("clientId")})
    except WebSocketDisconnect:
        whiteboard_hub.disconnect(websocket)


@router.websocket("/ws/reminders")
async def reminder_socket(websocket: WebSocket) -> None:
    await reminder_hub.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        reminder_hub.disconnect(websocket)


@router.websocket("/ws/mirror")
async def mirror_socket(websocket: WebSocket) -> None:
    await mirror_hub.connect(websocket)
    try:
        while True:
            data = await websocket.receive_json()
            event_type = data.get("type")
            if event_type == "start":
                state = mirror_service.start(
                    source_label=data.get("source_label", ""),
                    started_at=data.get("started_at"),
                )
                await mirror_hub.broadcast({"type": "snapshot", "mirror": state.model_dump()})
            elif event_type == "frame":
                frame_data_url = data.get("frame_data_url")
                if not frame_data_url:
                    continue
                state = mirror_service.update_frame(
                    frame_data_url=frame_data_url,
                    source_label=data.get("source_label", ""),
                    started_at=data.get("started_at"),
                )
                await mirror_hub.broadcast({"type": "frame", "mirror": state.model_dump()})
            elif event_type == "stop":
                state = mirror_service.stop()
                await mirror_hub.broadcast({"type": "stop", "mirror": state.model_dump()})
    except WebSocketDisconnect:
        mirror_hub.disconnect(websocket)
