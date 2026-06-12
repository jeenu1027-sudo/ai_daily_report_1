#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import io
import logging
import time
from functools import wraps
from typing import List, Dict, Tuple, Optional

# UTF-8 인코딩 설정
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import requests
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path

OUTPUT_DIR = Path(__file__).parent
LOG_DIR = OUTPUT_DIR / "logs"
LOG_DIR.mkdir(exist_ok=True)

# 로거 설정
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# 파일 핸들러
log_file = LOG_DIR / "news_fetcher.log"
fh = logging.FileHandler(log_file, encoding='utf-8')
fh.setLevel(logging.INFO)
fh.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S'))

# 콘솔 핸들러
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
ch.setFormatter(logging.Formatter('%(levelname)s: %(message)s'))

# 기존 핸들러 제거 (중복 방지)
logger.handlers.clear()
logger.addHandler(fh)
logger.addHandler(ch)

# AI 뉴스 관련 키워드 (한글)
AI_KEYWORDS = [
    'AI', '인공지능', '머신러닝', '딥러닝',
    '신경망', 'LLM', 'GPT', 'Claude', '모델', '학습', '알고리즘',
    '트랜스포머', '언어모델', '데이터', '자동화', '챗봇',
    '생성형', '이미지생성', '음성인식', '자연어'
]

# 카테고리 매핑
CATEGORY_MAPPING = {
    'gpt': '생성형 AI',
    'chatgpt': '생성형 AI',
    'claude': '생성형 AI',
    'llm': '대형언어모델',
    '머신러닝': '머신러닝',
    '딥러닝': '딥러닝',
    '신경망': '신경망',
    '트랜스포머': '트랜스포머',
    '학습': '모델 학습',
    '알고리즘': '알고리즘',
    '데이터': '데이터',
    '자동화': '자동화',
    '생성형': '생성형 AI',
    '이미지': '이미지생성',
    '음성': '음성인식'
}

# AI 생성 기사 감지 키워드
AI_GENERATED_KEYWORDS = [
    'AI가 작성', 'AI가 쓴', 'AI 생성', 'ChatGPT가 작성',
    'Claude가 작성', 'GPT가 생성', '인공지능 생성', '자동 생성',
    'AI 기사', 'AI 뉴스', '생성형 AI가', 'AI로 만든'
]

# 논문/학술자료 감지 키워드
ACADEMIC_KEYWORDS = [
    '논문', 'arXiv', 'PDF', '연구', '학술', '페이퍼',
    '백서', '리서치', '저널', '저자', '인용'
]

# GitHub 콘텐츠 감지 키워드
GITHUB_KEYWORDS = [
    'github', 'repository', '저장소', '코드', 'commit',
    'pull request', 'issue', '오픈소스', 'open source',
    'github.com', 'repo', 'fork', 'star'
]

