@echo off
REM AI Daily News Report - Scheduled Task Batch File
REM Runs the news fetcher script daily at 8:00 AM JST

cd /d "C:\ai_daily_report_1"
python news_fetcher.py
