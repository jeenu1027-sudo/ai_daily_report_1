#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import io
import json
from datetime import datetime

# UTF-8 인코딩 설정
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# 뉴스 주제 (Step 1에서 수집된 뉴스의 주제들)
news_topics = ["AI", "인공지능", "머신러닝", "LLM", "Claude", "생성형 AI"]

# GitHub 이슈 데이터
issues = [
    {
        "number": 7,
        "title": "테스트: 세 문서 최적화 완료 검증",
        "labels": [],
        "createdAt": "2026-06-12T01:40:14Z"
    },
    {
        "number": 4,
        "title": "Improve error handling for network failures",
        "labels": ["enhancement"],
        "createdAt": "2026-06-12T00:07:07Z"
    },
    {
        "number": 3,
        "title": "Improve documentation for time zone configuration",
        "labels": ["documentation"],
        "createdAt": "2026-06-11T09:48:40Z"
    },
    {
        "number": 1,
        "title": "Add email notification feature",
        "labels": ["enhancement"],
        "createdAt": "2026-06-11T09:48:13Z"
    }
]

def categorize_issue(title, labels):
    """이슈 카테고리 결정"""
    title_lower = title.lower()

    if "bug" in title_lower or "error" in title_lower or "fail" in title_lower:
        return "bug"
    elif "test" in title_lower or "테스트" in title:
        return "test"
    elif "doc" in title_lower or "documentation" in title_lower or "문서" in title:
        return "documentation"
    elif "email" in title_lower or "notification" in title_lower:
        return "feature"
    elif "enhancement" in labels:
        return "feature"
    else:
        return "task"

def calculate_priority_score(issue, news_topics):
    """우선순위 점수 계산"""
    title = issue["title"]
    category = categorize_issue(title, issue["labels"])

    # 영향도 (Impact) - 50%
    impact = 40  # 기본값
    if category == "bug":
        impact = 85  # 버그는 높음
    elif category == "feature":
        impact = 60  # 기능은 중간
    elif category == "documentation":
        impact = 35  # 문서는 낮음
    elif category == "test":
        impact = 30  # 테스트는 매우 낮음

    # 긴급성 (Urgency) - 30%
    urgency = 40  # 기본값
    if category == "bug":
        urgency = 90  # 버그는 긴급
    elif category == "feature":
        urgency = 50
    elif category == "test":
        urgency = 20  # 테스트는 낮음

    # 복잡도 (Complexity) - 감점 20%
    complexity = 50  # 기본값
    if "error handling" in title.lower():
        complexity = 70
    elif "email" in title.lower():
        complexity = 60
    elif "documentation" in title.lower():
        complexity = 30

    # 뉴스 관련성 (News Relevance) - 10% 보너스
    news_relevance = 0
    for topic in news_topics:
        if topic.lower() in title.lower():
            news_relevance = 50
            break

    # 최종 점수 계산
    score = (impact * 0.5) + (urgency * 0.3) - (complexity * 0.2) + (news_relevance * 0.1)

    return {
        "score": min(100, max(0, score)),
        "impact": impact,
        "urgency": urgency,
        "complexity": complexity,
        "news_relevance": news_relevance,
        "category": category
    }

def get_priority_level(score):
    """점수에 따른 우선순위 레벨"""
    if score >= 70:
        return "🔴 Critical"
    elif score >= 50:
        return "🟠 High"
    elif score >= 30:
        return "🟡 Medium"
    else:
        return "🟢 Low"

# 분석
print("=" * 70)
print("🔍 GitHub 이슈 우선순위 분석 리포트")
print("=" * 70)
print(f"📅 분석 날짜: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print(f"📊 분석된 이슈: {len(issues)}개")
print()

# 점수 계산
analyzed = []
for issue in issues:
    analysis = calculate_priority_score(issue, news_topics)
    analyzed.append({
        **issue,
        **analysis
    })

# 점수순 정렬
analyzed.sort(key=lambda x: x["score"], reverse=True)

# 결과 출력
for idx, item in enumerate(analyzed, 1):
    priority = get_priority_level(item["score"])
    print(f"{idx}. #{item['number']} - {item['title']}")
    print(f"   우선순위: {priority}")
    print(f"   점수: {item['score']:.1f}/100")
    print(f"   분석:")
    print(f"     • 영향도: {item['impact']}/100")
    print(f"     • 긴급성: {item['urgency']}/100")
    print(f"     • 복잡도: {item['complexity']}/100 (감점)")
    print(f"     • 뉴스관련성: {item['news_relevance']}/100 (보너스)")
    print(f"   카테고리: {item['category'].upper()}")
    print()

# 통계
print("=" * 70)
print("📊 우선순위 분포")
print("=" * 70)
critical = sum(1 for x in analyzed if x["score"] >= 70)
high = sum(1 for x in analyzed if 50 <= x["score"] < 70)
medium = sum(1 for x in analyzed if 30 <= x["score"] < 50)
low = sum(1 for x in analyzed if x["score"] < 30)

print(f"🔴 Critical (≥70):  {critical}개")
print(f"🟠 High (50-69):    {high}개")
print(f"🟡 Medium (30-49):  {medium}개")
print(f"🟢 Low (<30):       {low}개")
print()

# 권장사항
print("=" * 70)
print("💡 권장사항")
print("=" * 70)
if critical > 0:
    critical_issues = [x for x in analyzed if x["score"] >= 70]
    print(f"🔴 즉시 처리 필요 ({critical}개):")
    for issue in critical_issues:
        print(f"   - #{issue['number']}: {issue['title']}")
    print()

if high > 0:
    high_issues = [x for x in analyzed if 50 <= x["score"] < 70]
    print(f"🟠 이번 주 우선 처리 ({high}개):")
    for issue in high_issues:
        print(f"   - #{issue['number']}: {issue['title']}")
    print()

print("=" * 70)
