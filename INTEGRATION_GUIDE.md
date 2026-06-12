# 🚀 Harness 프로젝트 통합 가이드

Harness 팀 에이전트를 실제 프로젝트에 통합하여 자동화를 설정하는 방법입니다.

---

## 📋 목차

1. [환경 변수 설정](#1-환경-변수-설정)
2. [자동 스케줄 설정](#2-자동-스케줄-설정)
3. [Hooks 이해하기](#3-hooks-이해하기)
4. [첫 실행 테스트](#4-첫-실행-테스트)
5. [모니터링](#5-모니터링)
6. [문제 해결](#6-문제-해결)

---

## 1. 환경 변수 설정

### Step 1️⃣: .env 파일 생성

```bash
# .env.example을 .env로 복사
cp .env.example .env
```

### Step 2️⃣: 필수 정보 입력

`.env` 파일을 열고 다음 항목들을 채우세요:

```env
# 필수
ANTHROPIC_API_KEY=sk-ant-api03-your-key-here
ANTHROPIC_ENVIRONMENT_ID=env_your-environment-id-here

# GitHub (선택)
GITHUB_TOKEN=ghp_your-github-token-here
```

### Step 3️⃣: 권한 설정

```powershell
# .env 파일 권한 설정 (중요: 다른 사용자가 읽지 못하도록)
icacls ".env" /grant:r "%USERNAME%:F" /inheritance:r
```

---

## 2. 자동 스케줄 설정

### Step 1️⃣: PowerShell 관리자 권한 실행

```powershell
# PowerShell을 "관리자 권한"으로 실행
# (윈도우에서 PowerShell 검색 → 우클릭 → 관리자 권한으로 실행)
```

### Step 2️⃣: 스케줄 설정 스크립트 실행

```powershell
# 프로젝트 폴더로 이동
cd C:\ai_daily_report_1

# 스케줄 설정 (8시 JST)
.\setup-schedule.ps1 -Time "08:00"

# 다른 시간으로 설정하려면
.\setup-schedule.ps1 -Time "09:00"
```

### Step 3️⃣: 설정 확인

```powershell
# 스케줄된 작업 확인
Get-ScheduledTask -TaskName "AI-Daily-Report-Harness" | Format-Table -AutoSize

# 자세한 정보 보기
Get-ScheduledTask -TaskName "AI-Daily-Report-Harness" | Get-ScheduledTaskInfo
```

---

## 3. Hooks 이해하기

### 자동화 흐름

```
매일 8시 JST
    ↓
┌─ before_morning_briefing (시작 전)
│  ├─ Git 저장소 동기화 (git pull)
│  └─ 로그 시작 기록
│
├─ after_news_fetch (뉴스 수집 후)
│  ├─ 뉴스 파일 스테이징 (git add)
│  ├─ 커밋 (뉴스 리포트)
│  └─ 로그 기록
│
├─ after_issue_analysis (이슈 분석 후)
│  ├─ 이슈 보고서 스테이징 (git add)
│  ├─ 커밋 (이슈 분석)
│  └─ 로그 기록
│
└─ after_morning_briefing (완료 후)
   ├─ GitHub 푸시 (git push)
   ├─ 로그 완료 기록
   └─ 오래된 로그 삭제
```

### Hooks 파일 위치

**파일**: `.claude/hooks.json`

```json
{
  "before_morning_briefing": {
    "description": "아침 브리핑 시작 전 실행",
    "trigger": "morning-briefing 에이전트 시작",
    "actions": [...]
  },
  
  "after_news_fetch": {
    "description": "뉴스 수집 완료 후 실행",
    "trigger": "news-fetcher-agent 완료",
    "actions": [...]
  },
  
  "after_issue_analysis": {
    "description": "이슈 분석 완료 후 실행",
    "trigger": "issue-analyzer 에이전트 완료",
    "actions": [...]
  },
  
  "after_morning_briefing": {
    "description": "아침 브리핑 전체 완료 후 실행",
    "trigger": "morning-briefing 에이전트 완료",
    "actions": [...]
  },
  
  "on_error": {
    "description": "에러 발생 시 실행",
    "trigger": "any agent fails",
    "actions": [...]
  }
}
```

### Hooks 커스터마이징

원하는 동작을 추가하려면 `hooks.json`을 수정하세요:

```json
{
  "after_morning_briefing": {
    "actions": [
      {
        "name": "custom_action",
        "command": "echo 'Custom action executed'",
        "timeout": 10,
        "on_error": "warn"
      }
    ]
  }
}
```

---

## 4. 첫 실행 테스트

### 수동으로 먼저 실행해보기

```powershell
# 프로젝트 폴더로 이동
cd C:\ai_daily_report_1

# 수동 실행 스크립트 실행
.\run-morning-briefing.ps1

# 로그 확인
cat .\.claude\logs\daily.log
```

### 스케줄 작업 수동 실행

```powershell
# 스케줄된 작업을 지금 바로 실행 (테스트용)
Start-ScheduledTask -TaskName "AI-Daily-Report-Harness"

# 5초 대기 후 로그 확인
Start-Sleep -Seconds 5
Get-Content .\.claude\logs\daily.log | Select-Object -Last 20
```

### 실행 결과 확인

로그 파일 위치: `.claude/logs/daily.log`

```
[2026-06-12 08:00:01] [START] ========================================
[2026-06-12 08:00:01] [INFO] Morning Briefing 에이전트 시작
[2026-06-12 08:00:02] [INFO] 프로젝트 경로: C:\ai_daily_report_1
[2026-06-12 08:00:03] [INFO] ✓ .env 파일 로드 완료
[2026-06-12 08:00:05] [INFO] ✓ Git 동기화 완료
[2026-06-12 08:00:25] [INFO] ✓ morning-briefing 에이전트 실행 중...
[2026-06-12 08:00:30] [INFO] ✓ 뉴스 리포트 생성됨: ai-news-digest-2026-06-12.html
[2026-06-12 08:00:35] [INFO] ✓ 이슈 보고서 생성됨: issue-priority-report-2026-06-12.md
[2026-06-12 08:00:40] [INFO] ✓ Git 커밋 완료
[2026-06-12 08:00:50] [INFO] ✓ GitHub 푸시 완료
[2026-06-12 08:00:51] [COMPLETE] ========================================
```

---

## 5. 모니터링

### 일일 로그 확인

```powershell
# 오늘의 로그 전체 보기
Get-Content .\.claude\logs\daily.log

# 마지막 10줄만 보기
Get-Content .\.claude\logs\daily.log | Select-Object -Last 10

# 실시간 모니터링 (매초 업데이트)
Get-Content .\.claude\logs\daily.log -Wait
```

### 에러 로그 확인

```powershell
# 에러 로그 보기
Get-Content .\.claude\logs\error.log -ErrorAction SilentlyContinue
```

### 스케줄 작업 상태 확인

```powershell
# 작업 상태
Get-ScheduledTask -TaskName "AI-Daily-Report-Harness" | Format-List

# 마지막 실행 결과
Get-ScheduledTaskInfo -TaskName "AI-Daily-Report-Harness" | Format-List
```

---

## 6. 문제 해결

### 문제 1️⃣: 스케줄이 실행되지 않음

**원인**: 관리자 권한 부족

**해결**:
```powershell
# 작업 삭제
Unregister-ScheduledTask -TaskName "AI-Daily-Report-Harness" -Confirm:$false

# PowerShell을 관리자 권한으로 다시 실행
# 스케줄 재설정
.\setup-schedule.ps1 -Time "08:00"
```

### 문제 2️⃣: API 키 오류

**원인**: ANTHROPIC_API_KEY가 설정되지 않음

**해결**:
```powershell
# .env 파일 확인
cat .env | grep ANTHROPIC_API_KEY

# 또는 환경 변수 직접 설정
$env:ANTHROPIC_API_KEY = "sk-ant-api03-..."
```

### 문제 3️⃣: Git 커밋/푸시 실패

**원인**: GitHub 토큰 만료 또는 권한 부족

**해결**:
```powershell
# GitHub 인증 재설정
gh auth login

# .env 파일에서 GITHUB_TOKEN 업데이트
```

### 문제 4️⃣: 로그 파일이 없음

**원인**: 로그 디렉토리가 없거나 권한 부족

**해결**:
```powershell
# 로그 디렉토리 생성
New-Item -ItemType Directory -Path ".\.claude\logs\archive" -Force

# 권한 설정
icacls ".\.claude\logs" /grant:r "%USERNAME%:F" /inheritance:r
```

---

## 📊 체크리스트

아래 항목들을 모두 체크했는지 확인하세요:

- [ ] `.env` 파일이 생성되고 필수 정보 입력됨
- [ ] `ANTHROPIC_API_KEY` 설정됨
- [ ] `ANTHROPIC_ENVIRONMENT_ID` 설정됨 (선택)
- [ ] 스케줄 설정 스크립트 실행됨 (관리자 권한)
- [ ] 스케줄 작업이 "AI-Daily-Report-Harness" 이름으로 생성됨
- [ ] `.claude/logs` 디렉토리가 생성됨
- [ ] 수동 테스트 실행 성공
- [ ] 로그 파일에서 성공 메시지 확인
- [ ] `.env` 파일의 권한이 제한됨 (보안)

---

## 🚀 다음 단계

1. **모니터링 자동화**: 이메일 알림 설정
2. **리포트 배포**: 생성된 HTML 리포트를 웹서버에 배포
3. **대시보드**: 매일 생성되는 통계를 시각화
4. **Slack 연동**: 완료 알림을 Slack에 전송

---

**마지막 업데이트**: 2026-06-12  
**버전**: Harness v2.0.0
