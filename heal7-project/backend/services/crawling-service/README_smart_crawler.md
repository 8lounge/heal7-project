# 🧠 HEAL7 Smart Crawler System

3-Tier 지능형 크롤링 시스템과 멀티모달 AI 분석 통합 솔루션

## 🎯 주요 특징

### 🕷️ 3-Tier 크롤링 아키텍처
- **Tier 1**: `httpx` - 빠른 정적 사이트 및 API
- **Tier 2**: `playwright` - 동적 콘텐츠 및 JavaScript 렌더링
- **Tier 3**: `selenium + undetected` - Anti-bot 우회 및 최대 호환성

### 🤖 멀티모달 AI 분석
- **Gemini Flash** (1순위): 무료, 빠름
- **GPT-4o** (2순위): 강력한 비전 능력
- **Claude Sonnet** (3순위): 문서 이해 특화

### 🧠 지능형 기능
- 자동 폴백 시스템
- 도메인별 최적 크롤러 학습
- 성능 기반 우선순위 조정
- 실시간 상태 모니터링

## 📂 프로젝트 구조

```
crawling-service/
├── core/
│   ├── crawlers/
│   │   ├── base_crawler.py          # 크롤러 기본 클래스
│   │   ├── httpx_crawler.py         # Tier 1: httpx
│   │   ├── playwright_crawler.py    # Tier 2: Playwright
│   │   └── selenium_crawler.py      # Tier 3: Selenium
│   └── smart_crawler.py             # 통합 지능형 크롤러
├── multimodal/
│   ├── ai_analyzer.py               # 멀티모달 AI 분석
│   └── document_processor.py        # 문서 처리
├── demo_smart_crawler.py            # 데모 및 테스트
└── requirements.txt                 # 의존성
```

## 🚀 빠른 시작

### 1. 의존성 설치
```bash
pip install -r requirements.txt

# Playwright 브라우저 설치
playwright install chromium
```

### 2. API 키 설정 (선택사항)
```bash
export GEMINI_API_KEY="your-gemini-api-key"
export OPENAI_API_KEY="your-openai-api-key"  
export ANTHROPIC_API_KEY="your-anthropic-api-key"
```

### 3. 데모 실행
```bash
python demo_smart_crawler.py
```

## 💻 기본 사용법

### 단일 URL 크롤링
```python
from core.smart_crawler import SmartCrawler, CrawlStrategy

# 크롤러 생성 및 초기화
crawler = SmartCrawler()
await crawler.initialize()

# 자동 전략으로 크롤링
result = await crawler.crawl("https://example.com", strategy=CrawlStrategy.AUTO)

if result.success:
    print(f"성공! 크롤러: {result.crawler_used.value}")
    print(f"HTML 크기: {len(result.html)} bytes")
else:
    print(f"실패: {result.error}")

await crawler.cleanup()
```

### 배치 크롤링
```python
urls = [
    "https://api.github.com/users/octocat",
    "https://httpbin.org/json",
    "https://example.com"
]

results = await crawler.batch_crawl(urls, max_concurrent=3)

for result in results:
    print(f"{result.url}: {'✅' if result.success else '❌'}")
```

### 전략별 크롤링
```python
# 빠른 크롤링 (httpx 우선)
result = await crawler.crawl(url, strategy=CrawlStrategy.FAST)

# 렌더링 필요 (playwright 우선)  
result = await crawler.crawl(url, strategy=CrawlStrategy.RENDER)

# 스텔스 모드 (selenium 우선)
result = await crawler.crawl(url, strategy=CrawlStrategy.STEALTH)
```

## 🎨 멀티모달 AI 분석

### 이미지 분석
```python
from multimodal.ai_analyzer import MultimodalAnalyzer

analyzer = MultimodalAnalyzer()
await analyzer.initialize()

# 스크린샷 분석
result = await analyzer.analyze_webpage_screenshot("screenshot.png")
print(result['content'])

# 테이블 추출
table_data = await analyzer.extract_table_from_image("table_image.png")
print(table_data['parsed_tables'])
```

