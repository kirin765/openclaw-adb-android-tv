from __future__ import annotations

from dataclasses import dataclass, field
from threading import Lock
from typing import Any


@dataclass
class WhiteboardState:
    strokes: dict[str, dict[str, Any]] = field(default_factory=dict)
    order: list[str] = field(default_factory=list)


class WhiteboardStore:
    def __init__(self) -> None:
        self._lock = Lock()
        self._state = WhiteboardState()

    def snapshot(self) -> WhiteboardState:
        with self._lock:
            return WhiteboardState(
                strokes={stroke_id: dict(stroke) for stroke_id, stroke in self._state.strokes.items()},
                order=list(self._state.order),
            )

    def upsert_stroke(self, stroke: dict[str, Any]) -> None:
        with self._lock:
            stroke_id = str(stroke["id"])
            if stroke_id not in self._state.strokes:
                self._state.order.append(stroke_id)
                self._state.strokes[stroke_id] = {
                    "id": stroke_id,
                    "points": [],
                    "color": stroke.get("color", "#7dd3fc"),
                    "size": stroke.get("size", 4),
                    "tool": stroke.get("tool", "pen"),
                }
            current = self._state.strokes[stroke_id]
            current["color"] = stroke.get("color", current["color"])
            current["size"] = stroke.get("size", current["size"])
            current["tool"] = stroke.get("tool", current["tool"])
            current["points"].extend(stroke.get("points", []))

    def clear(self) -> None:
        with self._lock:
            self._state = WhiteboardState()


whiteboard_store = WhiteboardStore()
