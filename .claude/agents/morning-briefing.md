# 🌅 아침 브리핑 에이전트 (morning-briefing)

## Metadata

- **name**: morning-briefing
- **type**: coordinator-agent (팀 코디네이터)
- **version**: v2.0.0
- **description**: 팀 에이전트를 조정하여 AI 뉴스 수집 및 분석을 관리하는 코디네이터 에이전트
- **schedule**: `0 8 * * *` (매일 08:00 JST)
- **status**: Active
- **multiagent_enabled**: true (팀 멤버: news-fetcher-agent, issue-analyzer)

---

## 📋 개요

`morning-briefing`은 하네스의 **진입점(Entry Point)**입니다.

매일 정해진 시간(8시 JST)에 자동으로 실행되어, 하위 에이전트들을 순차적으로 호출하고 전체 워크플로우를 조정합니다.

**역할 (팀 코디네이터)**:
- **news-fetcher-agent**: 팀 멤버로 위임 (뉴스 수집)
- **issue-analyzer**: 팀 멤버로 위임 (이슈 분석)
- 각 팀 멤버의 작업 조정 및 모니터링
- 팀 멤버 간 데이터 공유 및 협력
- 최종 보고서 및 권장사항 생성

---

## 🔄 워크플로우

```
[정해진 시간 (8시 JST) 도달]
           ↓
┌─────────────────────────────────────────┐
│   morning-briefing 에이전트 자동 시작    │
└─────────────────────────────────────────┘
           ↓
┌──────────────────────┬──────────────────────┐
│                      │                      │
│   Step 1: 사전 준비   │   Step 1: 사전 준비   │
│  (실행 환경 검증)     │  (실행 환경 검증)     │
│                      │                      │
└──────────────────────┴──────────────────────┘
           ↓
┌──────────────────────┬──────────────────────┐
│                      │                      │
│  Step 2: news-       │  Step 2: issue-      │
│  fetcher-agent       │  analyzer 호출       │
│  호출 (뉴스 수집)     │  (이슈 분석)         │
│  ⏱️ ~5분              │  ⏱️ ~3분              │
│                      │                      │
└──────────────────────┴──────────────────────┘
           ↓
       [병렬 실행]
           ↓
┌─────────────────────────────────────────┐
│    Step 3: 결과 수집 및 검증              │
│  - 뉴스 HTML 파일 확인                    │
│  - 이슈 분석 결과 확인                    │
└─────────────────────────────────────────┘
           ↓
┌─────────────────────────────────────────┐
│    Step 4: 최종 보고서 생성               │
│  - 오늘의 요약 (news count, issues)       │
│  - 실행 성공 여부                         │
│  - 다음 실행 예정 시간                    │
└─────────────────────────────────────────┘
           ↓
┌─────────────────────────────────────────┐
│    Step 5: 자동 커밋 및 푸시               │
│  - Git add & commit                       │
│  - GitHub push                            │
└─────────────────────────────────────────┘
           ↓
        [완료] ✅
```

---

## 🤝 팀 협력 방식 (Team Coordination)

### Coordinator의 책임

```
1️⃣ 팀 멤버 역할 정의
   ├─ news-fetcher-agent: "최신 AI 뉴스 5-8개 수집해줄래?"
   └─ issue-analyzer: "수집된 뉴스와 관련해서 이슈 분석해줄래?"

2️⃣ 작업 지시 (Task Delegation)
   ├─ 명확한 지시: "한국어 뉴스만 수집" → news-fetcher-agent
   └─ 컨텍스트 제공: "뉴스 결과를 고려하면서" → issue-analyzer

3️⃣ 결과 수집 (Results Collection)
   ├─ news-fetcher-agent 결과: HTML 리포트 + 뉴스 요약
   └─ issue-analyzer 결과: 우선순위 보고서 + 분석

4️⃣ 데이터 통합 (Data Integration)
   ├─ "뉴스에서 언급된 주제와 이슈 연관성 분석"
   ├─ "팀 멤버들의 의견을 종합한 최종 권장사항 제시"
   └─ "내일 우선 처리할 항목 정리"

5️⃣ 최종 브리핑 (Final Briefing)
   └─ "이런 뉴스가 나왔고, 이런 이슈가 있습니다. 따라서..."
```

### 팀 멤버 간 의사소통

- **news-fetcher-agent → morning-briefing**: "수집 완료. 주요 주제는 AI 윤리, LLM 성능입니다."
- **morning-briefing → issue-analyzer**: "뉴스에서 본 주제: AI 윤리, LLM 성능. 이와 관련된 이슈 우선순위를 높여줄래?"
- **issue-analyzer → morning-briefing**: "분석 완료. 보안 관련 이슈 3개를 최우선으로 올렸습니다."

---

## 🎮 실행 방식

### 자동 실행 (권장)

```bash
# 매일 8시 JST에 자동으로 실행됨
# 별도의 수동 명령 불필요
```

### 수동 실행

```bash
# 필요시 언제든지 수동으로 실행 가능
claude /agents morning-briefing
```

---

## 👥 팀 구성 (Multiagent Configuration)

```yaml
multiagent:
  type: coordinator
  agents:
    - name: news-fetcher-agent
      role: "News Collection Specialist"
      description: "AI 뉴스 수집 및 한국어 리포트 생성"
      
    - name: issue-analyzer
      role: "Issue Analysis Specialist"
      description: "GitHub 이슈 분석 및 우선순위 결정"
      
    - name: morning-briefing (self)
      role: "Team Coordinator"
      description: "팀 멤버 조정, 데이터 통합, 최종 보고"
```

