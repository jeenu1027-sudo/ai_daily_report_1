# GitHub Issue Briefing Improver Skill

## Metadata
- **name**: briefing-improver
- **description**: GitHub 이슈를 생성하고 분석한 후 실제 코드 수정까지 완료하는 완전 자동화 워크플로우
- **version**: 1.0.0

## Summary

이 스킬은 GitHub 이슈 관리의 전체 라이프사이클을 자동화합니다. 사용자가 원하는 기능이나 버그를 설명하면, 이슈를 생성하고, 분석하고, 계획을 수립한 후, 실제로 코드를 수정하고 GitHub에 반영하는 모든 과정을 자동으로 처리합니다.

## Usage

사용자가 다음과 같은 요청을 할 때 이 스킬을 사용하세요:

- "새 기능을 추가하고 구현해줘"
- "버그를 찾고 수정해줘"
- "이슈를 등록하고 해결해줘"
- "문제를 설명하면 처리해줄래?"

## Parameters

### Required
- **action** (string): 실행 모드
  - `create-only`: 이슈 생성만 (issue-writer)
  - `analyze-only`: 이슈 분석만 (issue-runner analyze)
  - `plan-only`: 계획 수립만 (issue-runner plan)
  - `complete`: 전체 처리 (생성 → 분석 → 계획 → 구현)
  - `implement-only`: 코드 수정만 (issue-runner implement)

### Optional (이슈 생성 시)
- **title** (string): 이슈 제목
- **description** (string): 이슈 상세 설명
- **labels** (array): 라벨 (bug, enhancement, feature, documentation)
- **issue_number** (integer): 기존 이슈 번호 (생성 생략)

### Optional (코드 수정 시)
- **create_pr** (boolean): Pull Request 자동 생성 여부 (기본값: false)
- **branch_name** (string): 커밋 브랜치명 (기본값: feature/issue-N)

## Workflow

### 1️⃣ 이슈 생성 (Issue-Writer)
```
사용자 요청
   ↓
제목/설명 검증
   ↓
GitHub에 이슈 생성
   ↓
이슈 URL 반환
```

### 2️⃣ 이슈 분석 (Issue-Runner Analyze)
```
이슈 상세 조회
   ↓
요구사항 파악
   ↓
영향 범위 식별
   ↓
분석 결과 요약
```

### 3️⃣ 계획 수립 (Issue-Runner Plan)
```
문제 정의
   ↓
근본 원인 분석
   ↓
해결 방법 도출
   ↓
영향받는 파일 식별
   ↓
구현 계획서 작성
```

### 4️⃣ 코드 구현 (Issue-Runner Implement)
```
필요 파일 수정
   ↓
코드 작성/변경
   ↓
테스트 실행
   ↓
문서 업데이트
   ↓
커밋 및 푸시
   ↓
(선택) PR 생성
```

## Step-by-Step Instructions

### 신규 기능/버그 보고 (complete 모드)

```
1️⃣  사용자: "새 기능을 추가하고 구현해줘"
     └─ 제목과 설명 제공

2️⃣  스킬: issue-writer 실행
     └─ GitHub에 이슈 생성
     └─ 이슈 번호 획득 (예: #5)

3️⃣  스킬: issue-runner analyze 실행
     └─ Issue #5 상세 분석
     └─ 요구사항 파악

4️⃣  스킬: issue-runner plan 실행
     └─ 상세한 구현 계획 수립
     └─ 영향 범위 및 일정 예측

5️⃣  스킬: issue-runner implement 실행
     └─ 코드 수정
     └─ 테스트 및 검증
     └─ 문서 업데이트
     └─ 커밋 및 푸시

6️⃣  결과: 
     └─ GitHub 이슈 CLOSED
     └─ 코드 변경 반영
     └─ (선택) PR 생성
```

## Examples

### 예시 1: 전체 프로세스 (생성 → 구현)

**사용자**:
```
"이메일 알림 기능을 추가해줘. 
매일 뉴스를 이메일로 발송하는 기능이 필요해."
```

**스킬 실행**:
```
1. issue-writer
   → Issue #5 생성: "Add email notification feature"

2. issue-runner analyze
   → 이슈 분석: 이메일 발송, SMTP 연동 필요

3. issue-runner plan
   → 계획 수립: news_mailer.py 생성, 스케줄 통합

4. issue-runner implement
   → 코드 구현
   → news_mailer.py 작성
   → setup_schedule.ps1 수정
   → README 업데이트
   → 커밋: Fix #5: Add email notification feature

5. 결과
   → Issue #5 CLOSED
   → Pull Request 자동 생성
```

**시간 소요**: ~1시간

---

### 예시 2: 분석만 수행

**사용자**:
```
"등록된 모든 버그를 확인해줘. 
어떤 것부터 처리해야 할지 알고 싶어."
```

**스킬 실행**:
```
action=analyze-only
```

**결과**:
```
🔍 버그 분석 결과:

🔴 긴급 (즉시 수정):
   - Issue #2: RSS 피드 파싱 오류
   - 영향: 뉴스 수집 불가
   - 예상 시간: 30분

🟠 높음 (이번 주):
   - Issue #6: 시간대 설정 오류
   - 영향: 스케줄 정확성
   - 예상 시간: 1시간

🟡 중간 (다음 주):
   - Issue #8: 문서 개선
   - 영향: 사용자 경험
   - 예상 시간: 2시간
```

