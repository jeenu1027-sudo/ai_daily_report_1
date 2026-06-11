# Claude Code Configuration

프로젝트 설정 및 커스텀 스킬 정의

## 📋 프로젝트 개요

**AI Daily News Report** - AI 동향 관련 뉴스를 매일 아침 자동으로 수집하여 HTML 리포트로 생성하는 프로젝트

- **언어**: Python 3.14.6
- **주요 스크립트**: `news_fetcher.py`
- **자동화**: Windows Task Scheduler
- **실행 시간**: 매일 08:00 (JST)

## 🎯 프로젝트 구조

```
ai_daily_report_1/
├── .claude/
│   └── skills/
│       └── git_issue.md           # GitHub 이슈 생성 스킬
├── news_fetcher.py                # 메인 뉴스 수집 스크립트
├── run_news_fetcher.bat           # Windows 배치 파일
├── setup_schedule.ps1             # 스케줄 설정 스크립트
├── requirements.txt               # Python 의존성
├── README.md                      # 프로젝트 설명
├── SCHEDULE_SETUP.md              # 스케줄 설정 가이드
└── CLAUDE.md                      # 이 파일
```

## ⚙️ Claude Code 설정

### 프로젝트 명령어

프로젝트에서 자주 사용되는 명령어:

```bash
# 뉴스 수집 스크립트 실행
python news_fetcher.py

# 의존성 설치
pip install -r requirements.txt

# Windows 작업 스케줄러 설정
.\setup_schedule.ps1
```

### 사용 가능한 스킬

#### 1. `git_issue` - GitHub 이슈 생성 스킬

**설명**: GitHub 레포지토리(jeenu1027-sudo/ai_daily_report_1)에 이슈를 자동으로 생성합니다.

**사용 예시**:
```
사용자: "버그 리포트를 이슈로 등록해줘: 뉴스 수집 시 타임아웃 에러 발생"

Claude: git_issue 스킬 실행
→ GitHub 이슈 생성
→ 이슈 URL 반환
```

**파라미터**:
- **title** (필수): 이슈 제목
- **description** (필수): 이슈 상세 설명
- **labels** (선택): 라벨 (bug, enhancement, feature, documentation 등)
- **assignee** (선택): 담당자 (GitHub username)

**사용 시나리오**:
- "버그 리포트 이슈 만들어줘"
- "기능 요청 이슈 생성해줘"
- "문서 업데이트 이슈를 등록해줘"

자세한 정보는 [git_issue.md](./.claude/skills/git_issue.md) 참고

## 📝 스킬 개발 가이드

### 새 스킬 추가 방법

1. `.claude/skills/` 디렉토리에 `skill_name.md` 파일 생성
2. 스킬의 메타데이터, 설명, 사용 예시 작성
3. 필요한 명령어 및 파라미터 정의
4. `CLAUDE.md`에 스킬 등록

### 스킬 포맷

```markdown
# Skill Name

## Metadata
- **name**: skill_name
- **description**: 스킬 설명

## Summary
스킬의 간단한 설명

## Usage
사용자가 어떻게 사용할 수 있는지

## Parameters
필수/선택 파라미터 정의

## Examples
사용 예시
```

## 🔧 권장 설정

### `.claude/settings.json` (선택사항)

프로젝트별 Claude Code 설정을 자동화할 수 있습니다:

```json
{
  "model": "claude-opus-4-8",
  "permissions": {
    "gh": "allow",
    "bash": "allow",
    "python": "allow"
  }
}
```

## 🚀 실행 방법

### 1. 로컬 개발

```bash
cd C:\ai_daily_report_1
python news_fetcher.py
```

### 2. 자동화 스케줄

Windows Task Scheduler에서 매일 08:00에 자동 실행
(설정 방법: SCHEDULE_SETUP.md 참고)

### 3. GitHub 이슈 생성

Claude Code에서 `git_issue` 스킬 사용:
```
사용자: "버그 이슈를 생성해줘"
Claude: git_issue 스킬 실행 → GitHub 이슈 생성
```

## 📚 문서

- **README.md**: 프로젝트 기본 설명 및 사용 방법
- **SCHEDULE_SETUP.md**: Windows Task Scheduler 자동화 상세 가이드
- **PROJECT_SUMMARY.md**: 프로젝트 완전 정보
- **.claude/skills/git_issue.md**: GitHub 이슈 생성 스킬 상세 문서

## 🐛 주요 파일 설명

### news_fetcher.py
- **목적**: AI 뉴스 수집 및 HTML 생성
- **실행**: `python news_fetcher.py`
- **출력**: `ai-news-digest-YYYY-MM-DD.html`
- **시간대**: JST(UTC+9)

### run_news_fetcher.bat
- **목적**: Windows Task Scheduler와 Python 스크립트 연동
- **내용**: Python 스크립트 경로 및 실행 명령어

### setup_schedule.ps1
- **목적**: Windows Task Scheduler에 작업 등록 (관리자 권한 필요)
- **실행**: `.\setup_schedule.ps1`

### requirements.txt
- **requests**: HTTP 요청
- **beautifulsoup4**: HTML 파싱

## 💡 개발 팁

### 디버깅
```bash
# 스크립트 실행 시 상세 출력 확인
python news_fetcher.py

# 생성된 HTML 파일 확인
start ai-news-digest-2026-06-11.html
```

### 로그 확인
Windows Task Scheduler 히스토리:
1. 작업 스케줄러 열기
2. AI News 폴더 → Daily AI News Report
3. 하단의 "히스토리" 탭 확인

### 문제 해결
- 모듈 오류: `pip install -r requirements.txt`
- 권한 오류: 관리자 권한으로 PowerShell 실행
- 시간대 오류: `SCHEDULE_SETUP.md`의 시간대 변환표 참고

## 🔗 유용한 링크

- **GitHub 레포지토리**: https://github.com/jeenu1027-sudo/ai_daily_report_1
- **GitHub CLI 문서**: https://cli.github.com/manual/
- **Python requests 문서**: https://requests.readthedocs.io/
- **BeautifulSoup 문서**: https://www.crummy.com/software/BeautifulSoup/

## 📄 라이선스

개인 사용 목적으로 자유롭게 사용 및 수정 가능합니다.

---

**프로젝트 생성일**: 2026-06-11  
**마지막 업데이트**: 2026-06-11  
**상태**: ✅ 운영 준비 완료

**관리자**: Claude Code AI Assistant
