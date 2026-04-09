# LCAS (Local Command Automation System)

MVP implementation for a local command automation server.

## Features
- FastAPI HTTP API
- Simple Web UI
- Rule-first command routing
- Optional OpenClaw/LLM intent bridge
- Redis + RQ async task queue
- Executor abstraction for Android TV, shell, Python, and OpenClaw bridge
- Cancel requests for running or queued tasks
- Browser launch commands from natural language
- Heuristic learning that stores successful natural-language commands as local rules
- Task status tracking
- Shared realtime whiteboard
- Local media upload and playback
- Favorite video link launcher
- Fridge and side-dish inventory with recipe recommendations
- Family-shared calendar with local event storage
- Family calendar day tags with a predefined brown tag
- Family mood slider records with per-member trend graphs
- Family shared TODO list with completion toggles
- Family shared bulletin board with realtime updates
- TV text input, power off, and delayed power off
- TV power on and screen wake
- Scheduled reminders that can wake the TV and show an alert on screen
- Standby weather screen
- Yonhap News RSS screen with a fullscreen overlay
- Real-time mobile screen mirroring from supported Android/iOS browsers

## Run

```bash
cd lcas
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload
```

Then open:
- `http://localhost:8000/`

## Optional worker

```bash
cd lcas
source .venv/bin/activate
rq worker lcas
```

## Environment

Copy `.env.example` to `.env` and edit values.
By default, Android TV commands are sent to `192.168.0.161` over ADB. Change `DEFAULT_ANDROID_TV_IP` if your target device is different.
Local uploads are stored under `storage/`.
Weather uses Open-Meteo with `WEATHER_LATITUDE` / `WEATHER_LONGITUDE`.

## API
- `GET /`
- `POST /command`
- `GET /status/{task_id}`
- `GET /health`
- `GET /reminders`
- `POST /reminders`
- `DELETE /reminders/{reminder_id}`
- `GET /fridge/state`
- `POST /fridge/items`
- `DELETE /fridge/items/{fridge_item_id}`
- `GET /family-calendar/state`
- `POST /family-calendar/events`
- `DELETE /family-calendar/events/{calendar_event_id}`
- `GET /family-mood/state`
- `POST /family-mood/records`
- `DELETE /family-mood/records/{mood_record_id}`
- `GET /family-todo/state`
- `POST /family-todo/items`
- `PATCH /family-todo/items/{todo_item_id}`
- `DELETE /family-todo/items/{todo_item_id}`
- `GET /family-board/state`
- `POST /family-board/posts`
- `DELETE /family-board/posts/{board_post_id}`
- `GET /tv/power/schedule`
- `POST /tv/power/schedule`
- `DELETE /tv/power/schedule/{timer_id}`

## Web UI
- Enter API token
- Submit natural language command
- Let the system learn repeat commands into local rules automatically
- Open URLs directly from the URL input
- Cancel the current task from the status panel
- Use the on-screen remote for up/down/left/right/confirm
- Draw together on the shared whiteboard in real time
- Upload media files and play them in the browser
- Save favorite video links and play them quickly
- Register fridge ingredients and side dishes, then get recipe suggestions
- Register family events in a shared calendar and review today's schedule
- Tag family calendar items with the predefined brown tag
- Save family mood ratings by member and view the trend graph
- Share a TODO list, mark items complete, and remove finished tasks
- Post family notes and see them update live on every browser
- Send text directly to the TV input
- Turn the TV off now or after a delay
- Schedule time-based reminders that wake the TV and show a visible alert
- Show a standby weather screen
- Show the Yonhap News feed in a standalone screen or fullscreen overlay
- Start mobile screen mirroring from a supported browser and view it live on other devices
- Poll task status and result automatically
- Quick action buttons for common TV commands

## Notes
This MVP keeps task status in memory for API reads, while execution runs through RQ when Redis is configured. If Redis is unavailable, the API can still enqueue to an in-process background fallback.
Browser launch commands use the local desktop's default browser when available.
