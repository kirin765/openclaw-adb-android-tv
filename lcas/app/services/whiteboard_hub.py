from __future__ import annotations

from typing import Any

from fastapi import WebSocket

from app.services.whiteboard import whiteboard_store


class WhiteboardHub:
    def __init__(self) -> None:
        self._connections: set[WebSocket] = set()

    async def connect(self, websocket: WebSocket) -> None:
        await websocket.accept()
        self._connections.add(websocket)
        snapshot = whiteboard_store.snapshot()
        strokes = [snapshot.strokes[stroke_id] for stroke_id in snapshot.order]
        await websocket.send_json({"type": "snapshot", "strokes": strokes})

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


whiteboard_hub = WhiteboardHub()