---

### 예시 3: 기존 이슈 처리

**사용자**:
```
"Issue #4를 분석하고 해결해줘"
```

**스킬 실행**:
```
action=complete
issue_number=4
```

**결과**:
```
분석 → 계획 → 구현 → PR 생성
```

---

## 스킬 선택 가이드

### 어떤 액션을 선택할까?

| 상황 | 액션 | 이유 |
|------|------|------|
| 새 기능 제안 | `create-only` | 먼저 팀과 검토 후 진행 |
| 버그 분류 | `analyze-only` | 우선순위 결정 후 처리 |
| 작은 버그 수정 | `complete` | 빠른 해결 |
| 복잡한 기능 | `plan-only` | 먼저 계획 검토 후 구현 |
| 기존 이슈 처리 | `complete` | 전체 자동 처리 |

---

## 의사결정 기준

### 이슈 생성 여부
```
✅ 생성한다:
   - 새로운 요청/문제를 발견했을 때
   - 향후 참조가 필요할 때
   - 팀과 논의가 필요할 때

❌ 생성하지 않는다:
   - 즉시 해결 가능한 경우
   - 중복 이슈가 있을 때
   - 범위가 너무 클 때 (먼저 분류)
```

### 구현 실행 여부
```
✅ 즉시 구현:
   - 버그 (서비스 장애)
   - 작은 개선사항
   - 명확한 요구사항

❌ 검토 후 구현:
   - 복잡한 기능
   - 아키텍처 변경
   - 외부 API 연동
```

---

## 생성된 산출물

### 이슈 생성 후
- ✅ GitHub 이슈 (타입, 설명, 라벨 포함)
- ✅ 이슈 URL 및 번호
- ✅ 초기 분석 결과

### 분석 완료 후
- ✅ 상세 분석 보고서
- ✅ 우선순위 평가
- ✅ 예상 작업 시간

### 계획 수립 후
- ✅ 상세 구현 계획서
- ✅ 영향 범위 및 위험 평가
- ✅ 리소스 예측

### 구현 완료 후
- ✅ 수정된 코드
- ✅ 업데이트된 문서
- ✅ 테스트 결과
- ✅ Git 커밋
- ✅ Pull Request (선택사항)
- ✅ 이슈 CLOSED

---

## Error Handling

| 오류 | 해결 방법 |
|------|---------|
| 이슈 없음 | `gh issue list`로 먼저 확인 |
| 권한 오류 | GitHub 계정 권한 확인 |
| 파일 충돌 | `git pull origin main` 후 재시도 |
| 커밋 실패 | 변경사항 확인 및 스테이징 |
| PR 생성 실패 | 브랜치명 및 권한 확인 |

## Best Practices

### 1️⃣ 이슈 작성
```
✅ 좋은 이슈:
- 명확한 제목
- 상세한 설명
- 기대 결과 명시
- 재현 방법 포함

❌ 나쁜 이슈:
- "버그 있음"
- 설명 없음
- 모호한 요구사항
```

### 2️⃣ 액션 선택
```
순차 실행 (권장):
create → analyze → plan → 검토 → implement

병렬 실행 (가능):
여러 이슈를 각각 complete로 처리
```

### 3️⃣ 코드 구현
```
✅ 하기:
- 테스트 자동 실행
- 문서 함께 수정
- 명확한 커밋 메시지
- 작은 단위 커밋

❌ 하지 않기:
- 검증 없이 푸시
- 문서 미업데이트
- 큰 덩어리 커밋
- 자동 머지
```

## Workflow Tips

### Tip 1: 우선순위 정렬
버그 → 기능 → 문서 순으로 처리

### Tip 2: 의존성 확인
다른 이슈에 의존하는지 먼저 확인

### Tip 3: 테스트 커버리지
변경 후 관련된 모든 기능 테스트

### Tip 4: 코드 리뷰
자신의 코드를 다시 한 번 검토

## Links

- 📖 [GitHub CLI 이슈 명령어](https://cli.github.com/manual/gh_issue)
- 🔗 [GitHub 이슈 API](https://docs.github.com/en/rest/issues)
- 📝 [Git 커밋 가이드](https://git-scm.com/book/en/v2/Git-Basics-Recording-Changes-to-the-Repository)
- 🐛 [현재 등록된 이슈들](https://github.com/jeenu1027-sudo/ai_daily_report_1/issues)

## Changelog

### v1.0.0 (2026-06-12)
- 초기 스킬 작성
- issue-writer + issue-runner 통합
- 4가지 주요 액션 모드 지원
- 상세한 예시 및 가이드 제공
- 의사결정 기준 및 best practices 포함

---

**마지막 업데이트**: 2026-06-12  
**유지관리자**: Claude Code

> 💡 **팁**: 복잡한 작업은 `plan-only`로 계획을 먼저 검토하고, 확인 후 `implement-only`로 진행하는 것이 안전합니다!
