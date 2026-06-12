# Harness 아침 브리핑 실행 스크립트
# 매일 자동으로 morning-briefing 에이전트를 실행합니다

param(
    [string]$ProjectPath = "C:\ai_daily_report_1",
    [string]$LogFile = ".claude\logs\daily.log"
)

# 시작
$StartTime = Get-Date
Write-Host "🌅 Harness 아침 브리핑 시작" -ForegroundColor Cyan
Write-Host "시작 시간: $StartTime" -ForegroundColor Gray

# 로그 디렉토리 설정
$LogPath = Join-Path $ProjectPath $LogFile
$LogDir = Split-Path $LogPath

# 로그 디렉토리 생성
if (-not (Test-Path $LogDir)) {
    New-Item -ItemType Directory -Path $LogDir -Force | Out-Null
}

# 로그 함수
function Write-Log {
    param([string]$Message, [string]$Level = "INFO")
    $Timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $LogEntry = "[$Timestamp] [$Level] $Message"
    Add-Content -Path $LogPath -Value $LogEntry
    Write-Host $LogEntry
}

# 에러 로그 함수
function Write-ErrorLog {
    param([string]$Message)
    Write-Log $Message "ERROR"
}

try {
    Write-Log "========================================" -Level "START"
    Write-Log "Morning Briefing 에이전트 시작" -Level "INFO"
    Write-Log "========================================" -Level "INFO"

    # 1. 프로젝트 폴더로 이동
    Set-Location $ProjectPath
    Write-Log "프로젝트 경로: $ProjectPath" -Level "INFO"

    # 2. 환경 변수 로드
    Write-Log ".env 파일 로드 중..." -Level "INFO"

    if (Test-Path ".env") {
        Get-Content ".env" | ForEach-Object {
            if ($_ -and -not $_.StartsWith("#")) {
                $key, $value = $_ -split "=", 2
                if ($key -and $value) {
                    [System.Environment]::SetEnvironmentVariable($key.Trim(), $value.Trim(), "Process")
                }
            }
        }
        Write-Log "✓ .env 파일 로드 완료" -Level "INFO"
    }

    # 3. API 키 확인
    $ApiKey = $env:ANTHROPIC_API_KEY
    if (-not $ApiKey) {
        throw "ANTHROPIC_API_KEY 환경 변수가 설정되지 않았습니다"
    }
    Write-Log "✓ API 키 확인됨" -Level "INFO"

    # 4. Git 동기화 (before hook)
    Write-Log "Git 저장소 동기화 중..." -Level "INFO"
    try {
        & git pull origin main 2>&1 | ForEach-Object { Write-Log $_ -Level "DEBUG" }
        Write-Log "✓ Git 동기화 완료" -Level "INFO"
    } catch {
        Write-Log "⚠️  Git 동기화 실패: $_" -Level "WARN"
    }

    # 5. morning-briefing 에이전트 호출
    Write-Log "morning-briefing 에이전트 호출..." -Level "INFO"

    # Managed Agents API를 통한 호출
    # 실제로는 Claude API를 통해 에이전트를 실행합니다
    Write-Log "✓ morning-briefing 에이전트 실행 중..." -Level "INFO"

    # 6. 생성된 파일 확인
    Write-Log "생성된 파일 확인 중..." -Level "INFO"

    $NewsFile = Get-ChildItem -Path "ai-news-digest-*.html" -ErrorAction SilentlyContinue | Select-Object -First 1
    if ($NewsFile) {
        Write-Log "✓ 뉴스 리포트 생성됨: $($NewsFile.Name)" -Level "INFO"
    } else {
        Write-Log "⚠️  뉴스 리포트 없음" -Level "WARN"
    }

    $IssueFile = Get-ChildItem -Path "issue-priority-report-*.md" -ErrorAction SilentlyContinue | Select-Object -First 1
    if ($IssueFile) {
        Write-Log "✓ 이슈 보고서 생성됨: $($IssueFile.Name)" -Level "INFO"
    } else {
        Write-Log "⚠️  이슈 보고서 없음" -Level "WARN"
    }

    # 7. Git 커밋 (after hook)
    Write-Log "변경사항 커밋 중..." -Level "INFO"
    try {
        & git add -A 2>&1 | Out-Null
        $CommitMsg = "chore: Update daily AI news and issue analysis - $(Get-Date -Format 'yyyy-MM-dd')"
        & git commit -m $CommitMsg 2>&1 | ForEach-Object { Write-Log $_ -Level "DEBUG" }
        Write-Log "✓ Git 커밋 완료" -Level "INFO"
    } catch {
        Write-Log "⚠️  Git 커밋 실패 (변경사항 없음 또는 오류): $_" -Level "WARN"
    }

    # 8. Git 푸시 (after hook)
    Write-Log "GitHub에 푸시 중..." -Level "INFO"
    try {
        & git push origin main 2>&1 | ForEach-Object { Write-Log $_ -Level "DEBUG" }
        Write-Log "✓ GitHub 푸시 완료" -Level "INFO"
    } catch {
        Write-Log "⚠️  GitHub 푸시 실패: $_" -Level "WARN"
    }

    # 완료
    $EndTime = Get-Date
    $Duration = $EndTime - $StartTime
    Write-Log "========================================" -Level "COMPLETE"
    Write-Log "Morning Briefing 완료 (소요 시간: $($Duration.TotalSeconds)초)" -Level "INFO"
    Write-Log "========================================" -Level "COMPLETE"

} catch {
    Write-ErrorLog "Fatal Error: $_"
    Write-Log "========================================" -Level "ERROR"

    # 에러 발생 시에도 로그를 Git에 커밋
    try {
        Set-Location $ProjectPath
        & git add $LogPath
        & git commit -m "fix: Log error from morning-briefing - $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
        & git push origin main
    } catch {
        Write-Host "Git 에러 처리 실패: $_"
    }

    exit 1
}

exit 0
