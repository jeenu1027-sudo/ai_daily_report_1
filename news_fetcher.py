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
            'url': 'https://feeds.theverge.com/theverge/index.xml',
            'name': 'The Verge'
        },
        {
            'url': 'https://feeds.arstechnica.com/arstechnica/index',
            'name': 'Ars Technica'
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
    """현대적인 디자인의 HTML 리포트 생성"""
    today = datetime.now()
    formatted_date = today.strftime('%Y년 %m월 %d일')
    file_name = f"ai-news-digest-{today.strftime('%Y-%m-%d')}"

    # 뉴스 HTML 생성
    news_html = ''
    for idx, news in enumerate(news_items, 1):
        news_html += f'''
      <div class="news-item">
        <div class="news-number">{idx}</div>
        <h3>{news['title']}</h3>
        <div class="news-meta">
          <span class="source">{news['source']}</span>
        </div>
        {f'<a href="{news["url"]}" target="_blank">기사 보기 →</a>' if news['url'] else ''}
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
