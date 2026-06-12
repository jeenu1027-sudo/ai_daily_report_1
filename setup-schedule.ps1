# Harness 자동 스케줄 설정 스크립트
# 매일 8시 JST에 morning-briefing 에이전트를 자동으로 실행합니다

param(
    [string]$Time = "08:00",
    [string]$ProjectPath = "C:\ai_daily_report_1"
)

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "🌅 Harness 자동 스케줄 설정" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

# 1. 프로젝트 경로 확인
Write-Host "`n✓ 프로젝트 경로: $ProjectPath"

# 2. 환경 변수 로드
Write-Host "`n📋 환경 변수 설정..."

# .env 파일 확인
if (Test-Path "$ProjectPath\.env") {
    Write-Host "  ✓ .env 파일 찾음" -ForegroundColor Green
    Get-Content "$ProjectPath\.env" | ForEach-Object {
        if ($_ -and -not $_.StartsWith("#")) {
            $key, $value = $_ -split "=", 2
            [System.Environment]::SetEnvironmentVariable($key.Trim(), $value.Trim(), "Process")
        }
    }
} else {
    Write-Host "  ⚠️  .env 파일 없음 (선택사항)" -ForegroundColor Yellow
}

# 3. 스케줄된 작업 확인
Write-Host "`n🔍 기존 스케줄 확인..."
$existingTask = Get-ScheduledTask -TaskName "AI-Daily-Report-Harness" -ErrorAction SilentlyContinue

if ($existingTask) {
    Write-Host "  ✓ 기존 작업 찾음: $($existingTask.TaskName)"
    Write-Host "  다음 실행: $($existingTask.Triggers.StartBoundary)"
}

# 4. 스케줄된 작업 만들기 또는 업데이트
Write-Host "`n⚙️  스케줄 설정 중 ($Time JST)..."

# PowerShell 스크립트 경로
$ScriptPath = "$ProjectPath\run-morning-briefing.ps1"

# 작업 설정
$TaskName = "AI-Daily-Report-Harness"
$TaskDescription = "Harness 팀 에이전트 - 매일 아침 뉴스 및 이슈 분석"

# 시간 문자열 변환 (HH:mm 형식)
$TimeObj = [DateTime]::ParseExact($Time, "HH:mm", $null)
$Trigger = New-ScheduledTaskTrigger -Daily -At $TimeObj

# 작업 액션
$Action = New-ScheduledTaskAction `
    -Execute "powershell.exe" `
    -Argument "-NoProfile -ExecutionPolicy Bypass -File `"$ScriptPath`""

# 기존 작업이 있으면 삭제
if ($existingTask) {
    Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false
    Write-Host "  ✓ 기존 작업 삭제됨" -ForegroundColor Green
}

# 새 작업 등록
try {
    Register-ScheduledTask `
        -TaskName $TaskName `
        -Trigger $Trigger `
        -Action $Action `
        -Description $TaskDescription `
        -RunLevel Highest `
        -Force | Out-Null

    Write-Host "  ✓ 스케줄 작업 등록 완료!" -ForegroundColor Green
} catch {
    Write-Host "  ❌ 에러: $_" -ForegroundColor Red
    Write-Host "  💡 관리자 권한으로 실행해주세요" -ForegroundColor Yellow
    exit 1
}

# 5. 정보 출력
Write-Host "`n📊 설정 정보:"
Write-Host "  작업 이름: $TaskName"
Write-Host "  실행 시간: $Time (매일)"
Write-Host "  프로젝트: $ProjectPath"
Write-Host "  스크립트: $ScriptPath"

# 6. 스케줄 확인
Write-Host "`n✅ 스케줄 확인:"
$Task = Get-ScheduledTask -TaskName $TaskName
Write-Host "  다음 실행: $($Task.Triggers.StartBoundary)" -ForegroundColor Green
Write-Host "  상태: $($Task.State)" -ForegroundColor Green

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "✨ 설정 완료!" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "`n📌 참고:"
Write-Host "  • 작업 확인: Get-ScheduledTask -TaskName 'AI-Daily-Report-Harness'"
Write-Host "  • 작업 삭제: Unregister-ScheduledTask -TaskName 'AI-Daily-Report-Harness' -Confirm:`$false"
