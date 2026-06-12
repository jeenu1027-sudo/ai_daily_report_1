# 한국 AI 뉴스 RSS 통합 구현 가이드

이 문서는 현재의 `news_fetcher.py`에 한국 AI 뉴스 RSS 소스를 통합하는 방법을 설명합니다.

---

## 🎯 개요

현재 구현 상황:
- ✅ 영어 뉴스: Hacker News, Bloomberg, The Verge, Ars Technica
- ✅ 한국 소스: GitHub AI 프로젝트, Medium (혼합)
- ❌ **한국 AI 뉴스**: 전담 소스 없음

목표:
- **한국 AI 뉴스 5-10개 항목을 최우선으로 표시**
- **안정적인 RSS 피드 사용 (크롤링 최소화)**
- **일일 자동 수집 (08:00 JST 작동)**

---

## 📝 권장 코드 구현

### 방식 1: 최소 변경 (권장)

`news_fetcher.py`의 `fetch_ai_news()` 함수에 다음을 추가:

```python
def fetch_korean_ai_news():
    """한국 AI 뉴스를 우선순위 높게 수집"""
    korean_sources = [
        {
            'url': 'https://www.venturesquare.net/feed',
            'name': '🇰🇷 VentureSquare'
        },
        {
            'url': 'https://news.google.com/rss/search?q=AI%20%ED%95%9C%EA%B5%AD&hl=ko&gl=KR&ceid=KR:ko',
            'name': '🇰🇷 Google News Korea'
        },
        {
            'url': 'https://zdnet.co.kr/feed/',
            'name': '🇰🇷 ZDNet Korea'
        },
    ]
    
    all_news = []
    
    for source in korean_sources:
        news = fetch_rss_feed(source['url'], source['name'])
        all_news.extend(news)
    
    return all_news

def fetch_ai_news():
    """AI 관련 뉴스 수집 - 한국 우선"""
    all_news = []
    
    # 1. 한국 뉴스 최우선
    korean_news = fetch_korean_ai_news()
    all_news.extend(korean_news)
    
    # 2. 영어 뉴스 (기존)
    hn_news = fetch_hacker_news()
    all_news.extend(hn_news)
    
    sources = [
        {'url': 'https://feeds.bloomberg.com/markets/news.rss', 'name': 'Bloomberg'},
        {'url': 'https://feeds.theverge.com/theverge/index.xml', 'name': 'The Verge'},
        {'url': 'https://feeds.arstechnica.com/arstechnica/index', 'name': 'Ars Technica'},
    ]
    
    for source in sources:
        news = fetch_rss_feed(source['url'], source['name'])
        all_news.extend(news)
    
    # 3. 한국 GitHub (기존)
    korean_github = fetch_korean_github_ai()
    all_news.extend(korean_github)
    
    korean_medium = fetch_korean_medium_ai()
    all_news.extend(korean_medium)
    
    # 중복 제거
    seen = set()
    unique_news = []
    
    for item in all_news:
        if item['title'] not in seen:
            seen.add(item['title'])
            unique_news.append(item)
    
    # 한국 뉴스를 절대 우선순위로 앞에 배치
    korean_tagged = [item for item in unique_news if '🇰🇷' in item.get('source', '')]
    other_news = [item for item in unique_news if '🇰🇷' not in item.get('source', '')]
    
    # 한국 뉴스를 앞에 배치하고 최대 20개 반환 (한국 8-10 + 영어 10-12)
    prioritized_news = korean_tagged + other_news
    return prioritized_news[:20]
```

---

## 📊 예상 결과

### Before (현재)
```
1. [Hacker News] LLM training breakthrough...
2. [The Verge] Tech company launches AI...
3. [Medium] Machine learning tutorial...
...
```

### After (개선)
```
1. [🇰🇷 VentureSquare] 스타트업이 AI 기술을 어떻게...
2. [🇰🇷 Google News Korea] AI 정책 관련 뉴스
3. [🇰🇷 ZDNet Korea] 한국 기업 AI 투자...
4. [Hacker News] LLM training breakthrough...
5. [The Verge] Tech company launches AI...
...
```

---

## 🔄 방식 2: 향상된 구현

더 나은 필터링과 카테고리 분류:

