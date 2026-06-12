# News Filtering Skill

## Metadata
- **name**: news-filtering
- **description**: AI 뉴스 필터링 및 품질 평가 로직
- **version**: v1.0.0
- **category**: News Processing
- **dependencies**: news-fetcher-agent

---

## Summary

당신의 프로젝트에서 수집한 뉴스를 **6가지 엄격한 필터링 규칙**에 따라 검증하고 품질 점수를 부여합니다.

---

## Filtering Rules (필터링 규칙)

### 규칙 1️⃣: 한국어 뉴스만 선별
```
조건: 기사 언어 == "Korean"
처리: 영어/다른 언어 기사 제외
이유: 한국 사용자 중심 정보 제공
```

### 규칙 2️⃣: AI 생성 콘텐츠 제외
```
조건: 기사 출처 타입 != "AI-generated"
처리: ChatGPT, Claude, Gemini 등으로 생성된 기사 제외
이유: 원본 뉴스 가치 높음
```

### 규칙 3️⃣: GitHub 자료 제외
```
조건: 기사 출처 도메인 != "github.com"
처리: GitHub README, Gist, Discussion 제외
이유: 뉴스와 코드 자료 구분
```

### 규칙 4️⃣: 국내 대형 포털 제외
```
조건: 기사 출처 도메인 NOT IN ["naver.com", "daum.net", ...]
처리: Naver, Daum, Google News 포털 기사 제외
이유: 원문 매체의 신뢰도 확보
```

### 규칙 5️⃣: 학술 논문 제외
```
조건: 기사 타입 != "Academic Paper"
처리: arXiv, Scholar, 학술 DB 논문 제외
이유: 토큰 절감 + 뉴스 가치 중심
```

### 규칙 6️⃣: 웹 출처 제한 (최대 10개)
```
조건: DISTINCT(기사 출처 도메인) <= 10
처리: 출처가 10개를 초과하면 신뢰도 높은 출처부터 선별
이유: 토큰 절감 + 다양한 관점 유지
```

---

## Quality Scoring (품질 점수)

```python
def calculate_quality_score(article):
    """
    기사 품질을 0-100으로 평가
    
    기본점: 100
    감점 요인:
    - 날짜 오래됨: -10 (1주일 이상)
    - 출처 신뢰도 낮음: -15
    - 콘텐츠 깊이 부족: -20
    - 기술적 정확도 의심: -25
    
    최종 점수 = 기본점 - 감점
    """
    score = 100
    
    # 시간 점수
    age_days = (today - article.published_date).days
    if age_days > 7:
        score -= 10
    if age_days > 30:
        score -= 20
    
    # 출처 신뢰도
    if article.source_credibility < 0.7:
        score -= 15
    
    # 내용 깊이 (단어 수)
    if len(article.content.split()) < 500:
        score -= 20
    
    # 기술 정확도 (전문가 평가)
    if article.technical_accuracy < 0.8:
        score -= 25
    
    return max(0, score)  # 음수 방지
```

---

## Parameters

### Input
```json
{
  "articles": [
    {
      "title": "string",
      "content": "string",
      "source": "string",
      "published_date": "ISO-8601",
      "language": "korean|english|...",
      "source_type": "news|blog|academic|...",
      "url": "string"
    }
  ]
}
```

### Output
```json
{
  "filtered_articles": [
    {
      "title": "string",
      "source": "string",
      "quality_score": 85,
      "reason_for_inclusion": "string",
      "tags": ["AI", "LLM", "보안"]
    }
  ],
  "excluded_articles": [
    {
      "title": "string",
      "exclusion_reason": "AI-generated content",
      "rule_violated": 2
    }
  ],
  "statistics": {
    "total_input": 20,
    "total_output": 8,
    "filter_effectiveness": "40%"
  }
}
```

---

## Examples

### ✅ 포함되는 기사
```
제목: "Claude 3.5 Sonnet, 새로운 성능 기준 수립"
출처: VentureSquare (한국)
언어: 한국어
타입: 뉴스 기사
품질점수: 92/100
이유: 원본 매체, 신뢰도 높음, 기술 깊이 충분
```

### ❌ 제외되는 기사
```
제목: "ChatGPT가 쓴 AI 뉴스 요약"
출처: AI-generated content
제외 사유: Rule 2 위반 (AI 생성 콘텐츠)
```

```
제목: "[공식] GitHub Copilot 업데이트"
출처: github.com/blog
제외 사유: Rule 3 위반 (GitHub 자료)
```

```
제목: "Deep Learning 논문 100편 모음"
출처: arxiv.org
제외 사유: Rule 5 위반 (학술 논문)
```

---

## Integration with Agents

### 사용하는 에이전트
- **news-fetcher-agent**: 뉴스 수집 후 이 스킬 적용
- **morning-briefing**: 최종 품질 검증

### 호출 방식
```
1. news-fetcher-agent가 20개 뉴스 수집
2. news-filtering 스킬 적용
3. 필터링된 8개 뉴스만 반환
4. morning-briefing에 전달
```

---

## Maintenance

### 필터링 규칙 업데이트
```
- 매월 1회 검토
- 사용자 피드백 반영
- 새로운 AI 생성 도구 추가 시 Rule 2 업데이트
```

### 성능 모니터링
```
- 필터링 효율성 (입력 대비 출력 비율)
- 제외 기사의 사후 검토
- 사용자 만족도 추적
```

---

**마지막 업데이트**: 2026-06-12  
**버전**: v1.0.0 (Harness Release)
