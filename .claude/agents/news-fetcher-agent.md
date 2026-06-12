# 📰 뉴스 수집 에이전트 (news-fetcher-agent)

## Metadata

- **name**: news-fetcher-agent
- **type**: task-agent (작업 에이전트)
- **version**: v1.0.0
- **description**: AI 뉴스를 자동으로 수집하고 한국어 HTML 리포트 생성
- **called_by**: morning-briefing (마스터 에이전트)
- **status**: Active

---

## 📋 개요

`news-fetcher-agent`는 **뉴스 수집 전담 에이전트**입니다.

morning-briefing에 의해 호출되어 다음 작업을 수행합니다:
1. 한국의 AI 뉴스 소스에서 최신 기사 검색
2. 엄격한 필터링 기준 적용 (생성형 AI, GitHub 제외 등)
3. 한국어 HTML 리포트 생성
4. 실행 결과 검증

**핵심 역할**:
- 매일 최신 AI 뉴스 수집
- 품질 기준에 맞는 기사만 선별
- 사용자 친화적인 HTML 리포트 생성
- 수집 결과 로깅 및 추적

---

## ⚙️ 기술 구성

```
news-fetcher-agent 호출
       ↓
  [실행 환경 확인]
  - Python 설치 여부
  - 필요한 라이브러리 설치
       ↓
  [news_fetcher.py 실행]
  - 3개 한국 뉴스 소스 접근
  - 최신 기사 검색 (최대 15개)
  - 필터링 및 검증
       ↓
  [HTML 리포트 생성]
  - 현대적 UI/UX (CSS3 활용)
  - 한국어 완전 지원
  - 모바일 반응형
       ↓
  [결과 검증]
  - 파일 생성 확인
  - 콘텐츠 품질 확인
  - 오류 로깅
       ↓
  [보고]
  - 수집된 뉴스 개수
  - 파일 경로
  - 실행 소요 시간
```

---

## 🔄 실행 흐름

### Step 1: 실행 환경 검증

```bash
# 필수 요구사항 확인
✓ Python 3.8+ 설치
✓ requests 라이브러리 설치
✓ beautifulsoup4 설치
✓ feedparser 설치
✓ 작업 디렉토리 접근 권한
```

### Step 2: 뉴스 수집

```
한국 AI 뉴스 소스 (3개)
├─ VentureSquare (벤처스퀘어)
│  └─ RSS 피드: AI/빅데이터 카테고리
│
├─ IT World Korea (아이티월드코리아)
│  └─ RSS 피드: AI/머신러닝 섹션
│
└─ The Hankyoreh (한겨레)
   └─ RSS 피드: AI 관련 기사
```

### Step 3: 필터링 기준

다음 항목에 해당하는 기사는 **자동으로 제외**됩니다:

| 기준 | 설명 | 예시 |
|-----|------|------|
| 생성형 AI 제외 | 생성형 AI로 작성된 기사 제외 | "AI가 작성한 기사", "ChatGPT 기반" |
| GitHub 제외 | GitHub의 README, 저장소 정보 제외 | "github.com", "GitHub repo" |
| 포털 뉴스 제외 | 네이버, 다음 등 대형 포털 기사 제외 | "naver.com", "daum.net" |
| 논문 제외 | 학술 논문, 아카이브 제외 | "arxiv.org", "scholar.google" |
| 웹사이트 제한 | 출처 웹사이트 10개 이내로 제한 | 다양한 출처 권장 |
| 초보자 난이도 | AI 초보자 입장에서 이해하기 쉬운 내용만 선별 | 기술 용어 최소화 |

### Step 4: HTML 리포트 생성

```
생성 파일: ai-news-digest-YYYY-MM-DD.html

포함 내용:
├─ 헤더
│  ├─ 제목 "AI 뉴스 일일 리포트"
│  ├─ 생성 날짜 (YYYY-MM-DD)
│  ├─ 수집된 뉴스 개수
│  └─ 마지막 업데이트 시간
│
├─ 본문
│  ├─ 기사 1
│  │  ├─ 제목 (클릭 가능 링크)
│  │  ├─ 출처
│  │  ├─ 게시 날짜
│  │  ├─ 요약 (자동 생성)
│  │  └─ 카테고리
│  │
│  ├─ 기사 2
│  └─ ... (최대 15개)
│
└─ 푸터
   ├─ 생성 시간
   ├─ 다음 업데이트 예정
   └─ 저작권 정보
```

---

## 📊 입력값 (Inputs)

| 파라미터 | 기본값 | 설명 | 예시 |
|---------|-------|------|------|
| `date` | 오늘 날짜 | 리포트 생성 날짜 | `2026-06-12` |
| `max_articles` | `15` | 수집할 최대 뉴스 개수 | `10` ~ `20` |
| `lang` | `ko` | 언어 (한국어 고정) | `ko` |
| `filter_level` | `strict` | 필터링 엄격도 | `strict`, `normal` |
| `timeout` | `30` | 요청 타임아웃 (초) | `30` |

