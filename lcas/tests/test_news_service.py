from __future__ import annotations

from app.services.news_service import NewsService


def test_news_service_parses_rss_feed():
    xml = """<?xml version="1.0" encoding="UTF-8"?>
    <rss version="2.0">
      <channel>
        <title>연합뉴스</title>
        <link>https://www.yna.co.kr</link>
        <lastBuildDate>Fri, 10 Apr 2026 10:00:00 +0900</lastBuildDate>
        <item>
          <title>첫 번째 기사</title>
          <link>https://www.yna.co.kr/view/AKR1</link>
          <pubDate>Fri, 10 Apr 2026 09:30:00 +0900</pubDate>
          <description><![CDATA[<p>요약 1</p>]]></description>
        </item>
        <item>
          <title>두 번째 기사</title>
          <link>https://www.yna.co.kr/view/AKR2</link>
          <pubDate>Fri, 10 Apr 2026 09:00:00 +0900</pubDate>
          <description>요약 2</description>
        </item>
      </channel>
    </rss>
    """

    feed = NewsService("https://example.com/rss")._parse_feed(xml)

    assert feed.source == "yonhap"
    assert feed.title == "연합뉴스"
    assert len(feed.items) == 2
    assert feed.items[0].title == "첫 번째 기사"
    assert feed.items[0].summary == "요약 1"
