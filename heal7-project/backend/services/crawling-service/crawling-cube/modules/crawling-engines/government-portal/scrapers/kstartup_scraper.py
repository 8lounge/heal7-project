"""
K-Startup (k-startup.go.kr) 전용 SPA 스크래퍼
정부 창업 지원 플랫폼 실시간 모니터링

Author: Paperwork AI Team
Version: 2.0.0
Date: 2025-08-23
"""

import asyncio
import hashlib
import json
import logging
import re
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from urllib.parse import urljoin, urlparse, parse_qs

import aiohttp
from bs4 import BeautifulSoup
from dataclasses import dataclass
from playwright.async_api import async_playwright, Browser, Page

from utils.rate_limiter import RateLimiter
from utils.content_cleaner import ContentCleaner
from database.db_manager import DatabaseManager

logger = logging.getLogger(__name__)

@dataclass
class KStartupConfig:
    """K-Startup 스크래핑 설정"""
    base_url: str = "https://www.k-startup.go.kr"
    max_pages: int = 30
    max_concurrent: int = 3  # SPA이므로 낮게 설정
    request_delay: float = 2.0  # SPA이므로 높게 설정
    timeout: int = 45
    retries: int = 3
    headless: bool = True
    viewport_width: int = 1920
    viewport_height: int = 1080

