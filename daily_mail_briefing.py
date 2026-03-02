#!/usr/bin/env python3
"""Daily mail briefing for configured providers (Naver + Gmail)."""

import argparse
import email
import html
import imaplib
import os
import re
from datetime import datetime
from email.header import decode_header
from email.message import Message
from email.utils import parsedate_to_datetime
from typing import Dict, List, Tuple


AI_NEWSLETTER_SENDERS = (
    "swyx",
    "ainews",
    "latentspace",
    "newsletter",
    "ai secret",
    "anthropic",
    "openai",
    "huggingface",
    "googleai",
    "deepmind",
    "cohere",
    "stability",
    "substack",
)
AI_NEWSLETTER_SUBJECTS = (
    "ai ",
    "ai",  # for korean/short labels like 'AI ...'
    "artificial intelligence",
    "machine learning",
    "llm",
    "gpt",
    "chatgpt",
    "claude",
    "gemini",
    "llama",
)


def load_env(path: str = ".env"):
    """Load .env only if values are not already present in environment."""
    if not os.path.exists(path):
        return

    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            os.environ.setdefault(k.strip(), v.strip())


def decode_mime(value: str) -> str:
    if not value:
        return ""
    parts = decode_header(value)
    out = []
    for part, enc in parts:
        if isinstance(part, bytes):
            out.append(part.decode(enc or "utf-8", errors="replace"))
        else:
            out.append(part)
    return "".join(out).strip()


def _strip_html(raw_html: str) -> str:
    if not raw_html:
        return ""
    text = html.unescape(raw_html)
    text = re.sub(r"<style[\s\S]*?</style>", " ", text, flags=re.I)
    text = re.sub(r"<script[\s\S]*?</script>", " ", text, flags=re.I)
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def extract_text(msg: Message, max_chars: int = 240) -> str:
    text = ""

    if msg.is_multipart():
        for part in msg.walk():
            ctype = part.get_content_type()
            disp = str(part.get("Content-Disposition", ""))
            if ctype == "text/plain" and "attachment" not in disp:
                payload = part.get_payload(decode=True)
                if payload is None:
                    continue
                charset = part.get_content_charset() or "utf-8"
                text = payload.decode(charset, errors="replace")
                break
            if ctype == "text/html" and "attachment" not in disp and not text:
                payload = part.get_payload(decode=True)
                if payload is None:
                    continue
                charset = part.get_content_charset() or "utf-8"
                text = _strip_html(payload.decode(charset, errors="replace"))
                break
    else:
        payload = msg.get_payload(decode=True)
        if payload:
            charset = msg.get_content_charset() or "utf-8"
            raw = payload.decode(charset, errors="replace")
            ctype = msg.get_content_type()
            text = _strip_html(raw) if ctype == "text/html" else raw

    text = re.sub(r"\s+", " ", text).strip()
    return text[:max_chars]


def is_ai_newsletter(subject: str, sender: str) -> bool:
    s_sender = sender.lower()
    s_subject = subject.lower()

    for key in AI_NEWSLETTER_SENDERS:
        if key in s_sender:
            return True

    # AI 뉴스레터는 제목/본문에서도 충분히 많이 드러남
    return any(key in s_subject for key in AI_NEWSLETTER_SUBJECTS)


def parse_key_points(snippet: str, max_points: int = 3) -> List[str]:
    if not snippet:
        return []
    parts = re.split(r"(?<=[.!?\n])\s+|\s{2,}", snippet)
    parts = [p.strip(" -\u2014").strip() for p in parts]
    parts = [p for p in parts if len(p) >= 18]
    return parts[:max_points]


def importance_score(subject: str, sender: str, snippet: str) -> int:
    s = f"{subject} {sender} {snippet}".lower()

    high_kw = [
        "긴급", "urgent", "중요", "결제", "청구", "invoice", "security", "보안",
        "인증", "otp", "로그인", "비밀번호", "password", "계정", "account",
        "면접", "인터뷰", "interview", "마감", "due", "deadline", "오류", "실패",
    ]
    med_kw = [
        "회의", "meeting", "일정", "캘린더", "calendar", "확인", "review", "요청",
        "request", "업데이트", "update", "배송", "delivery", "승인", "approval",
    ]

    score = 0
    for kw in high_kw:
        if kw in s:
            score += 3
    for kw in med_kw:
        if kw in s:
            score += 1

    # Promotions/newsletters lower priority
    for kw in ["광고", "newsletter", "promo", "프로모션", "할인", "쿠폰"]:
        if kw in s:
            score -= 1

    # AI 뉴스레터는 별도 노이즈 필터를 위해 기본적으로 중간 가중치
    if is_ai_newsletter(subject, sender):
        score += 1

    return score


def action_hint(subject: str, snippet: str) -> str:
    s = f"{subject} {snippet}".lower()
    if any(k in s for k in ["긴급", "urgent", "마감", "deadline", "오늘", "지금"]):
        return "빠른 확인/처리 필요"
    if any(k in s for k in ["결제", "청구", "invoice", "payment"]):
        return "결제/청구 확인"
    if any(k in s for k in ["회의", "meeting", "일정", "calendar"]):
        return "일정 반영 여부 확인"
    if any(k in s for k in ["인증", "otp", "로그인", "security", "보안"]):
        return "보안 알림 확인"
    if any(k in s for k in ["요청", "request", "review", "승인", "approval"]):
        return "요청사항 확인 후 응답"
    return "읽고 중요도 판단"


