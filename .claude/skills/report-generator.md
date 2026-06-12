# Report Generator Skill

## Metadata
- **name**: report-generator
- **description**: 아침 브리핑 최종 리포트 생성 (HTML + Markdown)
- **version**: v1.0.0
- **category**: Report Generation
- **dependencies**: morning-briefing

---

## Summary

**뉴스** + **이슈 분석** 결과를 통합하여 시각화된 **아침 브리핑 리포트**를 생성합니다.

최신 CSS3 기술을 활용한 모던 디자인과 한국어 완전 지원입니다.

---

## Report Structure (리포트 구조)

```
📊 AI Daily Report
├─ 1️⃣ Executive Summary (요약)
│   ├─ 오늘의 주요 뉴스 3개
│   ├─ 긴급 이슈 2-3개
│   └─ 권장 조치사항
│
├─ 2️⃣ News Section (뉴스)
│   ├─ 주요 주제별 그룹화
│   ├─ 각 기사 요약 + 링크
│   └─ 품질 점수
│
├─ 3️⃣ Issue Analysis (이슈 분석)
│   ├─ 우선순위별 정렬
│   ├─ 뉴스와의 연관성 표시
│   └─ 담당자 지정
│
└─ 4️⃣ Recommendations (권장사항)
    ├─ 즉시 조치 필요 항목
    ├─ 이번 주 완료 예정
    └─ 백로그 추가 항목
```

---

## Report Sections (상세 섹션)

### Section 1: Executive Summary (경영진 요약)

```html
<section class="executive-summary">
  <h2>🎯 오늘의 핵심 (Executive Summary)</h2>
  
  <div class="key-insights">
    <h3>📰 주요 뉴스</h3>
    <ul>
      <li>주제 1: AI 보안 위협 증가</li>
      <li>주제 2: LLM 성능 경쟁</li>
      <li>주제 3: 규제 동향</li>
    </ul>
  </div>
  
  <div class="critical-actions">
    <h3>🚨 즉시 조치 필요</h3>
    <ul>
      <li>API 인증 취약점 수정 (Score: 87/100)</li>
      <li>성능 개선 계획 수립 (Score: 75/100)</li>
    </ul>
  </div>
</section>
```

### Section 2: News Deep Dive (뉴스 상세)

```html
<section class="news-section">
  <h2>📰 AI 뉴스 (Today's Updates)</h2>
  
  <article class="news-item">
    <header>
      <h3>Claude 3.5 Sonnet, 성능 기준 수립</h3>
      <span class="metadata">
        <span class="source">VentureSquare</span>
        <span class="quality-score">92/100</span>
        <span class="date">2026-06-12</span>
      </span>
    </header>
    
    <summary>
      최신 LLM 모델의 성능이 업계 표준을 초과하여...
    </summary>
    
    <tags>
      <span class="tag">LLM</span>
      <span class="tag">성능</span>
      <span class="tag">기술</span>
    </tags>
    
    <footer>
      <a href="링크" class="read-more">전문 읽기 →</a>
    </footer>
  </article>
  
  <!-- 추가 뉴스 아이템 -->
</section>
```

### Section 3: Issue Analysis (이슈 분석)

```html
<section class="issues-section">
  <h2>🔍 GitHub 이슈 분석</h2>
  
  <div class="priority-tabs">
    <div class="priority-group critical">
      <h3>🔴 Critical (3개)</h3>
      
      <div class="issue-card">
        <header>
          <span class="issue-id">#123</span>
          <h4>API 인증 우회 버그</h4>
          <span class="score">87/100</span>
        </header>
        
        <body>
          <p class="description">로그인 검증 로직 결함...</p>
          <div class="news-connection">
            🔗 연관 뉴스: "AI 보안 위협"
          </div>
        </body>
        
        <footer>
          <span class="category">🐛 Bug</span>
          <span class="assignee">@developer</span>
          <span class="eta">즉시 처리</span>
        </footer>
      </div>
    </div>
    
    <div class="priority-group high">
      <h3>🟠 High (5개)</h3>
      <!-- 이슈 카드들 -->
    </div>
    
    <div class="priority-group medium">
      <h3>🟡 Medium (7개)</h3>
      <!-- 이슈 카드들 -->
    </div>
  </div>
</section>
```

### Section 4: Recommendations (권장사항)

