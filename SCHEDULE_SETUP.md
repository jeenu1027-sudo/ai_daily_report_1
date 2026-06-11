# ⏰ 스케줄 설정 가이드

AI 뉴스 리포트를 매일 8시(JST)에 자동으로 실행하도록 설정하는 방법입니다.

## 방법 1: Windows 작업 스케줄러 (권장)

### 1단계: 작업 스케줄러 열기
- `Windows + R` 키를 누르고 `taskschd.msc` 입력 후 Enter
- 또는 시작 메뉴에서 "작업 스케줄러" 검색

### 2단계: 작업 폴더 생성
1. 왼쪽 패널에서 "작업 스케줄러 라이브러리" 선택
2. 오른쪽 패널에서 "폴더 만들기" 선택
3. 폴더명: `AI News` 입력

### 3단계: 새 작업 생성
1. 생성된 "AI News" 폴더 오른쪽 클릭
2. "기본 작업 만들기" 선택
3. 다음 정보 입력:

**일반 탭:**
- 이름: `Daily AI News Report`
- 설명: `AI 동향 뉴스를 매일 수집하여 HTML 리포트 생성`
- ☑ 최대 권한으로 실행 (체크)

**트리거 탭:**
- "새로 만들기" 클릭
- 트리거: `매일`
- 시작: 매일 `08:00` 
  > ⏰ 참고: 시간대를 확인하세요. 
  > - 서버가 JST(UTC+9)면 08:00으로 설정
  > - 다른 시간대면 JST 기준 08:00으로 변환 필요

**동작 탭:**
- "새로 만들기" 클릭
- 동작: `프로그램 시작`
- 프로그램/스크립트: `C:\ai_daily_report_1\run_news_fetcher.bat`
- 시작: `C:\ai_daily_report_1`

**조건 탭:**
- ☑ 네트워크 사용 가능한 경우에만 시작

**설정 탭:**
- ☑ 작업을 실행 중인 경우 강제로 종료
- ☑ 작업이 실패한 경우 다시 시작

### 4단계: 저장 및 테스트
1. "확인" 클릭하여 작업 생성
2. 생성된 작업 오른쪽 클릭 → "실행"으로 테스트
3. `C:\ai_daily_report_1\` 폴더에 HTML 파일이 생성되었는지 확인

---

## 방법 2: PowerShell로 설정 (관리자 권한 필요)

```powershell
# 관리자 권한으로 PowerShell 실행 후 다음 명령어 실행:
cd "C:\ai_daily_report_1"
.\setup_schedule.ps1
```

---

## 방법 3: Python APScheduler 사용

`scheduler_daemon.py`를 만들어 백그라운드 서비스로 실행할 수 있습니다:

```python
from apscheduler.schedulers.background import BackgroundScheduler
import subprocess
import time

scheduler = BackgroundScheduler()

def fetch_news():
    subprocess.run(['python', 'news_fetcher.py'], cwd='C:\\ai_daily_report_1')

scheduler.add_job(fetch_news, 'cron', hour=8, minute=0)
scheduler.start()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    scheduler.shutdown()
```

---

## 확인 및 테스트

### 수동 테스트
```bash
cd C:\ai_daily_report_1
python news_fetcher.py
```

### 생성된 파일 확인
- 파일명: `ai-news-digest-YYYY-MM-DD.html`
- 위치: `C:\ai_daily_report_1\`
- 브라우저에서 HTML 파일을 열어 리포트 확인

### 작업 로그 확인
1. 작업 스케줄러에서 생성된 작업 선택
2. 하단의 "히스토리" 탭 확인
3. 성공/실패 여부 확인

---

## 시간대 설정

### JST(동경표준시) 기준 변환
서버의 시간대가 다른 경우 다음과 같이 변환하세요:

| 서버 시간대 | JST 08:00 변환 |
|-----------|--------------|
| UTC       | 17:00 (전날) |
| UTC+1     | 16:00 (전날) |
| UTC+8     | 09:00       |
| UTC+9     | 08:00 ✓     |

현재 서버 시간대 확인:
```powershell
[System.TimeZone]::CurrentTimeZone.StandardName
```

---

## 문제 해결

### ❌ "파일이 생성되지 않음"
- `run_news_fetcher.bat` 파일 경로 확인
- 작업 실행 시 에러 메시지 확인 (작업 스케줄러 히스토리)
- 네트워크 연결 상태 확인

### ❌ "권한 오류"
- 관리자 권한으로 작업 스케줄러 실행
- 작업의 "최대 권한으로 실행" 옵션 체크

### ❌ "인코딩 오류"
- `run_news_fetcher.bat` 파일의 인코딩을 UTF-8로 저장
- Python 스크립트 실행 권한 확인

---

## 추가 설정

### HTML 리포트 자동 오픈
작업 생성 후 동작 탭에서 추가 동작을 만들 수 있습니다:
- 프로그램: `cmd.exe`
- 인수: `/c start "" "C:\ai_daily_report_1\ai-news-digest-%date:~10,4%-%date:~4,2%-%date:~7,2%.html"`

### 이메일 알림 추가
작업 완료 후 이메일 발송 (Windows 10/11):
- Windows 자동화 또는 PowerShell 스크립트 활용
- 별도의 SMTP 설정 필요

---

**문제가 발생하면 `news_fetcher.py` 실행 후 에러 메시지를 확인하세요!**
