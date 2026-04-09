from __future__ import annotations

import asyncio
from datetime import datetime
from typing import Any

from fastapi import WebSocket

from app.services.family_todo_store import FamilyTodoStore


class FamilyTodoHub:
    def __init__(self) -> None:
        self._connections: set[WebSocket] = set()
        self._loop: asyncio.AbstractEventLoop | None = None
        self._store: FamilyTodoStore | None = None

    def set_loop(self, loop: asyncio.AbstractEventLoop) -> None:
        self._loop = loop

    def set_store(self, store: FamilyTodoStore) -> None:
        self._store = store

    async def connect(self, websocket: WebSocket) -> None:
        await websocket.accept()
        self._connections.add(websocket)
        items = self._store.list_items() if self._store else []
        await websocket.send_json(
            {
                "type": "snapshot",
                "items": [item.model_dump() for item in items],
                "checked_at": datetime.now().isoformat(timespec="seconds"),
            }
        )

    def disconnect(self, websocket: WebSocket) -> None:
        self._connections.discard(websocket)

    async def broadcast(self, payload: dict[str, Any]) -> None:
        stale: set[WebSocket] = set()
        for connection in list(self._connections):
            try:
                await connection.send_json(payload)
            except Exception:
                stale.add(connection)
        for connection in stale:
            self._connections.discard(connection)

    def broadcast_from_thread(self, payload: dict[str, Any]) -> None:
        if not self._loop:
            return
        asyncio.run_coroutine_threadsafe(self.broadcast(payload), self._loop)


family_todo_hub = FamilyTodoHub()