def format_dt(raw_date: str) -> str:
    if not raw_date:
        return "(date 없음)"
    try:
        dt = parsedate_to_datetime(raw_date)
        return dt.strftime("%Y-%m-%d %H:%M")
    except Exception:
        return raw_date


def summarize_items(items):
    high = [x for x in items if x["score"] >= 4]
    med = [x for x in items if 1 <= x["score"] < 4]
    low = [x for x in items if x["score"] < 1]

    lines = [
        f"- 높음: {len(high)}",
        f"- 보통: {len(med)}",
        f"- 낮음: {len(low)}",
        "",
    ]

    for idx, it in enumerate(
        sorted(items, key=lambda x: (x["is_ai_newsletter"], x["score"]), reverse=True),
        1,
    ):
        lvl = "높음" if it["score"] >= 4 else ("보통" if it["score"] >= 1 else "낮음")
        lines.append(f"### {idx}. [{lvl}] {it['subject'] or '(제목 없음)'}")
        lines.append(f"- 보낸사람: {it['from']}")
        lines.append(f"- 날짜: {it['date']}")
        lines.append(f"- 할 일: {it['action']}")
        if it["is_ai_newsletter"]:
            if it.get("summary"):
                lines.append(f"- AI 뉴스레터 상세 요약: {it['summary']}")
            if it.get("key_points"):
                lines.append("- 핵심 포인트:")
                for p in it["key_points"]:
                    lines.append(f"  - {p}")
        else:
            lines.append(f"- 한줄 요약: {it['snippet'] or '(본문 미리보기 없음)'}")
        lines.append("")

    return lines


def summarize_ai_items(items):
    ai_items = [x for x in items if x["is_ai_newsletter"]]
    if not ai_items:
        return ["- AI 관련 뉴스레터: 확인 대상 없음", ""]

    lines = ["## AI 뉴스레터 집중 정리", ""]
    for idx, it in enumerate(sorted(ai_items, key=lambda x: x["score"], reverse=True), 1):
        lines.append(f"### {idx}. {it['subject'] or '(제목 없음)'}")
        lines.append(f"- 보낸사람: {it['from']}")
        lines.append(f"- 날짜: {it['date']}")
        if it.get("summary"):
            lines.append(f"- 요약: {it['summary']}")
        if it.get("key_points"):
            lines.append("- 핵심 포인트:")
            for p in it["key_points"]:
                lines.append(f"  - {p}")
        if it.get("snippet") and not it.get("summary"):
            lines.append(f"- 한줄 요약: {it['snippet']}")
        lines.append("")
    return lines


def fetch_emails(conf: Dict[str, str], limit: int, unread_only: bool) -> List[Dict[str, object]]:
    user = conf.get("email")
    password = conf.get("password")
    host = conf.get("host", "imap.gmail.com")
    port = int(conf.get("port", "993"))
    mailbox = conf.get("mailbox", "INBOX")

    if not user or not password:
        return []

    conn = imaplib.IMAP4_SSL(host, port)
    conn.login(user, password)
    conn.select(mailbox)

    criteria = "UNSEEN" if unread_only else "ALL"
    status, data = conn.search(None, criteria)
    if status != "OK":
        conn.logout()
        raise RuntimeError(f"[{conf['name']}] 메일 검색 실패")

    ids = data[0].split()
    target_ids = ids[-limit:]

    items: List[Dict[str, object]] = []
    for msg_id in reversed(target_ids):
        status, fetched = conn.fetch(msg_id, "(RFC822)")
        if status != "OK" or not fetched or fetched[0] is None:
            continue

        raw = fetched[0][1]
        msg = email.message_from_bytes(raw)

        subject = decode_mime(msg.get("Subject", ""))
        sender = decode_mime(msg.get("From", ""))
        date_s = format_dt(msg.get("Date", ""))

        ai_news = is_ai_newsletter(subject, sender)
        snippet = extract_text(msg, max_chars=700 if ai_news else 260)
        score = importance_score(subject, sender, snippet)
        action = action_hint(subject, snippet)
        points = parse_key_points(snippet) if ai_news else []
        summary = " | ".join(points[:2]) if points else ""

        item = {
            "subject": subject,
            "from": sender,
            "date": date_s,
            "snippet": snippet,
            "score": score,
            "action": action,
            "is_ai_newsletter": ai_news,
            "key_points": points,
            "summary": summary,
        }

        items.append(item)

    conn.close()
    conn.logout()
    return items