def retry_with_backoff(max_retries: int = 3, base_delay: int = 1):
    """Exponential backoff를 사용한 재시도 데코레이터"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            delay = base_delay
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except requests.RequestException as e:
                    if attempt == max_retries - 1:
                        logger.error(f"최종 실패 ({max_retries}회 재시도): {str(e)}")
                        raise
                    logger.warning(f"재시도 {attempt+1}/{max_retries} (대기 {delay}초)... - {str(e)[:50]}")
                    time.sleep(delay)
                    delay *= 2
            return None
        return wrapper
    return decorator

def get_category(title: str) -> str:
    """뉴스 제목 기반 한글 카테고리 생성"""
    title_lower = title.lower()
    for keyword, category in CATEGORY_MAPPING.items():
        if keyword in title_lower:
            return category
    return 'AI 뉴스'

def is_ai_related(title: str, description: str = '') -> bool:
    """AI 관련 뉴스인지 확인"""
    text = (title + ' ' + description).lower()
    return any(keyword.lower() in text for keyword in AI_KEYWORDS)

def is_generated_by_ai(title: str, description: str = '') -> bool:
    """AI가 생성한 기사인지 감지"""
    text = (title + ' ' + description).lower()
    return any(keyword.lower() in text for keyword in AI_GENERATED_KEYWORDS)

def is_academic_paper(title: str, description: str = '') -> bool:
    """논문/학술자료인지 감지"""
    text = (title + ' ' + description).lower()
    return any(keyword.lower() in text for keyword in ACADEMIC_KEYWORDS)

def is_github_content(title: str, description: str = '') -> bool:
    """GitHub 콘텐츠인지 감지"""
    text = (title + ' ' + description).lower()
    return any(keyword.lower() in text for keyword in GITHUB_KEYWORDS)

def calculate_quality_score(
    title: str,
    description: str = '',
    source: str = '',
    published_date: Optional[str] = None
) -> int:
    """
    뉴스 기사의 품질 점수 계산 (0-100점)

    신선도(30점) + 길이(40점) + 출처신뢰도(30점) = 최대 100점

    Args:
        title: 기사 제목
        description: 기사 설명/본문
        source: 출처명
        published_date: 게시 날짜 (ISO format)

    Returns:
        품질 점수 (0-100)
    """
    score = 0

    # 신선도 점수 (0-30점) - 기본값 30점 (최근 뉴스 가정)
    if published_date:
        try:
            pub_date = datetime.fromisoformat(published_date)
            age_days = (datetime.now() - pub_date).days
            if age_days == 0:
                score += 30
            elif age_days <= 7:
                score += 20
            elif age_days <= 30:
                score += 10
            else:
                score += 5
        except Exception:
            score += 25  # 파싱 실패 시에도 충분한 점수
    else:
        score += 30  # 날짜 없으면 최근 뉴스로 가정

    # 길이 점수 (0-40점)
    content_length = len(description.split())
    if content_length >= 500:
        score += 40
    elif content_length >= 300:
        score += 20
    elif content_length >= 100:
        score += 10
    else:
        score += 5  # 매우 짧은 설명도 기본 점수

    # 출처 신뢰도 (0-30점)
    trusted_sources = ['VentureSquare', 'ZDNet', 'IT World', 'Hankyoreh']
    if any(trusted in source for trusted in trusted_sources):
        score += 30
    else:
        score += 15

    return min(score, 100)

def measure_filtering_effectiveness(
    original_items: List[Dict[str, str]],
    filtered_items: List[Dict[str, str]]
) -> Dict[str, float]:
    """필터링 전후 효과 측정"""
    quality_scores = [
        calculate_quality_score(
            item.get('title', ''),
            item.get('description', ''),
            item.get('source', '')
        )
        for item in filtered_items
    ]

    filter_rate = len(filtered_items) / len(original_items) if original_items else 0
    avg_quality = sum(quality_scores) / len(quality_scores) if quality_scores else 0

    return {
        'total_original': len(original_items),
        'total_filtered': len(filtered_items),
        'filter_rate': filter_rate,
        'avg_quality_score': round(avg_quality, 1)
    }

def fetch_korean_news_sources() -> List[Dict[str, str]]:
    """한국 AI 뉴스 소스 통합 수집"""
    korean_sources = [
        {
            'url': 'https://www.venturesquare.net/feed',
            'name': '🇰🇷 VentureSquare',
            'priority': 3
        },
        {
            'url': 'https://feeds.zdnet.co.kr/zdnet/',
            'name': '🇰🇷 ZDNet Korea',
            'priority': 2
        },
        {
            'url': 'https://www.itworld.co.kr/feed/',
            'name': '🇰🇷 IT World Korea',
            'priority': 2
        },
        {
            'url': 'https://www.hani.co.kr/rss/science/',
            'name': '🇰🇷 The Hankyoreh',
            'priority': 2
        },
    ]

    all_news = []
    for source in korean_sources:
        news = fetch_rss_feed(source['url'], source['name'])
        # 필터링 적용
        filtered_news = []
        for item in news:
            title = item.get('title', '')
            if (is_ai_related(title) and
                not is_generated_by_ai(title) and
                not is_academic_paper(title) and
                not is_github_content(title)):
                # 품질 점수 계산 후 추가
                item['quality_score'] = calculate_quality_score(
                    title,
                    item.get('description', ''),
                    item.get('source', '')
                )
                filtered_news.append(item)
        all_news.extend(filtered_news)

    return all_news

@retry_with_backoff(max_retries=3, base_delay=1)
def fetch_rss_feed(feed_url: str, source_name: str) -> List[Dict[str, str]]:
    """
    RSS 피드에서 뉴스 수집

    Args:
        feed_url: RSS 피드 URL
        source_name: 뉴스 출처명

    Returns:
        뉴스 항목 리스트 (title, url, source, category, quality_score)

    Raises:
        requests.RequestException: 네트워크 오류 시
        ET.ParseError: XML 파싱 오류 시
    """
    logger.info(f"수집 중: {source_name}")
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

    try:
        response = requests.get(feed_url, headers=headers, timeout=10)
        response.raise_for_status()
    except requests.Timeout:
        logger.error(f"타임아웃: {source_name} (10초 초과)")
        return []
    except requests.ConnectionError:
        logger.error(f"연결 오류: {source_name}")
        return []
    except requests.HTTPError:
        logger.error(f"HTTP 오류: {source_name} - {response.status_code}")
        return []
    except requests.RequestException as e:
        logger.error(f"요청 오류: {source_name} - {str(e)[:100]}")
        return []

    try:
        response.encoding = 'utf-8'
        root = ET.fromstring(response.content)
    except ET.ParseError as e:
        logger.error(f"파싱 오류: {source_name} - {str(e)[:100]}")
        return []

    news = []

    # RSS/Atom 형식 항목 추출
    items = root.findall('.//item') or root.findall('.//{http://www.w3.org/2005/Atom}entry')

    for item in items[:15]:
        try:
            title_elem = item.find('title')
            if title_elem is None:
                title_elem = item.find('{http://www.w3.org/2005/Atom}title')

            link_elem = item.find('link')
            if link_elem is None:
                link_elem = item.find('{http://www.w3.org/2005/Atom}link')

            title = (title_elem.text if title_elem is not None else '')
            link = (link_elem.text if link_elem is not None else '')

            # Atom 형식의 링크 속성 처리
            if not link and link_elem is not None:
                link = link_elem.get('href', '')

            if title and is_ai_related(title):
                news.append({
                    'title': title[:100],
                    'url': link[:500] if link else '',
                    'source': source_name,
                    'category': get_category(title),
                    'description': ''
                })
        except Exception as e:
            logger.debug(f"항목 파싱 실패: {str(e)[:50]}")
            continue

    logger.info(f"수집 완료: {source_name} ({len(news)}개)")
    return news[:3]


def fetch_ai_news() -> List[Dict[str, str]]:
    """한국 AI 뉴스만 수집"""
    logger.info("한국 AI 뉴스 수집 시작")

    # 한국 뉴스 소스에서만 수집
    news_items = fetch_korean_news_sources()

    # 중복 제거
    seen = set()
    unique_news = []

    for item in news_items:
        if item['title'] not in seen:
            seen.add(item['title'])
            unique_news.append(item)

    # 최대 15개 반환
    result = unique_news[:15]
    logger.info(f"수집 완료: 총 {len(result)}개 뉴스")
    return result

def generate_html(news_items: List[Dict[str, str]]) -> Tuple[str, str]:
    """
    현대적인 디자인의 HTML 리포트 생성

    Args:
        news_items: 뉴스 항목 리스트

    Returns:
        (HTML 내용, 파일명)
    """
    today = datetime.now()
    formatted_date = today.strftime('%Y년 %m월 %d일')
    file_name = f"ai-news-digest-{today.strftime('%Y-%m-%d')}"

    # 뉴스 HTML 생성
    news_html = ''
    for idx, news in enumerate(news_items, 1):
        category = news.get('category', 'AI 뉴스')
        news_html += f'''
      <div class="news-item">
        <div class="news-number">{idx}</div>
        <div class="news-content">
          <div class="news-category">{category}</div>
          <h3>{news['title']}</h3>
          <div class="news-meta">
            <span class="source">{news['source']}</span>
          </div>
          {f'<a href="{news["url"]}" target="_blank">기사 보기 →</a>' if news['url'] else ''}
        </div>
      </div>
    '''

    html_content = f'''<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI 동향 뉴스 리포트 - {formatted_date}</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        :root {{
            --primary: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            --secondary: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            --light-bg: #f8fafc;
            --text-primary: #1e293b;
            --text-secondary: #64748b;
            --border-color: #e2e8f0;
        }}

        html {{
            scroll-behavior: smooth;
        }}

        body {{
            font-family: 'Noto Sans KR', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
            padding: 20px;
            min-height: 100vh;
            color: var(--text-primary);
            line-height: 1.6;
        }}

        .container {{
            max-width: 900px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            overflow: hidden;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.08);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.8);
            animation: slideIn 0.6s ease-out;
        }}

        @keyframes slideIn {{
            from {{
                opacity: 0;
                transform: translateY(20px);
            }}
            to {{
                opacity: 1;
                transform: translateY(0);
            }}
        }}

        .header {{
            background: var(--primary);
            color: white;
            padding: 50px 40px;
            text-align: center;
            position: relative;
            overflow: hidden;
        }}

        .header::before {{
            content: '';
            position: absolute;
            top: -50%;
            right: -50%;
            width: 200%;
            height: 200%;
            background: radial-gradient(circle, rgba(255,255,255,0.1) 1px, transparent 1px);
            background-size: 50px 50px;
            animation: drift 20s linear infinite;
        }}

        @keyframes drift {{
            0% {{
                transform: translate(0, 0);
            }}
            100% {{
                transform: translate(50px, 50px);
            }}
        }}

        .header-content {{
            position: relative;
            z-index: 1;
        }}

        .header-title {{
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 12px;
            font-size: 36px;
            font-weight: 700;
            margin-bottom: 12px;
            letter-spacing: -0.5px;
        }}

        .header-date {{
            font-size: 18px;
            opacity: 0.95;
            font-weight: 400;
            letter-spacing: 0.5px;
        }}

        .content {{
            padding: 45px 40px;
        }}

        .news-item {{
            display: flex;
            gap: 16px;
            margin-bottom: 32px;
            padding: 24px;
            background: linear-gradient(135deg, rgba(102, 126, 234, 0.05), rgba(118, 75, 162, 0.05));
            border-radius: 16px;
            border: 1px solid var(--border-color);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            position: relative;
            overflow: hidden;
        }}

        .news-item::before {{
            content: '';
            position: absolute;
            left: 0;
            top: 0;
            bottom: 0;
            width: 4px;
            background: var(--primary);
            transform: scaleY(0);
            transform-origin: center;
            transition: transform 0.3s ease;
        }}

        .news-item:hover {{
            transform: translateY(-4px);
            box-shadow: 0 12px 24px rgba(102, 126, 234, 0.15);
            border-color: rgba(102, 126, 234, 0.2);
        }}

        .news-item:hover::before {{
            transform: scaleY(1);
        }}

        .news-item:last-child {{
            margin-bottom: 0;
        }}

        .news-number {{
            display: flex;
            align-items: center;
            justify-content: center;
            width: 40px;
            height: 40px;
            min-width: 40px;
            background: var(--primary);
            color: white;
            border-radius: 10px;
            font-weight: 700;
            font-size: 16px;
            flex-shrink: 0;
        }}

        .news-content {{
            flex: 1;
        }}

        .news-category {{
            display: inline-block;
            font-size: 12px;
            font-weight: 600;
            color: white;
            background: linear-gradient(135deg, #667eea, #764ba2);
            padding: 4px 10px;
            border-radius: 12px;
            margin-bottom: 8px;
            letter-spacing: 0.5px;
        }}

        .news-item h3 {{
            font-size: 20px;
            color: var(--text-primary);
            margin-bottom: 12px;
            line-height: 1.6;
            font-weight: 600;
        }}

        .news-meta {{
            display: flex;
            align-items: center;
            gap: 12px;
            flex-wrap: wrap;
            margin-bottom: 14px;
        }}

        .source {{
            font-size: 13px;
            color: white;
            background: linear-gradient(135deg, #667eea, #764ba2);
            padding: 6px 14px;
            border-radius: 20px;
            font-weight: 500;
            letter-spacing: 0.3px;
        }}

        .news-item a {{
            display: inline-block;
            color: #667eea;
            text-decoration: none;
            font-weight: 600;
            font-size: 14px;
            padding: 8px 16px;
            background: rgba(102, 126, 234, 0.1);
            border-radius: 8px;
            transition: all 0.3s ease;
            border: 1px solid rgba(102, 126, 234, 0.2);
        }}

        .news-item a:hover {{
            background: rgba(102, 126, 234, 0.2);
            transform: translateX(4px);
            color: #764ba2;
        }}

        .empty-state {{
            text-align: center;
            padding: 60px 30px;
            color: var(--text-secondary);
        }}

        .empty-state p {{
            font-size: 16px;
        }}

        .footer {{
            background: linear-gradient(135deg, rgba(102, 126, 234, 0.05), rgba(118, 75, 162, 0.05));
            padding: 30px 40px;
            text-align: center;
            font-size: 14px;
            color: var(--text-secondary);
            border-top: 1px solid var(--border-color);
            display: flex;
            align-items: center;
            justify-content: space-between;
            flex-wrap: wrap;
            gap: 20px;
        }}

        .footer-info {{
            display: flex;
            align-items: center;
            gap: 8px;
        }}

        .stats {{
            display: flex;
            gap: 20px;
            font-size: 13px;
            color: var(--text-secondary);
            font-weight: 500;
        }}

        @media (max-width: 768px) {{
            .container {{
                border-radius: 16px;
            }}

            .header {{
                padding: 36px 24px;
            }}

            .header-title {{
                font-size: 28px;
                gap: 8px;
            }}

            .header-date {{
                font-size: 16px;
            }}

            .content {{
                padding: 28px 24px;
            }}

            .news-item {{
                padding: 20px;
                margin-bottom: 24px;
                flex-direction: column;
                gap: 12px;
            }}

            .news-item h3 {{
                font-size: 18px;
            }}

            .footer {{
                flex-direction: column;
                text-align: center;
                padding: 24px;
            }}

            .stats {{
                flex-direction: column;
                gap: 12px;
                justify-content: center;
            }}
        }}

        @media (max-width: 480px) {{
            body {{
                padding: 12px;
            }}

            .header {{
                padding: 28px 16px;
            }}

            .header-title {{
                font-size: 24px;
                gap: 6px;
            }}

            .content {{
                padding: 20px 16px;
            }}

            .news-item {{
                padding: 16px;
                margin-bottom: 20px;
            }}

            .news-number {{
                width: 36px;
                height: 36px;
                font-size: 14px;
            }}

            .news-item h3 {{
                font-size: 16px;
            }}

            .news-item a {{
                font-size: 12px;
                padding: 6px 12px;
            }}
        }}

        /* 접근성 */
        @media (prefers-reduced-motion: reduce) {{
            * {{
                animation: none !important;
                transition: none !important;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="header-content">
                <div class="header-title">
                    <span>🤖</span>
                    <span>AI 뉴스 리포트</span>
                </div>
                <div class="header-date">{formatted_date}</div>
            </div>
        </div>

        <div class="content">
            {f'<div class="empty-state"><p>📭 뉴스를 불러올 수 없습니다.<br/>나중에 다시 시도해주세요.</p></div>' if not news_html.strip() else '<div class="news-list">' + news_html + '</div>'}
        </div>

        <div class="footer">
            <div class="footer-info">
                <span>⏰ 매일 8시 (JST) 자동 생성</span>
            </div>
            <div class="stats">
                <span>📰 총 {len(news_items)}개 기사</span>
                <span>🔄 최신 업데이트</span>
            </div>
        </div>
    </div>

    <script>
        document.addEventListener('DOMContentLoaded', function() {{
            const items = document.querySelectorAll('.news-item');
            items.forEach((item, index) => {{
                item.style.animationDelay = (index * 0.1) + 's';
                item.style.animation = 'slideIn 0.6s ease-out forwards';
            }});
        }});
    </script>
</body>
</html>'''

    return html_content, file_name

def main() -> int:
    """
    메인 함수

    Returns:
        0 (성공) 또는 1 (실패)
    """
    logger.info("=" * 60)
    logger.info("AI 뉴스 수집 시작")
    logger.info("=" * 60)

    try:
        # 뉴스 수집
        news_items = fetch_ai_news()

        if not news_items:
            logger.warning("수집된 뉴스가 없습니다. 샘플 데이터를 사용합니다.")
            news_items = [{
                'title': 'AI 기술이 빠르게 발전하고 있습니다',
                'url': 'https://example.com',
                'source': 'Sample',
                'category': 'AI 뉴스',
                'quality_score': 50
            }]

        # HTML 생성
        html_content, file_name = generate_html(news_items)

        # 파일 저장
        file_path = OUTPUT_DIR / f"{file_name}.html"
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(html_content)

        logger.info(f"파일 저장: {file_path}")
        logger.info(f"수집된 뉴스: {len(news_items)}개")
        logger.info("=" * 60)
        logger.info("AI 뉴스 수집 완료")
        logger.info("=" * 60)

        return 0

    except Exception as e:
        logger.critical(f"예상 외 오류 발생: {type(e).__name__}: {str(e)}", exc_info=True)
        return 1

if __name__ == '__main__':
    sys.exit(main())
