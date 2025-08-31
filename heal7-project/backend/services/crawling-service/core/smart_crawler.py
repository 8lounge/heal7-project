#!/usr/bin/env python3
"""
🧠 스마트 크롤러 - 지능형 3-Tier 통합 시스템
자동 폴백 및 최적 크롤러 선택

Features:
- 자동 크롤러 선택
- 순차 폴백 시스템
- 성능 기반 학습
- 배치 처리
- 실시간 모니터링

Author: HEAL7 Development Team
Version: 1.0.0
Date: 2025-08-30
"""

import asyncio
import logging
import time
import statistics
from typing import Dict, Any, List, Optional, Union
from dataclasses import dataclass, field
from enum import Enum
from collections import defaultdict, deque
from urllib.parse import urlparse

from .crawlers import (
    BaseCrawler, CrawlResult, CrawlConfig, CrawlerType,
    HttpxCrawler, PlaywrightCrawler, SeleniumCrawler
)


logger = logging.getLogger(__name__)


class CrawlStrategy(Enum):
    """크롤링 전략"""
    AUTO = "auto"           # 자동 선택
    FAST = "fast"          # 속도 우선 (httpx → playwright → selenium)
    RENDER = "render"      # 렌더링 우선 (playwright → httpx → selenium)  
    STEALTH = "stealth"    # 스텔스 우선 (selenium → playwright → httpx)
    SAFE = "safe"          # 안정성 우선 (모든 크롤러 시도)


@dataclass
class CrawlerStats:
    """크롤러 통계"""
    total_requests: int = 0
    successful_requests: int = 0
    failed_requests: int = 0
    average_response_time: float = 0.0
    recent_response_times: deque = field(default_factory=lambda: deque(maxlen=10))
    error_types: Dict[str, int] = field(default_factory=dict)
    last_used: Optional[float] = None
    
    def update(self, result: CrawlResult):
        """통계 업데이트"""
        self.total_requests += 1
        self.last_used = time.time()
        
        if result.success:
            self.successful_requests += 1
        else:
            self.failed_requests += 1
            if result.error_type:
                self.error_types[result.error_type] = self.error_types.get(result.error_type, 0) + 1
        
        if result.response_time:
            self.recent_response_times.append(result.response_time)
            self.average_response_time = statistics.mean(self.recent_response_times)
    
    @property
    def success_rate(self) -> float:
        """성공률"""
        if self.total_requests == 0:
            return 0.0
        return self.successful_requests / self.total_requests
    
    @property
    def reliability_score(self) -> float:
        """신뢰도 점수 (성공률 + 속도 고려)"""
        if self.total_requests < 3:  # 최소 3번의 시도 필요
            return 0.5
        
        # 성공률 (70%) + 속도 점수 (30%)
        speed_score = max(0, 1 - (self.average_response_time / 30))  # 30초를 기준
        return (self.success_rate * 0.7) + (speed_score * 0.3)