### 문서 처리
```python
from multimodal.document_processor import DocumentProcessor

processor = DocumentProcessor()
await processor.initialize()

# PDF 문서 처리
result = await processor.process_document("document.pdf", include_ai_analysis=True)

if result.success:
    print(f"텍스트 블록: {len(result.text_content)}")
    print(f"테이블: {len(result.tables)}")
    print(f"AI 요약: {result.ai_summary}")
```

## 🔧 고급 기능

### 크롤러 설정
```python
from core.crawlers import CrawlConfig

config = CrawlConfig(
    url="https://example.com",
    timeout=30,
    screenshot=True,
    wait_for_load=True,
    stealth_mode=True
)

result = await crawler.crawl(config)
```

### 상태 모니터링
```python
# 시스템 상태 확인
health = await crawler.health_check()
print(f"시스템 상태: {health['system_healthy']}")

# 크롤러별 통계
for crawler_type in crawler.crawlers:
    stats = crawler.get_crawler_stats(crawler_type)
    print(f"{crawler_type.value}: {stats['success_rate']:.1%} 성공률")

# 성능 최적화
crawler.optimize_performance()
```

## 📊 성능 벤치마크

### 크롤러별 특성
| 크롤러 | 속도 | JavaScript | Anti-bot | 메모리 사용량 |
|--------|------|------------|----------|---------------|
| httpx | ⭐⭐⭐⭐⭐ | ❌ | ❌ | 낮음 |
| playwright | ⭐⭐⭐ | ✅ | ⭐⭐ | 중간 |
| selenium | ⭐⭐ | ✅ | ⭐⭐⭐⭐⭐ | 높음 |

### AI 모델별 특성
| 모델 | 속도 | 비용 | 정확도 | 특화 분야 |
|------|------|------|--------|-----------|
| Gemini Flash | ⭐⭐⭐⭐⭐ | 무료 | ⭐⭐⭐⭐ | 범용 |
| GPT-4o | ⭐⭐⭐ | 유료 | ⭐⭐⭐⭐⭐ | 이미지/차트 |
| Claude Sonnet | ⭐⭐⭐⭐ | 유료 | ⭐⭐⭐⭐⭐ | 문서/테이블 |

## 🔍 트러블슈팅

### 일반적인 문제

**Q: 크롤링이 너무 느려요**
```python
# 빠른 전략 사용
result = await crawler.crawl(url, strategy=CrawlStrategy.FAST)

# 또는 httpx 직접 사용
from core.crawlers import HttpxCrawler
httpx_crawler = HttpxCrawler()
await httpx_crawler.initialize()
result = await httpx_crawler.crawl(CrawlConfig(url=url))
```

**Q: Bot 감지로 차단되어요**
```python
# 스텔스 전략 사용
result = await crawler.crawl(url, strategy=CrawlStrategy.STEALTH)

# 또는 selenium 직접 사용
from core.crawlers import SeleniumCrawler
selenium_crawler = SeleniumCrawler(use_undetected=True)
result = await selenium_crawler.solve_captcha(CrawlConfig(url=url))
```

**Q: JavaScript 렌더링이 안 돼요**
```python
# 렌더링 전략 사용
result = await crawler.crawl(url, strategy=CrawlStrategy.RENDER)

# 또는 대기 설정 추가
config = CrawlConfig(
    url=url,
    wait_for_load=True,
    wait_for_selector=".main-content"
)
```

### 로그 레벨 조정
```python
import logging
logging.getLogger('core.smart_crawler').setLevel(logging.DEBUG)
logging.getLogger('multimodal').setLevel(logging.INFO)
```

## 📈 성능 최적화 팁

1. **적절한 전략 선택**: API는 FAST, 동적 사이트는 RENDER
2. **배치 처리 활용**: 대량 URL은 `batch_crawl()` 사용
3. **AI 분석 선택적 사용**: 필요한 경우만 AI 분석 활성화
4. **캐시 활용**: 같은 도메인은 자동으로 최적 크롤러 학습
5. **리소스 정리**: 사용 후 반드시 `cleanup()` 호출

## 🤝 기여하기

1. 새로운 크롤러 추가
2. AI 모델 통합
3. 문서 형식 지원 확장
4. 성능 최적화
5. 테스트 케이스 추가

## 📄 라이선스

MIT License - 자유롭게 사용하세요!

---

**🎯 HEAL7 Smart Crawler System** - 차세대 지능형 웹 크롤링 솔루션