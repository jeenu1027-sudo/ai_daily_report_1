#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""단위 테스트: analyze_issues.py"""

import unittest
from analyze_issues import (
    categorize_issue,
    calculate_priority_score,
    get_priority_level
)


class TestCategorizeIssue(unittest.TestCase):
    """이슈 카테고리 함수 테스트"""

    def test_categorize_bug(self):
        """버그 카테고리 분류"""
        self.assertEqual(categorize_issue("Fix critical bug", []), "bug")
        self.assertEqual(categorize_issue("Error handling issue", []), "bug")
        self.assertEqual(categorize_issue("System failure detected", []), "bug")

    def test_categorize_test(self):
        """테스트 카테고리 분류"""
        self.assertEqual(categorize_issue("Add unit tests", []), "test")
        self.assertEqual(categorize_issue("테스트 코드 작성", []), "test")

    def test_categorize_documentation(self):
        """문서 카테고리 분류"""
        self.assertEqual(categorize_issue("Update documentation", []), "documentation")
        self.assertEqual(categorize_issue("문서화 개선", []), "documentation")

    def test_categorize_feature(self):
        """기능 카테고리 분류"""
        self.assertEqual(categorize_issue("Add email notification", []), "feature")
        self.assertEqual(categorize_issue("New feature", ["enhancement"]), "feature")

    def test_categorize_default(self):
        """기본 카테고리"""
        self.assertEqual(categorize_issue("General task", []), "task")


class TestCalculatePriorityScore(unittest.TestCase):
    """우선순위 점수 계산 함수 테스트"""

    def test_calculate_priority_score_bug(self):
        """버그는 높은 점수"""
        issue = {
            "title": "Critical security bug",
            "labels": ["bug"],
            "createdAt": "2026-06-12T00:00:00Z"
        }
        score_dict = calculate_priority_score(issue, [])

        self.assertGreater(score_dict['score'], 50)
        self.assertEqual(score_dict['category'], "bug")

    def test_calculate_priority_score_documentation(self):
        """문서는 낮은 점수"""
        issue = {
            "title": "Improve documentation",
            "labels": ["documentation"],
            "createdAt": "2026-06-12T00:00:00Z"
        }
        score_dict = calculate_priority_score(issue, [])

        self.assertLess(score_dict['score'], 40)
        self.assertEqual(score_dict['category'], "documentation")

    def test_calculate_priority_score_news_relevance(self):
        """뉴스 관련성 보너스"""
        issue_with_relevance = {
            "title": "Improve AI model handling",
            "labels": [],
            "createdAt": "2026-06-12T00:00:00Z"
        }

        issue_without_relevance = {
            "title": "Improve UI styling",
            "labels": [],
            "createdAt": "2026-06-12T00:00:00Z"
        }

        score1 = calculate_priority_score(issue_with_relevance, ["AI"])['score']
        score2 = calculate_priority_score(issue_without_relevance, ["AI"])['score']

        # 뉴스 관련성이 있는 이슈가 더 높은 점수
        self.assertGreater(score1, score2)

    def test_calculate_priority_score_structure(self):
        """반환값 구조 확인"""
        issue = {
            "title": "Test issue",
            "labels": [],
            "createdAt": "2026-06-12T00:00:00Z"
        }
        result = calculate_priority_score(issue, [])

        # 모든 필수 키 존재 확인
        self.assertIn('score', result)
        self.assertIn('impact', result)
        self.assertIn('urgency', result)
        self.assertIn('complexity', result)
        self.assertIn('news_relevance', result)
        self.assertIn('category', result)

        # 점수는 0-100 범위
        self.assertGreaterEqual(result['score'], 0)
        self.assertLessEqual(result['score'], 100)


class TestGetPriorityLevel(unittest.TestCase):
    """우선순위 레벨 함수 테스트"""

    def test_get_priority_level_critical(self):
        """높은 점수 = Critical"""
        self.assertEqual(get_priority_level(80), "🔴 Critical")
        self.assertEqual(get_priority_level(100), "🔴 Critical")

    def test_get_priority_level_high(self):
        """중간-높은 점수 = High (50-69)"""
        self.assertEqual(get_priority_level(69), "🟠 High")
        self.assertEqual(get_priority_level(50), "🟠 High")

    def test_get_priority_level_medium(self):
        """중간 점수 = Medium (30-49)"""
        self.assertEqual(get_priority_level(49), "🟡 Medium")
        self.assertEqual(get_priority_level(30), "🟡 Medium")

    def test_get_priority_level_low(self):
        """낮은 점수 = Low (<30)"""
        self.assertEqual(get_priority_level(29), "🟢 Low")
        self.assertEqual(get_priority_level(0), "🟢 Low")


if __name__ == '__main__':
    unittest.main()
