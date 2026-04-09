from __future__ import annotations

from app.services.mirror_service import MirrorService


def test_mirror_service_tracks_state_and_frames():
    service = MirrorService()

    started = service.start("Android")
    assert started.active is True
    assert started.source_label == "Android"
    assert started.frame_count == 0

    frame = service.update_frame("data:image/jpeg;base64,AAAA", "Android")
    assert frame.active is True
    assert frame.frame_data_url.startswith("data:image/jpeg")
    assert frame.frame_count == 1

    stopped = service.stop()
    assert stopped.active is False
