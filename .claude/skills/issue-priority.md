# Issue Priority Skill

## Metadata
- **name**: issue-priority
- **description**: GitHub 이슈 우선순위 평가 및 스코링 알고리즘
- **version**: v1.0.0
- **category**: Issue Management
- **dependencies**: issue-analyzer

---

## Summary

GitHub의 오픈 이슈들을 **점수 기반 알고리즘**으로 평가하여 우선순위를 자동 결정합니다.

특히 **뉴스와의 연관성**을 고려하여 관련성 높은 이슈를 상위에 배치합니다.

---

## Scoring Algorithm (점수 계산 알고리즘)

```python
def calculate_issue_priority_score(issue, news_context=None):
    """
    이슈 우선순위를 0-100으로 평가
    
    점수 = (영향도 × 0.5) + (긴급성 × 0.3) - (복잡도 × 0.2) + (관련성 × 0.1)
    
    각 항목은 0-100 범위
    """
    
    # 1. 영향도 (Impact) - 50% 가중치
    impact_score = calculate_impact(issue)
    
    # 2. 긴급성 (Urgency) - 30% 가중치
    urgency_score = calculate_urgency(issue)
    
    # 3. 복잡도 (Complexity) - 20% 감점
    complexity_score = calculate_complexity(issue)
    
    # 4. 뉴스 관련성 (News Relevance) - 10% 보너스
    relevance_bonus = 0
    if news_context:
        relevance_bonus = calculate_news_relevance(issue, news_context)
    
    # 최종 점수
    final_score = (
        (impact_score * 0.5) +
        (urgency_score * 0.3) -
        (complexity_score * 0.2) +
        (relevance_bonus * 0.1)
    )
    
    return min(100, max(0, final_score))
```

---

## Scoring Components

### 1️⃣ Impact (영향도) - 50%
```
측정 기준:
- 영향받는 사용자 수
- 비즈니스 영향
- 기술 범위

점수 매기기:
0-20:    소수 사용자 영향
21-40:   중간 규모 영향
41-60:   큰 영향
61-80:   매우 큰 영향
81-100:  전체 서비스 영향

예시:
"로그인 실패" → 80점 (모든 사용자 영향)
"폰트 오류" → 30점 (디자인만 영향)
```

### 2️⃣ Urgency (긴급성) - 30%
```
측정 기준:
- 문제 심각도 (Critical/High/Medium/Low)
- 사용자 불만 수
- 버그 로그 증가 추세
- 경쟁사 대비 상황

점수 매기기:
0-25:    낮음 (다음 분기)
26-50:   중간 (이번 분기)
51-75:   높음 (이번 주)
76-100:  긴급 (오늘)

예시:
"Critical 버그" → 90점
"기능 요청" → 20점
```

### 3️⃣ Complexity (복잡도) - 감점 20%
```
측정 기준:
- 예상 개발 시간
- 테스트 범위
- 의존성 수
- 리스크 수준

점수 매기기:
0-25:    간단 (1시간)
26-50:   중간 (1일)
51-75:   복잡 (3일)
76-100:  매우 복잡 (1주+)

예시:
"README 수정" → 5점 (거의 감점 없음)
"아키텍처 재설계" → 95점 (심각한 감점)
```

### 4️⃣ News Relevance (뉴스 관련성) - 보너스 10%
```
측정 기준:
- 뉴스에 언급된 주제와의 일치도
- 관련 이슈 수
- 커뮤니티 관심도

점수 매기기:
0:    관련 없음
5-25:  약간 관련
26-50: 중간 관련
51-100: 직접 관련

예시:
뉴스: "AI 보안 위협 증가"
관련 이슈: "API 인증 취약점" → +40점
관련 없는 이슈: "UI 버튼 위치" → +0점
```

---

## Category Classification (카테고리 분류)

