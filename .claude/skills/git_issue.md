# GitHub Issue Creator Skill

## Metadata
- **name**: git_issue
- **description**: GitHub 레포지토리에 이슈를 신속하게 생성합니다
- **version**: 1.0.0

## Summary

이 스킬은 GitHub 레포지토리(jeenu1027-sudo/ai_daily_report_1)에 이슈를 자동으로 생성합니다. 사용자가 제공하는 제목과 설명 기반으로 이슈를 생성하며, 라벨, 담당자, 마일스톤 등을 선택적으로 지정할 수 있습니다.

## Usage

사용자가 다음과 같은 요청을 할 때 이 스킬을 사용하세요:

- "이슈 생성해줘"
- "GitHub에 버그 리포트 올려줘"
- "기능 요청 이슈 만들어줘"
- "이슈를 등록해줘"

## Parameters

### Required
- **title** (string): 이슈의 제목 (필수)
  - 예: "뉴스 수집 실패 버그"
  - 최대 길이: 256자

- **description** (string): 이슈의 상세 설명 (필수)
  - 예: "특정 RSS 피드에서 뉴스를 수집하지 못함"
  - Markdown 형식 지원

### Optional
- **labels** (array of strings): 이슈에 붙을 라벨들
  - 예: `["bug", "enhancement", "documentation"]`
  - 기본값: 없음
  - 사용 가능한 라벨:
    - bug: 버그 관련
    - enhancement: 기능 개선
    - documentation: 문서
    - feature: 새 기능
    - help-wanted: 도움 필요
    - wontfix: 수정하지 않음

- **assignee** (string): 이슈 담당자 (GitHub username)
  - 예: "jeenu1027-sudo"
  - 기본값: 없음

- **milestone** (string): 마일스톤 제목
  - 예: "v1.1.0"
  - 기본값: 없음

## Repository Configuration

이 스킬은 다음 레포지토리를 대상으로 합니다:
- **Owner**: jeenu1027-sudo
- **Repository**: ai_daily_report_1
- **URL**: https://github.com/jeenu1027-sudo/ai_daily_report_1

## Prerequisites

- GitHub CLI (`gh`) 설치 필요
- GitHub 계정 로그인: `gh auth login`
- 저장소에 대한 쓰기 권한 필요

## Instructions

1. **사용자 입력 확인**: 제목과 설명이 충분히 자세한지 확인
2. **이슈 유형 판단**: 버그, 기능, 문서 중 어떤 유형인지 판단
3. **자동 라벨 지정** (선택):
   - "bug" - 버그 보고일 경우
   - "enhancement" - 개선 사항일 경우
   - "feature" - 새 기능 요청일 경우
   - "documentation" - 문서 관련일 경우

4. **gh CLI 명령어 실행**:
   ```bash
   gh issue create \
     --repo jeenu1027-sudo/ai_daily_report_1 \
     --title "제목" \
     --body "설명" \
     --label "라벨1,라벨2" \
     --assignee "담당자"
   ```

5. **결과 출력**: 생성된 이슈 URL 및 번호 표시

## Examples

### 버그 보고
**사용자**: "뉴스 수집이 실패하는 버그를 리포트해줘"

**스킬 실행**:
```bash
gh issue create \
  --repo jeenu1027-sudo/ai_daily_report_1 \
  --title "뉴스 수집 스크립트 오류" \
  --body "Hacker News에서 뉴스를 수집할 때 타임아웃 오류 발생" \
  --label "bug"
```

**결과**: Issue #1 생성

### 기능 요청
**사용자**: "이메일로 뉴스를 자동 발송하는 기능을 요청해줘"

**스킬 실행**:
```bash
gh issue create \
  --repo jeenu1027-sudo/ai_daily_report_1 \
  --title "이메일 자동 발송 기능 추가" \
  --body "## 기능 설명\n일일 뉴스 리포트를 이메일로 자동 발송합니다.\n\n## 구현 방법\n- SMTP 설정\n- 이메일 템플릿\n- 스케줄 통합" \
  --label "feature,enhancement"
```

**결과**: Issue #2 생성

## Error Handling

| 오류 | 해결 방법 |
|------|---------|
| `gh: not found` | GitHub CLI 설치: https://cli.github.com |
| `Not authenticated` | `gh auth login` 실행 |
| `repository not found` | 레포지토리 이름 및 권한 확인 |
| `invalid label` | 사용 가능한 라벨 목록 확인 |

## Best Practices

1. **명확한 제목**: 문제를 한 줄로 요약
   - ❌ "버그 있음"
   - ✅ "HTML 생성 시 인코딩 오류 발생"

2. **상세한 설명**: 재현 방법, 예상 결과, 실제 결과 포함
   ```markdown
   ### 재현 방법
   1. news_fetcher.py 실행
   2. Hacker News 뉴스 수집 시작
   3. 에러 발생
   
   ### 예상 결과
   HTML 파일 정상 생성
   
   ### 실제 결과
   UnicodeEncodeError 발생
   ```

3. **적절한 라벨 사용**: 최대 3-4개까지 사용
4. **담당자 지정**: 필요시에만 지정

## Links

- 📖 [GitHub CLI 문서](https://cli.github.com/manual/)
- 🔗 [이슈 API 문서](https://docs.github.com/en/rest/issues)
- 📝 [프로젝트 README](../../../README.md)
- 🐛 [이미 생성된 이슈 보기](https://github.com/jeenu1027-sudo/ai_daily_report_1/issues)

## Changelog

### v1.0.0 (2026-06-11)
- 초기 스킬 작성
- 기본 이슈 생성 기능 구현
- 라벨, 담당자, 마일스톤 지원

---

**마지막 업데이트**: 2026-06-11  
**유지관리자**: Claude Code
