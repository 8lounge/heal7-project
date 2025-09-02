#!/usr/bin/env python3
"""
🕷️ 최적화된 Tier 1-3 크롤러 매니저
리소스 효율성과 성능을 극대화한 3계층 크롤링 시스템

Tier 1: httpx (경량, API/JSON 처리) - 90%+ 요청 처리
Tier 2: httpx + BeautifulSoup (정적 HTML 파싱) - 5-8% 요청 처리  
Tier 3: Playwright (동적 JavaScript 필요시만) - 2-5% 요청 처리

Author: HEAL7 Development Team
Version: 2.0.0 (Optimized)
Date: 2025-09-02
"""

import asyncio
import time
import logging
from typing import Dict, List, Any, Optional, Union, Callable
from dataclasses import dataclass, field
from enum import Enum
from urllib.parse import urlparse, urljoin
import re

from .crawlers.base_crawler import (
    BaseCrawler, CrawlResult, CrawlConfig, CrawlerType, 
    CrawlStatus, create_default_headers, is_valid_url
)
from .crawlers.httpx_crawler import HttpxCrawler

logger = logging.getLogger(__name__)


class OptimizedTier(Enum):
    """최적화된 크롤링 계층"""
    TIER1 = "tier1"  # httpx only (경량)
    TIER2 = "tier2"  # httpx + BeautifulSoup (정적 HTML)
    TIER3 = "tier3"  # Playwright (동적 JavaScript)


@dataclass
class TierMetrics:
    """계층별 성능 지표"""
    tier: OptimizedTier
    request_count: int = 0
    success_count: int = 0
    total_response_time: float = 0.0
    memory_usage: float = 0.0
    
    @property
    def success_rate(self) -> float:
        return self.success_count / max(self.request_count, 1)
    
    @property
    def avg_response_time(self) -> float:
        return self.total_response_time / max(self.request_count, 1)


