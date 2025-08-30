#!/usr/bin/env python3
"""
🎭 Playwright 동적 테스트 시스템
AI가 생성한 수집 전략을 실제 브라우저에서 테스트 및 검증

Author: HEAL7 Development Team
Version: 1.0.0
Date: 2025-08-29
"""

import asyncio
import json
import logging
import re
import time
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Any, Union
from dataclasses import dataclass, asdict
from enum import Enum

import asyncpg
from playwright.async_api import async_playwright, Browser, BrowserContext, Page, TimeoutError as PlaywrightTimeoutError

# AI Research Engine에서 필요한 클래스들 import
from ai_research_engine import CollectionStrategy, StrategyConfidence


logger = logging.getLogger(__name__)


class TestResult(Enum):
    """테스트 결과 상태"""
    SUCCESS = "success"
    PARTIAL_SUCCESS = "partial_success"
    FAILURE = "failure"
    ERROR = "error"


@dataclass
class TestMetrics:
    """테스트 메트릭 데이터"""
    selector_success_rate: float = 0.0
    data_quality_score: float = 0.0  
    extraction_speed: float = 0.0  # items/second
    error_count: int = 0
    total_items_found: int = 0
    valid_items_extracted: int = 0
    test_duration: float = 0.0


@dataclass
class StrategyTestResult:
    """전략 테스트 결과"""
    strategy_id: str
    test_id: str
    site_url: str
    
    # 테스트 결과
    overall_result: TestResult
    metrics: TestMetrics
    
    # 상세 결과
    selector_results: Dict[str, Any] = None
    sample_data: List[Dict] = None
    error_messages: List[str] = None
    
    # 개선 제안
    improvement_suggestions: List[str] = None
    updated_strategy: Optional[CollectionStrategy] = None
    
    # 메타데이터
    tested_at: str = ""
    test_duration: float = 0.0
    browser_info: Dict[str, str] = None
    
    def __post_init__(self):
        if self.selector_results is None:
            self.selector_results = {}
        if self.sample_data is None:
            self.sample_data = []
        if self.error_messages is None:
            self.error_messages = []
        if self.improvement_suggestions is None:
            self.improvement_suggestions = []
        if not self.tested_at:
            self.tested_at = datetime.now().isoformat()
        if self.browser_info is None:
            self.browser_info = {}


