# 🤝 팀 에이전트 구성 가이드

## 개요

당신의 프로젝트가 **팀 에이전트 구성(Multi-Agent Team Setup)**으로 업그레이드되었습니다!

### 이전 vs 이후

#### 이전 구조 (순차 호출)
```
morning-briefing (마스터)
    ↓ 호출만 함
    ├─ news-fetcher-agent
    └─ issue-analyzer
```

#### 이후 구조 (팀 협력)
```
morning-briefing (코디네이터/coordinator)
    ↓ 지시 및 조정
    ├─ news-fetcher-agent (팀 멤버)
    │   └─ "뉴스 수집하고 결과 알려줄래?"
    └─ issue-analyzer (팀 멤버)
        └─ "뉴스 주제를 고려해서 이슈 분석해줄래?"
```

---

## 📋 변경사항

### 1️⃣ morning-briefing.md
- **type**: `master-agent` → `coordinator-agent`
- **version**: v1.0.0 → v2.0.0
- **새로운 섹션**: 🤝 팀 협력 방식 추가
- **multiagent**: true로 설정

### 2️⃣ news-fetcher-agent.md
- **type**: `task-agent` → `team-member (News Specialist)`
- **version**: v1.0.0 → v2.0.0
- **coordinator**: morning-briefing으로 지정

### 3️⃣ issue-analyzer.md
- **type**: `task-agent` → `team-member (Analysis Specialist)`
- **version**: v1.0.0 → v2.0.0
- **coordinator**: morning-briefing으로 지정

### 4️⃣ settings.json
```json
"multiagent": {
  "enabled": true,
  "coordinator": "morning-briefing",
  "team_members": [...]
}
```

---

## 🎯 팀 협력 흐름

### Step 1: 코디네이터 초기화
```
morning-briefing이 아침 8시에 깨어남
↓
"오늘 뭐 해야 하지?"
```

### Step 2: 팀 멤버에게 지시
```
morning-briefing → news-fetcher-agent
"최신 AI 뉴스 5-8개 수집해줄래?"
↓
news-fetcher-agent가 작업 수행
↓
news-fetcher-agent → morning-briefing
"수집 완료! 주요 주제는 AI 윤리, LLM 성능입니다."
```

### Step 3: 컨텍스트 공유
```
morning-briefing → issue-analyzer
"뉴스에서 본 주제: AI 윤리, LLM 성능
이와 관련된 이슈를 우선순위 높게 분석해줄래?"
↓
issue-analyzer가 작업 수행
```

### Step 4: 결과 통합
```
morning-briefing이 모든 결과 수집
↓
최종 브리핑 작성:
"이런 뉴스가 나왔고, 이런 이슈가 우선순위입니다.
따라서 이렇게 행동해야 합니다."
```

---

## 💡 팀 에이전트의 장점

| 특징 | 이전 | 이후 |
|------|------|------|
| 에이전트 간 통신 | ❌ 없음 | ✅ 있음 |
| 컨텍스트 공유 | ❌ 없음 | ✅ 자동 |
| 협력 방식 | 순차 호출 | 지시 + 피드백 |
| 확장성 | 낮음 | 높음 |
| 팀원 추가 | 어려움 | 간단함 |

---

## 🧪 테스트 방법

### 1. 테스트 스크립트 실행
```bash
# 환경 ID 설정 (실제 Managed Agents 환경)
export ANTHROPIC_ENVIRONMENT_ID="env_..."

# 테스트 실행
python test_multiagent_team.py
```

### 2. 기대 결과
```
🚀 팀 에이전트 협력 세션 시작...
✅ 세션 생성됨: sesn_...
📊 팀 협력 진행 중...

morning-briefing: "news-fetcher-agent에게 뉴스 수집 지시..."
news-fetcher-agent: "최신 AI 뉴스 수집 중..."
news-fetcher-agent: "수집 완료!"

morning-briefing: "issue-analyzer에게 분석 지시..."
issue-analyzer: "관련 이슈 분석 중..."
issue-analyzer: "분석 완료!"

morning-briefing: "최종 브리핑..."
✅ 팀 작업 완료!
```

---

## 🎓 핵심 개념

### Coordinator (코디네이터)
- **역할**: 팀 멤버들을 조정, 지시, 결과 통합
- **누가**: morning-briefing
- **책임**:
  - 팀 멤버에게 명확한 지시 전달
  - 작업 결과 수집
  - 최종 의사결정

### Team Member (팀 멤버)
- **역할**: 각 분야 전담, 코디네이터의 지시 따르기
- **누가**: news-fetcher-agent, issue-analyzer
- **책임**:
  - 전문 분야 작업 수행
  - 결과를 코디네이터에게 명확하게 보고
  - 코디네이터의 추가 지시에 반응

### Context Sharing (컨텍스트 공유)
- 한 팀 멤버의 결과가 다른 팀 멤버의 입력이 됨
- 예: news-fetcher-agent 결과 → issue-analyzer의 분석 기준

---

## 🚀 다음 단계 (선택사항)

### 팀 확장
새로운 팀 멤버 추가:
```python
# 예: sentiment-analyzer (감정 분석 에이전트)
multiagent={
    "type": "coordinator",
    "agents": [
        news_fetcher.id,
        issue_analyzer.id,
        sentiment_analyzer.id,  # 새로운 멤버
        {"type": "self"}
    ]
}
```

### 팀 멤버 간 직접 통신
```
현재: coordinator ↔ team_members
미래: coordinator ↔ team_members, 
      team_members ↔ team_members
```

### 다중 코디네이터
```
여러 coordinator가 다른 팀 관리
예: morning-briefing (뉴스/이슈 팀),
    evening-briefing (보안/성능 팀)
```

---

## ✅ 체크리스트

팀 에이전트 구성 완료 확인:

- [x] morning-briefing을 coordinator로 전환
- [x] news-fetcher-agent를 team member로 지정
- [x] issue-analyzer를 team member로 지정
- [x] settings.json에 multiagent 설정 추가
- [x] 팀 협력 가이드 작성 (이 문서)
- [x] 테스트 스크립트 작성 (test_multiagent_team.py)
- [ ] 실제 Managed Agents 환경에서 테스트
- [ ] 운영 환경 배포

---

## 📚 참고 자료

- Managed Agents 공식 문서: `shared/managed-agents-multiagent.md`
- 팀 협력 패턴: `shared/managed-agents-core.md`
- 다중 에이전트 설계: `shared/agent-design.md`

---

**작성일**: 2026-06-12  
**버전**: 2.0.0 (Team Agents)
