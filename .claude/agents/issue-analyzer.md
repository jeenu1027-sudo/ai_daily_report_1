# 🔍 이슈 분석 에이전트 (issue-analyzer)

## Metadata

- **name**: issue-analyzer
- **type**: task-agent (작업 에이전트)
- **version**: v1.0.0
- **description**: GitHub 이슈를 자동으로 분석하고 우선순위 결정
- **called_by**: morning-briefing (마스터 에이전트)
- **status**: Active

---

## 📋 개요

`issue-analyzer`는 **GitHub 이슈 분석 전담 에이전트**입니다.

morning-briefing에 의해 호출되어 다음 작업을 수행합니다:
1. 레포지토리의 모든 열린 이슈(Open) 조회
2. 각 이슈를 자동으로 분석 및 분류
3. 우선순위 및 영향도 평가
4. 분석 결과를 이슈 코멘트로 자동 추가
5. 우선순위 보고서 생성

**핵심 역할**:
- 이슈 자동 분류 (버그, 기능, 문서 등)
- 우선순위 결정 (높음, 중간, 낮음)
- 영향 범위 분석
- 해결 난이도 추정
- 팀의 의사결정 지원

---

## ⚙️ 기술 구성

```
issue-analyzer 호출
       ↓
  [GitHub 연결 확인]
  - GitHub CLI (gh) 설치 여부
  - 저장소 접근 권한
  - 인증 토큰 유효성
       ↓
  [이슈 목록 조회]
  - gh issue list --state=open
  - JSON 형식으로 파싱
  - 메타데이터 추출
       ↓
  [이슈 분석]
  - 제목 및 설명 분석
  - 라벨 확인
  - 담당자 확인
  - 댓글 수 카운팅
       ↓
  [분류 및 우선순위 결정]
  - 카테고리 자동 분류
  - 영향도 점수 계산
  - 난이도 추정
  - 우선순위 결정
       ↓
  [결과 반영]
  - 이슈에 자동 코멘트 추가
  - 라벨 제안 (선택)
  - 우선순위 보고서 생성
       ↓
  [보고]
  - 분석된 이슈 개수
  - 우선순위별 분포
  - 권장 조치 사항
```

---

## 🔄 실행 흐름

### Step 1: GitHub 연결 확인 (5초)

```bash
✓ GitHub CLI (gh) 설치 확인
✓ 저장소 접근 권한 확인
✓ 인증 토큰 유효성 검증
✓ 레포지토리: jeenu1027-sudo/ai_daily_report_1
```

### Step 2: 이슈 목록 조회 (10초)

```bash
$ gh issue list --state=open --json title,number,labels,comments

예시:
#5  | Test: briefing-improver 통합 스킬 검증
#7  | docs: Update documentation
#8  | enhancement: Add new feature
...
```

### Step 3: 이슈별 분석 (이슈당 3~5초)

각 이슈마다 다음을 분석합니다:

```
이슈 제목 분석
├─ 키워드 추출 (bug, feature, docs, etc.)
├─ 긴급도 감지 (critical, urgent 등)
└─ 범위 파악 (scope 추정)

이슈 설명 분석
├─ 문제 설명 상세도
├─ 재현 방법 명확성
├─ 기대 결과 정의
└─ 실제 결과 설명

메타데이터 분석
├─ 라벨 개수 및 종류
├─ 댓글 수 (활발도)
├─ 담당자 지정 여부
└─ 마일스톤 포함 여부
```

### Step 4: 분류 및 우선순위 결정 (2초 per issue)

