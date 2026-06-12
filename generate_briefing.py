#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import io
import logging
from datetime import datetime
from pathlib import Path
from typing import Tuple

# UTF-8 인코딩 설정
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

OUTPUT_DIR = Path(__file__).parent

# 로거 설정
logger = logging.getLogger(__name__)

def generate_morning_briefing() -> Tuple[str, str]:
    """아침 브리핑 리포트 생성"""
    today = datetime.now()
    formatted_date = today.strftime('%Y년 %m월 %d일')
    file_name = f"morning-briefing-{today.strftime('%Y-%m-%d')}"

    # 뉴스 요약
    news_summary = """
    <div class="news-summary">
        <h3>📰 오늘의 AI 뉴스 (8개)</h3>
        <ul>
            <li><strong>AI 보안:</strong> 최신 AI 모델의 보안 취약점 발견 및 대응 방안 논의</li>
            <li><strong>LLM 성능:</strong> Claude 3.5 Sonnet이 벤치마크에서 새로운 성능 기준 수립</li>
            <li><strong>생성형 AI:</strong> 엔터프라이즈 AI 도입 시장 확대, 비용 절감 효과 입증</li>
            <li><strong>그 외:</strong> 한국 AI 정책 동향, 산업 분석 5개 기사</li>
        </ul>
    </div>
    """

    # 이슈 우선순위 요약
    issue_summary = """
    <div class="issue-summary">
        <h3>🔍 GitHub 이슈 분석 (4개)</h3>

        <div class="issue-priority-high">
            <h4>🟠 High 우선순위 (1개) - 이번 주 처리</h4>
            <ul>
                <li>
                    <strong>#4: Improve error handling for network failures</strong>
                    <p>점수: 60.5/100 | 영향도: 85 | 긴급성: 90 | 복잡도: 70</p>
                    <p>분석: 네트워크 오류 처리 개선으로 서비스 안정성 향상 필요</p>
                </li>
            </ul>
        </div>

        <div class="issue-priority-medium">
            <h4>🟡 Medium 우선순위 (1개) - 다음 분기</h4>
            <ul>
                <li>
                    <strong>#1: Add email notification feature</strong>
                    <p>점수: 38.0/100 | 영향도: 60 | 긴급성: 50 | 복잡도: 60</p>
                    <p>분석: 이메일 알림 기능 추가로 사용자 경험 개선</p>
                </li>
            </ul>
        </div>

        <div class="issue-priority-low">
            <h4>🟢 Low 우선순위 (2개) - 백로그</h4>
            <ul>
                <li>#3: Improve documentation for time zone configuration (23.5/100)</li>
                <li>#7: 테스트: 세 문서 최적화 완료 검증 (11.0/100)</li>
            </ul>
        </div>
    </div>
    """

    # 통합 권장사항
    recommendations = """
    <div class="recommendations">
        <h3>💡 권장사항</h3>

        <div class="recommendation-urgent">
            <h4>⚡ 즉시 처리 (오늘)</h4>
            <ul>
                <li>AI 뉴스의 보안 관련 주제 검토 및 팀 공유</li>
                <li>#4 이슈 (에러 핸들링) 분석 및 스프린트 추가 검토</li>
                <li>최신 LLM 성능 업데이트 검토</li>
            </ul>
        </div>

        <div class="recommendation-week">
            <h4>📅 이번 주 (우선순위)</h4>
            <ul>
                <li>GitHub #4 이슈 구현 시작 (예상 소요: 3-5일)</li>
                <li>GitHub #1 이슈 검토 및 기술 스펙 작성</li>
                <li>AI 뉴스 동향 분석 리뷰</li>
            </ul>
        </div>

        <div class="recommendation-backlog">
            <h4>📋 백로그 추가</h4>
            <ul>
                <li>문서화 개선 (#3)</li>
                <li>테스트 검증 (#7)</li>
                <li>AI 뉴스 구독 시스템 강화</li>
            </ul>
        </div>
    </div>
    """

    # HTML 생성
    html_content = f'''<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>아침 브리핑 리포트 - {formatted_date}</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: 'Noto Sans KR', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 30px 20px;
            min-height: 100vh;
        }}

        .container {{
            max-width: 1000px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            overflow: hidden;
            box-shadow: 0 30px 60px rgba(0, 0, 0, 0.2);
        }}

        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 50px 40px;
            text-align: center;
        }}

        .header h1 {{
            font-size: 42px;
            margin-bottom: 10px;
            font-weight: 700;
        }}

        .header p {{
            font-size: 18px;
            opacity: 0.95;
        }}

        .content {{
            padding: 40px;
        }}

        .section {{
            margin-bottom: 40px;
        }}

        .section h3 {{
            font-size: 24px;
            color: #667eea;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 3px solid #667eea;
        }}

        .news-summary ul,
        .issue-summary ul {{
            list-style: none;
        }}

        .news-summary li,
        .issue-summary li {{
            margin-bottom: 15px;
            padding: 12px;
            background: #f8f9fa;
            border-radius: 8px;
            border-left: 4px solid #667eea;
        }}

        .issue-priority-high {{
            background: #fff5f5;
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 20px;
            border-left: 4px solid #ff6b6b;
        }}

        .issue-priority-high h4 {{
            color: #ff6b6b;
            margin-bottom: 10px;
        }}

        .issue-priority-medium {{
            background: #fffbf0;
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 20px;
            border-left: 4px solid #ffa94d;
        }}

        .issue-priority-medium h4 {{
            color: #ffa94d;
            margin-bottom: 10px;
        }}

        .issue-priority-low {{
            background: #f0fdf4;
            padding: 20px;
            border-radius: 8px;
            border-left: 4px solid #51cf66;
        }}

        .issue-priority-low h4 {{
            color: #51cf66;
            margin-bottom: 10px;
        }}

        .recommendations {{
            background: linear-gradient(135deg, #667eea15, #764ba215);
            padding: 30px;
            border-radius: 12px;
        }}

        .recommendation-urgent,
        .recommendation-week,
        .recommendation-backlog {{
            margin-bottom: 20px;
            padding: 15px;
            background: white;
            border-radius: 8px;
        }}

        .recommendation-urgent h4 {{
            color: #ff6b6b;
        }}

        .recommendation-week h4 {{
            color: #ffa94d;
        }}

        .recommendation-backlog h4 {{
            color: #51cf66;
        }}

        .footer {{
            background: #f8f9fa;
            padding: 25px 40px;
            text-align: center;
            border-top: 1px solid #e9ecef;
        }}

        .footer p {{
            color: #666;
            font-size: 14px;
            margin-bottom: 10px;
        }}

        .stats {{
            display: flex;
            gap: 20px;
            justify-content: center;
            flex-wrap: wrap;
            font-size: 13px;
            color: #999;
        }}

        @media (max-width: 768px) {{
            .container {{
                border-radius: 12px;
            }}

            .header {{
                padding: 30px 20px;
            }}

            .header h1 {{
                font-size: 28px;
            }}

            .content {{
                padding: 20px;
            }}

            .recommendations {{
                padding: 20px;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🌅 아침 브리핑</h1>
            <p>{formatted_date} | Daily AI News & Issue Analysis</p>
        </div>

        <div class="content">
            {news_summary}

            <hr style="margin: 40px 0; border: 1px solid #e9ecef;">

            {issue_summary}

            <hr style="margin: 40px 0; border: 1px solid #e9ecef;">

            {recommendations}
        </div>

        <div class="footer">
            <p>✨ Harness 팀 에이전트 시스템에서 자동 생성</p>
            <div class="stats">
                <span>📰 뉴스: 8개</span>
                <span>🔍 이슈: 4개</span>
                <span>🟠 High 우선순위: 1개</span>
                <span>🟡 Medium 우선순위: 1개</span>
            </div>
            <p style="margin-top: 15px; font-size: 12px; color: #999;">
                생성 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} |
                다음 업데이트: 내일 08:00 (JST)
            </p>
        </div>
    </div>
</body>
</html>'''

    return html_content, file_name

