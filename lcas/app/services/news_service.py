from __future__ import annotations

import re
from html import unescape
from xml.etree import ElementTree as ET

import httpx

from app.models.schemas import NewsFeedResponse, NewsItem


class NewsService:
    def __init__(self, feed_url: str):
        self.feed_url = feed_url

    async def get_yonhap_feed(self) -> NewsFeedResponse:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(self.feed_url)
            response.raise_for_status()
        return self._parse_feed(response.text)

    def _parse_feed(self, xml_text: str) -> NewsFeedResponse:
        root = ET.fromstring(xml_text)
        channel = root.find("channel")
        if channel is None:
            raise ValueError("Invalid RSS feed")

        title = self._text(channel.find("title")) or "연합뉴스"
        link = self._text(channel.find("link"))
        updated_at = self._text(channel.find("lastBuildDate"))
        items: list[NewsItem] = []
        for item in channel.findall("item")[:12]:
            items.append(
                NewsItem(
                    title=self._text(item.find("title")) or "(제목 없음)",
                    link=self._text(item.find("link")) or link or self.feed_url,
                    published_at=self._text(item.find("pubDate")),
                    summary=self._clean_summary(self._text(item.find("description"))),
                )
            )

        return NewsFeedResponse(source="yonhap", title=title, link=link, updated_at=updated_at, items=items)

    def _text(self, node: ET.Element | None) -> str | None:
        if node is None or node.text is None:
            return None
        return unescape(node.text.strip())

    def _clean_summary(self, value: str | None) -> str | None:
        if not value:
            return None
        cleaned = unescape(value)
        cleaned = re.sub(r"<[^>]+>", " ", cleaned)
        cleaned = re.sub(r"\s+", " ", cleaned).strip()
        return cleaned or None