```python
def fetch_korean_ai_news_advanced():
    """한국 AI 뉴스 수집 - 향상된 필터링"""
    korean_sources = [
        {
            'url': 'https://www.venturesquare.net/feed',
            'name': '🇰🇷 VentureSquare',
            'priority': 'high',
            'ai_keywords': ['AI', '인공지능', 'LLM', '생성형', 'GPT', 'Claude', '머신러닝']
        },
        {
            'url': 'https://news.google.com/rss/search?q=AI%20%ED%95%9C%EA%B5%AD&hl=ko&gl=KR&ceid=KR:ko',
            'name': '🇰🇷 Google News Korea',
            'priority': 'high',
            'ai_keywords': []  # 이미 AI 필터링된 쿼리
        },
        {
            'url': 'https://zdnet.co.kr/feed/',
            'name': '🇰🇷 ZDNet Korea',
            'priority': 'medium',
            'ai_keywords': ['AI', 'IT', '기술']
        },
        {
            'url': 'https://www.itworld.co.kr/feed/',
            'name': '🇰🇷 IT World',
            'priority': 'medium',
            'ai_keywords': ['AI', 'IT', '기술']
        },
    ]
    
    all_news = []
    
    for source in korean_sources:
        try:
            news = fetch_rss_feed(source['url'], source['name'])
            
            # 우선순위 태그 추가
            for item in news:
                item['korean_priority'] = source['priority']
                item['source_id'] = source['name']
            
            all_news.extend(news)
        except Exception as e:
            print(f"⚠️  {source['name']} 수집 실패: {str(e)}")
            continue
    
    return all_news

def fetch_ai_news_advanced():
    """AI 관련 뉴스 수집 - 우선순위 기반"""
    all_news = []
    
    # 1. 한국 뉴스 - HIGH 우선순위
    korean_high = [n for n in fetch_korean_ai_news_advanced() if n.get('korean_priority') == 'high']
    all_news.extend(korean_high)
    
    # 2. 한국 뉴스 - MEDIUM 우선순위
    korean_medium = [n for n in fetch_korean_ai_news_advanced() if n.get('korean_priority') == 'medium']
    all_news.extend(korean_medium)
    
    # 3. 영어 뉴스
    hn_news = fetch_hacker_news()
    all_news.extend(hn_news)
    
    # ... 나머지 영어 소스 ...
    
    # 중복 제거 및 정렬
    seen = set()
    unique_news = []
    
    for item in all_news:
        if item['title'] not in seen:
            seen.add(item['title'])
            unique_news.append(item)
    
    return unique_news[:20]
```

---

## 🛠️ 업데이트 체크리스트

구현 전 확인사항:

- [ ] `fetch_korean_ai_news()` 함수 추가
- [ ] `fetch_ai_news()` 함수 수정 (한국 우선순위 추가)
- [ ] RSS 타임아웃 설정 (5-10초)
- [ ] 에러 핸들링 추가
- [ ] 로깅 추가 (각 소스별 수집 상태)
- [ ] 테스트: `python news_fetcher.py` 실행
- [ ] 수집된 한국 뉴스 수 확인 (5-10개 예상)
- [ ] HTML 리포트에서 한국 뉴스가 상단에 표시되는지 확인
- [ ] 배치 작업 테스트 (08:00 JST 실행)

---

## 🚨 주의사항

### Google News Korea RSS 특징
```
URL: https://news.google.com/rss/search?q=AI%20%ED%95%9C%EA%B5%AD&hl=ko&gl=KR&ceid=KR:ko

파라미터 설명:
- q=AI%20%ED%95%9C%EA%B5%AD : 검색 쿼리 ("AI 한국")
- hl=ko : 한국어 인터페이스
- gl=KR : 한국 위치
- ceid=KR:ko : 한국 시간대

중요: 
- URL을 정확히 유지해야 함 (파라미터 변경 금지)
- Google 약관 준수 필요
- 과도한 요청 피하기 (1시간에 1-2회 권장)
```

### RSS 파싱 호환성
```python
# 모든 소스가 다음과 호환됨:

# RSS 2.0 형식
root.findall('.//item')
title_elem = item.find('title')

# Atom 1.0 형식
root.findall('.//{http://www.w3.org/2005/Atom}entry')
title_elem = item.find('{http://www.w3.org/2005/Atom}title')
```

---

## 📈 성능 최적화

