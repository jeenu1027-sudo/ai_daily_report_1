# AI Daily News Report - Enhanced Scheduled Task Setup
# This script creates a Windows Task Scheduler job with retry policy

# 관리자 권한 확인
if (-not ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) {
    Write-Host "ERROR: Administrator privileges required" -ForegroundColor Red
    Write-Host "Please run this script as Administrator"
    exit 1
}

$taskName = "AI Daily News Report"
$taskDescription = "매일 아침 8시에 AI 동향 뉴스를 자동으로 수집하고 HTML 리포트를 생성합니다"
$batchFile = "C:\ai_daily_report_1\run_news_fetcher.bat"
$taskPath = "\AI News\"

# Batch 파일 존재 확인
if (-not (Test-Path $batchFile)) {
    Write-Host "ERROR: Batch file not found: $batchFile" -ForegroundColor Red
    exit 1
}

# 기존 작업 제거
Write-Host "Checking for existing task..."
try {
    $existingTask = Get-ScheduledTask -TaskName $taskName -TaskPath $taskPath -ErrorAction SilentlyContinue
    if ($existingTask) {
        Write-Host "Removing existing task..."
        Unregister-ScheduledTask -TaskName $taskName -TaskPath $taskPath -Confirm:$false | Out-Null
    }
}
catch {
    # Task not found, continue
}

# 매일 08:00 (JST 기준)에 실행되는 트리거 생성
Write-Host "Creating daily trigger at 08:00..."
$trigger = New-ScheduledTaskTrigger -Daily -At "08:00"

# 재시도 정책: 5분 간격, 3회 반복 (총 15분)
$trigger.Repetition = New-ScheduledTaskTrigger -Once -At (Get-Date) -RepetitionInterval (New-TimeSpan -Minutes 5) -RepetitionDuration (New-TimeSpan -Minutes 15)

# 작업의 실행 설정
$action = New-ScheduledTaskAction `
    -Execute $batchFile `
    -WorkingDirectory "C:\ai_daily_report_1"

# 작업의 설정
$settings = New-ScheduledTaskSettingsSet `
    -AllowStartIfOnBatteries `
    -DontStopIfGoingOnBatteries `
    -RunOnlyIfNetworkAvailable `
    -StartWhenAvailable `
    -MultipleInstances IgnoreNew `
    -ExecutionTimeLimit (New-TimeSpan -Hours 1)

# 작업 등록
try {
    Write-Host "Registering scheduled task..."
    Register-ScheduledTask `
        -TaskName $taskName `
        -TaskPath $taskPath `
        -Action $action `
        -Trigger $trigger `
        -Settings $settings `
        -Description $taskDescription `
        -RunLevel Highest `
        -Force | Out-Null

    Write-Host ""
    Write-Host "✅ Task registered successfully!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Task Information:"
    Write-Host "  - Task name: $taskName"
    Write-Host "  - Path: $taskPath"
    Write-Host "  - Execute time: Daily at 08:00"
    Write-Host "  - Batch file: $batchFile"
    Write-Host "  - Retry policy: Every 5 minutes, 3 times (15 minutes total)"
    Write-Host ""
    Write-Host "Log location: C:\ai_daily_report_1\logs\news_fetcher.log"
}
catch {
    Write-Host "ERROR: Failed to register task: $_" -ForegroundColor Red
    exit 1
}

# 등록된 작업 정보 표시
Write-Host ""
Write-Host "Task Details:"
Write-Host "-" * 60
$registeredTask = Get-ScheduledTask -TaskName $taskName -TaskPath $taskPath
$registeredTask | Get-ScheduledTaskInfo | Format-List

# 작업 테스트 옵션
Write-Host ""
Write-Host "💡 To test the task, run:" -ForegroundColor Cyan
Write-Host "   Start-ScheduledTask -TaskName '$taskName' -TaskPath '$taskPath'"
Write-Host ""
Write-Host "To view logs:"
Write-Host "   Get-Content -Tail 20 'C:\ai_daily_report_1\logs\news_fetcher.log'"

exit 0
