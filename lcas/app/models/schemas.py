from __future__ import annotations

from enum import Enum
from typing import Any, Dict, Optional
from uuid import uuid4

from pydantic import BaseModel, Field


class TaskStatus(str, Enum):
    pending = "pending"
    running = "running"
    done = "done"
    failed = "failed"
    canceled = "canceled"


class ReminderStatus(str, Enum):
    scheduled = "scheduled"
    fired = "fired"
    canceled = "canceled"


class RiskLevel(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"
    blocked = "blocked"


class CommandRequest(BaseModel):
    command: str = Field(..., min_length=1)
    user_id: Optional[str] = None
    source: str = "web"


class CommandAcceptedResponse(BaseModel):
    status: str = "accepted"
    task_id: str


class TaskResult(BaseModel):
    message: str
    executed_command: Optional[str] = None
    device: Optional[str] = None
    raw: Optional[Dict[str, Any]] = None


class TaskStatusResponse(BaseModel):
    task_id: str
    status: TaskStatus
    result: Optional[TaskResult] = None
    error: Optional[str] = None
    cancel_requested: bool = False


class IntentPayload(BaseModel):
    intent: str
    parameters: Dict[str, Any] = Field(default_factory=dict)
    target_device: str = "android_tv"
    risk_level: RiskLevel = RiskLevel.low
    source: str = "rule_engine"
    requires_confirmation: bool = False


class TaskRecord(BaseModel):
    task_id: str = Field(default_factory=lambda: str(uuid4()))
    command: str
    status: TaskStatus = TaskStatus.pending
    intent: Optional[IntentPayload] = None
    result: Optional[TaskResult] = None
    error: Optional[str] = None
    cancel_requested: bool = False


class MediaKind(str, Enum):
    video = "video"
    audio = "audio"
    image = "image"
    file = "file"


class MediaItem(BaseModel):
    media_id: str = Field(default_factory=lambda: str(uuid4()))
    original_name: str
    stored_name: str
    content_type: str
    kind: MediaKind
    size_bytes: int
    url: str
    created_at: str


class FavoriteVideoLink(BaseModel):
    favorite_id: str = Field(default_factory=lambda: str(uuid4()))
    title: str
    url: str
    created_at: str


class MediaUploadRequest(BaseModel):
    filename: str
    content_type: str
    data_base64: str


class MediaUploadResponse(BaseModel):
    item: MediaItem


class MediaLibraryResponse(BaseModel):
    uploads: list[MediaItem]
    favorites: list[FavoriteVideoLink]


class FavoriteVideoRequest(BaseModel):
    title: str
    url: str


class TextInputRequest(BaseModel):
    text: str = Field(..., min_length=1)


class WeatherResponse(BaseModel):
    label: str
    temperature_c: float | None = None
    description: str
    wind_speed: float | None = None
    humidity: int | None = None
    observation_time: str | None = None


class NewsItem(BaseModel):
    title: str
    link: str
    published_at: str | None = None
    summary: str | None = None


class NewsFeedResponse(BaseModel):
    source: str
    title: str
    link: str | None = None
    updated_at: str | None = None
    items: list[NewsItem]


class PowerTimerRequest(BaseModel):
    minutes: int = Field(..., ge=1, le=720)


class PowerTimerResponse(BaseModel):
    timer_id: str
    minutes: int
    due_at: str


class ReminderRequest(BaseModel):
    title: str = Field(..., min_length=1)
    due_at: str = Field(..., min_length=1)
    note: str = ""
    power_on: bool = True
    wake_screen: bool = True


class ReminderItem(BaseModel):
    reminder_id: str = Field(default_factory=lambda: str(uuid4()))
    title: str
    due_at: str
    note: str = ""
    created_at: str
    status: ReminderStatus = ReminderStatus.scheduled
    fired_at: str | None = None
    power_on: bool = True
    wake_screen: bool = True
