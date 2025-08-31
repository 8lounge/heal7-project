#!/usr/bin/env python3
"""
🛡️ Selenium + Undetected 크롤러 (Tier 3)
Anti-bot 우회 및 최대 호환성 크롤링

Features:
- Cloudflare 우회
- Bot 감지 회피
- 강력한 사이트 호환성
- 캡차 대응 가능
- 레거시 브라우저 지원

Author: HEAL7 Development Team
Version: 1.0.0
Date: 2025-08-30
"""

import asyncio
import time
import json
from typing import Optional, Dict, Any, List
from concurrent.futures import ThreadPoolExecutor
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import (
    TimeoutException, WebDriverException, NoSuchElementException
)

try:
    import undetected_chromedriver as uc
except ImportError:
    uc = None

from .base_crawler import (
    BaseCrawler, CrawlResult, CrawlConfig, CrawlerType,
    CrawlingError, TimeoutError, AntiBotDetectionError, create_default_headers, is_valid_url
)


class SeleniumCrawler(BaseCrawler):
    """🛡️ Selenium + Undetected 기반 스텔스 크롤러"""
    
    def __init__(self, use_undetected: bool = True, headless: bool = True):
        super().__init__("selenium")
        self.use_undetected = use_undetected
        self.headless = headless
        self.driver = None
        self.executor = ThreadPoolExecutor(max_workers=1)  # Selenium은 동기식
        
        # Chrome 옵션
        self.chrome_options = self._create_chrome_options()
        
    def _create_chrome_options(self):
        """Chrome 옵션 생성"""
        if self.use_undetected and uc:
            options = uc.ChromeOptions()
        else:
            from selenium.webdriver.chrome.options import Options
            options = Options()
        
        # 기본 옵션
        if self.headless:
            options.add_argument('--headless')
        
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument('--disable-extensions')
        options.add_argument('--disable-logging')
        options.add_argument('--disable-web-security')
        options.add_argument('--allow-running-insecure-content')
        options.add_argument('--ignore-certificate-errors')
        
        # 스텔스 옵션 (Chrome 호환성 최적화)
        options.add_argument('--disable-blink-features=AutomationControlled')
        # Chrome 최신 버전 호환성을 위해 실험적 옵션 제거
        # options.add_experimental_option("excludeSwitches", ["enable-automation"])
        # options.add_experimental_option('useAutomationExtension', False)
        
        # 창 크기
        options.add_argument('--window-size=1920,1080')
        
        # 사용자 에이전트
        options.add_argument(
            '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
            'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        )
        
        return options
    
    async def initialize(self):
        """Selenium 드라이버 초기화"""
        if self.is_initialized:
            return
            
        def _init_driver():
            try:
                if self.use_undetected and uc:
                    # Undetected Chrome 사용
                    driver = uc.Chrome(options=self.chrome_options)
                    
                    # 추가 스텔스 설정
                    driver.execute_script("""
                        Object.defineProperty(navigator, 'webdriver', {
                            get: () => undefined,
                        });
                    """)
                    
                    driver.execute_cdp_cmd('Network.setUserAgentOverride', {
                        "userAgent": driver.execute_script("return navigator.userAgent").replace("Headless", "")
                    })
                    
                else:
                    # 일반 Chrome WebDriver
                    from selenium.webdriver import Chrome
                    driver = Chrome(options=self.chrome_options)
                
                return driver
                
            except Exception as e:
                raise CrawlingError(f"Selenium 드라이버 초기화 실패: {e}")
        
        try:
            # 비동기적으로 드라이버 초기화
            self.driver = await asyncio.get_event_loop().run_in_executor(
                self.executor, _init_driver
            )
            
            self.is_initialized = True
            driver_type = "Undetected Chrome" if self.use_undetected else "Chrome"
            self.logger.info(f"✅ Selenium ({driver_type}) 크롤러 초기화 완료")
            
        except Exception as e:
            self.logger.error(f"❌ Selenium 초기화 실패: {e}")
            raise CrawlingError(f"Selenium 초기화 실패: {e}")
    
    async def cleanup(self):
        """리소스 정리"""
        def _cleanup_driver():
            if self.driver:
                try:
                    self.driver.quit()
                except:
                    pass
        
        if self.driver:
            await asyncio.get_event_loop().run_in_executor(
                self.executor, _cleanup_driver
            )
            self.driver = None
        
        if hasattr(self, 'executor'):
            self.executor.shutdown(wait=True)
        
        self.is_initialized = False
        self.logger.info("🛑 Selenium 크롤러 정리 완료")
    
    async def crawl(self, config: CrawlConfig) -> CrawlResult:
        """메인 크롤링 함수"""
        if not self.is_initialized:
            await self.initialize()
        
        start_time = time.time()
        
        def _crawl_sync():
            try:
                # URL 유효성 검사
                if not is_valid_url(config.url):
                    raise CrawlingError(f"잘못된 URL: {config.url}")
                
                # 페이지 로드
                self.driver.set_page_load_timeout(config.timeout)
                self.driver.get(config.url)
                
                # Anti-bot 감지 확인
                if self._is_bot_detected():
                    raise AntiBotDetectionError("Bot 감지됨")
                
                # 콘텐츠 로드 대기
                self._wait_for_content(config)
                
                # HTML 추출
                html = self.driver.page_source
                
                # 스크린샷 (선택사항)
                screenshot = None
                if config.screenshot:
                    screenshot = self._take_screenshot(config)
                
                # 메타데이터 수집
                metadata = self._collect_metadata()
                
                return CrawlResult(
                    success=True,
                    html=html,
                    screenshot=screenshot,
                    metadata=metadata,
                    crawler_used=CrawlerType.SELENIUM,
                    url=config.url,
                    response_time=time.time() - start_time
                )
                
            except TimeoutException:
                raise TimeoutError(f"페이지 로드 타임아웃: {config.url}")
            except AntiBotDetectionError:
                raise
            except Exception as e:
                raise CrawlingError(f"Selenium 크롤링 실패: {e}")
        
        try:
            # 동기 함수를 비동기로 실행
            result = await asyncio.get_event_loop().run_in_executor(
                self.executor, _crawl_sync
            )
            
            self.update_stats(result)
            return result
            
        except AntiBotDetectionError:
            error_msg = f"Bot 감지로 인한 크롤링 실패: {config.url}"
            self.logger.warning(error_msg)
            return CrawlResult(
                success=False,
                error=error_msg,
                error_type="antibot_detection",
                crawler_used=CrawlerType.SELENIUM,
                url=config.url,
                response_time=time.time() - start_time
            )
            
        except TimeoutError as e:
            return CrawlResult(
                success=False,
                error=str(e),
                error_type="timeout",
                crawler_used=CrawlerType.SELENIUM,
                url=config.url,
                response_time=time.time() - start_time
            )
            
        except Exception as e:
            return CrawlResult(
                success=False,
                error=str(e),
                error_type="selenium_error",
                crawler_used=CrawlerType.SELENIUM,
                url=config.url,
                response_time=time.time() - start_time
            )
    
    def _is_bot_detected(self) -> bool:
        """Bot 감지 여부 확인"""
        try:
            # Cloudflare 감지
            if "Checking your browser" in self.driver.page_source:
                return True
            
            # 기타 bot 감지 패턴
            bot_indicators = [
                "Access denied",
                "Blocked",
                "Captcha",
                "Please verify you are human",
                "Security check"
            ]
            
            page_text = self.driver.page_source.lower()
            return any(indicator.lower() in page_text for indicator in bot_indicators)
            
        except:
            return False
    
    def _wait_for_content(self, config: CrawlConfig):
        """콘텐츠 로드 대기"""
        wait = WebDriverWait(self.driver, 10)
        
        try:
            # 특정 선택자 대기
            if config.wait_for_selector:
                wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, config.wait_for_selector)))
            
            # DOM 로드 완료 대기
            if config.wait_for_load:
                wait.until(lambda driver: driver.execute_script("return document.readyState") == "complete")
                
                # JavaScript 실행 대기 (추가)
                time.sleep(2)
            
        except TimeoutException:
            # 타임아웃되어도 계속 진행
            pass
    
    def _take_screenshot(self, config: CrawlConfig) -> Optional[bytes]:
        """스크린샷 캡처"""
        try:
            if config.screenshot_full_page:
                # 전체 페이지 스크린샷
                total_height = self.driver.execute_script("return document.body.scrollHeight")
                self.driver.set_window_size(1920, total_height)
                time.sleep(1)
            
            return self.driver.get_screenshot_as_png()
            
        except Exception as e:
            self.logger.error(f"스크린샷 캡처 실패: {e}")
            return None
    
    def _collect_metadata(self) -> Dict[str, Any]:
        """메타데이터 수집"""
        try:
            metadata = {
                'title': self.driver.title,
                'final_url': self.driver.current_url,
                'window_size': self.driver.get_window_size(),
                'cookies': self.driver.get_cookies(),
                'user_agent': self.driver.execute_script("return navigator.userAgent")
            }
            
            # 성능 메트릭 (지원하는 경우)
            try:
                performance = self.driver.execute_script("""
                    const perfData = performance.getEntriesByType('navigation')[0];
                    return perfData ? {
                        loadTime: perfData.loadEventEnd - perfData.loadEventStart,
                        domContentLoaded: perfData.domContentLoadedEventEnd - perfData.domContentLoadedEventStart
                    } : {};
                """)
                metadata['performance'] = performance
            except:
                pass
            
            return metadata
            
        except Exception as e:
            self.logger.error(f"메타데이터 수집 실패: {e}")
            return {}
    
    async def can_handle(self, url: str) -> bool:
        """URL 처리 가능 여부 판단"""
        if not is_valid_url(url):
            return False
        
        url_lower = url.lower()
        
        # Cloudflare 보호 사이트 (최우선)
        cloudflare_indicators = ['cloudflare', 'cf-ray', '.cloudflareinsights.com']
        if any(indicator in url_lower for indicator in cloudflare_indicators):
            return True
        
        # Anti-bot 보호가 예상되는 사이트
        protected_domains = [
            'amazon.com', 'booking.com', 'ticketmaster.com',
            'stubhub.com', 'nike.com', 'supreme.com'
        ]
        if any(domain in url_lower for domain in protected_domains):
            return True
        
        # 일반적으로 모든 웹사이트 처리 가능
        return True
    
    async def solve_captcha(self, config: CrawlConfig) -> CrawlResult:
        """캡차 해결 시도 (기본적인 대기 전략)"""
        if not self.is_initialized:
            await self.initialize()
        
        def _solve_captcha_sync():
            try:
                self.driver.get(config.url)
                
                # 캡차 감지
                captcha_selectors = [
                    'div[class*="captcha"]',
                    'iframe[src*="recaptcha"]',
                    'div[id*="challenge"]'
                ]
                
                wait = WebDriverWait(self.driver, 10)
                captcha_found = False
                
                for selector in captcha_selectors:
                    try:
                        element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, selector)))
                        if element:
                            captcha_found = True
                            break
                    except:
                        continue
                
                if captcha_found:
                    # 수동 해결을 위한 긴 대기 (headless가 아닌 경우)
                    if not self.headless:
                        self.logger.info("캡차 감지됨. 수동 해결을 기다립니다... (60초 대기)")
                        time.sleep(60)
                    else:
                        raise AntiBotDetectionError("캡차 감지됨 - headless 모드에서는 해결 불가")
                
                # 최종 HTML 추출
                html = self.driver.page_source
                
                return CrawlResult(
                    success=True,
                    html=html,
                    crawler_used=CrawlerType.SELENIUM,
                    url=config.url,
                    metadata={'captcha_encountered': captcha_found}
                )
                
            except Exception as e:
                raise CrawlingError(f"캡차 해결 실패: {e}")
        
        try:
            result = await asyncio.get_event_loop().run_in_executor(
                self.executor, _solve_captcha_sync
            )
            return result
            
        except Exception as e:
            return CrawlResult(
                success=False,
                error=str(e),
                crawler_used=CrawlerType.SELENIUM,
                url=config.url
            )
    
    async def interact_and_crawl(self, url: str, interactions: List[Dict]) -> CrawlResult:
        """페이지 상호작용 후 크롤링"""
        if not self.is_initialized:
            await self.initialize()
        
        start_time = time.time()
        
        def _interact_sync():
            try:
                self.driver.get(url)
                self._wait_for_content(CrawlConfig(url=url))
                
                # 상호작용 실행
                for interaction in interactions:
                    self._execute_interaction(interaction)
                    time.sleep(1)
                
                # 최종 결과
                html = self.driver.page_source
                screenshot = None
                
                if interaction.get('screenshot', False):
                    screenshot = self.driver.get_screenshot_as_png()
                
                return CrawlResult(
                    success=True,
                    html=html,
                    screenshot=screenshot,
                    crawler_used=CrawlerType.SELENIUM,
                    url=url,
                    response_time=time.time() - start_time,
                    metadata={'interactions_count': len(interactions)}
                )
                
            except Exception as e:
                raise CrawlingError(f"상호작용 크롤링 실패: {e}")
        
        try:
            result = await asyncio.get_event_loop().run_in_executor(
                self.executor, _interact_sync
            )
            return result
            
        except Exception as e:
            return CrawlResult(
                success=False,
                error=str(e),
                crawler_used=CrawlerType.SELENIUM,
                url=url,
                response_time=time.time() - start_time
            )
    
    def _execute_interaction(self, interaction: Dict):
        """개별 상호작용 실행"""
        action = interaction.get('action')
        selector = interaction.get('selector')
        value = interaction.get('value')
        
        wait = WebDriverWait(self.driver, 10)
        
        if action == 'click':
            element = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, selector)))
            element.click()
            
        elif action == 'type':
            element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, selector)))
            element.clear()
            element.send_keys(value)
            
        elif action == 'scroll':
            if value:
                self.driver.execute_script(f"window.scrollTo(0, {value});")
            else:
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                
        elif action == 'wait':
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, selector)))
            
        elif action == 'hover':
            element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, selector)))
            ActionChains(self.driver).move_to_element(element).perform()
    
    def get_supported_features(self) -> List[str]:
        """지원하는 기능 목록"""
        return [
            "antibot_bypass",
            "cloudflare_bypass",
            "captcha_handling",
            "page_interaction",
            "screenshot_capture",
            "stealth_mode",
            "legacy_support"
        ]


# 유틸리티 함수

async def bypass_protection(url: str, wait_time: int = 10) -> CrawlResult:
    """보호된 사이트 우회 크롤링"""
    crawler = SeleniumCrawler(use_undetected=True)
    try:
        await crawler.initialize()
        config = CrawlConfig(url=url, timeout=wait_time, wait_for_load=True)
        result = await crawler.crawl(config)
        
        # Bot 감지시 캡차 해결 시도
        if not result.success and result.error_type == "antibot_detection":
            result = await crawler.solve_captcha(config)
        
        return result
        
    finally:
        await crawler.cleanup()


async def stealth_screenshot(url: str, save_path: str = None) -> bool:
    """스텔스 모드 스크린샷"""
    crawler = SeleniumCrawler(use_undetected=True, headless=False)
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