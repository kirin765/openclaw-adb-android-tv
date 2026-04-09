from __future__ import annotations

from pathlib import Path
import asyncio

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.api.pages import router as pages_router
from app.api.routes import router as api_router
from app.core.settings import get_settings
from app.services.family_board_hub import family_board_hub
from app.services.family_board_store import build_family_board_store
from app.services.family_mood_hub import family_mood_hub
from app.services.family_mood_store import build_family_mood_store
from app.services.family_todo_hub import family_todo_hub
from app.services.family_todo_store import build_family_todo_store
from app.services.mirror_hub import mirror_hub
from app.services.reminder_hub import reminder_hub

BASE_DIR = Path(__file__).resolve().parent
MEDIA_DIR = BASE_DIR.parent / "storage" / "uploads"
MEDIA_DIR.mkdir(parents=True, exist_ok=True)

app = FastAPI(title="LCAS", version="0.1.0")


@app.on_event("startup")
async def startup_event() -> None:
    settings = get_settings()
    reminder_hub.set_loop(asyncio.get_running_loop())
    mirror_hub.set_loop(asyncio.get_running_loop())
    family_board_hub.set_loop(asyncio.get_running_loop())
    family_board_hub.set_store(build_family_board_store(settings.storage_dir))
    family_mood_hub.set_loop(asyncio.get_running_loop())
    family_mood_hub.set_store(build_family_mood_store(settings.storage_dir))
    family_todo_hub.set_loop(asyncio.get_running_loop())
    family_todo_hub.set_store(build_family_todo_store(settings.storage_dir))


app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")
app.mount("/media-files", StaticFiles(directory=str(MEDIA_DIR)), name="media-files")
app.include_router(pages_router)
app.include_router(api_router)