```
분류 체계
├─ 🐛 Bug (버그)
│  └─ 기존 기능 오류
├─ ✨ Enhancement (기능)
│  └─ 새로운 기능 요청
├─ 📚 Documentation (문서)
│  └─ 문서 추가/수정
├─ ♻️ Refactor (리팩토링)
│  └─ 코드 최적화
└─ 🔧 Chore (기타)
   └─ 설정, 도구 등

우선순위 결정 알고리즘
┌─────────────────────────────┐
│ 점수 = (영향도 × 0.5) +     │
│        (긴급도 × 0.3) +     │
│        (난이도 × -0.2)      │
│                             │
│ 점수 > 7.5  → 높음 (High)   │
│ 3.0~7.5     → 중간 (Medium) │
│ < 3.0       → 낮음 (Low)    │
└─────────────────────────────┘

영향도 (Impact Score)
├─ 크리티컬 (영향도 10): 서비스 중단
├─ 높음 (영향도 7~9): 주요 기능 오류
├─ 중간 (영향도 4~6): 제한된 기능 오류
└─ 낮음 (영향도 1~3): 미미한 영향

긴급도 (Urgency Score)
├─ 매우 높음 (긴급도 10): 즉시 처리 필요
├─ 높음 (긴급도 7~9): 이번 스프린트 내 처리
├─ 중간 (긴급도 4~6): 다음 스프린트 고려
└─ 낮음 (긴급도 1~3): 향후 처리 가능

난이도 (Complexity Score)
├─ 매우 어려움 (난이도 9~10): 3일 이상
├─ 어려움 (난이도 6~8): 1~3일
├─ 중간 (난이도 3~5): 4시간~1일
└─ 쉬움 (난이도 1~2): 1시간 이내
```

### Step 5: 결과 반영 (이슈당 2초)

생성되는 자동 코멘트:

```markdown
## 🤖 자동 분석 결과

### 분류
🐛 **Category**: Bug (버그)

### 우선순위
🔴 **Priority**: High (높음)

### 세부 분석
- **영향도**: 7/10 (주요 기능 영향)
- **긴급도**: 8/10 (빠른 처리 필요)
- **난이도**: 4/10 (중간 수준 작업)

### 권장 조치
1. 이번 스프린트 내 처리 권장
2. 담당자 지정 필요
3. 재현 방법 상세 제공 필요

### 관련 이슈
- Issue #5 (Related)
- Issue #7 (Related)

---
*이 분석은 자동으로 생성되었습니다. AI 분석이므로 수동 검토를 권장합니다.*
```

---

## 📊 입력값 (Inputs)

| 파라미터 | 기본값 | 설명 |
|---------|-------|------|
| `repo` | `jeenu1027-sudo/ai_daily_report_1` | 분석할 GitHub 저장소 |
| `state` | `open` | 조회할 이슈 상태 (open, closed, all) |
| `labels` | `none` | 특정 라벨 필터 (선택) |
| `assignee` | `none` | 담당자 필터 (선택) |
| `add_comment` | `true` | 분석 결과 자동 코멘트 추가 |
| `update_labels` | `true` | 라벨 자동 추가 (선택) |

---

## 📁 출력값 (Outputs)

### 성공 시

```
✅ 생성 파일
├─ .claude/logs/issue-analyzer-YYYY-MM-DD.log (실행 로그)
└─ issue-priority-report-YYYY-MM-DD.md (우선순위 보고서)

📊 반환되는 메타데이터
{
  "status": "success",
  "total_issues": 5,
  "analyzed_issues": 5,
  "priority_distribution": {
    "high": 2,
    "medium": 2,
    "low": 1
  },
  "categories": {
    "bug": 2,
    "enhancement": 2,
    "documentation": 1
  },
  "comments_added": 5,
  "execution_time": "23.4s"
}
```

### 우선순위 보고서 예시

```markdown
# 📊 GitHub 이슈 우선순위 보고서

**생성 날짜**: 2026-06-12  
**분석된 이슈**: 5개

## 🔴 높은 우선순위 (2개)

1. **#5**: briefing-improver 통합 스킬 검증
   - 카테고리: 기능
   - 영향도: 7/10
   - 난이도: 4/10
   - 권장: 이번 스프린트 처리

2. **#7**: Update documentation  
   - 카테고리: 문서
   - 영향도: 6/10
   - 난이도: 2/10
   - 권장: 우선 처리

## 🟡 중간 우선순위 (2개)

3. **#8**: enhancement: Add new feature
   - 카테고리: 기능
   - 영향도: 5/10
   - 난이도: 6/10

... (생략)
```