class SmartCrawler:
    """🧠 지능형 3-Tier 크롤러 시스템"""
    
    def __init__(self):
        self.name = "smart_crawler"
        self.logger = logging.getLogger(f"{__name__}.SmartCrawler")
        
        # 크롤러 인스턴스들
        self.crawlers: Dict[CrawlerType, BaseCrawler] = {}
        self.crawler_stats: Dict[CrawlerType, CrawlerStats] = {
            CrawlerType.HTTPX: CrawlerStats(),
            CrawlerType.PLAYWRIGHT: CrawlerStats(), 
            CrawlerType.SELENIUM: CrawlerStats()
        }
        
        # 도메인별 최적 크롤러 캐시
        self.domain_preferences: Dict[str, CrawlerType] = {}
        
        # 전역 설정
        self.max_retries = 2
        self.retry_delay = 1.0
        self.is_initialized = False
        
        # 성능 임계값
        self.performance_thresholds = {
            'min_success_rate': 0.7,
            'max_response_time': 30.0,
            'min_reliability_score': 0.6
        }
    
    async def initialize(self):
        """모든 크롤러 초기화"""
        if self.is_initialized:
            return
        
        self.logger.info("🧠 Smart Crawler 시스템 초기화 시작")
        
        try:
            # 크롤러 인스턴스 생성
            self.crawlers = {
                CrawlerType.HTTPX: HttpxCrawler(),
                CrawlerType.PLAYWRIGHT: PlaywrightCrawler(headless=True),
                CrawlerType.SELENIUM: SeleniumCrawler(use_undetected=True, headless=True)
            }
            
            # 병렬 초기화
            init_tasks = []
            for crawler_type, crawler in self.crawlers.items():
                init_tasks.append(self._safe_initialize_crawler(crawler_type, crawler))
            
            await asyncio.gather(*init_tasks)
            
            self.is_initialized = True
            self.logger.info("✅ Smart Crawler 시스템 초기화 완료")
            
        except Exception as e:
            self.logger.error(f"❌ Smart Crawler 초기화 실패: {e}")
            raise
    
    async def _safe_initialize_crawler(self, crawler_type: CrawlerType, crawler: BaseCrawler):
        """안전한 크롤러 초기화"""
        try:
            await crawler.initialize()
            self.logger.info(f"✅ {crawler_type.value} 크롤러 초기화 완료")
        except Exception as e:
            self.logger.error(f"❌ {crawler_type.value} 크롤러 초기화 실패: {e}")
            # 초기화 실패한 크롤러는 제거
            if crawler_type in self.crawlers:
                del self.crawlers[crawler_type]
    
    async def cleanup(self):
        """모든 크롤러 정리"""
        cleanup_tasks = []
        for crawler in self.crawlers.values():
            cleanup_tasks.append(crawler.cleanup())
        
        await asyncio.gather(*cleanup_tasks, return_exceptions=True)
        
        self.crawlers.clear()
        self.is_initialized = False
        self.logger.info("🛑 Smart Crawler 시스템 정리 완료")
    
    async def crawl(
        self, 
        url: str, 
        strategy: CrawlStrategy = CrawlStrategy.AUTO,
        **kwargs
    ) -> CrawlResult:
        """지능형 크롤링 실행"""
        if not self.is_initialized:
            await self.initialize()
        
        config = CrawlConfig(url=url, **kwargs)
        
        # 크롤러 순서 결정
        crawler_order = await self._determine_crawler_order(url, strategy)
        
        if not crawler_order:
            return CrawlResult(
                success=False,
                error="사용 가능한 크롤러가 없습니다",
                url=url
            )
        
        # 순차적으로 크롤러 시도
        last_result = None
        attempts = 0
        
        for crawler_type in crawler_order:
            if crawler_type not in self.crawlers:
                continue
            
            crawler = self.crawlers[crawler_type]
            attempts += 1
            
            try:
                self.logger.info(f"🎯 크롤링 시도 {attempts}: {crawler_type.value} - {url}")
                
                result = await crawler.crawl(config)
                
                # 통계 업데이트
                self.crawler_stats[crawler_type].update(result)
                
                if result.success:
                    # 성공한 크롤러를 도메인 선호도에 저장
                    domain = self._extract_domain(url)
                    self.domain_preferences[domain] = crawler_type
                    
                    self.logger.info(f"✅ 크롤링 성공: {crawler_type.value}")
                    return result
                else:
                    self.logger.warning(f"❌ {crawler_type.value} 실패: {result.error}")
                    last_result = result
                    
            except Exception as e:
                error_msg = f"{crawler_type.value} 예외: {e}"
                self.logger.error(error_msg)
                
                # 통계 업데이트 (실패)
                dummy_result = CrawlResult(
                    success=False,
                    error=error_msg,
                    crawler_used=crawler_type,
                    url=url
                )
                self.crawler_stats[crawler_type].update(dummy_result)
                
                last_result = dummy_result
        
        # 모든 크롤러 실패
        return last_result or CrawlResult(
            success=False,
            error="모든 크롤러 실패",
            url=url
        )
    
    async def _determine_crawler_order(self, url: str, strategy: CrawlStrategy) -> List[CrawlerType]:
        """크롤러 우선순위 결정"""
        domain = self._extract_domain(url)
        
        # 도메인 기반 선호도가 있으면 우선 적용
        if domain in self.domain_preferences:
            preferred = self.domain_preferences[domain]
            if preferred in self.crawlers:
                other_crawlers = [c for c in self.crawlers.keys() if c != preferred]
                # 성능 기준으로 정렬
                other_crawlers.sort(key=lambda c: self.crawler_stats[c].reliability_score, reverse=True)
                return [preferred] + other_crawlers
        
        # 전략별 순서 결정
        if strategy == CrawlStrategy.FAST:
            order = [CrawlerType.HTTPX, CrawlerType.PLAYWRIGHT, CrawlerType.SELENIUM]
        elif strategy == CrawlStrategy.RENDER:
            order = [CrawlerType.PLAYWRIGHT, CrawlerType.HTTPX, CrawlerType.SELENIUM]
        elif strategy == CrawlStrategy.STEALTH:
            order = [CrawlerType.SELENIUM, CrawlerType.PLAYWRIGHT, CrawlerType.HTTPX]
        elif strategy == CrawlStrategy.SAFE:
            # 모든 크롤러를 안정성 순으로
            order = sorted(self.crawlers.keys(), 
                         key=lambda c: self.crawler_stats[c].reliability_score, 
                         reverse=True)
        else:  # AUTO
            order = await self._auto_determine_order(url)
        
        # 사용 가능한 크롤러만 반환
        return [c for c in order if c in self.crawlers]
    
    async def _auto_determine_order(self, url: str) -> List[CrawlerType]:
        """자동 크롤러 순서 결정"""
        url_lower = url.lower()
        
        # URL 패턴 기반 분석
        if any(keyword in url_lower for keyword in ['api', '.json', '/rest/', '/graphql']):
            # API 엔드포인트 -> httpx 우선
            return [CrawlerType.HTTPX, CrawlerType.PLAYWRIGHT, CrawlerType.SELENIUM]
        
        elif any(keyword in url_lower for keyword in ['cloudflare', 'protection']):
            # 보호된 사이트 -> selenium 우선
            return [CrawlerType.SELENIUM, CrawlerType.PLAYWRIGHT, CrawlerType.HTTPX]
        
        elif '.go.kr' in url_lower or '.gov' in url_lower:
            # 정부 사이트 -> selenium 우선 (보안이 강함)
            return [CrawlerType.SELENIUM, CrawlerType.PLAYWRIGHT, CrawlerType.HTTPX]
        
        else:
            # 일반 사이트 -> 성능 기준 정렬
            available_crawlers = list(self.crawlers.keys())
            available_crawlers.sort(
                key=lambda c: self.crawler_stats[c].reliability_score, 
                reverse=True
            )
            return available_crawlers
    
    def _extract_domain(self, url: str) -> str:
        """URL에서 도메인 추출"""
        try:
            parsed = urlparse(url)
            return parsed.netloc.lower()
        except:
            return url.lower()
    
    async def batch_crawl(
        self, 
        urls: List[str], 
        strategy: CrawlStrategy = CrawlStrategy.AUTO,
        max_concurrent: int = 5,
        **kwargs
    ) -> List[CrawlResult]:
        """배치 크롤링"""
        if not self.is_initialized:
            await self.initialize()
        
        semaphore = asyncio.Semaphore(max_concurrent)
        
        async def crawl_single(url: str) -> CrawlResult:
            async with semaphore:
                return await self.crawl(url, strategy, **kwargs)
        
        self.logger.info(f"🚀 배치 크롤링 시작: {len(urls)}개 URL")
        
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
        
        # 성공률 통계
        successful = sum(1 for r in processed_results if r.success)
        self.logger.info(f"✅ 배치 크롤링 완료: {successful}/{len(urls)} 성공")
        
        return processed_results
    
    async def health_check(self) -> Dict[str, Any]:
        """시스템 상태 확인"""
        health_status = {
            'system_healthy': True,
            'initialized': self.is_initialized,
            'available_crawlers': list(self.crawlers.keys()),
            'crawler_health': {},
            'performance_summary': {}
        }
        
        if not self.is_initialized:
            health_status['system_healthy'] = False
            return health_status
        
        # 각 크롤러 상태 확인
        for crawler_type, crawler in self.crawlers.items():
            try:
                is_healthy = await crawler.health_check()
                health_status['crawler_health'][crawler_type.value] = {
                    'healthy': is_healthy,
                    'stats': self.get_crawler_stats(crawler_type)
                }
                
                if not is_healthy:
                    health_status['system_healthy'] = False
                    
            except Exception as e:
                health_status['crawler_health'][crawler_type.value] = {
                    'healthy': False,
                    'error': str(e)
                }
                health_status['system_healthy'] = False
        
        # 전체 성능 요약
        health_status['performance_summary'] = self.get_performance_summary()
        
        return health_status
    
    def get_crawler_stats(self, crawler_type: CrawlerType) -> Dict[str, Any]:
        """크롤러별 통계"""
        stats = self.crawler_stats[crawler_type]
        return {
            'total_requests': stats.total_requests,
            'success_rate': stats.success_rate,
            'average_response_time': stats.average_response_time,
            'reliability_score': stats.reliability_score,
            'error_types': dict(stats.error_types),
            'last_used': stats.last_used
        }
    
    def get_performance_summary(self) -> Dict[str, Any]:
        """전체 성능 요약"""
        total_requests = sum(stats.total_requests for stats in self.crawler_stats.values())
        total_successful = sum(stats.successful_requests for stats in self.crawler_stats.values())
        
        if total_requests == 0:
            return {
                'overall_success_rate': 0.0,
                'total_requests': 0,
                'best_performer': None,
                'domain_preferences_count': len(self.domain_preferences)
            }
        
        # 최고 성능 크롤러
        best_performer = max(
            self.crawler_stats.items(),
            key=lambda x: x[1].reliability_score
        )[0].value if self.crawler_stats else None
        
        return {
            'overall_success_rate': total_successful / total_requests,
            'total_requests': total_requests,
            'best_performer': best_performer,
            'domain_preferences_count': len(self.domain_preferences),
            'avg_response_time': statistics.mean([
                stats.average_response_time 
                for stats in self.crawler_stats.values() 
                if stats.average_response_time > 0
            ]) if any(stats.average_response_time > 0 for stats in self.crawler_stats.values()) else 0
        }
    
    def optimize_performance(self):
        """성능 최적화"""
        self.logger.info("🔧 성능 최적화 실행")
        
        # 성능이 낮은 크롤러의 도메인 선호도 제거
        domains_to_remove = []
        for domain, preferred_crawler in self.domain_preferences.items():
            if preferred_crawler in self.crawler_stats:
                stats = self.crawler_stats[preferred_crawler]
                if stats.reliability_score < self.performance_thresholds['min_reliability_score']:
                    domains_to_remove.append(domain)
        
        for domain in domains_to_remove:
            del self.domain_preferences[domain]
            self.logger.info(f"도메인 선호도 제거: {domain}")
        
        self.logger.info("✅ 성능 최적화 완료")


# 유틸리티 함수들

async def quick_crawl(url: str, strategy: str = "auto", **kwargs) -> CrawlResult:
    """빠른 크롤링 (원샷 함수)"""
    crawler = SmartCrawler()
    try:
        await crawler.initialize()
        strategy_enum = CrawlStrategy(strategy.lower())
        return await crawler.crawl(url, strategy_enum, **kwargs)
    finally:
        await crawler.cleanup()


async def smart_batch_crawl(urls: List[str], **kwargs) -> List[CrawlResult]:
    """스마트 배치 크롤링"""
    crawler = SmartCrawler()
    try:
        await crawler.initialize()
        return await crawler.batch_crawl(urls, **kwargs)
    finally:
        await crawler.cleanup()


def create_smart_crawler() -> SmartCrawler:
    """스마트 크롤러 팩토리"""
    return SmartCrawler()