class KStartupScraper:
    """K-Startup 전용 SPA 대응 스크래퍼"""
    
    def __init__(self, db_manager: DatabaseManager, rate_limiter: RateLimiter):
        self.config = KStartupConfig()
        self.db_manager = db_manager
        self.rate_limiter = rate_limiter
        self.content_cleaner = ContentCleaner()
        
        # Playwright 브라우저 설정
        self.playwright = None
        self.browser = None
        self.pages_pool = []
        
        # 스크래핑 대상 URL
        self.target_urls = {
            'business_announcements': '/homepage/powerup/business/list.do',
            'startup_programs': '/homepage/bizplan/program/list.do',
            'education_courses': '/homepage/academy/education/list.do',
            'contest_events': '/homepage/contest/list.do',
            'support_programs': '/homepage/support/program/list.do'
        }
        
        # API 엔드포인트 (가능한 경우)
        self.api_endpoints = {
            'business_list': '/api/business/announcements',
            'program_list': '/api/programs/list',
            'education_list': '/api/education/courses'
        }
        
        # 수집 통계
        self.stats = {
            'total_requests': 0,
            'successful_requests': 0,
            'failed_requests': 0,
            'programs_found': 0,
            'api_calls': 0,
            'browser_actions': 0,
            'start_time': None
        }
        
        logger.info("🚀 K-Startup SPA 스크래퍼 초기화 완료")
    
    async def initialize(self):
        """스크래퍼 초기화 (Playwright 브라우저 시작)"""
        if not self.playwright:
            self.playwright = await async_playwright().start()
            
            # 브라우저 시작
            self.browser = await self.playwright.chromium.launch(
                headless=self.config.headless,
                args=[
                    '--no-sandbox',
                    '--disable-setuid-sandbox',
                    '--disable-dev-shm-usage',
                    '--disable-extensions',
                    '--disable-gpu',
                    '--disable-web-security',
                    '--disable-features=VizDisplayCompositor'
                ]
            )
            
            # 페이지 풀 생성
            await self.create_page_pool()
            
            logger.info("✅ K-Startup 브라우저 초기화 완료")
    
    async def create_page_pool(self):
        """브라우저 페이지 풀 생성"""
        for i in range(self.config.max_concurrent):
            context = await self.browser.new_context(
                viewport={'width': self.config.viewport_width, 'height': self.config.viewport_height},
                user_agent='Mozilla/5.0 (compatible; PaperworkAI-KStartup/2.0; +http://paperwork.heal7.com/bot)'
            )
            
            page = await context.new_page()
            
            # 기본 설정
            await page.set_extra_http_headers({
                'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7'
            })
            
            self.pages_pool.append(page)
            
        logger.info(f"📄 브라우저 페이지 풀 생성 완료: {len(self.pages_pool)}개")
    
    async def close(self):
        """스크래퍼 정리"""
        if self.pages_pool:
            for page in self.pages_pool:
                await page.context.close()
            self.pages_pool.clear()
        
        if self.browser:
            await self.browser.close()
            self.browser = None
            
        if self.playwright:
            await self.playwright.stop()
            self.playwright = None
            
        logger.info("🔒 K-Startup 스크래퍼 정리 완료")
    
    async def get_status(self) -> Dict:
        """스크래퍼 상태 조회"""
        return {
            "scraper": "kstartup",
            "status": "active" if self.browser else "inactive",
            "browser_pages": len(self.pages_pool),
            "stats": self.stats.copy(),
            "last_run": await self.db_manager.get_last_scraping_time('kstartup')
        }
    
    async def scrape_all_programs(self, force_update: bool = False) -> List[Dict]:
        """모든 K-Startup 프로그램 스크래핑"""
        self.stats['start_time'] = datetime.now()
        
        if not self.browser:
            await self.initialize()
        
        logger.info("🚀 K-Startup 전체 스크래핑 시작")
        
        all_programs = []
        
        # API 먼저 시도
        api_programs = await self.try_api_scraping()
        if api_programs:
            all_programs.extend(api_programs)
            logger.info(f"📡 API 스크래핑: {len(api_programs)}개 프로그램")
        
        # 브라우저 스크래핑
        for category_name, url_path in self.target_urls.items():
            logger.info(f"📂 카테고리 스크래핑 시작: {category_name}")
            
            try:
                programs = await self.scrape_category_spa(url_path, category_name, force_update)
                all_programs.extend(programs)
                self.stats['programs_found'] += len(programs)
                
                logger.info(f"✅ {category_name} 완료: {len(programs)}개 프로그램")
                
                # 카테고리간 딜레이
                await asyncio.sleep(self.config.request_delay)
                
            except Exception as e:
                logger.error(f"❌ {category_name} 스크래핑 실패: {str(e)}")
                continue
        
        # 중복 제거
        unique_programs = self.remove_duplicates(all_programs)
        
        total_time = (datetime.now() - self.stats['start_time']).total_seconds()
        logger.info(f"🎉 K-Startup 스크래핑 완료: {len(unique_programs)}개 프로그램 ({total_time:.1f}초)")
        
        return unique_programs
    
    async def try_api_scraping(self) -> List[Dict]:
        """API 엔드포인트 스크래핑 시도"""
        api_programs = []
        
        async with aiohttp.ClientSession() as session:
            for endpoint_name, endpoint_path in self.api_endpoints.items():
                try:
                    await self.rate_limiter.acquire()
                    
                    url = f"{self.config.base_url}{endpoint_path}"
                    
                    async with session.get(url, timeout=aiohttp.ClientTimeout(total=15)) as response:
                        if response.status == 200:
                            data = await response.json()
                            
                            if isinstance(data, dict) and 'data' in data:
                                programs = data['data']
                            elif isinstance(data, list):
                                programs = data
                            else:
                                continue
                            
                            # API 데이터 표준화
                            standardized_programs = [
                                self.standardize_api_data(program, endpoint_name) 
                                for program in programs
                            ]
                            
                            api_programs.extend(standardized_programs)
                            self.stats['api_calls'] += 1
                            
                            logger.info(f"📡 API 성공 {endpoint_name}: {len(programs)}개")
                            
                        else:
                            logger.debug(f"⚠️ API 실패 {endpoint_name}: HTTP {response.status}")
                            
                except Exception as e:
                    logger.debug(f"⚠️ API 오류 {endpoint_name}: {str(e)}")
                    continue
        
        return api_programs
    
    def standardize_api_data(self, api_data: Dict, endpoint_name: str) -> Dict:
        """API 데이터를 표준 형식으로 변환"""
        standardized = {
            'title': api_data.get('title', api_data.get('name', 'N/A')),
            'agency': 'K-Startup',
            'category': endpoint_name,
            'status': api_data.get('status', api_data.get('state', 'N/A')),
            'application_period': api_data.get('period', api_data.get('deadline', 'N/A')),
            'detail_url': self.construct_detail_url(api_data, endpoint_name),
            'program_id': self.generate_program_id_from_api(api_data, endpoint_name),
            'portal_id': 'kstartup',
            'scraped_at': datetime.now().isoformat(),
            'source': 'api'
        }
        
        # 추가 필드
        if 'description' in api_data:
            standardized['description'] = api_data['description']
        if 'budget' in api_data:
            standardized['budget'] = api_data['budget']
        
        return standardized
    
    async def scrape_category_spa(self, url_path: str, category_name: str, force_update: bool) -> List[Dict]:
        """SPA 카테고리 스크래핑"""
        programs = []
        page = await self.get_page_from_pool()
        
        if not page:
            logger.error("❌ 사용 가능한 페이지 없음")
            return []
        
        try:
            full_url = f"{self.config.base_url}{url_path}"
            
            # 페이지 로드
            await self.rate_limiter.acquire()
            await page.goto(full_url, wait_until='networkidle', timeout=30000)
            
            self.stats['browser_actions'] += 1
            
            # 페이지 로딩 대기
            await self.wait_for_content_load(page)
            
            # 무한스크롤 또는 페이지네이션 처리
            await self.handle_pagination_or_scroll(page, category_name)
            
            # 프로그램 목록 추출
            program_elements = await page.query_selector_all(self.get_program_selectors(category_name))
            
            logger.info(f"📋 {category_name} 요소 발견: {len(program_elements)}개")
            
            # 각 프로그램 정보 추출
            for i, element in enumerate(program_elements):
                try:
                    program_data = await self.extract_program_from_element(element, page, category_name)
                    if program_data:
                        programs.append(program_data)
                        
                        # 진행률 로깅
                        if (i + 1) % 10 == 0:
                            logger.info(f"📊 {category_name} 진행률: {i + 1}/{len(program_elements)}")
                            
                except Exception as e:
                    logger.error(f"❌ 프로그램 추출 오류 {i}: {str(e)}")
                    continue
            
        except Exception as e:
            logger.error(f"❌ {category_name} SPA 스크래핑 실패: {str(e)}")
        
        finally:
            await self.return_page_to_pool(page)
        
        return programs
    
    async def get_page_from_pool(self) -> Optional[Page]:
        """페이지 풀에서 페이지 가져오기"""
        if self.pages_pool:
            return self.pages_pool.pop()
        return None
    
    async def return_page_to_pool(self, page: Page):
        """페이지를 풀에 반환"""
        try:
            # 페이지 정리
            await page.evaluate('() => { document.body.innerHTML = ""; }')
            self.pages_pool.append(page)
        except Exception as e:
            logger.error(f"❌ 페이지 반환 오류: {str(e)}")
    
    async def wait_for_content_load(self, page: Page):
        """콘텐츠 로딩 대기"""
        try:
            # 일반적인 로딩 인디케이터 대기
            await page.wait_for_selector('body', timeout=10000)
            
            # 추가 로딩 대기 (Ajax 등)
            await page.wait_for_timeout(3000)
            
            # 로딩 스피너가 사라질 때까지 대기
            try:
                await page.wait_for_selector('.loading, .spinner, .ajax-loading', state='detached', timeout=5000)
            except:
                pass  # 로딩 스피너가 없을 수도 있음
                
        except Exception as e:
            logger.warning(f"⚠️ 콘텐츠 로딩 대기 오류: {str(e)}")
    
    async def handle_pagination_or_scroll(self, page: Page, category_name: str):
        """페이지네이션 또는 무한스크롤 처리"""
        try:
            # 무한스크롤 확인
            has_infinite_scroll = await page.evaluate('''
                () => {
                    const scrollElements = document.querySelectorAll('[data-infinite], .infinite-scroll, .load-more');
                    return scrollElements.length > 0;
                }
            ''')
            
            if has_infinite_scroll:
                await self.handle_infinite_scroll(page)
            else:
                await self.handle_pagination(page)
                
        except Exception as e:
            logger.error(f"❌ 페이지네이션 처리 오류: {str(e)}")
    
    async def handle_infinite_scroll(self, page: Page):
        """무한스크롤 처리"""
        logger.info("📜 무한스크롤 감지, 스크롤 시작")
        
        previous_height = 0
        scroll_attempts = 0
        max_scrolls = 10
        
        while scroll_attempts < max_scrolls:
            # 페이지 끝까지 스크롤
            await page.evaluate('window.scrollTo(0, document.body.scrollHeight)')
            
            # 새 콘텐츠 로딩 대기
            await page.wait_for_timeout(2000)
            
            # 페이지 높이 확인
            current_height = await page.evaluate('document.body.scrollHeight')
            
            if current_height == previous_height:
                # 더 이상 새로운 콘텐츠가 없음
                break
            
            previous_height = current_height
            scroll_attempts += 1
            
            logger.info(f"📜 스크롤 {scroll_attempts}/{max_scrolls}: 높이 {current_height}")
        
        logger.info(f"✅ 무한스크롤 완료: {scroll_attempts}회 스크롤")
    
    async def handle_pagination(self, page: Page):
        """페이지네이션 처리"""
        logger.info("📄 페이지네이션 감지, 페이지 순회 시작")
        
        current_page = 1
        max_pages = min(self.config.max_pages, 10)  # SPA는 페이지 제한
        
        while current_page <= max_pages:
            try:
                # 다음 페이지 버튼 찾기
                next_selectors = [
                    '.pagination .next:not(.disabled)',
                    '.paging .next:not(.disabled)', 
                    '.page-nav .next:not(.disabled)',
                    'a[onclick*="page"]:has-text("다음")',
                    'button:has-text("다음"):not(:disabled)'
                ]
                
                next_button = None
                for selector in next_selectors:
                    try:
                        next_button = await page.query_selector(selector)
                        if next_button:
                            break
                    except:
                        continue
                
                if not next_button:
                    logger.info("📄 더 이상 페이지 없음")
                    break
                
                # 다음 페이지 클릭
                await next_button.click()
                await self.wait_for_content_load(page)
                
                current_page += 1
                logger.info(f"📄 페이지 {current_page}/{max_pages} 로드 완료")
                
            except Exception as e:
                logger.error(f"❌ 페이지네이션 오류: {str(e)}")
                break
        
        logger.info(f"✅ 페이지네이션 완료: {current_page}페이지 처리")
    
    def get_program_selectors(self, category_name: str) -> str:
        """카테고리별 프로그램 셀렉터 반환"""
        selector_map = {
            'business_announcements': '.business-card, .announce-item, .program-item',
            'startup_programs': '.program-card, .startup-item, .biz-item', 
            'education_courses': '.course-card, .edu-item, .education-item',
            'contest_events': '.contest-card, .event-item, .competition-item',
            'support_programs': '.support-card, .program-card, .support-item'
        }
        
        return selector_map.get(category_name, '.card, .item, .program, .list-item, tr[onclick]')
    
    async def extract_program_from_element(self, element, page: Page, category_name: str) -> Optional[Dict]:
        """요소에서 프로그램 정보 추출"""
        try:
            # 기본 정보 추출
            title = await self.extract_text_from_element(element, ['.title', 'h3', 'h4', '.subject', 'strong'])
            status = await self.extract_text_from_element(element, ['.status', '.state', '.badge', '.label'])
            period = await self.extract_text_from_element(element, ['.period', '.date', '.deadline', '.term'])
            description = await self.extract_text_from_element(element, ['.description', '.content', '.summary'])
            
            # 링크 추출
            detail_url = await self.extract_link_from_element(element, page)
            
            # 추가 정보
            budget = await self.extract_text_from_element(element, ['.budget', '.amount', '.money'])
            target = await self.extract_text_from_element(element, ['.target', '.audience', '.who'])
            
            if not title or title == 'N/A':
                return None
            
            program_data = {
                'title': self.content_cleaner.clean_title(title),
                'agency': 'K-Startup',
                'category': category_name,
                'status': self.content_cleaner.clean_text(status) if status != 'N/A' else 'N/A',
                'application_period': self.content_cleaner.clean_text(period) if period != 'N/A' else 'N/A',
                'description': self.content_cleaner.clean_text(description) if description != 'N/A' else '',
                'detail_url': detail_url,
                'program_id': self.generate_program_id_from_spa({'title': title, 'category': category_name}),
                'portal_id': 'kstartup',
                'scraped_at': datetime.now().isoformat(),
                'source': 'spa'
            }
            
            # 선택적 필드
            if budget != 'N/A':
                program_data['budget'] = self.content_cleaner.clean_text(budget)
            if target != 'N/A':
                program_data['target_audience'] = self.content_cleaner.clean_text(target)
            
            # 해시값 생성
            program_data['hash_value'] = self.generate_content_hash(program_data)
            
            return program_data
            
        except Exception as e:
            logger.error(f"❌ 요소에서 프로그램 추출 실패: {str(e)}")
            return None
    
    async def extract_text_from_element(self, element, selectors: List[str]) -> str:
        """요소에서 텍스트 추출 (여러 셀렉터 시도)"""
        try:
            for selector in selectors:
                try:
                    sub_element = await element.query_selector(selector)
                    if sub_element:
                        text = await sub_element.inner_text()
                        if text and text.strip():
                            return text.strip()
                except:
                    continue
            
            # 직접 텍스트 추출 시도
            text = await element.inner_text()
            return text.strip() if text else 'N/A'
            
        except:
            return 'N/A'
    
    async def extract_link_from_element(self, element, page: Page) -> Optional[str]:
        """요소에서 링크 추출"""
        try:
            # 직접 링크
            link_element = await element.query_selector('a[href]')
            if link_element:
                href = await link_element.get_attribute('href')
                if href:
                    return urljoin(self.config.base_url, href)
            
            # onclick 이벤트에서 링크 추출
            onclick = await element.get_attribute('onclick')
            if onclick:
                # JavaScript 함수에서 ID 추출
                match = re.search(r'(?:viewDetail|showDetail|goDetail)\s*\(\s*[\'"]([^\'"]+)[\'"]', onclick)
                if match:
                    detail_id = match.group(1)
                    return f"{self.config.base_url}/homepage/detail.do?id={detail_id}"
            
            return None
            
        except:
            return None
    
    def construct_detail_url(self, api_data: Dict, endpoint_name: str) -> Optional[str]:
        """API 데이터에서 상세 URL 구성"""
        detail_id = api_data.get('id', api_data.get('programId', api_data.get('announcementId')))
        
        if not detail_id:
            return None
        
        url_patterns = {
            'business_list': f"/homepage/powerup/business/detail.do?id={detail_id}",
            'program_list': f"/homepage/bizplan/program/detail.do?id={detail_id}",
            'education_list': f"/homepage/academy/education/detail.do?id={detail_id}"
        }
        
        path = url_patterns.get(endpoint_name, f"/homepage/detail.do?id={detail_id}")
        return f"{self.config.base_url}{path}"
    
    def generate_program_id_from_api(self, api_data: Dict, endpoint_name: str) -> str:
        """API 데이터에서 프로그램 ID 생성"""
        content = f"kstartup_{endpoint_name}_{api_data.get('id', '')}{api_data.get('title', '')}"
        return hashlib.md5(content.encode()).hexdigest()[:12]
    
    def generate_program_id_from_spa(self, spa_data: Dict) -> str:
        """SPA 데이터에서 프로그램 ID 생성"""
        content = f"kstartup_{spa_data.get('category', '')}_{spa_data.get('title', '')}"
        return hashlib.md5(content.encode()).hexdigest()[:12]
    
    def generate_content_hash(self, program_data: Dict) -> str:
        """콘텐츠 변경 감지용 해시"""
        key_fields = ['title', 'status', 'application_period', 'description']
        content = ''.join(str(program_data.get(field, '')) for field in key_fields)
        return hashlib.sha256(content.encode()).hexdigest()
    
    def remove_duplicates(self, programs: List[Dict]) -> List[Dict]:
        """중복 프로그램 제거"""
        seen_ids = set()
        unique_programs = []
        
        for program in programs:
            program_id = program.get('program_id')
            if program_id and program_id not in seen_ids:
                seen_ids.add(program_id)
                unique_programs.append(program)
        
        logger.info(f"🔄 중복 제거: {len(programs)} → {len(unique_programs)}")
        return unique_programs