---

## 🔧 실행 명령

### morning-briefing에서 호출 (자동)

```bash
# morning-briefing이 자동으로 호출
# 별도의 수동 명령 불필요
```

### 수동 실행

```bash
# 표준 실행
claude /agents issue-analyzer

# 특정 라벨만 분석
claude /agents issue-analyzer --labels=bug,enhancement

# 코멘트 추가 없이 분석만
claude /agents issue-analyzer --add-comment=false

# 라벨도 자동 추가
claude /agents issue-analyzer --update-labels=true
```

---

## 🔍 분석 기준

### 버그(Bug) 탐지 규칙

```
제목에 포함된 키워드
├─ "bug", "error", "broken"
├─ "doesn't work", "fail"
└─ "issue", "problem"

설명에서 감지
├─ "재현 방법", "예상 결과"
├─ "실제 결과", "오류 메시지"
└─ 스택트레이스 포함 여부
```

### 기능(Enhancement) 탐지 규칙

```
제목에 포함된 키워드
├─ "feature", "add", "support"
├─ "enhancement", "improvement"
└─ "request", "want"

설명에서 감지
├─ "사용 시나리오", "이점"
├─ "구현 방법 제안"
└─ 유사 기능 참고 링크
```

### 문서(Documentation) 탐지 규칙

```
제목에 포함된 키워드
├─ "doc", "document", "readme"
├─ "guide", "tutorial"
└─ "clarify", "explain"

설명에서 감지
├─ "추가할 섹션", "개선할 부분"
├─ "현재 부족한 정보"
└─ 외부 문서 참고 링크
```

---

## ⚡ 예외 처리

| 상황 | 감지 | 대응 |
|-----|------|------|
| GitHub 연결 실패 | 네트워크 오류 | 3회 재시도 후 실패 반환 |
| 권한 부족 | 401/403 에러 | 권한 안내 후 스킵 |
| 이슈 없음 | 0개 조회 | 정상 완료 (분석 대상 없음) |
| 코멘트 추가 실패 | 쓰기 권한 부족 | 로그 기록 후 계속 진행 |
| 분석 타임아웃 | 이슈 분석 초과 | 부분 분석 결과 반환 |

---

## 📝 로그 포맷

```
[2026-06-12 08:05:35] INFO    issue-analyzer started
[2026-06-12 08:05:35] INFO    Connecting to GitHub repo: jeenu1027-sudo/ai_daily_report_1
[2026-06-12 08:05:37] INFO    GitHub connection established
[2026-06-12 08:05:37] INFO    Fetching open issues...
[2026-06-12 08:05:39] INFO    Found 5 open issues
[2026-06-12 08:05:40] INFO    Analyzing issue #5 (briefing-improver integration test)
[2026-06-12 08:05:42] INFO    Category: feature | Priority: HIGH
[2026-06-12 08:05:42] INFO    ✓ Comment added to issue #5
[2026-06-12 08:05:43] INFO    Analyzing issue #7 (docs: Update)
[2026-06-12 08:05:44] INFO    Category: documentation | Priority: MEDIUM
[2026-06-12 08:05:44] INFO    ✓ Comment added to issue #7
[2026-06-12 08:05:44] INFO    Analyzing issue #8 (enhancement)
[2026-06-12 08:05:46] INFO    Category: enhancement | Priority: MEDIUM
[2026-06-12 08:05:46] INFO    ✓ Comment added to issue #8
[2026-06-12 08:05:47] INFO    Analysis complete: 5 issues analyzed
[2026-06-12 08:05:47] INFO    Priority distribution: HIGH(2), MEDIUM(2), LOW(1)
[2026-06-12 08:05:48] INFO    Generating priority report...
[2026-06-12 08:05:48] INFO    ✓ Report saved: issue-priority-report-2026-06-12.md
[2026-06-12 08:05:48] INFO    issue-analyzer completed successfully
[2026-06-12 08:05:48] INFO    Execution time: 13.2s
```