class PlaywrightDynamicTester:
    """🎭 Playwright 기반 동적 수집 전략 테스터"""
    
    def __init__(self, headless: bool = True, slow_mo: int = 0):
        self.headless = headless
        self.slow_mo = slow_mo
        
        # Playwright 인스턴스
        self.playwright = None
        self.browser: Optional[Browser] = None
        self.context: Optional[BrowserContext] = None
        
        # 테스트 설정
        self.test_config = {
            "timeout": 30000,  # 30초
            "max_pages_to_test": 3,  # 최대 3페이지 테스트
            "min_items_for_validation": 5,  # 검증을 위한 최소 아이템 수
            "quality_threshold": 0.7  # 품질 임계값
        }
        
        # 데이터 품질 평가 기준
        self.quality_criteria = {
            "title": {
                "min_length": 3,
                "max_length": 300,
                "required": True
            },
            "agency": {
                "min_length": 2,
                "max_length": 100,
                "required": False
            },
            "url": {
                "must_be_valid_url": True,
                "required": True
            }
        }
        
        # 브라우저 설정
        self.browser_config = {
            "viewport": {"width": 1920, "height": 1080},
            "user_agent": "HEAL7-PlaywrightTester/1.0 (+https://heal7.com/testing)",
            "locale": "ko-KR",
            "timezone_id": "Asia/Seoul"
        }
    
    async def initialize(self):
        """Playwright 테스터 초기화"""
        logger.info("🎭 Playwright Dynamic Tester 초기화")
        
        try:
            # Playwright 시작
            self.playwright = await async_playwright().start()
            
            # 브라우저 시작
            self.browser = await self.playwright.chromium.launch(
                headless=self.headless,
                slow_mo=self.slow_mo,
                args=[
                    '--no-sandbox',
                    '--disable-dev-shm-usage',
                    '--disable-gpu',
                    '--disable-extensions'
                ]
            )
            
            # 컨텍스트 생성 
            self.context = await self.browser.new_context(
                viewport=self.browser_config["viewport"],
                user_agent=self.browser_config["user_agent"],
                locale=self.browser_config["locale"],
                timezone_id=self.browser_config["timezone_id"]
            )
            
            logger.info("✅ Playwright 초기화 완료")
            
        except Exception as e:
            logger.error(f"❌ Playwright 초기화 실패: {str(e)}")
            raise
    
    async def close(self):
        """리소스 정리"""
        try:
            if self.context:
                await self.context.close()
            if self.browser:
                await self.browser.close()
            if self.playwright:
                await self.playwright.stop()
            logger.info("🛑 Playwright 테스터 종료 완료")
        except Exception as e:
            logger.error(f"❌ Playwright 종료 중 오류: {str(e)}")
    
    async def test_collection_strategy(
        self, 
        strategy: CollectionStrategy,
        pages_to_test: int = None
    ) -> StrategyTestResult:
        """🧪 수집 전략 종합 테스트"""
        
        test_id = self._generate_test_id(strategy.strategy_id)
        pages_to_test = pages_to_test or self.test_config["max_pages_to_test"]
        
        logger.info(f"🧪 전략 테스트 시작: {strategy.strategy_id} ({strategy.site_url})")
        
        start_time = time.time()
        
        try:
            # 1. 기본 접근성 테스트
            accessibility_result = await self._test_site_accessibility(strategy.site_url)
            if not accessibility_result["accessible"]:
                return self._create_error_result(
                    strategy, test_id, 
                    f"사이트 접근 불가: {accessibility_result['error']}"
                )
            
            # 2. 선택자 유효성 테스트
            selector_results = await self._test_selectors(strategy)
            
            # 3. 데이터 추출 테스트
            extraction_results = await self._test_data_extraction(strategy, pages_to_test)
            
            # 4. 데이터 품질 평가
            quality_metrics = await self._evaluate_data_quality(extraction_results["sample_data"])
            
            # 5. 성능 측정
            performance_metrics = await self._measure_performance(strategy, extraction_results)
            
            # 6. 전체 메트릭 계산
            overall_metrics = self._calculate_overall_metrics(
                selector_results, extraction_results, quality_metrics, performance_metrics
            )
            
            # 7. 테스트 결과 결정
            overall_result = self._determine_overall_result(overall_metrics)
            
            # 8. 개선 제안 생성
            improvement_suggestions = await self._generate_improvement_suggestions(
                strategy, selector_results, extraction_results, overall_metrics
            )
            
            # 9. 업데이트된 전략 생성 (필요시)
            updated_strategy = None
            if overall_result in [TestResult.PARTIAL_SUCCESS, TestResult.FAILURE]:
                updated_strategy = await self._create_updated_strategy(
                    strategy, improvement_suggestions, selector_results
                )
            
            end_time = time.time()
            test_duration = end_time - start_time
            
            result = StrategyTestResult(
                strategy_id=strategy.strategy_id,
                test_id=test_id,
                site_url=strategy.site_url,
                overall_result=overall_result,
                metrics=overall_metrics,
                selector_results=selector_results,
                sample_data=extraction_results["sample_data"][:10],  # 샘플 10개만
                improvement_suggestions=improvement_suggestions,
                updated_strategy=updated_strategy,
                test_duration=test_duration,
                browser_info=await self._get_browser_info()
            )
            
            logger.info(f"✅ 전략 테스트 완료: {test_id} | 결과: {overall_result.value} | {test_duration:.1f}초")
            return result
            
        except Exception as e:
            end_time = time.time()
            test_duration = end_time - start_time
            
            logger.error(f"❌ 전략 테스트 실패: {test_id} - {str(e)}")
            
            return StrategyTestResult(
                strategy_id=strategy.strategy_id,
                test_id=test_id,
                site_url=strategy.site_url,
                overall_result=TestResult.ERROR,
                metrics=TestMetrics(test_duration=test_duration),
                error_messages=[str(e)],
                test_duration=test_duration
            )
    
    async def _test_site_accessibility(self, url: str) -> Dict[str, Any]:
        """사이트 접근성 테스트"""
        try:
            page = await self.context.new_page()
            
            # 페이지 로드 테스트
            response = await page.goto(url, timeout=self.test_config["timeout"])
            
            if response.status >= 400:
                await page.close()
                return {
                    "accessible": False,
                    "error": f"HTTP {response.status}",
                    "status_code": response.status
                }
            
            # 기본 컨텐츠 확인
            await page.wait_for_load_state("networkidle", timeout=10000)
            
            # 페이지 제목 확인
            title = await page.title()
            
            await page.close()
            
            return {
                "accessible": True,
                "status_code": response.status,
                "title": title,
                "load_time": time.time()
            }
            
        except Exception as e:
            return {
                "accessible": False,
                "error": str(e)
            }
    
    async def _test_selectors(self, strategy: CollectionStrategy) -> Dict[str, Any]:
        """선택자 유효성 테스트"""
        page = await self.context.new_page()
        
        try:
            await page.goto(strategy.site_url, timeout=self.test_config["timeout"])
            await page.wait_for_load_state("networkidle", timeout=10000)
            
            selector_results = {}
            
            # 각 선택자 테스트
            for field, selector in strategy.selectors.items():
                if not selector:
                    continue
                    
                try:
                    elements = await page.query_selector_all(selector)
                    
                    selector_results[field] = {
                        "selector": selector,
                        "found_count": len(elements),
                        "valid": len(elements) > 0,
                        "sample_texts": []
                    }
                    
                    # 샘플 텍스트 추출 (처음 3개)
                    for i, element in enumerate(elements[:3]):
                        try:
                            if field == "url":
                                text = await element.get_attribute("href")
                            else:
                                text = await element.text_content()
                            
                            if text and text.strip():
                                selector_results[field]["sample_texts"].append(text.strip()[:100])
                        except:
                            pass
                    
                    logger.debug(f"선택자 테스트 - {field}: {len(elements)}개 발견")
                    
                except Exception as e:
                    selector_results[field] = {
                        "selector": selector,
                        "found_count": 0,
                        "valid": False,
                        "error": str(e)
                    }
                    logger.warning(f"선택자 실패 - {field} ({selector}): {str(e)}")
            
            await page.close()
            return selector_results
            
        except Exception as e:
            await page.close()
            logger.error(f"선택자 테스트 실패: {str(e)}")
            return {"error": str(e)}
    
    async def _test_data_extraction(
        self, 
        strategy: CollectionStrategy, 
        pages_to_test: int
    ) -> Dict[str, Any]:
        """데이터 추출 테스트"""
        page = await self.context.new_page()
        
        try:
            all_extracted_data = []
            successful_pages = 0
            
            for page_num in range(1, pages_to_test + 1):
                try:
                    # 페이지 로드 (첫 페이지 또는 페이지네이션)
                    if page_num == 1:
                        await page.goto(strategy.site_url, timeout=self.test_config["timeout"])
                    else:
                        # 페이지네이션 처리
                        next_success = await self._navigate_to_next_page(page, strategy.pagination)
                        if not next_success:
                            logger.info(f"페이지 {page_num} 네비게이션 실패 - 테스트 중단")
                            break
                    
                    await page.wait_for_load_state("networkidle", timeout=10000)
                    
                    # 컨테이너 요소들 찾기
                    container_selector = strategy.selectors.get("container", "body")
                    containers = await page.query_selector_all(container_selector)
                    
                    if not containers:
                        logger.warning(f"페이지 {page_num}: 컨테이너 요소를 찾을 수 없음")
                        continue
                    
                    # 각 컨테이너에서 데이터 추출
                    page_data = []
                    for container in containers:
                        item_data = {}
                        
                        for field, selector in strategy.selectors.items():
                            if field == "container" or not selector:
                                continue
                            
                            try:
                                element = await container.query_selector(selector)
                                if element:
                                    if field == "url":
                                        value = await element.get_attribute("href")
                                        # 상대 URL을 절대 URL로 변환
                                        if value and not value.startswith("http"):
                                            base_url = page.url
                                            from urllib.parse import urljoin
                                            value = urljoin(base_url, value)
                                    else:
                                        value = await element.text_content()
                                    
                                    if value and value.strip():
                                        item_data[field] = value.strip()
                                
                            except Exception as e:
                                logger.debug(f"필드 추출 실패 - {field}: {str(e)}")
                        
                        # 최소한의 데이터가 있으면 추가
                        if len(item_data) >= 1:
                            item_data["_source_page"] = page_num
                            item_data["_extracted_at"] = datetime.now().isoformat()
                            page_data.append(item_data)
                    
                    all_extracted_data.extend(page_data)
                    successful_pages += 1
                    
                    logger.info(f"페이지 {page_num}: {len(page_data)}개 아이템 추출")
                    
                    # 페이지 간 지연
                    if strategy.pagination and strategy.pagination.get("delay_between_pages", 0) > 0:
                        await asyncio.sleep(strategy.pagination["delay_between_pages"])
                
                except Exception as e:
                    logger.warning(f"페이지 {page_num} 추출 실패: {str(e)}")
                    continue
            
            await page.close()
            
            return {
                "total_items": len(all_extracted_data),
                "successful_pages": successful_pages,
                "pages_tested": pages_to_test,
                "sample_data": all_extracted_data,
                "extraction_success_rate": successful_pages / pages_to_test if pages_to_test > 0 else 0
            }
            
        except Exception as e:
            await page.close()
            logger.error(f"데이터 추출 테스트 실패: {str(e)}")
            return {
                "total_items": 0,
                "successful_pages": 0,
                "pages_tested": pages_to_test,
                "sample_data": [],
                "extraction_success_rate": 0,
                "error": str(e)
            }
    
    async def _navigate_to_next_page(self, page: Page, pagination_config: Dict) -> bool:
        """다음 페이지로 네비게이션"""
        if not pagination_config or not pagination_config.get("enabled"):
            return False
        
        try:
            method = pagination_config.get("method", "link_based")
            
            if method == "link_based":
                # 링크 클릭 방식
                next_selector = pagination_config.get("selectors", {}).get("next_page")
                if next_selector:
                    next_link = await page.query_selector(next_selector)
                    if next_link:
                        await next_link.click()
                        await page.wait_for_load_state("networkidle", timeout=10000)
                        return True
            
            elif method == "button_based":
                # 버튼 클릭 방식  
                next_button_selector = pagination_config.get("selectors", {}).get("next_button")
                if next_button_selector:
                    next_button = await page.query_selector(next_button_selector)
                    if next_button:
                        await next_button.click()
                        await page.wait_for_load_state("networkidle", timeout=10000)
                        return True
            
            return False
            
        except Exception as e:
            logger.debug(f"페이지네이션 실패: {str(e)}")
            return False
    
    async def _evaluate_data_quality(self, sample_data: List[Dict]) -> Dict[str, Any]:
        """데이터 품질 평가"""
        if not sample_data:
            return {
                "overall_quality": 0.0,
                "total_items": 0,
                "valid_items": 0,
                "field_quality": {}
            }
        
        total_items = len(sample_data)
        valid_items = 0
        field_quality = {}
        
        # 각 필드별 품질 평가
        for field, criteria in self.quality_criteria.items():
            field_valid = 0
            field_total = 0
            
            for item in sample_data:
                if field in item:
                    field_total += 1
                    value = item[field]
                    
                    # 기본 검증
                    if value and isinstance(value, str) and len(value.strip()) > 0:
                        # 길이 검증
                        length = len(value.strip())
                        if (criteria.get("min_length", 0) <= length <= 
                            criteria.get("max_length", 1000)):
                            
                            # URL 검증
                            if field == "url" and criteria.get("must_be_valid_url"):
                                if self._is_valid_url(value):
                                    field_valid += 1
                            else:
                                field_valid += 1
            
            field_quality[field] = {
                "success_rate": field_valid / field_total if field_total > 0 else 0,
                "total_checked": field_total,
                "valid_count": field_valid
            }
        
        # 전체 아이템 유효성 검증
        for item in sample_data:
            is_valid = True
            
            # 필수 필드 확인
            for field, criteria in self.quality_criteria.items():
                if criteria.get("required", False):
                    if field not in item or not item[field]:
                        is_valid = False
                        break
            
            if is_valid:
                valid_items += 1
        
        overall_quality = valid_items / total_items if total_items > 0 else 0
        
        return {
            "overall_quality": overall_quality,
            "total_items": total_items,
            "valid_items": valid_items,
            "field_quality": field_quality
        }
    
    def _is_valid_url(self, url: str) -> bool:
        """URL 유효성 검증"""
        import re
        url_pattern = re.compile(
            r'^https?://'  # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
            r'localhost|'  # localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
            r'(?::\d+)?'  # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        return url_pattern.match(url) is not None
    
    async def _measure_performance(
        self, 
        strategy: CollectionStrategy, 
        extraction_results: Dict
    ) -> Dict[str, Any]:
        """성능 측정"""
        total_items = extraction_results.get("total_items", 0)
        successful_pages = extraction_results.get("successful_pages", 0)
        
        # 추출 속도 계산 (추정)
        estimated_time_per_page = strategy.performance_config.get("delay_between_requests", 2.0) * 2
        total_estimated_time = successful_pages * estimated_time_per_page
        
        extraction_speed = total_items / total_estimated_time if total_estimated_time > 0 else 0
        
        return {
            "extraction_speed": extraction_speed,
            "items_per_page": total_items / successful_pages if successful_pages > 0 else 0,
            "estimated_total_time": total_estimated_time,
            "page_success_rate": successful_pages / extraction_results.get("pages_tested", 1)
        }
    
    def _calculate_overall_metrics(
        self, 
        selector_results: Dict, 
        extraction_results: Dict,
        quality_metrics: Dict,
        performance_metrics: Dict
    ) -> TestMetrics:
        """전체 메트릭 계산"""
        
        # 선택자 성공률
        valid_selectors = sum(1 for r in selector_results.values() 
                            if isinstance(r, dict) and r.get("valid", False))
        total_selectors = len(selector_results)
        selector_success_rate = valid_selectors / total_selectors if total_selectors > 0 else 0
        
        # 기타 메트릭
        data_quality_score = quality_metrics.get("overall_quality", 0.0)
        extraction_speed = performance_metrics.get("extraction_speed", 0.0)
        total_items_found = extraction_results.get("total_items", 0)
        valid_items_extracted = quality_metrics.get("valid_items", 0)
        
        # 에러 카운트
        error_count = 0
        for result in selector_results.values():
            if isinstance(result, dict) and "error" in result:
                error_count += 1
        
        return TestMetrics(
            selector_success_rate=selector_success_rate,
            data_quality_score=data_quality_score,
            extraction_speed=extraction_speed,
            error_count=error_count,
            total_items_found=total_items_found,
            valid_items_extracted=valid_items_extracted
        )
    
    def _determine_overall_result(self, metrics: TestMetrics) -> TestResult:
        """전체 테스트 결과 결정"""
        
        # 성공 조건
        success_threshold = 0.8
        partial_success_threshold = 0.5
        
        # 종합 점수 계산
        overall_score = (
            metrics.selector_success_rate * 0.4 +
            metrics.data_quality_score * 0.4 +
            min(metrics.extraction_speed / 5.0, 1.0) * 0.2  # 5 items/sec을 최대로
        )
        
        if overall_score >= success_threshold and metrics.error_count == 0:
            return TestResult.SUCCESS
        elif overall_score >= partial_success_threshold:
            return TestResult.PARTIAL_SUCCESS  
        else:
            return TestResult.FAILURE
    
    async def _generate_improvement_suggestions(
        self,
        strategy: CollectionStrategy,
        selector_results: Dict,
        extraction_results: Dict,
        metrics: TestMetrics
    ) -> List[str]:
        """개선 제안 생성"""
        suggestions = []
        
        # 선택자 관련 제안
        for field, result in selector_results.items():
            if isinstance(result, dict):
                if not result.get("valid", False):
                    suggestions.append(f"'{field}' 선택자 수정 필요: {result.get('selector', '')}")
                elif result.get("found_count", 0) < 3:
                    suggestions.append(f"'{field}' 선택자가 충분한 요소를 찾지 못함 (발견: {result.get('found_count', 0)}개)")
        
        # 데이터 품질 관련 제안
        if metrics.data_quality_score < 0.7:
            suggestions.append("데이터 품질이 낮음 - 필드 추출 로직 개선 필요")
        
        # 성능 관련 제안
        if metrics.extraction_speed < 1.0:
            suggestions.append("추출 속도가 느림 - 성능 최적화 필요")
        
        # 에러 관련 제안
        if metrics.error_count > 0:
            suggestions.append(f"선택자 오류 {metrics.error_count}개 - 에러 처리 개선 필요")
        
        return suggestions
    
    async def _create_updated_strategy(
        self,
        original_strategy: CollectionStrategy,
        suggestions: List[str],
        selector_results: Dict
    ) -> CollectionStrategy:
        """개선된 전략 생성"""
        # 원본 전략 복사
        updated_strategy = CollectionStrategy(
            strategy_id=f"{original_strategy.strategy_id}_updated",
            site_id=original_strategy.site_id,
            site_url=original_strategy.site_url,
            selectors=original_strategy.selectors.copy(),
            pagination=original_strategy.pagination.copy(),
            extraction_rules=original_strategy.extraction_rules.copy(),
            performance_config=original_strategy.performance_config.copy(),
            confidence=StrategyConfidence.MEDIUM,  # 업데이트된 전략은 중간 신뢰도
            created_by="playwright_tester"
        )
        
        # 실패한 선택자를 대안으로 교체
        for field, result in selector_results.items():
            if isinstance(result, dict) and not result.get("valid", False):
                # 대안 선택자 제안 (패턴 기반)
                alternative_selectors = self._suggest_alternative_selectors(field)
                if alternative_selectors:
                    updated_strategy.selectors[field] = alternative_selectors[0]
        
        # 성능 설정 조정
        if "성능 최적화" in ' '.join(suggestions):
            updated_strategy.performance_config["delay_between_requests"] = max(
                updated_strategy.performance_config.get("delay_between_requests", 2.0) * 0.8,
                1.0
            )
        
        return updated_strategy
    
    def _suggest_alternative_selectors(self, field: str) -> List[str]:
        """필드별 대안 선택자 제안"""
        alternatives = {
            "title": ["h1", "h2", "h3", ".title", ".subject", ".headline", "a"],
            "agency": [".agency", ".author", ".publisher", ".org", ".institution"],
            "category": [".category", ".tag", ".type", ".classification"],
            "date": [".date", ".time", ".created", ".published", "[class*='date']"],
            "url": ["a[href]", ".link", "[href]"],
            "content": [".content", ".summary", ".description", "p"]
        }
        
        return alternatives.get(field, [])
    
    def _create_error_result(
        self, 
        strategy: CollectionStrategy, 
        test_id: str, 
        error_message: str
    ) -> StrategyTestResult:
        """에러 결과 생성"""
        return StrategyTestResult(
            strategy_id=strategy.strategy_id,
            test_id=test_id,
            site_url=strategy.site_url,
            overall_result=TestResult.ERROR,
            metrics=TestMetrics(),
            error_messages=[error_message]
        )
    
    def _generate_test_id(self, strategy_id: str) -> str:
        """테스트 ID 생성"""
        import hashlib
        timestamp = int(datetime.now().timestamp())
        hash_input = f"{strategy_id}_{timestamp}".encode()
        hash_hex = hashlib.md5(hash_input).hexdigest()[:8]
        return f"test_{hash_hex}_{timestamp}"
    
    async def _get_browser_info(self) -> Dict[str, str]:
        """브라우저 정보 수집"""
        if not self.browser:
            return {}
        
        try:
            return {
                "name": self.browser.browser_type.name,
                "version": self.browser.version,
                "headless": str(self.headless),
                "viewport": f"{self.browser_config['viewport']['width']}x{self.browser_config['viewport']['height']}"
            }
        except:
            return {}


# 유틸리티 함수들

async def test_strategy_with_playwright(
    strategy: CollectionStrategy,
    headless: bool = True,
    pages_to_test: int = 3
) -> StrategyTestResult:
    """Playwright로 전략 테스트 (원스톱 함수)"""
    
    tester = PlaywrightDynamicTester(headless=headless)
    
    try:
        await tester.initialize()
        result = await tester.test_collection_strategy(strategy, pages_to_test)
        return result
    finally:
        await tester.close()


async def batch_test_strategies(
    strategies: List[CollectionStrategy],
    headless: bool = True,
    max_concurrent: int = 3
) -> List[StrategyTestResult]:
    """여러 전략을 배치로 테스트"""
    
    semaphore = asyncio.Semaphore(max_concurrent)
    
    async def test_single_strategy(strategy: CollectionStrategy):
        async with semaphore:
            return await test_strategy_with_playwright(strategy, headless)
    
    tasks = [test_single_strategy(strategy) for strategy in strategies]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    
    # 예외 처리
    processed_results = []
    for i, result in enumerate(results):
        if isinstance(result, Exception):
            logger.error(f"전략 {strategies[i].strategy_id} 테스트 실패: {str(result)}")
            # 에러 결과 생성
            error_result = StrategyTestResult(
                strategy_id=strategies[i].strategy_id,
                test_id=f"error_{int(datetime.now().timestamp())}",
                site_url=strategies[i].site_url,
                overall_result=TestResult.ERROR,
                metrics=TestMetrics(),
                error_messages=[str(result)]
            )
            processed_results.append(error_result)
        else:
            processed_results.append(result)
    
    return processed_results


# 테스트 실행 함수
async def demo_playwright_testing():
    """Playwright 테스터 데모"""
    
    # 샘플 전략 생성
    sample_strategy = CollectionStrategy(
        strategy_id="demo_strategy_001",
        site_id="bizinfo_go_kr",
        site_url="https://www.bizinfo.go.kr/web/lay1/bbs/S1T122C128/AS/list.do",
        selectors={
            "container": "table tbody tr",
            "title": ".title a",
            "agency": ".agency",
            "date": ".date"
        },
        pagination={
            "enabled": True,
            "method": "link_based",
            "selectors": {"next_page": "a:contains('다음')"},
            "max_pages": 3
        }
    )
    
    logger.info("🧪 Playwright 테스터 데모 시작")
    
    try:
        result = await test_strategy_with_playwright(
            strategy=sample_strategy,
            headless=True,
            pages_to_test=2
        )
        
        logger.info(f"테스트 결과: {result.overall_result.value}")
        logger.info(f"총 아이템: {result.metrics.total_items_found}")
        logger.info(f"유효 아이템: {result.metrics.valid_items_extracted}")
        logger.info(f"선택자 성공률: {result.metrics.selector_success_rate:.1%}")
        logger.info(f"데이터 품질: {result.metrics.data_quality_score:.1%}")
        
        if result.improvement_suggestions:
            logger.info("개선 제안:")
            for suggestion in result.improvement_suggestions:
                logger.info(f"  - {suggestion}")
        
        return result
        
    except Exception as e:
        logger.error(f"❌ 데모 실행 실패: {str(e)}")
        raise


if __name__ == "__main__":
    # 로깅 설정
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # 데모 실행
    asyncio.run(demo_playwright_testing())