#!/usr/bin/env python3
import argparse
import email
import imaplib
import os
import re
from datetime import datetime
from email.header import decode_header
from email.utils import parsedate_to_datetime


def load_env(path: str = ".env"):
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


def extract_text(msg: email.message.Message, max_chars: int = 240) -> str:
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
    else:
        payload = msg.get_payload(decode=True)
        if payload:
            charset = msg.get_content_charset() or "utf-8"
            text = payload.decode(charset, errors="replace")

    text = re.sub(r"\s+", " ", text).strip()
    return text[:max_chars]


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
    low_kw = ["광고", "newsletter", "promo", "프로모션", "할인", "쿠폰"]
    for kw in low_kw:
        if kw in s:
            score -= 1

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


def summarize(items):
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    lines = [
        f"# Naver Mail Summary ({now})",
        "",
        f"총 {len(items)}개 메일 분석",
        "",
    ]

    high = [x for x in items if x["score"] >= 4]
    med = [x for x in items if 1 <= x["score"] < 4]
    low = [x for x in items if x["score"] < 1]

    lines.append("## 중요도 분류")
    lines.append(f"- 높음: {len(high)}")
    lines.append(f"- 보통: {len(med)}")
    lines.append(f"- 낮음: {len(low)}")
    lines.append("")

    lines.append("## 메일별 요약")
    for idx, it in enumerate(sorted(items, key=lambda x: x["score"], reverse=True), 1):
        lvl = "높음" if it["score"] >= 4 else ("보통" if it["score"] >= 1 else "낮음")
        lines.append(f"### {idx}. [{lvl}] {it['subject'] or '(제목 없음)'}")
        lines.append(f"- 보낸사람: {it['from']}")
        lines.append(f"- 날짜: {it['date']}")
        lines.append(f"- 할 일: {it['action']}")
        lines.append(f"- 한줄 요약: {it['snippet'] or '(본문 미리보기 없음)'}")
        lines.append("")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Summarize Naver emails via IMAP")
    parser.add_argument("--limit", type=int, default=15, help="How many latest emails to summarize")
    parser.add_argument("--unread-only", action="store_true", help="Summarize unread emails only")
    parser.add_argument("--out", default="naver_mail_summary.md", help="Output markdown file")
    args = parser.parse_args()

    load_env()

    user = os.getenv("NAVER_EMAIL")
    password = os.getenv("NAVER_APP_PASSWORD")
    host = os.getenv("NAVER_IMAP_HOST", "imap.naver.com")
    port = int(os.getenv("NAVER_IMAP_PORT", "993"))
    mailbox = os.getenv("NAVER_MAILBOX", "INBOX")

    if not user or not password:
        raise SystemExit("NAVER_EMAIL / NAVER_APP_PASSWORD 를 .env에 설정해 주세요.")

    conn = imaplib.IMAP4_SSL(host, port)
    conn.login(user, password)
    conn.select(mailbox)

    criteria = "UNSEEN" if args.unread_only else "ALL"
    status, data = conn.search(None, criteria)
    if status != "OK":
        raise SystemExit("메일 검색 실패")

    ids = data[0].split()
    target_ids = ids[-args.limit :]

    items = []
    for msg_id in reversed(target_ids):
        status, fetched = conn.fetch(msg_id, "(RFC822)")
        if status != "OK" or not fetched or fetched[0] is None:
            continue

        raw = fetched[0][1]
        msg = email.message_from_bytes(raw)

        subject = decode_mime(msg.get("Subject", ""))
        sender = decode_mime(msg.get("From", ""))
        date_s = format_dt(msg.get("Date", ""))
        snippet = extract_text(msg)
        score = importance_score(subject, sender, snippet)
        action = action_hint(subject, snippet)

        items.append(
            {
                "subject": subject,
                "from": sender,
                "date": date_s,
                "snippet": snippet,
                "score": score,
                "action": action,
            }
        )

    conn.close()
    conn.logout()

    report = summarize(items)
    with open(args.out, "w", encoding="utf-8") as f:
        f.write(report)

    print(report)
    print(f"\n저장됨: {args.out}")


if __name__ == "__main__":
    main()
