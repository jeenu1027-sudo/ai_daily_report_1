# GitHub Issue Runner Skill

## Metadata
- **name**: issue-runner
- **description**: 등록된 GitHub 이슈를 확인하고, 수정 계획을 수립한 후 실제 코드 변경을 수행합니다
- **version**: 1.0.0

## Summary

이 스킬은 GitHub 레포지토리(jeenu1027-sudo/ai_daily_report_1)의 이슈를 단계적으로 처리합니다. 열린 이슈를 확인하고 분석한 후, 수정 계획을 수립하고 실제로 코드를 변경하며 관련 문서를 업데이트합니다.

## Workflow

```
1. 이슈 목록 조회
   ↓
2. 이슈 상세 분석
   ↓
3. 수정 계획 수립
   ↓
4. 코드 구현/수정
   ↓
5. 테스트 및 검증
   ↓
6. 문서 업데이트
   ↓
7. 커밋 및 푸시
   ↓
8. Pull Request 생성 (선택)
```

## Usage

사용자가 다음과 같은 요청을 할 때 이 스킬을 사용하세요:

- "이슈를 확인하고 수정해줘"
- "GitHub 이슈를 처리해줘"
- "등록된 이슈 중 버그를 수정해줘"
- "이슈 #1을 해결해줘"
- "이슈들의 상황을 파악하고 계획을 세워줘"

## Parameters

### Required
- **action** (string): 실행할 작업
  - `analyze`: 모든 열린 이슈 분석만 수행
  - `plan`: 분석 후 수정 계획 수립
  - `implement`: 분석 → 계획 → 코드 수정 수행
  - `specific`: 특정 이슈 번호로 처리

### Optional
- **issue_number** (integer): 특정 이슈 번호
  - 예: `1`, `2`, `3`
  - 기본값: 모든 이슈

- **labels** (array of strings): 특정 라벨의 이슈만 처리
  - 예: `["bug"]`, `["enhancement"]`
  - 기본값: 모든 이슈

- **assignee** (string): 담당자 지정
  - 예: "jeenu1027-sudo"
  - 기본값: 없음

- **create_pr** (boolean): Pull Request 자동 생성 여부
  - 기본값: `false`

## Repository Configuration

이 스킬은 다음 레포지토리를 대상으로 합니다:
- **Owner**: jeenu1027-sudo
- **Repository**: ai_daily_report_1
- **URL**: https://github.com/jeenu1027-sudo/ai_daily_report_1

## Prerequisites

- GitHub CLI (`gh`) 설치 필요
- GitHub 계정 로그인: `gh auth login`
- Git 설정 완료
- 저장소에 대한 쓰기 권한 필요
- Claude Code의 코드 편집 권한

## Step-by-Step Instructions

### 1단계: 이슈 목록 조회
```bash
gh issue list --repo jeenu1027-sudo/ai_daily_report_1 --state open --limit 10
```

**출력 내용**:
- 이슈 번호
- 제목
- 라벨
- 상태
- 생성 시간

### 2단계: 이슈 상세 분석
각 이슈에 대해:
```bash
gh issue view <issue_number> --repo jeenu1027-sudo/ai_daily_report_1
```

**분석 항목**:
- 이슈 제목과 설명
- 요구 사항 파악
- 영향 범위 식별
- 필요한 파일/코드 파악

### 3단계: 수정 계획 수립

각 이슈별로:
1. **문제 정의**: 무엇이 문제인가?
2. **근본 원인**: 왜 발생했는가?
3. **해결 방법**: 어떻게 해결할 것인가?
4. **영향 범위**: 어떤 파일이 변경되는가?
5. **테스트 계획**: 어떻게 검증할 것인가?

### 4단계: 코드 구현

1. 새 브랜치 생성 (선택사항)
2. 필요한 파일 수정
3. 코드 작성/변경
4. 테스트 실행

### 5단계: 테스트 및 검증

- 스크립트 정상 작동 확인
- 생성된 HTML 파일 확인
- 에러 메시지 확인

### 6단계: 문서 업데이트

- README.md 업데이트
- 관련 가이드 문서 수정
- CHANGELOG 기록

### 7단계: 커밋 및 푸시

```bash
git add .
git commit -m "Fix #<issue_number>: <description>"
git push origin <branch_name>
```

### 8단계: Pull Request 생성 (선택)

```bash
gh pr create \
  --repo jeenu1027-sudo/ai_daily_report_1 \
  --title "Fix #<issue_number>: <title>" \
  --body "## Summary\n\n<description>" \
  --head <branch_name>
```

## Examples

### 예시 1: 모든 이슈 분석
**사용자**: "현재 등록된 이슈들을 분석해줘"

**스킬 실행**:
1. 모든 열린 이슈 조회
2. 각 이슈 상세 분석
3. 이슈 요약 및 우선순위 정리
4. 예상 작업 시간 계산

