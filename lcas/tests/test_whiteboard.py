from __future__ import annotations

from app.services.whiteboard import WhiteboardStore


def test_whiteboard_store_merges_points_by_stroke_id():
    store = WhiteboardStore()
    store.upsert_stroke({"id": "stroke-1", "points": [{"x": 10, "y": 20}], "color": "#fff", "size": 3})
    store.upsert_stroke({"id": "stroke-1", "points": [{"x": 15, "y": 25}], "color": "#000", "size": 5})

    snapshot = store.snapshot()
    stroke = snapshot.strokes["stroke-1"]

    assert snapshot.order == ["stroke-1"]
    assert stroke["color"] == "#000"
    assert stroke["size"] == 5
    assert stroke["points"] == [{"x": 10, "y": 20}, {"x": 15, "y": 25}]
