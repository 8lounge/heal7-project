#!/usr/bin/env python3
"""
🧰 크롤러 툴킷 - 1+1 폴백 체계
적시적소 크롤러 선택 및 자동 폴백 시스템

Features:
- 도메인별 최적 크롤러 조합 매핑
- 실패시 즉시 폴백 전환
- 성능 기반 동적 전략 조정
- AI 기반 페이지 분석 통합

Author: HEAL7 Development Team
Version: 1.0.0
Date: 2025-09-01
"""

import asyncio
import time
import logging
from typing import Dict, List, Any, Optional, Tuple, Union
from dataclasses import dataclass, asdict
from enum import Enum
from urllib.parse import urlparse
import json
from pathlib import Path


logger = logging.getLogger(__name__)


class CrawlerType(Enum):
    """크롤러 타입 (3단계 간소화 시스템)"""
    HTTPX = "httpx"           # Tier 1: 정적 콘텐츠, API 
    PLAYWRIGHT = "playwright" # Tier 2: JavaScript 렌더링, 복잡한 상호작용


class TaskType(Enum):
    """작업 타입"""
    API_DATA = "api_data"
    TABLE_EXTRACTION = "table_extraction"
    FORM_INTERACTION = "form_interaction"
    PAGE_ANALYSIS = "page_analysis"
    GOVERNMENT_PORTAL = "government_portal"
    LEGACY_SITE = "legacy_site"
    DISCOVERY = "discovery"


@dataclass
class CrawlerStrategy:
    """크롤러 전략"""
    primary: CrawlerType      # 주 크롤러
    fallback: CrawlerType     # 폴백 크롤러
    task_type: TaskType
    success_threshold: float  # 성공률 임계값 (%)
    timeout_seconds: int
    max_retries: int
    description: str


@dataclass
class ExecutionResult:
    """실행 결과"""
    success: bool
    crawler_used: CrawlerType
    execution_time: float
    data_count: int
    error_message: Optional[str] = None
    fallback_triggered: bool = False
    screenshot_path: Optional[str] = None
    performance_score: float = 0.0  # 0-100점