| # | 팀 멤버 | 역할 | 책임 | 예상 시간 |
|---|--------|------|------|---------|
| 1️⃣ | news-fetcher-agent | News Specialist | AI 뉴스 검색, 필터링, HTML 생성 | ~5분 |
| 2️⃣ | issue-analyzer | Analysis Specialist | GitHub 이슈 분석, 우선순위 평가 | ~3분 |
| 🎯 | morning-briefing | Coordinator | 팀 조정, 데이터 통합, 최종 브리핑 | ~2분 |

---

## ⚙️ 설정 파라미터

| 파라미터 | 기본값 | 설명 |
|---------|-------|------|
| `fetch_news` | `true` | 뉴스 수집 실행 여부 |
| `analyze_issues` | `true` | 이슈 분석 실행 여부 |
| `create_report` | `true` | 최종 보고서 생성 여부 |
| `auto_commit` | `true` | 결과 자동 커밋 여부 |
| `auto_push` | `true` | GitHub 자동 푸시 여부 |
| `max_retries` | `2` | 실패 시 재시도 횟수 |

---

## 📝 출력 결과

성공 시 다음 결과물을 생성합니다:

```
📁 생성되는 파일:
├── ai-news-digest-YYYY-MM-DD.html    ← 뉴스 HTML 리포트
├── .claude/logs/morning-briefing-YYYY-MM-DD.log  ← 실행 로그
└── (Git commit 자동 생성)

📊 로그에 기록되는 정보:
├── 시작 시간 및 종료 시간
├── 수집된 뉴스 개수
├── 분석된 이슈 개수
├── 발생한 오류 및 경고
└── 다음 실행 예정 시간
```

---

## ⚡ 예외 처리

| 상황 | 처리 방식 | 결과 |
|-----|---------|------|
| 뉴스 수집 실패 | 최대 2회 재시도 후 실패 로그 기록 | 이슈 분석만 진행 |
| 이슈 분석 실패 | 최대 2회 재시도 후 실패 로그 기록 | 뉴스 수집만 진행 |
| 네트워크 오류 | 자동 재시도 (지수 백오프) | 3회 실패 시 경고 알림 |
| 권한 부재 | 로그에 기록 후 스킵 | 다음 단계 계속 진행 |

---

## 🔗 의존성

### 필수 에이전트
- ✅ `news-fetcher-agent` (Step 4에서 생성)
- ✅ `issue-analyzer` (Step 5에서 생성)

### 필수 스킬
- ✅ `briefing-improver` (이미 완성됨)
- ✅ `issue-writer` (이미 완성됨)
- ✅ `issue-runner` (이미 완성됨)

### 필수 권한
- ✅ `python` (news_fetcher.py 실행)
- ✅ `bash` (스크립트 실행)
- ✅ `git` (커밋 및 푸시)
- ✅ `gh` (GitHub CLI)

---

## 💡 사용 예시

### 예시 1: 자동 실행 (기본 동작)

```
매일 08:00 JST
   ↓
morning-briefing 자동 시작
   ↓
뉴스 수집 + 이슈 분석 (병렬)
   ↓
결과 자동 커밋 및 푸시
   ↓
✅ 완료 (사람의 개입 0)
```

### 예시 2: 수동 실행 (즉시 필요한 경우)

```bash
# 언제든지 수동으로 실행 가능
claude /agents morning-briefing

# 특정 옵션으로 실행
claude /agents morning-briefing --fetch-news=true --analyze-issues=true
```

### 예시 3: 특정 단계만 실행

```bash
# 뉴스 수집만 실행
claude /agents morning-briefing --fetch-news=true --analyze-issues=false

# 이슈 분석만 실행
claude /agents morning-briefing --fetch-news=false --analyze-issues=true
```

---

## 📊 모니터링

### 로그 확인

```bash
# 오늘의 실행 로그 확인
cat .claude/logs/morning-briefing-2026-06-12.log

# 최근 10개 로그 확인
tail -n 10 .claude/logs/morning-briefing-*.log
```

### 실행 상태 확인

| 상태 | 의미 | 다음 액션 |
|-----|------|---------|
| ✅ Success | 정상 완료 | 결과 확인 |
| ⚠️ Warning | 부분 성공 (일부 단계 실패) | 로그 확인 및 재실행 |
| ❌ Failed | 완전 실패 | 오류 로그 분석 후 수동 개입 |

---

## 🚀 베스트 프래틱스

1. **정기적 모니터링**
   - 매일 한 번씩 로그 확인
   - 이슈 분석 결과 검토

2. **문제 발생 시 대응**
   - 로그에서 원인 파악
   - 필요시 즉시 수동 실행
   - GitHub 이슈에 기록

3. **설정 변경 시**
   - `settings.json`에서만 수정
   - 변경 후 재커밋
   - 다음 실행부터 적용됨

4. **버전 관리**
   - 변경사항 발생 시 버전 업그레이드
   - 커밋 메시지에 변경 내용 명시

---

## 📞 문제 해결

### Q: 8시에 실행되지 않음
**A**: `settings.json`에서 `agents.auto_run` 확인, schedule 시간대(JST) 확인

### Q: 뉴스는 수집되지만 이슈 분석 실패
**A**: GitHub 권한(`gh` permission) 확인, `issue-analyzer` 에이전트 존재 확인

### Q: 로그 파일이 너무 커짐
**A**: `.claude/logs/` 폴더에서 오래된 로그 정기적 삭제

### Q: 자동 커밋이 작동하지 않음
**A**: Git 권한(`git` permission) 확인, `git config user.name/email` 설정 확인

---

## 📌 버전 히스토리

| 버전 | 날짜 | 변경 사항 |
|-----|------|---------|
| v1.0.0 | 2026-06-12 | 초기 버전 작성 |

---

**마지막 업데이트**: 2026-06-12  
**관리자**: Claude Code