### 타임아웃 설정
```python
# 개선 전
response = requests.get(url, timeout=10)

# 개선 후
if 'google' in url.lower():
    response = requests.get(url, timeout=15)  # Google News는 느릴 수 있음
else:
    response = requests.get(url, timeout=8)
```

### 캐싱 전략
```python
import time
from pathlib import Path

CACHE_DIR = Path(__file__).parent / '.cache'
CACHE_TTL = 3600  # 1시간

def get_cached_feed(url, name):
    """RSS 피드 캐싱"""
    cache_file = CACHE_DIR / f"{name.replace(' ', '_')}.xml"
    
    # 캐시 확인
    if cache_file.exists():
        age = time.time() - cache_file.stat().st_mtime
        if age < CACHE_TTL:
            with open(cache_file, 'r', encoding='utf-8') as f:
                return f.read()
    
    # 새로 수집
    response = requests.get(url, timeout=10)
    
    # 캐시에 저장
    CACHE_DIR.mkdir(exist_ok=True)
    with open(cache_file, 'w', encoding='utf-8') as f:
        f.write(response.text)
    
    return response.text
```

---

## 🧪 테스트 코드

통합 후 검증:

```python
def test_korean_ai_news():
    """한국 AI 뉴스 수집 테스트"""
    news = fetch_korean_ai_news()
    
    print(f"✓ 수집된 한국 뉴스: {len(news)}개")
    
    for i, item in enumerate(news[:3], 1):
        print(f"\n{i}. [{item['source']}]")
        print(f"   Title: {item['title']}")
        print(f"   Category: {item.get('category', 'N/A')}")
        print(f"   URL: {item.get('url', 'N/A')}")
    
    # 검증
    assert len(news) > 0, "한국 뉴스가 수집되지 않았습니다"
    assert any('🇰🇷' in item['source'] for item in news), "한국 뉴스 태그가 없습니다"
    
    print("\n✓ 모든 테스트 통과")

# 실행
if __name__ == '__main__':
    test_korean_ai_news()
```

---

## 📋 마이그레이션 계획

단계별 구현:

### Phase 1: 검증 (1일)
```bash
# 1. RSS 피드 접근성 확인
python test_rss_feeds.py

# 2. 콘텐츠 샘플 확인
# 예상: 한국 뉴스 5-10개/시간
```

### Phase 2: 통합 (1-2일)
```bash
# 1. news_fetcher.py 수정
# 2. 로컬 테스트
python news_fetcher.py

# 3. HTML 리포트 확인
# 한국 뉴스가 상단에 표시되는지 확인
```

### Phase 3: 배포 (1일)
```bash
# 1. GitHub 커밋
git add news_fetcher.py
git commit -m "Add Korean AI news RSS sources"

# 2. 스케줄된 작업 재실행
# 08:00 JST 자동 실행 확인
```

### Phase 4: 모니터링 (지속)
```bash
# 일일 확인:
# - 한국 뉴스 수 (5-10개 예상)
# - 중복 제거 정상 작동
# - RSS 피드 접근성 (모두 OK)
# - HTML 리포트 생성 (매일 08:00)
```

---

## 💾 구성 파일 예제

`.env` 또는 `settings.json`에 다음 추가:

```json
{
  "korean_news_sources": [
    {
      "name": "VentureSquare",
      "url": "https://www.venturesquare.net/feed",
      "enabled": true,
      "priority": "high"
    },
    {
      "name": "Google News Korea AI",
      "url": "https://news.google.com/rss/search?q=AI%20%ED%95%9C%EA%B5%AD&hl=ko&gl=KR&ceid=KR:ko",
      "enabled": true,
      "priority": "high"
    },
    {
      "name": "ZDNet Korea",
      "url": "https://zdnet.co.kr/feed/",
      "enabled": true,
      "priority": "medium"
    },
    {
      "name": "IT World Korea",
      "url": "https://www.itworld.co.kr/feed/",
      "enabled": true,
      "priority": "medium"
    }
  ],
  "rss_timeout": 10,
  "rss_cache_ttl": 3600
}
```

---

## 🎓 참고자료

관련 문서:
- 상세 분석: `KOREAN_AI_NEWS_SOURCES.md`
- 기존 구현: `news_fetcher.py`
- 스케줄: `SCHEDULE_SETUP.md`

---

**작성일**: 2026년 6월 12일  
**상태**: 구현 가능 (테스트 권장)