---

## 📁 출력값 (Outputs)

### 성공 시

```
✅ 생성 파일
├─ ai-news-digest-YYYY-MM-DD.html (메인 리포트)
└─ .claude/logs/news-fetcher-YYYY-MM-DD.log (실행 로그)

📊 반환되는 메타데이터
{
  "status": "success",
  "html_report": "/path/to/ai-news-digest-2026-06-12.html",
  "news_count": 12,
  "sources_count": 8,
  "execution_time": "4.23s",
  "timestamp": "2026-06-12T08:05:30Z"
}
```

### 실패 시

```
❌ 오류 로그
├─ 실패 원인
├─ 영향 받은 소스
├─ 재시도 여부
└─ 권장 조치

📊 반환되는 메타데이터
{
  "status": "partial_success" | "failed",
  "news_count": 5,
  "error": "Failed to fetch from IT World Korea",
  "retry_count": 2,
  "execution_time": "8.45s"
}
```

---

## 🔧 실행 명령

### morning-briefing에서 호출 (자동)

```bash
# morning-briefing이 자동으로 호출
# 별도의 수동 명령 불필요
```

### 수동 실행

```bash
# 표준 실행
claude /agents news-fetcher-agent

# 옵션과 함께 실행
claude /agents news-fetcher-agent --max-articles=20 --filter-level=normal

# 오늘 뉴스 다시 수집 (기존 파일 덮어씀)
claude /agents news-fetcher-agent --force
```

---

## 🔍 상세 작업 흐름

### 1단계: 초기화 (10초)

```
✓ Python 환경 확인
✓ 필수 라이브러리 import
✓ 로깅 설정
✓ 타임존 설정 (JST)
```

### 2단계: 뉴스 수집 (3~5분)

```
소스별 수집:

VentureSquare
  ↓
  [RSS 피드 파싱]
  ↓
  [JSON 변환]
  ↓
  기사 5~10개 추출

IT World Korea
  ↓
  [RSS 피드 파싱]
  ↓
  [JSON 변환]
  ↓
  기사 3~8개 추출

The Hankyoreh
  ↓
  [RSS 피드 파싱]
  ↓
  [JSON 변환]
  ↓
  기사 2~5개 추출

합계: 10~23개 기사 → 필터링 후 최대 15개
```

### 3단계: 필터링 (10초)

```
수집된 기사 (20개 예시)
  ↓
[규칙 1] 생성형 AI 기사 제외 (-2개)
  ↓
[규칙 2] GitHub 콘텐츠 제외 (-1개)
  ↓
[규칙 3] 포털 뉴스 제외 (-3개)
  ↓
[규칙 4] 논문 제외 (-0개)
  ↓
[규칙 5] 웹사이트 제한 (10개 이내) (-1개)
  ↓
[규칙 6] 초보자 난이도 필터 (-1개)
  ↓
최종: 12개 기사 ✅
```

### 4단계: HTML 생성 (2~3초)

```
기사 정보 수집
  ↓
[Jinja2 템플릿 렌더링]
  ↓
[CSS3 스타일 적용]
  - 그래디언트 배경
  - 유리같은 효과 (glassmorphism)
  - 애니메이션
  - 모바일 반응형
  ↓
[한국어 완전 지원]
  - UTF-8 인코딩
  - 한글 폰트 적용
  ↓
html_report.html 생성 ✅
```

### 5단계: 검증 (5초)

```
✓ 파일 생성 확인
✓ 파일 크기 검사 (최소 50KB)
✓ HTML 유효성 검사
✓ 링크 유효성 샘플 검사
✓ 인코딩 확인 (UTF-8)
```

---

## ⚡ 예외 처리

| 상황 | 감지 | 대응 |
|-----|------|------|
| 소스 접근 실패 | HTTP 타임아웃 | 3회 재시도 (지수 백오프) |
| RSS 파싱 오류 | 포맷 오류 | 해당 소스 스킵, 다른 소스 계속 |
| 네트워크 오류 | 연결 불가 | 재시도 후 부분 성공 처리 |
| 파일 쓰기 실패 | 디스크 용량 부족 | 로그 기록 후 실패 반환 |
| 인코딩 오류 | 문자 깨짐 | UTF-8 강제 적용 |

---

## 📝 로그 포맷

