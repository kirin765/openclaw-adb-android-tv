from __future__ import annotations

import base64

from app.services.media_library import MediaLibrary


def test_media_library_upload_and_favorite(tmp_path):
    library = MediaLibrary(str(tmp_path))
    payload = base64.b64encode(b"hello world").decode("ascii")

    item = library.add_upload("clip.mp4", "video/mp4", payload)
    favorite = library.add_favorite("My Clip", "https://example.com/watch")

    assert item.kind.value == "video"
    assert (tmp_path / "uploads" / item.stored_name).exists()
    assert library.list_uploads()[0].original_name == "clip.mp4"
    assert library.list_favorites()[0].title == "My Clip"
    assert favorite.url == "https://example.com/watch"
