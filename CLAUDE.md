# Claude Code Configuration

Claude Code 설정 및 커스텀 스킬 정의

**관련 문서**: [프로젝트 개요](README.md) • [설계 철학](SOUL.md)

## ⚙️ Claude Code 설정

### 권장 settings.json

프로젝트별 Claude Code 설정을 자동화할 수 있습니다:

```json
{
  "model": "claude-opus-4-8",
  "permissions": {
    "gh": "allow",
    "bash": "allow",
    "python": "allow"
  }
}
```

## 📚 사용 가능한 스킬

### Harness 아키텍처 - 팀 에이전트 스킬

#### 4️⃣ `news-filtering` - AI 뉴스 필터링

최신 AI 뉴스를 **6가지 엄격한 필터링 규칙**에 따라 검증하고 품질 평가합니다.

**필터링 규칙**:
- 한국어 뉴스만 선별
- AI 생성 콘텐츠 제외
- GitHub 자료 제외
- 국내 대형 포털 제외
- 학술 논문 제외
- 웹 출처 제한 (최대 10개)

**품질 점수**: 기사를 0-100으로 평가 (신뢰도, 시간성, 기술 정확도 고려)

자세한 정보: [news-filtering.md](./.claude/skills/news-filtering.md)

---

#### 5️⃣ `issue-priority` - GitHub 이슈 우선순위 평가

GitHub 이슈를 점수 기반 알고리즘으로 평가하여 우선순위를 자동 결정합니다.

**점수 계산식**:
```
점수 = (영향도 × 0.5) + (긴급성 × 0.3) - (복잡도 × 0.2) + (뉴스 관련성 × 0.1)
```

**4개 평가 항목**:
- 영향도 (Impact): 50% 가중치
- 긴급성 (Urgency): 30% 가중치
- 복잡도 (Complexity): 감점 20%
- 뉴스 관련성 (News Relevance): 보너스 10%

자세한 정보: [issue-priority.md](./.claude/skills/issue-priority.md)

---

#### 6️⃣ `report-generator` - 아침 브리핑 리포트 생성

**뉴스** + **이슈 분석** 결과를 통합하여 시각화된 **HTML 리포트**를 생성합니다.

**리포트 구성**:
1. Executive Summary (요약)
2. News Deep Dive (뉴스 상세)
3. Issue Analysis (이슈 분석)
4. Recommendations (권장사항)

**특징**:
- 한국어 완전 지원
- CSS3 Glassmorphism 디자인
- 모바일 반응형
- 다크모드 지원
- 인쇄 최적화

**출력**: `ai-news-digest-YYYY-MM-DD.html`

자세한 정보: [report-generator.md](./.claude/skills/report-generator.md)

---

#### 7️⃣ `quality-rubric` - 프로젝트 품질 평가

프로젝트의 **견고성과 신뢰성**을 객관적으로 평가하는 종합 루브릭입니다.

**평가 항목** (5가지 × 각 20% 가중치):
1. **필터링 정확도** - 필터링 규칙 준수율, 효과 측정
2. **리포트 품질** - HTML 렌더링, 한글 지원, 반응형
3. **자동화 신뢰성** - 실행 성공률, 재시도 로직, 로깅
4. **코드 품질** - 타입힌팅, 테스트 커버리지, 에러 처리
5. **문서화** - README, API 문서, Docstring

**등급 판정**:
- 🟢 Excellent (85-100): 프로덕션 준비 완료
- 🟢 Good (75-84): 주요 기능 양호
- 🟡 Acceptable (60-74): 기본 작동
- 🟠 Needs Work (40-59): 즉시 개선 필요
- 🔴 Broken (<40): 심각한 결함

**사용 예**:
```
사용자: "프로젝트 품질을 평가해줘"
Claude: quality-rubric 평가 실행
  - 각 항목별 점수 계산
  - 종합 등급 산출
  - 개선 영역 도출
```

**현재 상태**: 🟢 Excellent (86/100)
- 필터링 정확도: 82/100 (🟢 Good)
- 리포트 품질: 90/100 (🟢 Excellent)
- 자동화 신뢰성: 87/100 (🟢 Excellent)
- 코드 품질: 85/100 (🟢 Good)
- 문서화: 88/100 (🟢 Good)

자세한 정보: [quality-rubric.md](./.claude/skills/quality-rubric.md)

---

### Legacy 스킬

#### 1. `briefing-improver` - 통합 이슈 관리 워크플로우 ⭐ 추천

GitHub 이슈의 생성부터 구현까지 전체 라이프사이클을 자동화합니다.

**사용 예**:
```
사용자: "새 기능을 추가하고 완전히 구현해줘"
Claude: briefing-improver (action=complete) 실행
  1. 이슈 생성
  2. 분석
  3. 계획 수립
  4. 코드 구현
  5. PR 생성
```

**5가지 모드**:
- `create-only`: 이슈 생성만
- `analyze-only`: 분석만
- `plan-only`: 계획 수립만
- `implement-only`: 코드 수정만
- `complete`: 전체 처리 (완전 자동)

자세한 정보: [briefing-improver.md](./.claude/skills/briefing-improver.md)

---

#### 2. `issue-writer` - GitHub 이슈 생성

이슈만 빠르게 생성합니다.

**사용 예**:
```
사용자: "버그 리포트를 이슈로 등록해줘"
Claude: issue-writer 스킬 실행 → GitHub 이슈 생성
```

자세한 정보: [issue-writer.md](./.claude/skills/issue-writer.md)

---

#### 3. `issue-runner` - GitHub 이슈 분석 및 수정

이슈를 분석하고 코드를 수정합니다.

**Workflow**:
```
분석 → 계획 → 구현 → 테스트 → 커밋 → PR
```

자세한 정보: [issue-runner.md](./.claude/skills/issue-runner.md)

---

## 🛠️ 스킬 개발 가이드

### 새 스킬 추가

1. `.claude/skills/skill_name.md` 파일 생성
2. 메타데이터, 설명, 사용 예시 작성
3. 이 파일(CLAUDE.md)에 스킬 추가

### 스킬 포맷

```markdown
# Skill Name

## Metadata
- **name**: skill_name
- **description**: 설명

## Summary
간단한 설명

## Parameters
파라미터 정의

## Examples
사용 예시
```

---

**마지막 업데이트**: 2026-06-12  
**관리자**: Claude Code