```
[2026-06-12 08:00:01] INFO    news-fetcher-agent started
[2026-06-12 08:00:02] INFO    Fetching from VentureSquare...
[2026-06-12 08:00:05] INFO    Retrieved 8 articles from VentureSquare
[2026-06-12 08:00:06] INFO    Fetching from IT World Korea...
[2026-06-12 08:00:09] INFO    Retrieved 6 articles from IT World Korea
[2026-06-12 08:00:10] INFO    Fetching from The Hankyoreh...
[2026-06-12 08:00:13] INFO    Retrieved 4 articles from The Hankyoreh
[2026-06-12 08:00:13] INFO    Total articles: 18
[2026-06-12 08:00:13] INFO    Filtering articles... (applying 6 rules)
[2026-06-12 08:00:14] INFO    After filtering: 12 articles
[2026-06-12 08:00:14] INFO    Generating HTML report...
[2026-06-12 08:00:17] INFO    HTML report generated: ai-news-digest-2026-06-12.html
[2026-06-12 08:00:17] INFO    Validating HTML...
[2026-06-12 08:00:18] INFO    ✅ Validation passed
[2026-06-12 08:00:18] INFO    news-fetcher-agent completed successfully
[2026-06-12 08:00:18] INFO    Execution time: 18.2s
```

---

## 🔗 의존성

### 필수 파일
- ✅ `news_fetcher.py` (프로젝트 루트)

### 필수 라이브러리
- ✅ `requests` (HTTP 요청)
- ✅ `beautifulsoup4` (HTML 파싱)
- ✅ `feedparser` (RSS 파싱)
- ✅ `jinja2` (템플릿 렌더링)

### 필수 권한
- ✅ `python` (스크립트 실행)
- ✅ `bash` (셸 명령)
- ✅ 인터넷 접근 (뉴스 소스 접근)

### 네트워크 의존성
- ✅ VentureSquare RSS 피드
- ✅ IT World Korea RSS 피드
- ✅ The Hankyoreh RSS 피드

---

## 💡 성능 최적화

### 캐싱 (향후)
```bash
# 동일한 기사 중복 제거
# 24시간 이내 수집된 기사 캐싱
```

### 병렬 처리 (향후)
```python
# 3개 소스를 동시에 수집
# 실행 시간 50% 단축 예상
```

### 증분 수집 (향후)
```bash
# 마지막 수집 이후의 신규 기사만 수집
# 네트워크 트래픽 감소
```

---

## 🚀 사용 예시

### 예시 1: 자동 실행 (기본)

```
[8:00 AM JST] morning-briefing 시작
   ↓
news-fetcher-agent 자동 호출
   ↓
AI 뉴스 18개 수집 → 필터링 12개
   ↓
ai-news-digest-2026-06-12.html 생성 ✅
   ↓
morning-briefing에 결과 반환
```

### 예시 2: 수동 실행 (즉시 필요)

```bash
# 언제든지 수동 실행
$ claude /agents news-fetcher-agent

✅ news-fetcher-agent started
📰 Fetching AI news...
✓ VentureSquare: 8 articles
✓ IT World Korea: 6 articles
✓ The Hankyoreh: 4 articles
📊 Total: 18 articles → Filtered: 12 articles
📄 HTML report generated: ai-news-digest-2026-06-12.html
⏱️ Execution time: 18.2s
```

### 예시 3: 오류 시 부분 성공

```bash
$ claude /agents news-fetcher-agent

⚠️ Warning: Failed to fetch from IT World Korea (timeout)
✓ VentureSquare: 8 articles
✗ IT World Korea: 0 articles (failed)
✓ The Hankyoreh: 4 articles
📊 Total: 12 articles → Filtered: 9 articles
⚠️ Partial success (2 sources available, 1 failed)
📄 HTML report generated: ai-news-digest-2026-06-12.html
```

---

## 📊 예상 성능

| 항목 | 값 |
|-----|-----|
| 평균 실행 시간 | 18~25초 |
| 네트워크 요청 수 | 3~5개 |
| 데이터 전송량 | 2~5MB |
| 최종 HTML 파일 크기 | 150~300KB |
| 평균 뉴스 수집 개수 | 10~15개 |

---

## 📞 문제 해결

### Q: "타임아웃" 오류 발생
**A**: 인터넷 연결 확인, 타임아웃 값 증가 시도, news_fetcher.py의 TIMEOUT 값 조정

### Q: 뉴스가 너무 적게 수집됨 (< 5개)
**A**: 필터링 규칙 확인, filter_level을 'normal'로 완화, 뉴스 소스 추가

### Q: HTML 파일이 생성되지 않음
**A**: 디스크 용량 확인, Jinja2 템플릿 파일 확인, 권한 확인

### Q: 한글이 깨져 표시됨
**A**: UTF-8 인코딩 확인, 브라우저 인코딩 설정 확인 (한국어로 설정)

---

## 📌 버전 히스토리

| 버전 | 날짜 | 변경 사항 |
|-----|------|---------|
| v1.0.0 | 2026-06-12 | 초기 버전 작성 |

---

**마지막 업데이트**: 2026-06-12  
**관리자**: Claude Code
