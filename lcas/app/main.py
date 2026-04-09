from __future__ import annotations

from pathlib import Path
import asyncio

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.api.pages import router as pages_router
from app.api.routes import router as api_router
from app.services.reminder_hub import reminder_hub

BASE_DIR = Path(__file__).resolve().parent
MEDIA_DIR = BASE_DIR.parent / "storage" / "uploads"
MEDIA_DIR.mkdir(parents=True, exist_ok=True)

app = FastAPI(title="LCAS", version="0.1.0")


@app.on_event("startup")
async def startup_event() -> None:
    reminder_hub.set_loop(asyncio.get_running_loop())


app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")
app.mount("/media-files", StaticFiles(directory=str(MEDIA_DIR)), name="media-files")
app.include_router(pages_router)
app.include_router(api_router)
