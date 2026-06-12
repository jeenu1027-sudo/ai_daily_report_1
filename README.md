# 🤖 AI 동향 뉴스 일일 리포트

매일 아침 8시(동경표준시)에 자동으로 AI 관련 최신 뉴스를 수집하여 깔끔한 HTML 형식으로 생성합니다.

## 🎯 주요 기능

- ✅ **한국어 전용**: VentureSquare, IT World Korea, The Hankyoreh 등에서 한국 AI 뉴스만 수집
- ✅ **지능형 필터링**: AI 생성 기사, 논문, GitHub 콘텐츠 자동 제외
- ✅ **초보자 친화적**: AI 초보자도 이해할 수 있는 수준의 기사만 선별
- ✅ **자동화**: 매일 8시(JST)에 자동 실행 ([SOUL.md](SOUL.md) 철학 기반)
- ✅ **깔끔한 리포트**: 반응형 HTML 디자인, 현대적 UI
- ✅ **최적화**: 중복 제거 및 최대 15개 뉴스 표시

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

## 🔧 뉴스 소스 (한국 전용)

현재 다음 한국 매체에서 AI 뉴스를 수집합니다:

| 소스 | 특징 | 우선순위 |
|------|------|--------|
| **VentureSquare** | 한국 스타트업 & AI 뉴스 | ⭐⭐⭐ |
| **IT World Korea** | IT 기술 뉴스 | ⭐⭐ |
| **The Hankyoreh (Science)** | 과학/기술 뉴스 | ⭐⭐ |

**필터링 규칙:**
- ✅ 한국어 기사만 수집
- ❌ AI가 생성한 기사 제외
- ❌ 학술 논문/백서 제외
- ❌ GitHub 저장소 및 코드 관련 콘텐츠 제외

더 많은 소스를 추가하려면 `news_fetcher.py`의 `fetch_korean_news_sources()` 함수를 수정하세요.

## 📝 로그

스크립트 실행 시 다음과 같은 로그를 확인할 수 있습니다:
- 각 뉴스 소스별 수집 상태
- 수집된 뉴스 총 개수
- 생성된 파일 경로

## ⚙️ 커스터마이징

### AI 키워드 추가
`news_fetcher.py`의 `AI_KEYWORDS` 리스트를 수정 (한글 권장):
```python
AI_KEYWORDS = [
    'AI', '인공지능', '머신러닝', '딥러닝', ..., '새로운키워드'
]
```

### 필터링 규칙 변경
필터링 키워드 리스트 수정:
```python
AI_GENERATED_KEYWORDS = [...]  # AI 생성 기사 감지
ACADEMIC_KEYWORDS = [...]      # 논문 감지
GITHUB_KEYWORDS = [...]        # GitHub 콘텐츠 감지
```

### 뉴스 소스 추가
`fetch_korean_news_sources()` 함수의 `korean_sources` 리스트에 새 피드 추가:
```python
korean_sources = [
    {
        'url': 'https://your-rss-feed-url',
        'name': '🇰🇷 Source Name',
        'priority': 2
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

| 문서 | 목적 |
|------|------|
| [SOUL.md](SOUL.md) | 프로젝트 비전, 핵심 가치, 설계 원칙 |
| [CLAUDE.md](CLAUDE.md) | Claude Code 설정, 커스텀 스킬 정의 |
| [SCHEDULE_SETUP.md](SCHEDULE_SETUP.md) | Windows Task Scheduler 자동 실행 설정 |

## 📄 라이선스

개인 사용 목적으로 자유롭게 사용 및 수정할 수 있습니다.

---

**마지막 업데이트**: 2026-06-12  
**자동 실행**: 매일 오전 8시 (JST)  
**언어**: Python 3.14.6
