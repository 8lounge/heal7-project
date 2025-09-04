"""
🕷️ HEAL7 3-단계 크롤링 시스템 (간소화)
- 단계 1: httpx (단순 HTTP 요청)
- 단계 2: httpx + BeautifulSoup (HTML 파싱 필요시)
- 단계 3: Playwright (JavaScript 렌더링 필요시)
"""

from .base_crawler import BaseCrawler, CrawlResult, CrawlerType, CrawlConfig
from .httpx_crawler import HttpxCrawler
from .playwright_crawler import PlaywrightCrawler

__all__ = [
    'BaseCrawler',
    'CrawlResult', 
    'CrawlerType',
    'CrawlConfig',
    'HttpxCrawler',
    'PlaywrightCrawler'
]