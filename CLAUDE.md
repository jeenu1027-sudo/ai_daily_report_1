# Claude Code Configuration

프로젝트 설정 및 커스텀 스킬 정의

> **프로젝트 정보**: 프로젝트 개요, 설치, 실행은 [README.md](README.md) 참고  
> **설계 철학**: 프로젝트 비전, 핵심 가치는 [SOUL.md](SOUL.md) 참고

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

### 1. `briefing-improver` - 통합 이슈 관리 워크플로우 ⭐ 추천

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

### 2. `issue-writer` - GitHub 이슈 생성

이슈만 빠르게 생성합니다.

**사용 예**:
```
사용자: "버그 리포트를 이슈로 등록해줘"
Claude: issue-writer 스킬 실행 → GitHub 이슈 생성
```

자세한 정보: [issue-writer.md](./.claude/skills/issue-writer.md)

---

### 3. `issue-runner` - GitHub 이슈 분석 및 수정

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
