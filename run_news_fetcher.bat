@echo off
REM AI Daily News Report - Enhanced Batch Script
REM Runs the news fetcher script daily at 8:00 AM JST with error handling and logging

chcp 65001 > nul
setlocal enabledelayedexpansion

set SCRIPT_DIR=%~dp0
set LOG_DIR=%SCRIPT_DIR%logs
set LOG_FILE=%LOG_DIR%\news_fetcher.log
set TIMESTAMP=%date:~10,4%-%date:~4,2%-%date:~7,2% %time:~0,2%:%time:~3,2%:%time:~6,2%

REM 로그 디렉토리 생성
if not exist "%LOG_DIR%" (
    mkdir "%LOG_DIR%"
    echo [!TIMESTAMP!] Created logs directory >> "%LOG_FILE%"
)

REM Python 설치 확인
python --version >nul 2>&1
if errorlevel 1 (
    echo [!TIMESTAMP!] ERROR: Python not found >> "%LOG_FILE%"
    echo ERROR: Python not found in PATH
    exit /b 1
)

REM 뉴스 수집 실행
echo [!TIMESTAMP!] Starting news fetcher... >> "%LOG_FILE%"
cd /d "%SCRIPT_DIR%"
python news_fetcher.py >> "%LOG_FILE%" 2>&1

if errorlevel 1 (
    echo [!TIMESTAMP!] ERROR: news_fetcher.py failed (exit code %errorlevel%) >> "%LOG_FILE%"
    echo ERROR: News fetcher failed. Check %LOG_FILE% for details.
    exit /b 1
)

echo [!TIMESTAMP!] Completed successfully >> "%LOG_FILE%"
exit /b 0