def build_report(results: List[Tuple[str, List[Dict[str, object]]]]) -> str:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    lines = [f"# Mail Briefing ({now})", "", "총 수집 메일: {}개".format(sum(len(items) for _, items in results)), ""]

    all_items: List[Dict[str, object]] = [it for _, items in results for it in items]
    lines.extend(summarize_ai_items(all_items))

    for provider, items in results:
        lines.append(f"## {provider}")
        lines.append(f"- 항목 수: {len(items)}")
        lines.append("")
        if not items:
            lines.append("- 수신된 메일 없음")
            lines.append("")
            continue
        lines.extend(summarize_items(items))

    return "\n".join(lines)



def _collect_provider_by_index(env_prefix: str, index: int, default_host: str) -> Dict[str, str] | None:
    idx = "" if index == 0 else f"_{index}"
    email_addr = os.getenv(f"{env_prefix}_EMAIL{idx}")
    app_password = os.getenv(f"{env_prefix}_APP_PASSWORD{idx}")

    if not email_addr or not app_password:
        return None

    return {
        "name": env_prefix,
        "email": email_addr,
        "password": app_password,
        "host": os.getenv(f"{env_prefix}_IMAP_HOST{idx}", os.getenv(f"{env_prefix}_IMAP_HOST", default_host)),
        "port": os.getenv(f"{env_prefix}_IMAP_PORT{idx}", os.getenv(f"{env_prefix}_IMAP_PORT", "993")),
        "mailbox": os.getenv(f"{env_prefix}_MAILBOX{idx}", os.getenv(f"{env_prefix}_MAILBOX", "INBOX")),
        "index": index,
    }


def collect_provider(env_prefix: str, default_host: str) -> List[Dict[str, str]]:
    accounts: List[Dict[str, str]] = []

    # 기존 단일 계정
    first = _collect_provider_by_index(env_prefix, 0, default_host)
    if first:
        accounts.append(first)

    # 추가 계정: ENV 확장 형태로 등록 (예: GMAIL_EMAIL_2, GMAIL_EMAIL_3 ...)
    i = 2
    while True:
        conf = _collect_provider_by_index(env_prefix, i, default_host)
        if not conf:
            break
        accounts.append(conf)
        i += 1

    # 구버전 호환: 한 번에 여러 계정 지정
    emails_raw = os.getenv(f"{env_prefix}_EMAILS")
    app_passwords_raw = os.getenv(f"{env_prefix}_APP_PASSWORDS")
    if emails_raw and app_passwords_raw:
        emails = [x.strip() for x in emails_raw.split(",") if x.strip()]
        app_passwords = [x.strip() for x in app_passwords_raw.split(",") if x.strip()]
        max_len = min(len(emails), len(app_passwords))
        for idx in range(max_len):
            if idx >= len(accounts):
                conf = {
                    "name": env_prefix,
                    "email": emails[idx],
                    "password": app_passwords[idx],
                    "host": os.getenv(f"{env_prefix}_IMAP_HOST", default_host),
                    "port": os.getenv(f"{env_prefix}_IMAP_PORT", "993"),
                    "mailbox": os.getenv(f"{env_prefix}_MAILBOX", "INBOX"),
                    "index": idx,
                }
                accounts.append(conf)

    # 중복 방지
    dedup: List[Dict[str, str]] = []
    seen = set()
    for conf in accounts:
        key = (conf.get("email"), conf.get("host"), conf.get("mailbox"))
        if key in seen:
            continue
        seen.add(key)
        dedup.append(conf)

    return dedup


def main():
    parser = argparse.ArgumentParser(description="Summarize Naver + Gmail inboxes")
    parser.add_argument("--limit", type=int, default=15, help="How many latest emails to summarize per account")
    parser.add_argument("--unread-only", action="store_true", help="Summarize unread emails only")
    parser.add_argument("--out", default="mail_briefing.md", help="Output markdown file")
    parser.add_argument("--skip-naver", action="store_true")
    parser.add_argument("--skip-gmail", action="store_true")
    args = parser.parse_args()

    load_env()

    providers: List[Tuple[str, Dict[str, str]]] = []

    if not args.skip_naver:
        naver_accounts = collect_provider("NAVER", "imap.naver.com")
        if naver_accounts:
            for idx, account in enumerate(naver_accounts, 1):
                label = "Naver" if len(naver_accounts) == 1 else f"Naver ({idx})"
                providers.append((label, account))
        else:
            print("[skip] NAVER env not configured")

    if not args.skip_gmail:
        gmail_accounts = collect_provider("GMAIL", "imap.gmail.com")
        if gmail_accounts:
            for idx, account in enumerate(gmail_accounts, 1):
                label = "Gmail" if len(gmail_accounts) == 1 else f"Gmail ({idx})"
                providers.append((label, account))
        else:
            print("[skip] GMAIL env not configured")

    if not providers:
        raise SystemExit("No configured provider. Set NAVER_* and/or GMAIL_* in .env")

    report_blocks = []
    for label, conf in providers:
        print(f"[{label}] summarize...", flush=True)
        items = fetch_emails(conf, args.limit, args.unread_only)
        report_blocks.append((label, items))

    report = build_report(report_blocks)
    with open(args.out, "w", encoding="utf-8") as f:
        f.write(report)

    print(report)
    print(f"\n저장됨: {args.out}")


if __name__ == "__main__":
    main()