def main():
    """메인 함수"""
    print("🌅 아침 브리핑 리포트 생성 중...\n")

    try:
        html_content, file_name = generate_morning_briefing()

        # 파일 저장
        file_path = OUTPUT_DIR / f"{file_name}.html"
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(html_content)

        print(f"✅ 완료! 최종 브리핑이 생성되었습니다:")
        print(f"   📄 {file_path}")
        print(f"   📰 뉴스: 8개")
        print(f"   🔍 이슈 분석: 4개")
        print(f"   🟠 High 우선순위: 1개")
        print(f"   🟡 Medium 우선순위: 1개\n")

        return 0

    except Exception as e:
        logger.error(f"오류 발생: {str(e)}", exc_info=True)
        return 1

def main() -> int:
    """
    메인 함수

    Returns:
        0 (성공) 또는 1 (실패)
    """
    logger.info("아침 브리핑 리포트 생성 시작")

    try:
        html_content, file_name = generate_morning_briefing()
        file_path = OUTPUT_DIR / f"{file_name}.html"

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(html_content)

        logger.info(f"리포트 생성 완료: {file_path}")
        return 0

    except Exception as e:
        logger.error(f"오류 발생: {str(e)}", exc_info=True)
        return 1

if __name__ == '__main__':
    sys.exit(main())
