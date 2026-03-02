# Naver Email IMAP 연동 가이드 (SSH 환경)

## 1) 네이버에서 IMAP 활성화
네이버 메일 > 환경설정 > POP3/IMAP 설정에서 **IMAP 사용 ON**.

## 2) 워크스페이스 설정
```bash
cd /home/k/.openclaw/workspace
cp .env.example .env
```

`.env`에 아래 값 입력:

```env
NAVER_EMAIL=yourid@naver.com
NAVER_APP_PASSWORD=your_app_password_here
NAVER_IMAP_HOST=imap.naver.com
NAVER_IMAP_PORT=993
NAVER_MAILBOX=INBOX
```

> 보안상 일반 계정 비밀번호 대신 앱 비밀번호 사용 권장.

## 3) 요약 실행
최근 15개 메일 요약:
```bash
python3 naver_mail_summary.py
```

안 읽은 메일만 요약:
```bash
python3 naver_mail_summary.py --unread-only
```

개수 지정:
```bash
python3 naver_mail_summary.py --limit 30
```

## 4) 결과 파일
- 기본 출력 파일: `naver_mail_summary.md`
- 콘솔에도 동일 내용 출력됨