class CrawlerToolkit:
    """🧰 크롤러 툴킷 - 1+1 폴백 시스템"""
    
    def __init__(self):
        self.strategies = self._initialize_strategies()
        self.performance_history: Dict[str, Dict] = {}
        self.fallback_stats = {
            "total_executions": 0,
            "fallback_triggered": 0,
            "success_with_primary": 0,
            "success_with_fallback": 0,
            "complete_failures": 0
        }
        
        logger.info("🧰 크롤러 툴킷 초기화 완료")
    
    def _initialize_strategies(self) -> Dict[TaskType, CrawlerStrategy]:
        """전략 매핑 초기화"""
        return {
            # 🚀 API 데이터 수집
            TaskType.API_DATA: CrawlerStrategy(
                primary=CrawlerType.HTTPX,
                fallback=CrawlerType.PLAYWRIGHT,
                task_type=TaskType.API_DATA,
                success_threshold=95.0,
                timeout_seconds=30,
                max_retries=3,
                description="REST API나 JSON 엔드포인트는 HTTPX가 최적, 웹UI 필요시 Playwright로 폴백"
            ),
            
            # 📊 테이블 데이터 추출
            TaskType.TABLE_EXTRACTION: CrawlerStrategy(
                primary=CrawlerType.PLAYWRIGHT,
                fallback=CrawlerType.HTTPX,  # 3단계 간소화: Selenium 제거
                task_type=TaskType.TABLE_EXTRACTION,
                success_threshold=85.0,
                timeout_seconds=60,
                max_retries=2,
                description="동적 테이블은 Playwright, 간단한 테이블은 HTTPX로 폴백 (3단계 간소화)"
            ),
            
            # 📝 폼 상호작용
            TaskType.FORM_INTERACTION: CrawlerStrategy(
                primary=CrawlerType.PLAYWRIGHT,  # 3단계 간소화: Selenium 제거
                fallback=CrawlerType.PLAYWRIGHT,
                task_type=TaskType.FORM_INTERACTION,
                success_threshold=80.0,
                timeout_seconds=90,
                max_retries=2,
                description="복잤 폼 입력/제출은 Playwright가 안정적 (3단계 간소화)"
            ),
            
            # 📄 정부 포털
            TaskType.GOVERNMENT_PORTAL: CrawlerStrategy(
                primary=CrawlerType.PLAYWRIGHT,
                fallback=CrawlerType.HTTPX,  # 3단계 간소화: Selenium 제거
                task_type=TaskType.GOVERNMENT_PORTAL,
                success_threshold=90.0,
                timeout_seconds=120,
                max_retries=2,
                description="정부 사이트는 JavaScript 필수, 단순 데이터는 HTTPX로 폴백 (3단계 간소화)"
            ),
            
            # 🔍 페이지 분석 (AI 지원)
            TaskType.PAGE_ANALYSIS: CrawlerStrategy(
                primary=CrawlerType.PLAYWRIGHT,
                fallback=CrawlerType.HTTPX,  # 3단계 간소화: Selenium 제거
                task_type=TaskType.PAGE_ANALYSIS,
                success_threshold=75.0,
                timeout_seconds=90,
                max_retries=1,
                description="스크린샷 + DOM 분석은 Playwright, 기본 분석은 HTTPX (3단계 간소화)"
            ),
            
            # 🏛️ 레거시 사이트
            TaskType.LEGACY_SITE: CrawlerStrategy(
                primary=CrawlerType.PLAYWRIGHT,  # 3단계 간소화: Selenium 제거
                fallback=CrawlerType.HTTPX,
                task_type=TaskType.LEGACY_SITE,
                success_threshold=70.0,
                timeout_seconds=180,
                max_retries=1,
                description="레거시 사이트도 Playwright로 처리, 단순 HTML만 있다면 HTTPX로 폴백 (3단계 간소화)"
            ),
            
            # 🔍 디스커버리 크롤링
            TaskType.DISCOVERY: CrawlerStrategy(
                primary=CrawlerType.PLAYWRIGHT,
                fallback=CrawlerType.HTTPX,  # 3단계 간소화: Selenium 제거
                task_type=TaskType.DISCOVERY,
                success_threshold=60.0,
                timeout_seconds=150,
                max_retries=1,
                description="자동 요소 탐지는 Playwright, 기본 요소는 HTTPX로 분석 (3단계 간소화)"
            )
        }
    
    def analyze_url_and_task(self, url: str, task_hint: str = None) -> TaskType:
        """URL과 작업 힌트 기반 작업 타입 결정"""
        
        domain = urlparse(url).netloc.lower()
        path = urlparse(url).path.lower()
        
        # 도메인 기반 분석
        if any(gov in domain for gov in ['gov.kr', 'go.kr', 'korea.kr']):
            return TaskType.GOVERNMENT_PORTAL
        elif 'api.' in domain or 'httpbin' in domain or path.startswith('/api/'):
            return TaskType.API_DATA
        elif any(legacy in domain for legacy in ['.co.kr', '.or.kr']) and '2000' in domain:
            return TaskType.LEGACY_SITE
        
        # 작업 힌트 기반 분석
        if task_hint:
            hint_lower = task_hint.lower()
            if 'table' in hint_lower or 'extract' in hint_lower:
                return TaskType.TABLE_EXTRACTION
            elif 'form' in hint_lower or 'submit' in hint_lower or 'login' in hint_lower:
                return TaskType.FORM_INTERACTION
            elif 'discover' in hint_lower or 'explore' in hint_lower:
                return TaskType.DISCOVERY
        
        # 기본값: 페이지 분석
        return TaskType.PAGE_ANALYSIS
    
    async def execute_with_fallback(
        self, 
        url: str, 
        task_hint: str = None,
        custom_strategy: CrawlerStrategy = None
    ) -> ExecutionResult:
        """🎯 메인 실행 함수 - 1+1 폴백 체계"""
        
        # 전략 선택
        if custom_strategy:
            strategy = custom_strategy
        else:
            task_type = self.analyze_url_and_task(url, task_hint)
            strategy = self.strategies[task_type]
        
        self.fallback_stats["total_executions"] += 1
        
        logger.info(f"🎯 작업 실행: {url}")
        logger.info(f"   전략: {strategy.task_type.value}")
        logger.info(f"   주 크롤러: {strategy.primary.value} → 폴백: {strategy.fallback.value}")
        
        # 1단계: 주 크롤러 시도
        primary_result = await self._execute_single_crawler(
            url, strategy.primary, strategy
        )
        
        if primary_result.success and primary_result.performance_score >= strategy.success_threshold:
            logger.info(f"✅ 주 크롤러({strategy.primary.value}) 성공!")
            self.fallback_stats["success_with_primary"] += 1
            self._update_performance_history(url, primary_result)
            return primary_result
        
        # 2단계: 폴백 크롤러 시도
        logger.warning(f"⚠️ 주 크롤러 실패/성능부족, 폴백({strategy.fallback.value}) 시도")
        self.fallback_stats["fallback_triggered"] += 1
        
        fallback_result = await self._execute_single_crawler(
            url, strategy.fallback, strategy
        )
        fallback_result.fallback_triggered = True
        
        if fallback_result.success:
            logger.info(f"✅ 폴백 크롤러({strategy.fallback.value}) 성공!")
            self.fallback_stats["success_with_fallback"] += 1
        else:
            logger.error(f"❌ 모든 크롤러 실패!")
            self.fallback_stats["complete_failures"] += 1
        
        self._update_performance_history(url, fallback_result)
        return fallback_result
    
    async def _execute_single_crawler(
        self, 
        url: str, 
        crawler_type: CrawlerType, 
        strategy: CrawlerStrategy
    ) -> ExecutionResult:
        """개별 크롤러 실행"""
        
        start_time = time.time()
        
        try:
            # TODO: 실제 크롤러 객체들과 연동
            # 현재는 시뮬레이션
            
            # 크롤러별 성공률 시뮬레이션 (실제 환경에서는 제거)
            if crawler_type == CrawlerType.HTTPX:
                success_prob = 0.95 if 'api' in url or 'httpbin' in url else 0.60
                data_count = random.randint(1, 50) if random.random() < success_prob else 0
            elif crawler_type == CrawlerType.PLAYWRIGHT:
                success_prob = 0.85 if 'gov' in url or 'dynamic' in url else 0.75
                data_count = random.randint(5, 100) if random.random() < success_prob else 0
            else:  # SELENIUM
                success_prob = 0.90 if 'form' in url or 'legacy' in url else 0.70
                data_count = random.randint(3, 80) if random.random() < success_prob else 0
            
            # 실행 시간 시뮬레이션
            if crawler_type == CrawlerType.HTTPX:
                await asyncio.sleep(random.uniform(0.5, 2.0))
            elif crawler_type == CrawlerType.PLAYWRIGHT:
                await asyncio.sleep(random.uniform(2.0, 5.0))
            else:  # SELENIUM
                await asyncio.sleep(random.uniform(5.0, 10.0))
            
            execution_time = time.time() - start_time
            success = data_count > 0
            
            # 성능 점수 계산
            performance_score = 0
            if success:
                time_score = max(0, 100 - (execution_time * 2))  # 시간 가점
                data_score = min(data_count * 2, 50)  # 데이터 양 가점  
                performance_score = min(time_score + data_score, 100)
            
            return ExecutionResult(
                success=success,
                crawler_used=crawler_type,
                execution_time=execution_time,
                data_count=data_count,
                performance_score=performance_score,
                error_message=None if success else f"{crawler_type.value} 크롤러 데이터 추출 실패"
            )
            
        except Exception as e:
            execution_time = time.time() - start_time
            logger.error(f"❌ {crawler_type.value} 크롤러 오류: {e}")
            
            return ExecutionResult(
                success=False,
                crawler_used=crawler_type,
                execution_time=execution_time,
                data_count=0,
                error_message=str(e),
                performance_score=0
            )
    
    def _update_performance_history(self, url: str, result: ExecutionResult):
        """성능 이력 업데이트"""
        domain = urlparse(url).netloc
        
        if domain not in self.performance_history:
            self.performance_history[domain] = {
                "total_runs": 0,
                "successful_runs": 0,
                "avg_execution_time": 0,
                "avg_performance_score": 0,
                "crawler_stats": {
                    "httpx": {"runs": 0, "successes": 0, "avg_time": 0},
                    "playwright": {"runs": 0, "successes": 0, "avg_time": 0}
                },
                "last_updated": None
            }
        
        history = self.performance_history[domain]
        crawler_name = result.crawler_used.value
        
        # 전체 통계 업데이트
        history["total_runs"] += 1
        if result.success:
            history["successful_runs"] += 1
        
        # 평균 실행시간 업데이트
        prev_time = history["avg_execution_time"]
        history["avg_execution_time"] = (prev_time * (history["total_runs"] - 1) + result.execution_time) / history["total_runs"]
        
        # 평균 성능점수 업데이트
        prev_score = history["avg_performance_score"]
        history["avg_performance_score"] = (prev_score * (history["total_runs"] - 1) + result.performance_score) / history["total_runs"]
        
        # 크롤러별 통계 업데이트
        crawler_stats = history["crawler_stats"][crawler_name]
        crawler_stats["runs"] += 1
        if result.success:
            crawler_stats["successes"] += 1
        
        prev_crawler_time = crawler_stats["avg_time"]
        crawler_stats["avg_time"] = (prev_crawler_time * (crawler_stats["runs"] - 1) + result.execution_time) / crawler_stats["runs"]
        
        history["last_updated"] = time.time()
    
    def get_domain_recommendation(self, url: str) -> Dict[str, Any]:
        """도메인별 추천 전략"""
        domain = urlparse(url).netloc
        
        if domain not in self.performance_history:
            # 첫 방문: URL 분석 기반 추천
            task_type = self.analyze_url_and_task(url)
            strategy = self.strategies[task_type]
            
            return {
                "domain": domain,
                "first_visit": True,
                "recommended_strategy": {
                    "primary": strategy.primary.value,
                    "fallback": strategy.fallback.value,
                    "reason": strategy.description
                },
                "confidence": "medium"
            }
        
        # 이력 기반 추천
        history = self.performance_history[domain]
        crawler_stats = history["crawler_stats"]
        
        # 최고 성능 크롤러 찾기
        best_crawler = None
        best_success_rate = 0
        
        for crawler_name, stats in crawler_stats.items():
            if stats["runs"] > 0:
                success_rate = stats["successes"] / stats["runs"]
                if success_rate > best_success_rate:
                    best_success_rate = success_rate
                    best_crawler = crawler_name
        
        return {
            "domain": domain,
            "first_visit": False,
            "total_runs": history["total_runs"],
            "success_rate": history["successful_runs"] / history["total_runs"],
            "avg_execution_time": history["avg_execution_time"],
            "best_crawler": best_crawler,
            "best_success_rate": best_success_rate,
            "recommended_strategy": self._get_optimized_strategy(domain, history),
            "confidence": "high" if history["total_runs"] >= 10 else "medium"
        }
    
    def _get_optimized_strategy(self, domain: str, history: Dict) -> Dict[str, str]:
        """성능 이력 기반 최적화된 전략"""
        crawler_stats = history["crawler_stats"]
        
        # 성공률 기준으로 정렬
        sorted_crawlers = sorted(
            crawler_stats.items(),
            key=lambda x: (x[1]["successes"] / max(x[1]["runs"], 1), -x[1]["avg_time"]),
            reverse=True
        )
        
        if len(sorted_crawlers) >= 2:
            primary = sorted_crawlers[0][0]
            fallback = sorted_crawlers[1][0]
        else:
            # 기본 전략 유지
            return {"primary": "playwright", "fallback": "httpx", "reason": "성능 데이터 부족 (3단계 간소화 시스템)"}
        
        return {
            "primary": primary,
            "fallback": fallback, 
            "reason": f"성능 이력 기반 최적화 ({history['total_runs']}회 실행 분석)"
        }
    
    def get_toolkit_stats(self) -> Dict[str, Any]:
        """툴킷 전체 통계"""
        return {
            "strategies_count": len(self.strategies),
            "tracked_domains": len(self.performance_history),
            "execution_stats": self.fallback_stats.copy(),
            "fallback_success_rate": (
                self.fallback_stats["success_with_fallback"] / 
                max(self.fallback_stats["fallback_triggered"], 1)
            ) * 100,
            "overall_success_rate": (
                (self.fallback_stats["success_with_primary"] + self.fallback_stats["success_with_fallback"]) /
                max(self.fallback_stats["total_executions"], 1)
            ) * 100
        }
    
    async def batch_analyze_urls(self, urls: List[str]) -> Dict[str, Dict]:
        """🔍 배치 URL 분석"""
        results = {}
        
        for url in urls:
            try:
                recommendation = self.get_domain_recommendation(url)
                task_type = self.analyze_url_and_task(url)
                
                results[url] = {
                    "task_type": task_type.value,
                    "recommendation": recommendation,
                    "estimated_complexity": self._estimate_complexity(url, task_type)
                }
                
            except Exception as e:
                results[url] = {
                    "error": str(e),
                    "task_type": "unknown"
                }
        
        return results
    
    def _estimate_complexity(self, url: str, task_type: TaskType) -> Dict[str, Any]:
        """복잡도 추정"""
        complexity_scores = {
            TaskType.API_DATA: {"score": 1, "level": "낮음"},
            TaskType.GOVERNMENT_PORTAL: {"score": 4, "level": "높음"},
            TaskType.TABLE_EXTRACTION: {"score": 3, "level": "중간"},
            TaskType.FORM_INTERACTION: {"score": 4, "level": "높음"},
            TaskType.PAGE_ANALYSIS: {"score": 2, "level": "낮음-중간"},
            TaskType.LEGACY_SITE: {"score": 5, "level": "매우 높음"},
            TaskType.DISCOVERY: {"score": 3, "level": "중간"}
        }
        
        base_complexity = complexity_scores.get(task_type, {"score": 3, "level": "중간"})
        
        # URL 특성 기반 조정
        domain = urlparse(url).netloc.lower()
        if 'gov.kr' in domain:
            base_complexity["score"] = min(5, base_complexity["score"] + 1)
        elif 'api.' in domain:
            base_complexity["score"] = max(1, base_complexity["score"] - 1)
        
        return base_complexity


