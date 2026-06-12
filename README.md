# 🤖 AI 동향 뉴스 일일 리포트

매일 아침 8시(동경표준시)에 자동으로 AI 관련 최신 뉴스를 수집하여 깔끔한 HTML 형식으로 생성합니다.

## 🎯 기능

- ✅ **다중 소스**: Hacker News, Bloomberg, The Verge, Ars Technica에서 뉴스 수집
- ✅ **스마트 필터**: AI 관련 뉴스만 자동 필터링
- ✅ **자동화**: 매일 8시(JST)에 자동 실행
- ✅ **깔끔한 리포트**: 반응형 HTML 디자인
- ✅ **최적화**: 중복 제거 및 최대 10개 뉴스 표시

> **프로젝트 철학**: [SOUL.md](SOUL.md) 참고

## 📦 설치

```bash
# 의존성 설치
pip install -r requirements.txt
```

## 🚀 사용 방법

### 수동 실행
```bash
python news_fetcher.py
```

**출력**: `ai-news-digest-YYYY-MM-DD.html` 파일 생성

### 자동 스케줄
매일 8시(JST)에 자동으로 실행됩니다.  
자세한 설정은 [SCHEDULE_SETUP.md](SCHEDULE_SETUP.md) 참고

## 📁 파일 구조

```
ai_daily_report_1/
├── .claude/
│   └── skills/               # Claude Code 커스텀 스킬
├── news_fetcher.py           # 뉴스 수집 및 HTML 생성
├── requirements.txt          # Python 의존성
├── README.md                 # 이 파일
├── SOUL.md                   # 프로젝트 철학
├── CLAUDE.md                 # Claude Code 설정
└── ai-news-digest-*.html     # 생성된 일일 리포트
```

## 📊 생성되는 파일

- `ai-news-digest-YYYY-MM-DD.html` 형식으로 매일 새로운 파일이 생성됩니다
- 파일은 현재 디렉토리 (C:\ai_daily_report_1\)에 저장됩니다
- 브라우저에서 열어보면 보기 좋은 리포트를 확인할 수 있습니다

## 🔧 뉴스 소스

현재 다음 소스에서 뉴스를 수집합니다:

1. **Hacker News** - 기술 뉴스 커뮤니티
2. **Bloomberg** - 비즈니스/기술 뉴스
3. **The Verge** - 기술 뉴스
4. **Ars Technica** - 기술/과학 뉴스 (안정성 개선)

더 많은 소스를 추가하려면 `news_fetcher.py`의 `sources` 배열을 수정하세요.

## 📝 로그

스크립트 실행 시 다음과 같은 로그를 확인할 수 있습니다:
- 각 뉴스 소스별 수집 상태
- 수집된 뉴스 총 개수
- 생성된 파일 경로

## ⚙️ 커스터마이징

### AI 키워드 추가
`news_fetcher.py`의 `AI_KEYWORDS` 리스트를 수정:
```python
AI_KEYWORDS = [
    'AI', 'machine learning', 'deep learning', ..., '새로운키워드'
]
```

### 뉴스 소스 추가
`fetch_ai_news()` 함수의 `sources` 리스트에 새 피드 추가:
```python
sources = [
    {
        'url': 'https://your-rss-feed-url',
        'name': 'Source Name'
    },
]
```

### HTML 스타일 변경
`generate_html()` 함수의 CSS 섹션 수정으로 색상, 폰트, 레이아웃 변경 가능

## 🐛 문제 해결

| 문제 | 해결 방법 |
|------|---------|
| 모듈 없음 오류 | `pip install -r requirements.txt` 실행 |
| 뉴스 수집 실패 | 인터넷 연결 확인, 뉴스 소스 URL 확인 |
| 파일 생성 안 됨 | 디렉토리 쓰기 권한 확인 |
| 스케줄 미실행 | [SCHEDULE_SETUP.md](SCHEDULE_SETUP.md) 참고 |

더 자세한 정보는 [SCHEDULE_SETUP.md](SCHEDULE_SETUP.md)를 참고하세요.

## 📖 문서

- **[SOUL.md](SOUL.md)**: 프로젝트 비전과 철학
- **[CLAUDE.md](CLAUDE.md)**: Claude Code 설정 및 스킬
- **[SCHEDULE_SETUP.md](SCHEDULE_SETUP.md)**: Windows Task Scheduler 설정
- **[PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)**: 상세 프로젝트 정보

## 📄 라이선스

개인 사용 목적으로 자유롭게 사용 및 수정할 수 있습니다.

---

**마지막 업데이트**: 2026-06-12  
**자동 실행**: 매일 오전 8시 (JST)  
**언어**: Python 3.14.6