---

## 🔗 의존성

### 필수 도구
- ✅ GitHub CLI (gh) - 설치 필수
- ✅ Git - 저장소 접근

### 필수 권한
- ✅ `gh` (GitHub CLI)
- ✅ `bash` (셸 명령)
- ✅ GitHub 저장소 접근 권한

### 필수 설정
- ✅ GitHub 인증 (`gh auth login`)
- ✅ 저장소 클론 또는 원격 접근

---

## 💡 성능 최적화

### 캐싱 (향후)
```bash
# 최근 분석 결과 캐싱
# 동일 이슈 중복 분석 방지
```

### 병렬 처리 (향후)
```python
# 여러 이슈 동시 분석
# 실행 시간 60% 단축 예상
```

### 머신러닝 모델 (향후)
```bash
# 과거 이슈 분석 데이터 학습
# 우선순위 예측 정확도 향상
```

---

## 🚀 사용 예시

### 예시 1: 자동 실행 (기본)

```
[8:05 AM JST] morning-briefing의 두 번째 단계
   ↓
issue-analyzer 자동 호출
   ↓
GitHub에서 열린 이슈 5개 조회
   ↓
각 이슈 자동 분석 (버그, 기능, 문서 등)
   ↓
우선순위 결정 및 분석 결과 코멘트 추가 ✅
   ↓
우선순위 보고서 생성 (issue-priority-report-YYYY-MM-DD.md)
   ↓
morning-briefing에 결과 반환
```

### 예시 2: 수동 실행 (즉시 필요)

```bash
$ claude /agents issue-analyzer

🔗 Connecting to GitHub...
✓ Repository: jeenu1027-sudo/ai_daily_report_1
📋 Found 5 open issues
🔍 Analyzing issues...
  ✓ #5 (Bug) → Priority: HIGH
  ✓ #7 (Docs) → Priority: MEDIUM
  ✓ #8 (Enhancement) → Priority: MEDIUM
  ✓ #9 (Bug) → Priority: HIGH
  ✓ #10 (Chore) → Priority: LOW
💬 Comments added: 5
📊 Priority distribution: HIGH(2) MEDIUM(2) LOW(1)
📄 Report: issue-priority-report-2026-06-12.md
⏱️ Execution time: 13.2s
```

### 예시 3: 특정 라벨만 분석

```bash
$ claude /agents issue-analyzer --labels=bug,critical

🔍 Filtering for labels: bug, critical
📋 Found 3 matching issues
  ✓ #5 (Bug - Critical)
  ✓ #9 (Bug)
  ✓ #11 (Bug - Critical)
💬 Comments added: 3
⏱️ Execution time: 8.4s
```

---

## 📊 예상 성능

| 항목 | 값 |
|-----|-----|
| 평균 실행 시간 (5개 이슈) | 13~20초 |
| 이슈당 분석 시간 | 2~4초 |
| 네트워크 요청 수 | 1~10개 |
| 코멘트 생성 시간 | 1초/개 |

---

## 📞 문제 해결

### Q: "GitHub 연결 실패" 오류
**A**: `gh auth login` 실행하여 GitHub 인증, 저장소 URL 확인

### Q: 코멘트가 추가되지 않음
**A**: GitHub 권한 확인, 저장소 쓰기 권한 확인, 토큰 유효성 확인

### Q: 분석이 너무 오래 걸림
**A**: 이슈 개수 많음 (100개 이상), --add-comment=false로 성능 개선

### Q: 라벨 추가가 작동하지 않음
**A**: --update-labels=true 옵션 사용, 라벨이 미리 생성되어 있는지 확인

---

## 📌 버전 히스토리

| 버전 | 날짜 | 변경 사항 |
|-----|------|---------|
| v1.0.0 | 2026-06-12 | 초기 버전 작성 |

---

**마지막 업데이트**: 2026-06-12  
**관리자**: Claude Code