# 전역 인스턴스
crawler_toolkit = CrawlerToolkit()


# 🎯 크롤러 조합 가이드
CRAWLER_COMBINATION_GUIDE = {
    "🚀 API/정적데이터": {
        "primary": "HTTPX",
        "fallback": "Playwright", 
        "use_cases": ["REST API", "JSON 엔드포인트", "정적 HTML", "CSV 다운로드"],
        "success_rate": "95%+",
        "avg_time": "1-3초"
    },
    
    "📊 테이블/동적데이터": {
        "primary": "Playwright",
        "fallback": "HTTPX",  # 3단계 간소화
        "use_cases": ["JavaScript 테이블", "AJAX 로딩", "무한스크롤", "차트 데이터"],
        "success_rate": "85%+", 
        "avg_time": "3-8초"
    },
    
    "📝 폼/상호작용": {
        "primary": "Playwright",  # 3단계 간소화 
        "fallback": "Playwright",
        "use_cases": ["로그인 폼", "다단계 입력", "파일 업로드", "드롭다운"],
        "success_rate": "80%+",
        "avg_time": "8-15초"
    },
    
    "📄 정부포털": {
        "primary": "Playwright",
        "fallback": "HTTPX",  # 3단계 간소화 
        "use_cases": ["정부24", "나라장터", "국가정보포털", "공공API"],
        "success_rate": "90%+",
        "avg_time": "5-12초"
    },
    
    "🏛️ 레거시사이트": {
        "primary": "Playwright",  # 3단계 간소화
        "fallback": "HTTPX",
        "use_cases": ["ActiveX 사이트", "Flash 콘텐츠", "구형 JSP", "프레임셋"],
        "success_rate": "70%+",
        "avg_time": "10-30초" 
    },
    
    "🔍 디스커버리": {
        "primary": "Playwright",
        "fallback": "HTTPX",  # 3단계 간소화
        "use_cases": ["요소 탐지", "구조 분석", "스크린샷", "AI 분석"],
        "success_rate": "75%+",
        "avg_time": "8-20초"
    }
}