```python
categories = {
    "Bug": {
        "urgency_boost": 20,  # 버그는 긴급성 +20
        "icon": "🐛"
    },
    "Enhancement": {
        "urgency_boost": 0,
        "icon": "✨"
    },
    "Documentation": {
        "urgency_boost": -10,  # 문서는 긴급성 감점
        "icon": "📚"
    },
    "Security": {
        "urgency_boost": 30,  # 보안은 높은 우선순위
        "icon": "🔒"
    },
    "Performance": {
        "urgency_boost": 15,
        "icon": "⚡"
    },
    "Refactor": {
        "urgency_boost": -15,  # 리팩토링은 낮은 우선순위
        "icon": "🔨"
    }
}
```

---

## Parameters

### Input
```json
{
  "issues": [
    {
      "id": 123,
      "title": "string",
      "description": "string",
      "category": "Bug|Enhancement|Documentation|...",
      "labels": ["bug", "critical"],
      "created_at": "ISO-8601",
      "comments_count": 5,
      "reactions": {"👍": 10},
      "assignee": "user"
    }
  ],
  "news_context": {
    "topics": ["AI Security", "LLM Performance"],
    "date": "2026-06-12"
  }
}
```

### Output
```json
{
  "prioritized_issues": [
    {
      "id": 123,
      "title": "string",
      "priority_score": 85,
      "priority_level": "High",
      "category": "Bug",
      "news_relevance": "High - 'AI Security' 주제와 관련",
      "scoring_breakdown": {
        "impact": 80,
        "urgency": 70,
        "complexity": 50,
        "news_relevance": 40
      },
      "recommendation": "이번 주 우선 처리"
    }
  ],
  "summary": {
    "total_issues": 15,
    "critical": 3,
    "high": 5,
    "medium": 7
  }
}
```

---

## Examples

### ✅ 높은 우선순위 (70점 이상)
```
제목: "API 인증 우회 버그 발견"
점수: 87/100

계산:
- 영향도: 90 (모든 API 사용자 영향)
- 긴급성: 95 (Critical 버그)
- 복잡도: 60 (중간 난이도)
- 뉴스 관련성: +40 (보안 뉴스 관련)

우선순위 레벨: 🔴 Critical
추천 조치: "즉시 핫픽스 필요"
```

### 🟡 중간 우선순위 (40-70점)
```
제목: "성능 개선: 캐싱 레이어 추가"
점수: 55/100

계산:
- 영향도: 60 (많은 사용자 영향)
- 긴급성: 40 (Enhancement)
- 복잡도: 70 (복잡함)
- 뉴스 관련성: +20 (성능 뉴스 약간 관련)

우선순위 레벨: 🟡 Medium
추천 조치: "이번 분기 예정"
```

### 🟢 낮은 우선순위 (40점 이하)
```
제목: "README에 예시 추가"
점수: 25/100

계산:
- 영향도: 20 (사용자 경험 미미)
- 긴급성: 15 (Documentation)
- 복잡도: 10 (매우 간단)
- 뉴스 관련성: +0 (관련 없음)

우선순위 레벨: 🟢 Low
추천 조치: "여유 있을 때 처리"
```

---

## Integration with Agents

### 사용하는 에이전트
- **issue-analyzer**: 이슈 분석 시 이 스킬 적용
- **morning-briefing**: 최종 우선순위 검증

### 호출 방식
```
1. issue-analyzer가 15개 오픈 이슈 수집
2. issue-priority 스킬 적용
3. 뉴스 컨텍스트 포함하여 점수 계산
4. 우선순위 정렬 (높음 → 낮음)
5. morning-briefing에 전달
```

---

## Maintenance

### 알고리즘 조정
```
- 매주 1회 검토
- 팀 피드백 반영
- 실제 개발 시간과 예측 비교
```

### 가중치 재조정
```
조건: 예측 정확도 < 70%
조치: 각 항목 가중치 조정
목표: 우선순위 정확도 80% 이상
```

---

**마지막 업데이트**: 2026-06-12  
**버전**: v1.0.0 (Harness Release)