class OptimizedCrawlerManager:
    """🚀 최적화된 크롤러 매니저"""
    
    def __init__(self):
        self.logger = logging.getLogger(f"{__name__}.OptimizedManager")
        
        # 계층별 크롤러 인스턴스
        self.tier1_crawler: Optional[HttpxCrawler] = None
        self.tier2_crawler: Optional[HttpxCrawler] = None  # httpx + BS4
        self.tier3_crawler = None  # Playwright (지연 로딩)
        
        # 성능 지표
        self.metrics = {
            OptimizedTier.TIER1: TierMetrics(OptimizedTier.TIER1),
            OptimizedTier.TIER2: TierMetrics(OptimizedTier.TIER2),
            OptimizedTier.TIER3: TierMetrics(OptimizedTier.TIER3),
        }
        
        # 시스템 설정
        self.tier3_threshold = 0.95  # Tier3 사용률 임계값 (95%)
        self.memory_threshold = 512  # MB 임계값
        self.is_initialized = False
        
        # URL 패턴 분류기
        self._setup_url_classifiers()
    
    def _setup_url_classifiers(self):
        """URL 패턴별 분류 규칙 설정"""
        self.tier1_patterns = [
            r'.*\.(json|xml|txt|csv)(\?.*)?$',  # 데이터 파일
            r'.*/api/.*',                        # API 엔드포인트
            r'.*/rest/.*',                       # REST API
            r'.*/v\d+/.*',                       # API 버전
            r'.*\.(pdf|doc|docx|xls|xlsx)(\?.*)?$',  # 문서 파일
        ]
        
        self.tier2_patterns = [
            r'.*\.(html?|htm)(\?.*)?$',          # HTML 파일
            r'.*/.*\.php(\?.*)?$',               # PHP 페이지
            r'.*/.*\.jsp(\?.*)?$',               # JSP 페이지
            r'.*/news/.*',                       # 뉴스 사이트
            r'.*/article/.*',                    # 기사 페이지
            r'.*/blog/.*',                       # 블로그 페이지
        ]
        
        # Tier3은 동적 컨텐츠가 확실한 경우만
        self.tier3_patterns = [
            r'.*react.*',                        # React 앱
            r'.*angular.*',                      # Angular 앱
            r'.*vue.*',                          # Vue 앱
            r'.*/spa/.*',                        # SPA 앱
        ]
        
        # 컴파일된 정규식
        self.tier1_regex = [re.compile(p, re.I) for p in self.tier1_patterns]
        self.tier2_regex = [re.compile(p, re.I) for p in self.tier2_patterns]
        self.tier3_regex = [re.compile(p, re.I) for p in self.tier3_patterns]
    
    async def initialize(self):
        """매니저 초기화"""
        if self.is_initialized:
            return
        
        try:
            # Tier 1 (httpx) 초기화
            self.tier1_crawler = HttpxCrawler()
            await self.tier1_crawler.initialize()
            
            # Tier 2 (httpx + BeautifulSoup) 초기화
            self.tier2_crawler = HttpxCrawler()
            await self.tier2_crawler.initialize()
            
            # Tier 3는 필요시에만 지연 로딩
            
            self.is_initialized = True
            self.logger.info("✅ 최적화된 크롤러 매니저 초기화 완료")
            
        except Exception as e:
            self.logger.error(f"❌ 매니저 초기화 실패: {e}")
            await self.cleanup()
            raise
    
    async def cleanup(self):
        """리소스 정리"""
        try:
            if self.tier1_crawler:
                await self.tier1_crawler.cleanup()
                
            if self.tier2_crawler:
                await self.tier2_crawler.cleanup()
            
            if self.tier3_crawler:
                await self.tier3_crawler.cleanup()
            
            self.is_initialized = False
            self.logger.info("🛑 최적화된 크롤러 매니저 정리 완료")
            
        except Exception as e:
            self.logger.error(f"❌ 정리 중 오류: {e}")
    
    def classify_url(self, url: str) -> OptimizedTier:
        """URL을 최적 계층으로 분류"""
        url_lower = url.lower()
        
        # Tier 1 패턴 확인 (최우선)
        for pattern in self.tier1_regex:
            if pattern.match(url):
                return OptimizedTier.TIER1
        
        # Tier 3 패턴 확인 (동적 컨텐츠)
        for pattern in self.tier3_regex:
            if pattern.match(url):
                return OptimizedTier.TIER3
        
        # Tier 2 패턴 확인
        for pattern in self.tier2_regex:
            if pattern.match(url):
                return OptimizedTier.TIER2
        
        # 기본값: 먼저 Tier 1로 시도
        return OptimizedTier.TIER1
    
    async def smart_crawl(self, config: CrawlConfig) -> CrawlResult:
        """지능형 크롤링 - 최적 계층 자동 선택"""
        if not self.is_initialized:
            await self.initialize()
        
        # 1. URL 분류로 초기 계층 결정
        initial_tier = self.classify_url(config.url)
        
        # 2. 계층별 순차 시도
        return await self._crawl_with_fallback(config, initial_tier)
    
    async def _crawl_with_fallback(self, config: CrawlConfig, start_tier: OptimizedTier) -> CrawlResult:
        """계층별 폴백 크롤링"""
        tiers = [OptimizedTier.TIER1, OptimizedTier.TIER2, OptimizedTier.TIER3]
        
        # 시작 계층부터 순차 시도
        start_index = tiers.index(start_tier)
        
        for i in range(start_index, len(tiers)):
            tier = tiers[i]
            
            # 메모리 사용량 체크
            if i >= 2 and await self._check_memory_usage():
                self.logger.warning("💾 메모리 사용량 임계값 초과, Tier3 생략")
                break
            
            result = await self._crawl_single_tier(config, tier)
            
            # 성공하면 반환
            if result.success or result.status == CrawlStatus.PARTIAL_SUCCESS:
                return result
            
            # Tier 1,2 실패시 다음 계층으로
            if i < len(tiers) - 1:
                self.logger.info(f"🔄 {tier.value} 실패, 다음 계층으로 시도")
        
        # 모든 계층 실패
        return CrawlResult(
            success=False,
            error="모든 크롤링 계층에서 실패",
            error_type="all_tiers_failed",
            url=config.url
        )
    
    async def _crawl_single_tier(self, config: CrawlConfig, tier: OptimizedTier) -> CrawlResult:
        """단일 계층으로 크롤링"""
        start_time = time.time()
        
        try:
            if tier == OptimizedTier.TIER1:
                result = await self._tier1_crawl(config)
            elif tier == OptimizedTier.TIER2:
                result = await self._tier2_crawl(config)
            else:  # TIER3
                result = await self._tier3_crawl(config)
            
            # 메트릭 업데이트
            self._update_metrics(tier, result, time.time() - start_time)
            
            return result
            
        except Exception as e:
            error_result = CrawlResult(
                success=False,
                error=f"{tier.value} 크롤링 오류: {e}",
                crawler_used=CrawlerType.HTTPX if tier != OptimizedTier.TIER3 else CrawlerType.PLAYWRIGHT,
                url=config.url,
                response_time=time.time() - start_time
            )
            
            self._update_metrics(tier, error_result, time.time() - start_time)
            return error_result
    
    async def _tier1_crawl(self, config: CrawlConfig) -> CrawlResult:
        """Tier 1: httpx 경량 크롤링"""
        result = await self.tier1_crawler.crawl(config)
        
        # HTML인 경우 간단한 검증
        if result.success and result.html:
            html_len = len(result.html)
            
            # 너무 적은 내용이면 동적 컨텐츠일 가능성
            if html_len < 500 and '<script' in result.html.lower():
                result.success = False
                result.error = "동적 컨텐츠 감지, 상위 계층 필요"
                result.status = CrawlStatus.PARTIAL_SUCCESS
        
        return result
    
    async def _tier2_crawl(self, config: CrawlConfig) -> CrawlResult:
        """Tier 2: httpx + BeautifulSoup 정적 HTML 처리"""
        from bs4 import BeautifulSoup
        
        # httpx로 기본 크롤링
        result = await self.tier2_crawler.crawl(config)
        
        if result.success and result.html:
            try:
                # BeautifulSoup로 HTML 파싱 및 정제
                soup = BeautifulSoup(result.html, 'html.parser')
                
                # 메타데이터 추출
                metadata = result.metadata or {}
                metadata.update({
                    'title': soup.title.text.strip() if soup.title else '',
                    'meta_description': '',
                    'links_count': len(soup.find_all('a')),
                    'images_count': len(soup.find_all('img')),
                    'scripts_count': len(soup.find_all('script')),
                    'processing_tier': 'tier2'
                })
                
                # 메타 설명 추출
                meta_desc = soup.find('meta', attrs={'name': 'description'})
                if meta_desc:
                    metadata['meta_description'] = meta_desc.get('content', '')[:200]
                
                # JavaScript가 많으면 동적 컨텐츠 가능성 표시
                if metadata['scripts_count'] > 10:
                    metadata['dynamic_content_likely'] = True
                    
                    # 내용이 적으면 Tier3 필요 시사
                    visible_text = soup.get_text().strip()
                    if len(visible_text) < 1000:
                        result.success = False
                        result.error = "JavaScript 렌더링 필요 가능성"
                        result.status = CrawlStatus.PARTIAL_SUCCESS
                
                result.metadata = metadata
                
            except Exception as e:
                self.logger.warning(f"BeautifulSoup 처리 중 오류: {e}")
                # 원본 결과 유지
        
        return result
    
    async def _tier3_crawl(self, config: CrawlConfig) -> CrawlResult:
        """Tier 3: Playwright 동적 컨텐츠 처리 (지연 로딩)"""
        if not self.tier3_crawler:
            await self._initialize_tier3()
        
        return await self.tier3_crawler.crawl(config)
    
    async def _initialize_tier3(self):
        """Tier 3 지연 초기화"""
        try:
            from .crawlers.playwright_crawler import PlaywrightCrawler
            self.tier3_crawler = PlaywrightCrawler(headless=True)
            await self.tier3_crawler.initialize()
            
            self.logger.info("🎭 Tier 3 (Playwright) 지연 초기화 완료")
            
        except ImportError:
            self.logger.warning("⚠️ Playwright 모듈 없음, Tier 3 비활성화")
            raise
        except Exception as e:
            self.logger.error(f"❌ Tier 3 초기화 실패: {e}")
            raise
    
    async def _check_memory_usage(self) -> bool:
        """메모리 사용량 확인"""
        try:
            import psutil
            memory = psutil.virtual_memory()
            used_mb = memory.used / 1024 / 1024
            return used_mb > self.memory_threshold
        except ImportError:
            return False
        except Exception:
            return False
    
    def _update_metrics(self, tier: OptimizedTier, result: CrawlResult, response_time: float):
        """메트릭 업데이트"""
        metric = self.metrics[tier]
        metric.request_count += 1
        metric.total_response_time += response_time
        
        if result.success:
            metric.success_count += 1
    
    async def batch_crawl(self, urls: List[str], max_concurrent: int = 5) -> List[CrawlResult]:
        """배치 크롤링 (최적화된 동시 처리)"""
        if not self.is_initialized:
            await self.initialize()
        
        # 동시 실행 제한
        semaphore = asyncio.Semaphore(max_concurrent)
        
        async def crawl_single(url: str) -> CrawlResult:
            async with semaphore:
                config = CrawlConfig(url=url)
                return await self.smart_crawl(config)
        
        tasks = [crawl_single(url) for url in urls]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # 예외 처리
        processed_results = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                processed_results.append(CrawlResult(
                    success=False,
                    error=str(result),
                    url=urls[i]
                ))
            else:
                processed_results.append(result)
        
        return processed_results
    
    def get_performance_report(self) -> Dict[str, Any]:
        """성능 보고서 생성"""
        report = {
            'total_requests': sum(m.request_count for m in self.metrics.values()),
            'tier_distribution': {},
            'performance_summary': {}
        }
        
        for tier, metric in self.metrics.items():
            if metric.request_count > 0:
                report['tier_distribution'][tier.value] = {
                    'requests': metric.request_count,
                    'success_rate': f"{metric.success_rate:.2%}",
                    'avg_response_time': f"{metric.avg_response_time:.2f}s"
                }
        
        # 성능 요약
        tier1_pct = (self.metrics[OptimizedTier.TIER1].request_count / 
                    max(report['total_requests'], 1) * 100)
        
        report['performance_summary'] = {
            'tier1_usage': f"{tier1_pct:.1f}%",
            'optimization_score': min(100, tier1_pct * 1.2),  # Tier1 사용률 기반 점수
            'memory_efficient': tier1_pct > 80
        }
        
        return report
    
    def get_optimization_recommendations(self) -> List[str]:
        """최적화 권장사항"""
        recommendations = []
        
        tier3_usage = (self.metrics[OptimizedTier.TIER3].request_count / 
                      max(sum(m.request_count for m in self.metrics.values()), 1))
        
        if tier3_usage > 0.2:  # 20% 이상
            recommendations.append("🎭 Tier3 사용률이 높습니다. URL 패턴 분류 규칙을 개선하세요.")
        
        if tier3_usage < 0.05:  # 5% 미만
            recommendations.append("✅ 최적화가 잘 되어 있습니다. Tier1/2 위주 처리 중")
        
        return recommendations


# 유틸리티 함수

async def quick_smart_crawl(url: str, **kwargs) -> CrawlResult:
    """빠른 지능형 크롤링"""
    manager = OptimizedCrawlerManager()
    try:
        await manager.initialize()
        config = CrawlConfig(url=url, **kwargs)
        return await manager.smart_crawl(config)
    finally:
        await manager.cleanup()


async def analyze_url_tier(url: str) -> Dict[str, Any]:
    """URL 최적 계층 분석"""
    manager = OptimizedCrawlerManager()
    tier = manager.classify_url(url)
    
    return {
        'url': url,
        'recommended_tier': tier.value,
        'expected_performance': 'high' if tier == OptimizedTier.TIER1 else 'medium' if tier == OptimizedTier.TIER2 else 'low',
        'memory_usage': 'low' if tier != OptimizedTier.TIER3 else 'high'
    }