async def demo_crawler_toolkit():
    """🧪 크롤러 툴킷 데모"""
    print("🧰 크롤러 툴킷 데모 시작")
    
    test_urls = [
        "https://httpbin.org/json",  # API
        "https://www.bizinfo.go.kr",  # 정부포털  
        "https://example.com/table",  # 테이블
        "https://old-site.co.kr"  # 레거시
    ]
    
    for url in test_urls:
        print(f"\n🎯 테스트 URL: {url}")
        result = await crawler_toolkit.execute_with_fallback(url)
        
        print(f"   결과: {'✅ 성공' if result.success else '❌ 실패'}")
        print(f"   크롤러: {result.crawler_used.value}")
        print(f"   실행시간: {result.execution_time:.2f}초")
        print(f"   성능점수: {result.performance_score:.1f}/100")
        if result.fallback_triggered:
            print(f"   🔄 폴백 사용됨")
    
    # 전체 통계
    stats = crawler_toolkit.get_toolkit_stats()
    print(f"\n📊 전체 통계:")
    print(f"   전체 성공률: {stats['overall_success_rate']:.1f}%")
    print(f"   폴백 성공률: {stats['fallback_success_rate']:.1f}%") 
    print(f"   추적 도메인: {stats['tracked_domains']}개")


if __name__ == "__main__":
    asyncio.run(demo_crawler_toolkit())