**결과**:
```
📋 등록된 이슈 분석 결과:

✅ Issue #1 - Add email notification feature [enhancement]
   - 설명: 이메일 자동 발송 기능
   - 우선순위: 중간
   - 예상 시간: 2-3시간
   - 필요 기술: SMTP, 스케줄링

🐛 Issue #2 - Fix RSS feed parsing error [bug]
   - 설명: Wired RSS 파싱 오류
   - 우선순위: 높음
   - 예상 시간: 30분
   - 필요 기술: XML 파싱, 오류 처리

📝 Issue #3 - Improve documentation [documentation]
   - 설명: 시간대 설정 문서 개선
   - 우선순위: 낮음
   - 예상 시간: 1시간
   - 필요 기술: 문서 작성
```

### 예시 2: 특정 이슈 수정
**사용자**: "Issue #2 버그를 수정해줘"

**스킬 실행**:
1. Issue #2 상세 조회
2. RSS 피드 파싱 문제 분석
3. 수정 방안 수립
4. news_fetcher.py 수정
5. 테스트 실행
6. 커밋 및 푸시

**결과**:
```
✅ Issue #2 해결 완료

📝 변경사항:
   - news_fetcher.py: RSS 피드 URL 업데이트
   - Wired 피드 대체 소스 추가
   - 오류 처리 로직 개선

🔗 커밋: Fix #2: Fix RSS feed parsing error for Wired
```

### 예시 3: 계획 수립만
**사용자**: "Issue #1의 수정 계획을 세워줘"

**스킬 실행**:
1. Issue #1 분석
2. 이메일 기능 요구사항 파악
3. 구현 계획서 작성

**결과**:
```
📋 Issue #1 수정 계획

## 구현 전략
1. 메일 발송 모듈 추가 (news_mailer.py)
2. SMTP 설정 파일 생성 (.env)
3. 스케줄 통합 (Task Scheduler 설정 확장)
4. 테스트 및 문서 작성

## 예상 파일 변경
- 신규: news_mailer.py
- 신규: .env.template
- 수정: news_fetcher.py
- 수정: setup_schedule.ps1
- 수정: README.md

## 예상 시간
- 개발: 2시간
- 테스트: 30분
- 문서: 30분
- 합계: 3시간
```

## Issue 타입별 처리 방식

### 🐛 Bug (버그)
1. 버그 재현 방법 확인
2. 원인 분석
3. 최소한의 변경으로 수정
4. 회귀 테스트

### 💡 Enhancement (개선)
1. 기존 코드 분석
2. 개선 방안 수립
3. 코드 리팩토링
4. 성능 테스트

### ✨ Feature (새 기능)
1. 요구사항 명확히
2. 아키텍처 설계
3. 단계적 구현
4. 통합 테스트

### 📚 Documentation (문서)
1. 현재 문서 검토
2. 개선사항 식별
3. 새 내용 작성
4. 검토 및 수정

## Error Handling

| 오류 | 해결 방법 |
|------|---------|
| 이슈 없음 | `gh issue list`로 먼저 확인 |
| 권한 오류 | GitHub 계정 권한 확인 |
| 파일 충돌 | `git pull origin main` 후 재시도 |
| 커밋 실패 | 변경사항 확인 및 스테이징 |
| PR 생성 실패 | 브랜치명 및 권한 확인 |

## Best Practices

1. **한 이슈 = 한 커밋**: 이슈당 하나의 논리적 변경
2. **명확한 커밋 메시지**: "Fix #123: 설명" 형식 사용
3. **테스트 우선**: 변경 후 항상 검증
4. **문서 동시 업데이트**: 코드와 함께 문서도 수정
5. **작은 단위 작업**: 한 번에 하나의 이슈만 처리

### 커밋 메시지 예시
```
Fix #2: Fix RSS feed parsing error for Wired

- Update Wired RSS feed URL
- Add fallback feed sources
- Improve error handling for feed parsing
- Add unit tests for feed parsing
```

### 좋은 계획의 특징
- ✅ 명확한 문제 정의
- ✅ 단계적 해결 방안
- ✅ 영향 범위 식별
- ✅ 테스트 계획 포함
- ✅ 예상 시간 산정

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

### v1.0.0 (2026-06-11)
- 초기 스킬 작성
- 이슈 분석 기능 구현
- 수정 계획 수립 기능 추가
- 코드 구현 및 커밋 기능 통합
- 다양한 이슈 타입 처리 가능

---

**마지막 업데이트**: 2026-06-11  
**유지관리자**: Claude Code

## Related Skills

- 📝 **issue-writer.md**: 새 이슈 생성
- 🔧 **git_push.md**: Git 커밋 및 푸시
