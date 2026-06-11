# 🤖 AI 동향 뉴스 일일 리포트

매일 아침 8시(동경표준시)에 자동으로 AI 관련 최신 뉴스를 수집하여 깔끔한 HTML 형식으로 생성합니다.

## 🎯 기능

- ✅ Hacker News, Bloomberg, Wired 등 신뢰할 수 있는 소스에서 뉴스 수집
- ✅ AI 관련 뉴스만 필터링
- ✅ 일일 자동 실행 (8시 JST)
- ✅ 반응형 디자인의 아름다운 HTML 리포트
- ✅ 중복 제거 및 최대 10개 뉴스 표시

## 📦 설치

```bash
# 프로젝트 디렉토리로 이동
cd C:\ai_daily_report_1

# 의존성 설치
npm install
```

## 🚀 사용 방법

### 수동 실행
```bash
npm run fetch
```

### 자동 스케줄 실행
매일 8시(JST)에 자동으로 실행되도록 설정되어 있습니다.
스케줄 관리는 Claude Code `schedule` 스킬로 수행됩니다.

## 📁 파일 구조

```
ai_daily_report_1/
├── news-fetcher.js       # 뉴스 수집 및 HTML 생성 메인 스크립트
├── package.json          # Node.js 프로젝트 설정
├── README.md             # 이 파일
├── schedule-info.md      # 스케줄 설정 정보
└── ai-news-digest-*.html # 생성된 일일 리포트 (자동 생성)
```

## 📊 생성되는 파일

- `ai-news-digest-YYYY-MM-DD.html` 형식으로 매일 새로운 파일이 생성됩니다
- 파일은 현재 디렉토리 (C:\ai_daily_report_1\)에 저장됩니다
- 브라우저에서 열어보면 보기 좋은 리포트를 확인할 수 있습니다

## 🔧 뉴스 소스

현재 다음 소스에서 뉴스를 수집합니다:

1. **Hacker News** - 기술 뉴스 커뮤니티
2. **Bloomberg** - 비즈니스/기술 뉴스
3. **Wired** - 기술/과학 잡지

더 많은 소스를 추가하려면 `news-fetcher.js`의 `sources` 배열을 수정하세요.

## 📝 로그

스크립트 실행 시 다음과 같은 로그를 확인할 수 있습니다:
- 각 뉴스 소스별 수집 상태
- 수집된 뉴스 총 개수
- 생성된 파일 경로

## ⚙️ 커스터마이징

### AI 키워드 추가
`news-fetcher.js`의 `AI_KEYWORDS` 배열을 수정:
```javascript
const AI_KEYWORDS = ['AI', 'artificial intelligence', ..., '새로운키워드'];
```

### 뉴스 소스 추가
`fetchAINews()` 함수에 새로운 RSS 피드 추가:
```javascript
const sources = [
  { url: 'https://your-rss-feed-url', name: 'Source Name' },
];
```

### HTML 스타일 변경
`generateHTML()` 함수의 `<style>` 섹션을 수정하여 색상, 폰트, 레이아웃을 변경할 수 있습니다.

## 🐛 문제 해결

- **모듈 찾을 수 없음 오류**: `npm install` 을 다시 실행하세요
- **뉴스가 수집되지 않음**: 인터넷 연결을 확인하고, 뉴스 소스 URL이 정상인지 확인하세요
- **파일이 생성되지 않음**: 디렉토리 쓰기 권한을 확인하세요

## 📄 라이선스

개인 사용 목적으로 자유롭게 사용 및 수정할 수 있습니다.

---

**마지막 업데이트**: 2026-06-11  
**자동 실행**: 매일 오전 8시 (JST)
