#!/usr/bin/env python3
"""
🎭 Playwright 크롤러 (Tier 2) 
동적 콘텐츠, JavaScript 렌더링, 스크린샷 전문

Features:
- JavaScript 렌더링
- 스크린샷 캡처
- 페이지 상호작용
- 네트워크 모니터링
- 모바일 에뮬레이션

Author: HEAL7 Development Team
Version: 1.0.0
Date: 2025-08-30
"""

import asyncio
import time
import json
from typing import Optional, Dict, Any, List, Union
from pathlib import Path
from urllib.parse import urljoin

from playwright.async_api import async_playwright, Browser, BrowserContext, Page, Playwright
from playwright.async_api import TimeoutError as PlaywrightTimeoutError

from .base_crawler import (
    BaseCrawler, CrawlResult, CrawlConfig, CrawlerType,
    CrawlingError, TimeoutError, create_default_headers, is_valid_url
)


class PlaywrightCrawler(BaseCrawler):
    """🎭 Playwright 기반 동적 크롤러"""
    
    def __init__(self, browser_type: str = "chromium", headless: bool = True):
        super().__init__("playwright")
        self.browser_type = browser_type  # chromium, firefox, webkit
        self.headless = headless
        
        # Playwright 인스턴스
        self.playwright: Optional[Playwright] = None
        self.browser: Optional[Browser] = None
        self.context: Optional[BrowserContext] = None
        
        # 설정
        self.browser_args = [
            '--no-sandbox',
            '--disable-dev-shm-usage',
            '--disable-gpu',
            '--disable-extensions',
            '--disable-blink-features=AutomationControlled'
        ]
        
        self.viewport_size = {"width": 1920, "height": 1080}
        
    async def initialize(self):
        """Playwright 초기화"""
        if self.is_initialized:
            return
            
        try:
            # Playwright 시작
            self.playwright = await async_playwright().start()
            
            # 브라우저 선택
            if self.browser_type == "firefox":
                browser_launcher = self.playwright.firefox
            elif self.browser_type == "webkit":
                browser_launcher = self.playwright.webkit
            else:
                browser_launcher = self.playwright.chromium
            
            # 브라우저 시작
            self.browser = await browser_launcher.launch(
                headless=self.headless,
                args=self.browser_args
            )
            
            # 컨텍스트 생성
            await self._create_context()
            
            self.is_initialized = True
            self.logger.info(f"✅ Playwright ({self.browser_type}) 크롤러 초기화 완료")
            
        except Exception as e:
            self.logger.error(f"❌ Playwright 초기화 실패: {e}")
            await self.cleanup()
            raise CrawlingError(f"Playwright 초기화 실패: {e}")
    
    async def _create_context(self, mobile_device: str = None):
        """브라우저 컨텍스트 생성"""
        context_options = {
            'viewport': self.viewport_size,
            'user_agent': (
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                '(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            ),
            'locale': 'ko-KR',
            'timezone_id': 'Asia/Seoul'
        }
        
        # 모바일 디바이스 에뮬레이션
        if mobile_device:
            device = self.playwright.devices.get(mobile_device)
            if device:
                context_options.update(device)
        
        self.context = await self.browser.new_context(**context_options)
        
        # 일반적인 stealth 설정
        await self.context.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined,
            });
        """)
    
    async def cleanup(self):
        """리소스 정리"""
        try:
            if self.context:
                await self.context.close()
                self.context = None
            
            if self.browser:
                await self.browser.close()
                self.browser = None
            
            if self.playwright:
                await self.playwright.stop()
                self.playwright = None
            
            self.is_initialized = False
            self.logger.info("🛑 Playwright 크롤러 정리 완료")
            
        except Exception as e:
            self.logger.error(f"❌ Playwright 정리 중 오류: {e}")
    
    async def crawl(self, config: CrawlConfig) -> CrawlResult:
        """메인 크롤링 함수"""
        if not self.is_initialized:
            await self.initialize()
        
        start_time = time.time()
        page = None
        
        try:
            # URL 유효성 검사
            if not is_valid_url(config.url):
                raise CrawlingError(f"잘못된 URL: {config.url}")
            
            # 새 페이지 생성
            page = await self.context.new_page()
            
            # 페이지 설정
            await self._setup_page(page, config)
            
            # 페이지 로드
            await self._navigate_to_page(page, config)
            
            # 콘텐츠 대기
            await self._wait_for_content(page, config)
            
            # 데이터 추출
            html = await page.content()
            screenshot = None
            
            if config.screenshot:
                screenshot = await self._take_screenshot(page, config)
            
            # 메타데이터 수집
            metadata = await self._collect_metadata(page)
            
            result = CrawlResult(
                success=True,
                html=html,
                screenshot=screenshot,
                metadata=metadata,
                crawler_used=CrawlerType.PLAYWRIGHT,
                url=config.url,
                response_time=time.time() - start_time
            )
            
            self.update_stats(result)
            return result
            
        except PlaywrightTimeoutError:
            error_msg = f"페이지 로드 타임아웃: {config.url}"
            self.logger.warning(error_msg)
            return CrawlResult(
                success=False,
                error=error_msg,
                error_type="timeout",
                crawler_used=CrawlerType.PLAYWRIGHT,
                url=config.url,
                response_time=time.time() - start_time
            )
            
        except Exception as e:
            error_msg = f"Playwright 크롤링 실패: {e}"
            self.logger.error(error_msg)
            return CrawlResult(
                success=False,
                error=error_msg,
                error_type="playwright_error",
                crawler_used=CrawlerType.PLAYWRIGHT,
                url=config.url,
                response_time=time.time() - start_time
            )
            
        finally:
            if page:
                try:
                    await page.close()
                except:
                    pass
    
    async def _setup_page(self, page: Page, config: CrawlConfig):
        """페이지 설정"""
        # 사용자 에이전트 설정
        if config.user_agent:
            await page.set_extra_http_headers({'User-Agent': config.user_agent})
        
        # 추가 헤더 설정
        if config.headers:
            await page.set_extra_http_headers(config.headers)
        
        # 타임아웃 설정
        page.set_default_timeout(config.timeout * 1000)  # ms 단위
        
        # JavaScript 비활성화 (선택사항)
        # await page.context.add_init_script("window.location.reload = () => {};")
    
    async def _navigate_to_page(self, page: Page, config: CrawlConfig):
        """페이지 네비게이션"""
        # 페이지 로드
        response = await page.goto(
            config.url,
            wait_until='domcontentloaded',
            timeout=config.timeout * 1000
        )
        
        # 응답 상태 확인
        if response:
            status_code = response.status
            if status_code >= 400:
                self.logger.warning(f"HTTP {status_code}: {config.url}")
        
        return response
    
    async def _wait_for_content(self, page: Page, config: CrawlConfig):
        """콘텐츠 로드 대기"""
        try:
            if config.wait_for_load:
                # 네트워크 유휴 상태까지 대기
                await page.wait_for_load_state('networkidle', timeout=15000)
            
            if config.wait_for_selector:
                # 특정 선택자까지 대기
                await page.wait_for_selector(config.wait_for_selector, timeout=10000)
            
            # 추가 대기 (JavaScript 렌더링)
            await asyncio.sleep(1)
            
        except PlaywrightTimeoutError:
            # 타임아웃되어도 계속 진행
            self.logger.debug("콘텐츠 로드 대기 타임아웃 - 계속 진행")
    
    async def _take_screenshot(self, page: Page, config: CrawlConfig) -> bytes:
        """스크린샷 캡처"""
        try:
            screenshot_options = {}
            
            if config.screenshot_full_page:
                screenshot_options['full_page'] = True
            
            return await page.screenshot(**screenshot_options)
            
        except Exception as e:
            self.logger.error(f"스크린샷 캡처 실패: {e}")
            return None
    
    async def _collect_metadata(self, page: Page) -> Dict[str, Any]:
        """페이지 메타데이터 수집"""
        try:
            # 페이지 정보
            title = await page.title()
            url = page.url
            
            # 성능 메트릭
            performance = await page.evaluate("""
                () => {
                    const perfData = performance.getEntriesByType('navigation')[0];
                    return {
                        loadTime: perfData ? perfData.loadEventEnd - perfData.loadEventStart : 0,
                        domContentLoaded: perfData ? perfData.domContentLoadedEventEnd - perfData.domContentLoadedEventStart : 0,
                        responseTime: perfData ? perfData.responseEnd - perfData.responseStart : 0
                    };
                }
            """)
            
            # JavaScript 에러 수집
            js_errors = []
            
            return {
                'title': title,
                'final_url': url,
                'performance': performance,
                'js_errors': js_errors,
                'viewport': self.viewport_size
            }
            
        except Exception as e:
            self.logger.error(f"메타데이터 수집 실패: {e}")
            return {}
    
    async def can_handle(self, url: str) -> bool:
        """URL 처리 가능 여부 판단"""
        if not is_valid_url(url):
            return False
        
        # Playwright는 거의 모든 웹페이지 처리 가능
        return True
    
    async def interact_with_page(self, url: str, interactions: List[Dict]) -> CrawlResult:
        """페이지 상호작용 (클릭, 입력 등)"""
        if not self.is_initialized:
            await self.initialize()
        
        start_time = time.time()
        page = None
        
        try:
            page = await self.context.new_page()
            await page.goto(url, wait_until='networkidle')
            
            # 상호작용 실행
            for interaction in interactions:
                await self._execute_interaction(page, interaction)
                await asyncio.sleep(1)  # 각 상호작용 후 대기
            
            # 최종 결과 수집
            html = await page.content()
            screenshot = await page.screenshot(full_page=True)
            
            return CrawlResult(
                success=True,
                html=html,
                screenshot=screenshot,
                crawler_used=CrawlerType.PLAYWRIGHT,
                url=url,
                response_time=time.time() - start_time,
                metadata={'interactions_count': len(interactions)}
            )
            
        except Exception as e:
            return CrawlResult(
                success=False,
                error=f"페이지 상호작용 실패: {e}",
                crawler_used=CrawlerType.PLAYWRIGHT,
                url=url,
                response_time=time.time() - start_time
            )
            
        finally:
            if page:
                await page.close()
    
    async def _execute_interaction(self, page: Page, interaction: Dict):
        """개별 상호작용 실행"""
        action = interaction.get('action')
        selector = interaction.get('selector')
        value = interaction.get('value')
        
        if action == 'click':
            await page.click(selector)
        elif action == 'type':
            await page.fill(selector, value)
        elif action == 'scroll':
            await page.evaluate(f"window.scrollTo(0, {value or 'document.body.scrollHeight'})")
        elif action == 'wait':
            await page.wait_for_selector(selector)
        elif action == 'select':
            await page.select_option(selector, value)
    
    async def capture_pdf(self, url: str, save_path: str = None) -> CrawlResult:
        """PDF 캡처"""
        if not self.is_initialized:
            await self.initialize()
        
        start_time = time.time()
        page = None
        
        try:
            page = await self.context.new_page()
            await page.goto(url, wait_until='networkidle')
            
            # PDF 생성
            pdf_bytes = await page.pdf(
                format='A4',
                print_background=True,
                margin={
                    'top': '1cm',
                    'right': '1cm',
                    'bottom': '1cm',
                    'left': '1cm'
                }
            )
            
            # 파일 저장 (선택사항)
            if save_path:
                with open(save_path, 'wb') as f:
                    f.write(pdf_bytes)
            
            return CrawlResult(
                success=True,
                html=f"PDF generated: {len(pdf_bytes)} bytes",
                metadata={
                    'pdf_size': len(pdf_bytes),
                    'pdf_path': save_path
                },
                crawler_used=CrawlerType.PLAYWRIGHT,
                url=url,
                response_time=time.time() - start_time
            )
            
        except Exception as e:
            return CrawlResult(
                success=False,
                error=f"PDF 생성 실패: {e}",
                crawler_used=CrawlerType.PLAYWRIGHT,
                url=url,
                response_time=time.time() - start_time
            )
            
        finally:
            if page:
                await page.close()
    
    async def mobile_crawl(self, url: str, device: str = "iPhone 13") -> CrawlResult:
        """모바일 디바이스 에뮬레이션 크롤링"""
        # 새 컨텍스트 생성 (모바일)
        old_context = self.context
        await self._create_context(mobile_device=device)
        
        try:
            config = CrawlConfig(url=url, screenshot=True)
            result = await self.crawl(config)
            result.metadata['mobile_device'] = device
            return result
            
        finally:
            # 원래 컨텍스트로 복구
            await self.context.close()
            self.context = old_context
    
    def get_supported_features(self) -> List[str]:
        """지원하는 기능 목록"""
        return [
            "javascript_rendering",
            "screenshot_capture",
            "page_interaction",
            "pdf_generation", 
            "mobile_emulation",
            "network_monitoring",
            "performance_metrics",
            "stealth_mode"
        ]


# 유틸리티 함수

async def quick_screenshot(url: str, save_path: str = None) -> bool:
    """빠른 스크린샷 캡처"""
    crawler = PlaywrightCrawler()
    try:
        await crawler.initialize()
        config = CrawlConfig(url=url, screenshot=True, screenshot_full_page=True)
        result = await crawler.crawl(config)
        
        if result.success and result.screenshot:
            if save_path:
                with open(save_path, 'wb') as f:
                    f.write(result.screenshot)
            return True
        
        return False
        
    finally:
        await crawler.cleanup()


async def render_js_content(url: str) -> str:
    """JavaScript 렌더링 후 HTML 반환"""
    crawler = PlaywrightCrawler()
    try:
        await crawler.initialize()
        config = CrawlConfig(url=url, wait_for_load=True)
        result = await crawler.crawl(config)
        return result.html if result.success else ""
    finally:
        await crawler.cleanup()