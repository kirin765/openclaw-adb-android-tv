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
    progress: str = ""


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
    progress: str = "대기 중"


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


class TvTrackpadRequest(BaseModel):
    action: str = Field(default="drag")
    delta_x: float = 0.0
    delta_y: float = 0.0
    duration_ms: int = Field(default=220, ge=50, le=2000)


class TvApp(BaseModel):
    package_name: str
    label: str
    activity_name: str = ""


class TvAppListResponse(BaseModel):
    apps: list[TvApp]
    checked_at: str
    error: str | None = None


class TvAppLaunchRequest(BaseModel):
    package_name: str
    activity_name: str = ""


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


class MirrorState(BaseModel):
    active: bool = False
    source_label: str = ""
    frame_data_url: str | None = None
    started_at: str | None = None
    updated_at: str | None = None
    frame_count: int = 0


class MirrorFrameRequest(BaseModel):
    type: str = "frame"
    frame_data_url: str = Field(..., min_length=1)
    source_label: str = ""
    started_at: str | None = None


class PowerTimerRequest(BaseModel):
    minutes: int = Field(..., ge=1, le=720)


class PowerTimerResponse(BaseModel):
    timer_id: str
    minutes: int
    due_at: str


class FridgeItemCategory(str, Enum):
    ingredient = "ingredient"
    side_dish = "side_dish"


class FridgeItemRequest(BaseModel):
    name: str = Field(..., min_length=1)
    category: FridgeItemCategory = FridgeItemCategory.ingredient
    quantity: str = ""
    note: str = ""


class FridgeItem(BaseModel):
    fridge_item_id: str = Field(default_factory=lambda: str(uuid4()))
    name: str
    category: FridgeItemCategory = FridgeItemCategory.ingredient
    quantity: str = ""
    note: str = ""
    created_at: str
    updated_at: str


class RecipeRecommendation(BaseModel):
    recipe_id: str
    title: str
    description: str
    score: int
    matched_items: list[str]
    missing_items: list[str]
    steps: list[str] = Field(default_factory=list)


class FridgeStateResponse(BaseModel):
    items: list[FridgeItem]
    recommendations: list[RecipeRecommendation]
    checked_at: str


class FamilyCalendarTag(str, Enum):
    brown = "김은영똥"


class FamilyCalendarEventRequest(BaseModel):
    title: str = Field(..., min_length=1)
    start_at: str = Field(..., min_length=1)
    end_at: str = ""
    location: str = ""
    attendees: str = ""
    tag: FamilyCalendarTag = FamilyCalendarTag.brown
    note: str = ""
    all_day: bool = False


class FamilyCalendarEvent(BaseModel):
    calendar_event_id: str = Field(default_factory=lambda: str(uuid4()))
    title: str
    start_at: str
    end_at: str = ""
    location: str = ""
    attendees: list[str] = Field(default_factory=list)
    tag: FamilyCalendarTag = FamilyCalendarTag.brown
    note: str = ""
    all_day: bool = False
    created_at: str
    updated_at: str


class FamilyCalendarStateResponse(BaseModel):
    events: list[FamilyCalendarEvent]
    today_events: list[FamilyCalendarEvent]
    upcoming_events: list[FamilyCalendarEvent]
    checked_at: str


class FamilyMoodRecordRequest(BaseModel):
    member: str = Field(..., min_length=1)
    mood: int = Field(..., ge=1, le=5)
    note: str = ""


class FamilyMoodRecord(BaseModel):
    mood_record_id: str = Field(default_factory=lambda: str(uuid4()))
    member: str
    mood: int = Field(..., ge=1, le=5)
    note: str = ""
    created_at: str


class FamilyMoodChartPoint(BaseModel):
    date: str
    mood: float
    count: int


class FamilyMoodSeries(BaseModel):
    member: str
    color: str
    points: list[FamilyMoodChartPoint]


class FamilyMoodStateResponse(BaseModel):
    records: list[FamilyMoodRecord]
    series: list[FamilyMoodSeries]
    members: list[str]
    checked_at: str


class FamilyBoardPostRequest(BaseModel):
    title: str = Field(..., min_length=1)
    author: str = Field(..., min_length=1)
    content: str = Field(..., min_length=1)
    pinned: bool = False


class FamilyBoardPost(BaseModel):
    board_post_id: str = Field(default_factory=lambda: str(uuid4()))
    title: str
    author: str
    content: str
    pinned: bool = False
    created_at: str
    updated_at: str


class FamilyBoardStateResponse(BaseModel):
    posts: list[FamilyBoardPost]
    checked_at: str


class FamilyTodoItemRequest(BaseModel):
    title: str = Field(..., min_length=1)
    owner: str = ""
    due_at: str = ""
    note: str = ""


class FamilyTodoItem(BaseModel):
    todo_item_id: str = Field(default_factory=lambda: str(uuid4()))
    title: str
    owner: str = ""
    due_at: str = ""
    note: str = ""
    done: bool = False
    created_at: str
    updated_at: str


class FamilyTodoStateResponse(BaseModel):
    items: list[FamilyTodoItem]
    checked_at: str


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
