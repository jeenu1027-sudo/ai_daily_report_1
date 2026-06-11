#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import io

# UTF-8 인코딩 설정
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import requests
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path

OUTPUT_DIR = Path(__file__).parent

# AI 뉴스 관련 키워드
AI_KEYWORDS = [
    'AI', 'artificial intelligence', 'machine learning', 'deep learning',
    'neural', 'LLM', 'GPT', 'Claude', 'model', 'training', 'algorithm',
    'transformer', 'neural network', 'data science', 'automation'
]

def is_ai_related(title, description=''):
    """AI 관련 뉴스인지 확인"""
    text = (title + ' ' + description).lower()
    return any(keyword.lower() in text for keyword in AI_KEYWORDS)

def fetch_hacker_news():
    """Hacker News에서 AI 관련 뉴스 수집"""
    try:
        print("📰 Hacker News에서 뉴스를 수집 중...")
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        response = requests.get('https://news.ycombinator.com/', headers=headers, timeout=10)
        response.encoding = 'utf-8'

        soup = BeautifulSoup(response.content, 'html.parser')
        news = []

        for item in soup.find_all('span', class_='titleline')[:30]:
            link = item.find('a')
            if link:
                title = link.get_text()
                url = link.get('href', '')

                if is_ai_related(title):
                    news.append({
                        'title': title[:100],
                        'url': url[:500] if url else '',
                        'source': 'Hacker News'
                    })

        return news[:5]
    except Exception as e:
        print(f"❌ Hacker News 수집 실패: {str(e)}")
        return []

def fetch_rss_feed(feed_url, source_name):
    """RSS 피드에서 뉴스 수집"""
    try:
        print(f"📰 {source_name}에서 뉴스를 수집 중...")
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        response = requests.get(feed_url, headers=headers, timeout=10)
        response.encoding = 'utf-8'

        root = ET.fromstring(response.content)
        news = []

        # RSS/Atom 네임스페이스 처리
        namespaces = {
            '': 'http://www.w3.org/2005/Atom',
            'content': 'http://purl.org/rss/1.0/modules/content/'
        }

        # Atom 형식
        items = root.findall('.//item') or root.findall('.//{http://www.w3.org/2005/Atom}entry')

        for item in items[:15]:
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
                    'source': source_name
                })

        return news[:3]
    except Exception as e:
        print(f"❌ {source_name} 수집 실패: {str(e)}")
        return []

def fetch_ai_news():
    """AI 관련 뉴스 수집"""
    all_news = []

    # Hacker News
    hn_news = fetch_hacker_news()
    all_news.extend(hn_news)

    # RSS 피드 소스
    sources = [
        {
            'url': 'https://feeds.bloomberg.com/markets/news.rss',
            'name': 'Bloomberg'
        },
        {
            'url': 'https://feeds2.wired.com/feed/category/ai/rss',
            'name': 'Wired'
        },
        {
            'url': 'https://feeds.theverge.com/theverge/index.xml',
            'name': 'The Verge'
        },
    ]

    for source in sources:
        news = fetch_rss_feed(source['url'], source['name'])
        all_news.extend(news)

    # 중복 제거
    seen = set()
    unique_news = []

    for item in all_news:
        if item['title'] not in seen:
            seen.add(item['title'])
            unique_news.append(item)

    return unique_news[:10]

def generate_html(news_items):
    """HTML 리포트 생성"""
    today = datetime.now()
    formatted_date = today.strftime('%Y년 %m월 %d일')
    file_name = f"ai-news-digest-{today.strftime('%Y-%m-%d')}"

    news_html = ''
    for idx, news in enumerate(news_items, 1):
        news_html += f'''
      <div class="news-item">
        <h3>{idx}. {news['title']}</h3>
        <p class="source">출처: {news['source']}</p>
        {f'<p class="link"><a href="{news["url"]}" target="_blank">기사 보기 →</a></p>' if news['url'] else ''}
      </div>
    '''

    # 뉴스가 없을 경우
    if not news_html:
        news_html = '<p style="text-align: center; color: #9ca3af;">뉴스를 불러올 수 없습니다. 나중에 다시 시도해주세요.</p>'

    html_content = f'''<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI 동향 뉴스 리포트 - {formatted_date}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Noto Sans KR', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            min-height: 100vh;
        }}

        .container {{
            max-width: 800px;
            margin: 0 auto;
            background: white;
            border-radius: 12px;
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.1);
            overflow: hidden;
        }}

        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px 30px;
            text-align: center;
        }}

        .header h1 {{
            font-size: 28px;
            margin-bottom: 10px;
            font-weight: 700;
        }}

        .header p {{
            font-size: 16px;
            opacity: 0.95;
        }}

        .content {{
            padding: 40px 30px;
        }}

        .news-item {{
            margin-bottom: 30px;
            padding-bottom: 30px;
            border-bottom: 1px solid #e5e7eb;
            transition: transform 0.2s ease;
        }}

        .news-item:last-child {{
            border-bottom: none;
            margin-bottom: 0;
            padding-bottom: 0;
        }}

        .news-item h3 {{
            font-size: 18px;
            color: #1f2937;
            margin-bottom: 12px;
            line-height: 1.5;
            font-weight: 600;
        }}

        .news-item .source {{
            font-size: 14px;
            color: #6b7280;
            margin-bottom: 10px;
            display: inline-block;
            background: #f3f4f6;
            padding: 4px 12px;
            border-radius: 20px;
        }}

        .news-item .link {{
            margin-top: 12px;
        }}

        .news-item a {{
            color: #667eea;
            text-decoration: none;
            font-weight: 500;
            transition: color 0.2s ease;
        }}

        .news-item a:hover {{
            color: #764ba2;
            text-decoration: underline;
        }}

        .footer {{
            background: #f9fafb;
            padding: 20px 30px;
            text-align: center;
            font-size: 14px;
            color: #6b7280;
            border-top: 1px solid #e5e7eb;
        }}

        @media (max-width: 640px) {{
            body {{
                padding: 10px;
            }}

            .header {{
                padding: 30px 20px;
            }}

            .header h1 {{
                font-size: 24px;
            }}

            .content {{
                padding: 20px;
            }}

            .news-item h3 {{
                font-size: 16px;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🤖 AI 동향 뉴스 리포트</h1>
            <p>{formatted_date}</p>
        </div>

        <div class="content">
            {news_html}
        </div>

        <div class="footer">
            <p>매일 아침 8시 (JST)에 자동으로 생성됩니다 | 최신 AI 뉴스로 업데이트를 유지하세요</p>
        </div>
    </div>
</body>
</html>'''

    return html_content, file_name

def main():
    """메인 함수"""
    print("🚀 AI 뉴스 수집을 시작합니다...\n")

    try:
        # 뉴스 수집
        news_items = fetch_ai_news()

        if not news_items:
            print("⚠️  뉴스를 찾을 수 없습니다. 샘플 데이터를 사용합니다.")
            news_items = [{
                'title': 'AI 기술이 빠르게 발전하고 있습니다',
                'url': 'https://example.com',
                'source': 'Sample'
            }]

        # HTML 생성
        html_content, file_name = generate_html(news_items)

        # 파일 저장
        file_path = OUTPUT_DIR / f"{file_name}.html"
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(html_content)

        print(f"✅ 완료! 파일이 생성되었습니다:")
        print(f"   📄 {file_path}")
        print(f"   📰 총 {len(news_items)}개의 뉴스가 수집되었습니다.\n")

        return 0

    except Exception as e:
        print(f"❌ 오류 발생: {str(e)}")
        return 1

if __name__ == '__main__':
    sys.exit(main())
