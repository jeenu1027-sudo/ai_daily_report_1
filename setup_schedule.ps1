# AI Daily News Report - Scheduled Task Setup
# This script creates a Windows Task Scheduler job to run the news fetcher daily at 8:00 AM

$taskName = "AI Daily News Report"
$taskDescription = "매일 아침 8시에 AI 동향 뉴스를 자동으로 수집하고 HTML 리포트를 생성합니다"
$scriptPath = "C:\ai_daily_report_1\run_news_fetcher.bat"
$taskPath = "\AI News\"

# 작업이 이미 존재하면 제거
try {
    $existingTask = Get-ScheduledTask -TaskName $taskName -TaskPath $taskPath -ErrorAction SilentlyContinue
    if ($existingTask) {
        Write-Host "기존 작업을 제거하고 있습니다..."
        Unregister-ScheduledTask -TaskName $taskName -TaskPath $taskPath -Confirm:$false
    }
}
catch {
    # 작업이 없으면 무시
}

# 매일 08:00 (JST 기준)에 실행되는 트리거 생성
# 주의: 이 시간은 서버의 로컬 시간대를 기준으로 합니다
# JST는 UTC+9 입니다. 필요시 로컬 시간대에 맞게 조정하세요
$trigger = New-ScheduledTaskTrigger -Daily -At "08:00"

# 작업의 실행 설정
$action = New-ScheduledTaskAction -Execute $scriptPath -WorkingDirectory "C:\ai_daily_report_1"

# 작업의 기본 설정
$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -RunOnlyIfNetworkAvailable

# 작업 등록
try {
    Register-ScheduledTask -TaskName $taskName `
        -TaskPath $taskPath `
        -Action $action `
        -Trigger $trigger `
        -Settings $settings `
        -Description $taskDescription `
        -RunLevel Highest `
        -Force | Out-Null

    Write-Host "✅ 작업이 성공적으로 등록되었습니다!"
    Write-Host ""
    Write-Host "작업 정보:"
    Write-Host "  - 작업명: $taskName"
    Write-Host "  - 경로: $taskPath"
    Write-Host "  - 실행 시간: 매일 08:00"
    Write-Host "  - 스크립트: $scriptPath"
    Write-Host ""
    Write-Host "💡 팁: JST(동경표준시)를 기준으로 실행하려면 로컬 시간대를 확인하세요."
    Write-Host "   Task Scheduler를 열어 작업의 트리거를 필요에 따라 조정할 수 있습니다."
}
catch {
    Write-Host "❌ 작업 등록 실패: $_"
    exit 1
}

# 작업이 제대로 등록되었는지 확인
$registeredTask = Get-ScheduledTask -TaskName $taskName -TaskPath $taskPath
if ($registeredTask) {
    Write-Host ""
    Write-Host "작업 스케줄 확인:"
    $registeredTask | Get-ScheduledTaskInfo
}
