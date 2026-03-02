#!/usr/bin/env python3
"""Daily global news briefing from public RSS feeds."""

from __future__ import annotations

import argparse
import html
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from pathlib import Path
from typing import List
from urllib.error import URLError
from urllib.request import Request, urlopen
from xml.etree import ElementTree as ET


@dataclass
class Item:
    title: str
    link: str
    source: str
    published: str


RSS_FEEDS = {
    "BBC World": "https://feeds.bbci.co.uk/news/world/rss.xml",
    "Google News": "https://news.google.com/rss?hl=en-US&gl=US&ceid=US:en",
    "Al Jazeera": "https://www.aljazeera.com/xml/rss/all.xml",
}


def _safe_text(value: str | None) -> str:
    if not value:
        return ""
    value = html.unescape(value)
    return re.sub(r"\s+", " ", value).strip()


def _format_dt(raw: str) -> str:
    if not raw:
        return ""
    try:
        dt = parsedate_to_datetime(raw)
        return dt.astimezone(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    except Exception:
        return raw.strip()


def _fetch_feed(url: str, timeout: int = 12) -> str:
    req = Request(url, headers={"User-Agent": "Mozilla/5.0 (X11; Linux x86_64)"})
    with urlopen(req, timeout=timeout) as resp:
        return resp.read().decode("utf-8", errors="replace")


def _parse_rss(xml_text: str, source: str) -> List[Item]:
    root = ET.fromstring(xml_text)
    items: List[Item] = []

    entries = root.findall(".//item")
    if not entries:
        entries = root.findall(".//{http://www.w3.org/2005/Atom}entry")

    for node in entries[:20]:
        title_node = node.findtext("title") or node.findtext("{http://www.w3.org/2005/Atom}title")
        link_node = node.findtext("link") or ""
        date_node = node.findtext("pubDate") or node.findtext("{http://www.w3.org/2005/Atom}published")

        if link_node and " rel=" in link_node:
            m = re.search(r"href=\"([^\"]+)\"", link_node)
            if m:
                link_node = m.group(1)

        title = _safe_text(title_node)
        link = (link_node or "").strip()
        if not title:
            continue

        items.append(
            Item(
                title=title,
                link=link,
                source=source,
                published=_format_dt(date_node or ""),
            )
        )

    dedup = []
    seen = set()
    for it in items:
        key = it.title.lower()
        if key in seen:
            continue
        seen.add(key)
        dedup.append(it)

    return dedup


def collect_news(limit: int) -> List[Item]:
    all_items: List[Item] = []

    per_source = max(2, limit // len(RSS_FEEDS))
    for source, feed_url in RSS_FEEDS.items():
        try:
            raw = _fetch_feed(feed_url)
            items = _parse_rss(raw, source)
            all_items.extend(items[:per_source])
        except (URLError, TimeoutError, ET.ParseError, ValueError) as e:
            print(f"[WARN] {source} 수집 실패: {e}")
            continue

    return all_items[:limit]


def build_report(items: List[Item], include_links: bool) -> str:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    lines = [f"# 글로벌 주요뉴스 브리핑 ({now})", ""]
    lines.append(f"총 수집: {len(items)}건")
    lines.append("")

    if not items:
        lines.append("- 오늘은 주요 뉴스 항목을 수집하지 못했습니다.")
        return "\n".join(lines)

    for idx, item in enumerate(items, 1):
        lines.append(f"### {idx}. {item.title}")
        lines.append(f"- 출처: {item.source}")
        if item.published:
            lines.append(f"- 발행: {item.published}")
        if include_links and item.link:
            lines.append(f"- 링크: {item.link}")
        lines.append("")

    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate a short global news briefing")
    parser.add_argument("--limit", type=int, default=15, help="Number of items in report")
    parser.add_argument("--out", default="global_news_briefing.md", help="Output markdown file")
    parser.add_argument("--no-links", action="store_true", help="Do not include source links")
    args = parser.parse_args()

    items = collect_news(limit=max(1, args.limit))
    report = build_report(items, include_links=not args.no_links)

    Path(args.out).write_text(report, encoding="utf-8")
    print(report)
    print(f"\n저장됨: {args.out}")


if __name__ == "__main__":
    main()
