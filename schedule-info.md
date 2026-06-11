# AI 관련 뉴스 정리 자동화 설정

## 설정 정보

**작업명**: daily-ai-news-digest  
**실행 시간**: 매일 아침 8시 동경표준시(JST)  
**저장 위치**: C:\ai_daily_report_1\  
**파일 형식**: HTML (ai-news-digest-YYYY-MM-DD.html)  
**설정 날짜**: 2026-06-11

## 작동 방식

1. **뉴스 수집**
   - 신뢰할 만한 AI 뉴스 사이트에서 최신 뉴스 수집
   - 사이트: TechCrunch, VentureBeat, The Verge, Reuters, BBC, Wired 등

2. **한국어 정리**
   - 각 뉴스를 한국어로 제목, 요약, 출처, 링크와 함께 정리
   - 10개 이내의 뉴스만 선정

3. **HTML 파일 생성**
   - 매일 새로운 HTML 파일 생성
   - 파일명: ai-news-digest-YYYY-MM-DD.html (예: ai-news-digest-2026-06-11.html)
   - 깔끔한 스타일링과 한글 폰트 적용

## 스케줄 관리

- **저장 위치**: C:\Users\Admin\.claude\scheduled-tasks\daily-ai-news-digest\SKILL.md
- **상태 확인**: Claude Code 앱의 "Scheduled" 섹션에서 관리 가능
- **수동 실행**: "Run now" 버튼으로 즉시 실행 가능

## 참고사항

- Claude Code 앱이 열려있을 때 스케줄이 실행됩니다
- 앱이 닫혀있던 시간의 스케줄은 앱 재실행 시 자동으로 실행됩니다
- 처음 실행 시 필요한 권한(웹 검색, 파일 생성)을 승인하면 이후 실행에서 권한 요청 없이 진행됩니다
