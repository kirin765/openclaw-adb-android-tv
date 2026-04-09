from __future__ import annotations

import base64

from fastapi import APIRouter, BackgroundTasks, Depends, Header, HTTPException, WebSocket, WebSocketDisconnect

from app.core.settings import Settings, get_settings
from app.models.schemas import (
    CommandAcceptedResponse,
    CommandRequest,
    FavoriteVideoLink,
    FavoriteVideoRequest,
    MediaLibraryResponse,
    MediaUploadRequest,
    MediaUploadResponse,
    NewsFeedResponse,
    ReminderItem,
    ReminderRequest,
    PowerTimerRequest,
    PowerTimerResponse,
    RiskLevel,
    TaskRecord,
    TaskStatusResponse,
    IntentPayload,
    TextInputRequest,
    WeatherResponse,
)
from app.services.command_router import CommandRouter
from app.services.learned_rule_service import LearnedRuleService
from app.services.media_library import build_media_library
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
