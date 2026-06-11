# 🤖 AI 동향 뉴스 일일 리포트 - 프로젝트 완성

## ✅ 프로젝트 완료

AI 관련 최신 뉴스를 **매일 아침 8시(JST)**에 자동으로 수집하여 **HTML 리포트**로 생성하는 프로젝트가 완성되었습니다.

---

## 📦 프로젝트 구조

```
C:\ai_daily_report_1\
├── 📄 news_fetcher.py              # 메인 뉴스 수집 스크립트 (Python)
├── 🔧 run_news_fetcher.bat         # Windows 작업 스케줄러용 배치 파일
├── ⏰ setup_schedule.ps1            # 작업 스케줄러 설정 PowerShell 스크립트
├── 📋 requirements.txt              # Python 의존성 목록
├── 📖 README.md                     # 프로젝트 설명서
├── ⏳ SCHEDULE_SETUP.md             # 스케줄 설정 가이드
├── .gitignore                       # Git 무시 파일
├── ai-news-digest-2026-06-11.html  # 생성된 일일 리포트 (샘플)
└── (이전) node.js 버전 파일들      # 초기 버전 (사용하지 않음)
    ├── news-fetcher.js
    └── package.json
```

---

## 🚀 주요 기능

### 뉴스 수집
- ✅ **Hacker News** - 기술 커뮤니티 뉴스
- ✅ **Bloomberg** - 비즈니스/기술 뉴스
- ✅ **Wired** - 기술/과학 저널
- ✅ **The Verge** - 기술 뉴스 (선택사항)

### 필터링
- AI, 머신러닝, 딥러닝, LLM, GPT, Claude 등 AI 관련 키워드로 자동 필터링
- 중복 제거로 깔끔한 리포트 생성
- 최대 10개 뉴스 표시

### HTML 리포트
- 📱 반응형 디자인 (데스크톱/모바일)
- 🎨 아름다운 그래디언트 스타일
- 🔗 원문 링크 제공
- 📅 날짜별 파일명 (`ai-news-digest-YYYY-MM-DD.html`)

### 자동화
- ⏰ 매일 8시(JST)에 자동 실행
- 💾 자동 파일 생성 및 저장
- 🔄 네트워크 자동 재시도 기능

---

## 📋 사용 방법

### 1️⃣ 수동 실행 (테스트)
```bash
cd C:\ai_daily_report_1
python news_fetcher.py
```

### 2️⃣ 자동화 설정 (스케줄)

**옵션 A: Windows 작업 스케줄러** (권장)
- `SCHEDULE_SETUP.md` 파일의 방법 1 참고
- GUI로 간단하게 설정 가능

**옵션 B: PowerShell 스크립트**
```powershell
# 관리자 권한 필요
cd "C:\ai_daily_report_1"
.\setup_schedule.ps1
```

**옵션 C: 수동 명령어**
```powershell
# 관리자 권한 필요
$trigger = New-ScheduledTaskTrigger -Daily -At "08:00"
$action = New-ScheduledTaskAction -Execute "C:\ai_daily_report_1\run_news_fetcher.bat"
Register-ScheduledTask -TaskName "AI Daily News Report" -Trigger $trigger -Action $action
```

### 3️⃣ 리포트 확인
- 생성된 HTML 파일을 브라우저에서 열기
- 파일 위치: `C:\ai_daily_report_1\ai-news-digest-YYYY-MM-DD.html`

---

## ⚙️ 설정 정보

### 시간대 설정
- **기본 설정**: 매일 08:00 실행
- **시간대**: 로컬 시간대 기준 (JST: UTC+9)
- **조정 필요 시**: `SCHEDULE_SETUP.md`의 "시간대 설정" 참고

### 뉴스 소스 커스터마이징

`news_fetcher.py` 파일을 편집하여:
1. **AI_KEYWORDS** 배열에 새로운 키워드 추가
2. **sources** 리스트에 새로운 RSS 피드 추가
3. **HTML 스타일** 변경

```python
# 키워드 추가 예
AI_KEYWORDS = ['AI', 'machine learning', '커스텀키워드', ...]

# 뉴스 소스 추가 예
sources = [
    {'url': 'https://your-rss-feed', 'name': 'Your Source'},
]
```

---

## 📊 생성되는 파일

### 파일 포맷
```
ai-news-digest-YYYY-MM-DD.html
```

### 파일 크기
- 약 5-7 KB (뉴스 10개 포함)

### 저장 위치
- `C:\ai_daily_report_1\`

### 파일 이름 예시
- `ai-news-digest-2026-06-11.html`
- `ai-news-digest-2026-06-12.html`
- `ai-news-digest-2026-06-13.html`

---

## 🔧 시스템 요구사항

### 필수 요구사항
- ✅ Python 3.8+ (현재: 3.14.6)
- ✅ Windows (작업 스케줄러 사용)
- ✅ 인터넷 연결

### 설치된 패키지
```
requests>=2.32.0       # HTTP 요청
beautifulsoup4>=4.12.0 # HTML 파싱
```

### 설치 방법
```bash
pip install -r requirements.txt
```

---

## 🐛 문제 해결

### "모듈을 찾을 수 없음"
```bash
pip install -r requirements.txt
```

### "파일이 생성되지 않음"
1. 뉴스 수집 권한 확인 (인터넷 연결)
2. 디렉토리 쓰기 권한 확인
3. 수동 실행으로 에러 메시지 확인

### "작업이 실행되지 않음"
1. 작업 스케줄러에서 작업 히스토리 확인
2. 네트워크 연결 상태 확인
3. Python 경로 및 배치 파일 경로 확인

---

## 📈 확장 계획

향후 추가 가능한 기능:
- [ ] 이메일로 자동 발송
- [ ] 슬랙/디스코드 봇 통합
- [ ] 데이터베이스에 뉴스 저장
- [ ] 웹 대시보드 생성
- [ ] 구글 드라이브 자동 백업
- [ ] 일주일/월간 요약 보고서

---

## 📝 라이선스

개인 사용 목적으로 자유롭게 사용 및 수정 가능합니다.

---

## 🎯 핵심 요약

| 항목 | 내용 |
|------|------|
| 🎯 목표 | AI 뉴스 일일 자동화 수집 |
| 📦 언어 | Python 3.14.6 |
| ⏰ 실행 시간 | 매일 08:00 (JST) |
| 📁 저장 위치 | C:\ai_daily_report_1\ |
| 📄 출력 형식 | HTML 파일 |
| 📊 뉴스 개수 | 최대 10개 |
| ✨ 상태 | **완성 & 테스트 완료** |

---

**프로젝트 완성일**: 2026-06-11  
**최종 상태**: ✅ 운영 준비 완료

Windows 작업 스케줄러를 통해 매일 자동으로 실행하도록 설정하면, 이 프로젝트는 완전히 자동화된 AI 뉴스 수집 시스템이 될 것입니다!
