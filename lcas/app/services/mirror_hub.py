from __future__ import annotations

import asyncio
from typing import Any

from fastapi import WebSocket

from app.services.mirror_store import mirror_store


class MirrorHub:
    def __init__(self) -> None:
        self._connections: set[WebSocket] = set()
        self._loop: asyncio.AbstractEventLoop | None = None

    def set_loop(self, loop: asyncio.AbstractEventLoop) -> None:
        self._loop = loop

    async def connect(self, websocket: WebSocket) -> None:
        await websocket.accept()
        self._connections.add(websocket)
        await websocket.send_json({"type": "snapshot", "mirror": mirror_store.snapshot().model_dump()})

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


mirror_hub = MirrorHub()
