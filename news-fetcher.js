const fetch = require('node-fetch');
const cheerio = require('cheerio');
const fs = require('fs');
const path = require('path');
const { format } = require('date-fns');

const OUTPUT_DIR = __dirname;

// AI 뉴스 관련 키워드
const AI_KEYWORDS = ['AI', 'artificial intelligence', 'machine learning', 'deep learning', 'neural', 'LLM', 'GPT', 'Claude', 'model', 'training', 'algorithm'];

function isAIRelated(title, description = '') {
  const text = (title + ' ' + description).toLowerCase();
  return AI_KEYWORDS.some(keyword => text.includes(keyword.toLowerCase()));
}

async function fetchHackerNews() {
  try {
    const response = await fetch('https://news.ycombinator.com/', {
      headers: { 'User-Agent': 'Mozilla/5.0' }
    });
    const html = await response.text();
    const $ = cheerio.load(html);

    const news = [];
    $('.athing').slice(0, 30).each((i, elem) => {
      const title = $(elem).find('.titleline > a').first().text();
      const url = $(elem).find('.titleline > a').first().attr('href');

      if (title && isAIRelated(title)) {
        news.push({
          title: title.substring(0, 100),
          url: url || '',
          source: 'Hacker News'
        });
      }
    });

    return news.slice(0, 5);
  } catch (error) {
    console.error('Hacker News fetch error:', error.message);
    return [];
  }
}

async function fetchRSSFeed(feedUrl, source) {
  try {
    const response = await fetch(feedUrl, {
      headers: { 'User-Agent': 'Mozilla/5.0' }
    });
    const xml = await response.text();

    // 간단한 XML 파싱
    const titleMatches = xml.match(/<title[^>]*>([^<]+)<\/title>/g) || [];
    const linkMatches = xml.match(/<link[^>]*>([^<]+)<\/link>/g) || [];

    const news = [];
    titleMatches.slice(1, 11).forEach((titleTag, i) => {
      const title = titleTag.replace(/<[^>]+>/g, '');
      if (isAIRelated(title)) {
        const linkTag = linkMatches[i + 1] || '';
        const url = linkTag.replace(/<[^>]+>/g, '');

        news.push({
          title: title.substring(0, 100),
          url: url.substring(0, 500),
          source: source
        });
      }
    });

    return news.slice(0, 3);
  } catch (error) {
    console.error(`RSS feed (${source}) fetch error:`, error.message);
    return [];
  }
}

async function fetchAINews() {
  const allNews = [];

  // Hacker News에서 AI 관련 뉴스 수집
  console.log('Fetching Hacker News...');
  const hnNews = await fetchHackerNews();
  allNews.push(...hnNews);

  // 추가 소스 (RSS 피드)
  const sources = [
    { url: 'https://feeds.bloomberg.com/markets/news.rss', name: 'Bloomberg Tech' },
    { url: 'https://feeds.wired.com/feed/category/ai/rss', name: 'Wired AI' },
  ];

  for (const source of sources) {
    console.log(`Fetching ${source.name}...`);
    const news = await fetchRSSFeed(source.url, source.name);
    allNews.push(...news);
  }

  // 중복 제거
  const seen = new Set();
  const uniqueNews = [];

  allNews.forEach(item => {
    if (!seen.has(item.title)) {
      seen.add(item.title);
      uniqueNews.push(item);
    }
  });

  return uniqueNews.slice(0, 10);
}

function generateHTML(newsItems) {
  const today = new Date();
  const formattedDate = format(today, 'yyyy년 MM월 dd일');
  const fileName = `ai-news-digest-${format(today, 'yyyy-MM-dd')}`;

  const newsHTML = newsItems
    .map((news, index) => `
      <div class="news-item">
        <h3>${index + 1}. ${news.title}</h3>
        <p class="source">출처: ${news.source}</p>
        ${news.url ? `<p class="link"><a href="${news.url}" target="_blank">기사 보기 →</a></p>` : ''}
      </div>
    `)
    .join('');

  const html = `<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI 동향 뉴스 리포트 - ${formattedDate}</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Noto Sans KR', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            min-height: 100vh;
        }

        .container {
            max-width: 800px;
            margin: 0 auto;
            background: white;
            border-radius: 12px;
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.1);
            overflow: hidden;
        }

        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px 30px;
            text-align: center;
        }

        .header h1 {
            font-size: 28px;
            margin-bottom: 10px;
            font-weight: 700;
        }

        .header p {
            font-size: 16px;
            opacity: 0.95;
        }

        .content {
            padding: 40px 30px;
        }

        .news-item {
            margin-bottom: 30px;
            padding-bottom: 30px;
            border-bottom: 1px solid #e5e7eb;
            transition: transform 0.2s ease;
        }

        .news-item:last-child {
            border-bottom: none;
            margin-bottom: 0;
            padding-bottom: 0;
        }

        .news-item h3 {
            font-size: 18px;
            color: #1f2937;
            margin-bottom: 12px;
            line-height: 1.5;
            font-weight: 600;
        }

        .news-item .source {
            font-size: 14px;
            color: #6b7280;
            margin-bottom: 10px;
            display: inline-block;
            background: #f3f4f6;
            padding: 4px 12px;
            border-radius: 20px;
        }

        .news-item .link {
            margin-top: 12px;
        }

        .news-item a {
            color: #667eea;
            text-decoration: none;
            font-weight: 500;
            transition: color 0.2s ease;
        }

        .news-item a:hover {
            color: #764ba2;
            text-decoration: underline;
        }

        .footer {
            background: #f9fafb;
            padding: 20px 30px;
            text-align: center;
            font-size: 14px;
            color: #6b7280;
            border-top: 1px solid #e5e7eb;
        }

        @media (max-width: 640px) {
            body {
                padding: 10px;
            }

            .header {
                padding: 30px 20px;
            }

            .header h1 {
                font-size: 24px;
            }

            .content {
                padding: 20px;
            }

            .news-item h3 {
                font-size: 16px;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🤖 AI 동향 뉴스 리포트</h1>
            <p>${formattedDate}</p>
        </div>

        <div class="content">
            ${newsHTML || '<p style="text-align: center; color: #9ca3af;">뉴스를 불러올 수 없습니다. 나중에 다시 시도해주세요.</p>'}
        </div>

        <div class="footer">
            <p>매일 아침 8시 (JST)에 자동으로 생성됩니다 | 최신 AI 뉴스로 업데이트를 유지하세요</p>
        </div>
    </div>
</body>
</html>`;

  return { html, fileName };
}

async function main() {
  console.log('🚀 AI 뉴스 수집을 시작합니다...');

  try {
    const newsItems = await fetchAINews();

    if (newsItems.length === 0) {
      console.log('⚠️  뉴스를 찾을 수 없습니다.');
      // 샘플 뉴스로 테스트
      newsItems.push({
        title: 'AI 기술이 빠르게 발전하고 있습니다',
        url: 'https://example.com',
        source: 'Sample'
      });
    }

    const { html, fileName } = generateHTML(newsItems);
    const filePath = path.join(OUTPUT_DIR, `${fileName}.html`);

    fs.writeFileSync(filePath, html, 'utf-8');
    console.log(`✅ 완료! 파일 생성: ${filePath}`);
    console.log(`📰 총 ${newsItems.length}개의 뉴스가 수집되었습니다.`);

  } catch (error) {
    console.error('❌ 오류 발생:', error.message);
    process.exit(1);
  }
}

main();