```html
<section class="recommendations-section">
  <h2>💡 권장 조치</h2>
  
  <div class="recommendation urgent">
    <h3>⚡ 즉시 (오늘)</h3>
    <ul>
      <li>API 보안 패치 배포 (#123)</li>
      <li>보안 감사 스케줄링</li>
    </ul>
  </div>
  
  <div class="recommendation this-week">
    <h3>📅 이번 주</h3>
    <ul>
      <li>성능 최적화 계획 검토 (#456)</li>
      <li>뉴스 주제 기술 도입 계획 (#789)</li>
    </ul>
  </div>
  
  <div class="recommendation backlog">
    <h3>📋 백로그 추가</h3>
    <ul>
      <li>UI 개선 논의 (#102)</li>
      <li>문서화 업데이트 (#103)</li>
    </ul>
  </div>
</section>
```

---

## Parameters

### Input
```json
{
  "date": "2026-06-12",
  "news_data": {
    "articles": [
      {
        "title": "string",
        "source": "string",
        "url": "string",
        "summary": "string",
        "quality_score": 92,
        "tags": ["AI", "보안"]
      }
    ]
  },
  "issue_data": {
    "prioritized_issues": [
      {
        "id": 123,
        "title": "string",
        "priority_score": 87,
        "priority_level": "Critical",
        "news_relevance": "High"
      }
    ]
  },
  "generated_by": "morning-briefing",
  "theme": "light|dark"
}
```

### Output
```
ai-news-digest-2026-06-12.html (생성된 리포트 파일)
```

---

## Design System (디자인 시스템)

### Color Palette (색상)
```css
/* Primary Colors */
--primary-cream: #F4F1EA
--primary-accent: #C17A3A (테라코타)
--secondary-accent: #D4AF8F (앰버)

/* Priority Colors */
--critical: #FF4444 (빨강)
--high: #FF9944 (주황)
--medium: #FFDD44 (노랑)
--low: #88BB44 (초록)

/* Neutrals */
--text-dark: #2C2C2C
--text-light: #666666
--bg-light: #FFFFFF
--border: #EEEEEE
```

### Typography
```css
/* Display */
--display-font: "Fraunces", serif
--display-size: 48px

/* Heading */
--heading-font: "Georgia", serif
--heading-size: 32px

/* Body */
--body-font: "Georgia", serif
--body-size: 16px
```

### Components
```css
/* Cards */
.news-card { background: linear gradient; border-radius: 8px }
.issue-card { background: rgba(255,255,255,0.7); backdrop-filter: blur(10px) }

/* Animations */
@keyframes slideIn { from { opacity: 0; transform: translateY(10px) } }
@keyframes fadeIn { from { opacity: 0 } to { opacity: 1 } }
```

---

## File Naming Convention

```
ai-news-digest-YYYY-MM-DD.html

예시:
- ai-news-digest-2026-06-12.html
- ai-news-digest-2026-06-13.html
```

---

## Examples

### ✅ 성공한 리포트
```
파일명: ai-news-digest-2026-06-12.html
크기: 45KB
생성 시간: 2026-06-12 08:15:30

포함 내용:
- 뉴스 8개
- 이슈 15개
- 우선순위 분석
- 권장사항 3개
```

### Features
```
✅ 한국어 완전 지원
✅ CSS3 Glassmorphism 디자인
✅ 모바일 반응형
✅ 다크모드 지원
✅ 인쇄 최적화
✅ 접근성 준수 (WCAG 2.1)
```

---

## Integration with Agents

### 사용하는 에이전트
- **morning-briefing**: 최종 리포트 생성
- **news-fetcher-agent**: 뉴스 데이터 제공
- **issue-analyzer**: 이슈 데이터 제공

### 호출 방식
```
1. news-fetcher-agent → 필터링된 뉴스
2. issue-analyzer → 우선순위 지정 이슈
3. morning-briefing 조정
4. report-generator 스킬 호출
5. HTML 파일 생성 (ai-news-digest-YYYY-MM-DD.html)
```

---

## Maintenance

### 디자인 업데이트
```
- 분기마다 1회 검토
- 사용자 피드백 반영
- 트렌드 반영
```

### 성능 최적화
```
- HTML 파일 크기: < 100KB 목표
- 로딩 시간: < 2초 목표
- 모바일 점수: 95+ 목표
```

---

**마지막 업데이트**: 2026-06-12  
**버전**: v1.0.0 (Harness Release)
