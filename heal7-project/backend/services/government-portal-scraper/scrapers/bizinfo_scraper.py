"""
기업마당 (bizinfo.go.kr) 전용 스크래퍼
정부 지원사업 통합 포털 실시간 모니터링

Author: Paperwork AI Team
Version: 2.0.0
Date: 2025-08-23
"""

import asyncio
import hashlib
import logging
import re
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from urllib.parse import urljoin, urlparse, parse_qs

import aiohttp
from bs4 import BeautifulSoup, NavigableString
from dataclasses import dataclass

from utils.rate_limiter import RateLimiter
from utils.content_cleaner import ContentCleaner
from database.db_manager import DatabaseManager

logger = logging.getLogger(__name__)

@dataclass
class ScrapingConfig:
    """스크래핑 설정"""
    base_url: str = "https://www.bizinfo.go.kr"
    max_pages: int = 50
    max_concurrent: int = 5
    request_delay: float = 1.0
    timeout: int = 30
    retries: int = 3

class BizinfoScraper:
    """기업마당 전용 지능형 스크래퍼"""
    
    def __init__(self, db_manager: DatabaseManager, rate_limiter: RateLimiter):
        self.config = ScrapingConfig()
        self.db_manager = db_manager
        self.rate_limiter = rate_limiter
        self.content_cleaner = ContentCleaner()
        
        # 세션 설정
        self.session = None
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (compatible; PaperworkAI/2.0; +http://paperwork.heal7.com/bot)',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'ko-KR,ko;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        }
        
        # 카테고리 매핑
        self.categories = {
            'all': '',
            'startup': 'STARTUP',       # 창업
            'funding': 'FUNDING',       # 자금
            'tech': 'TECH',            # 기술개발
            'export': 'EXPORT',        # 해외진출
            'market': 'MARKET',        # 판로
            'education': 'EDUCATION'    # 교육/컨설팅
        }
        
        # 수집 통계
        self.stats = {
            'total_requests': 0,
            'successful_requests': 0,
            'failed_requests': 0,
            'programs_found': 0,
            'start_time': None
        }
    
    async def initialize(self):
        """스크래퍼 초기화"""
        if not self.session:
            connector = aiohttp.TCPConnector(
                limit=self.config.max_concurrent,
                ttl_dns_cache=300,
                use_dns_cache=True,
                limit_per_host=3
            )
            
            timeout = aiohttp.ClientTimeout(total=self.config.timeout)
            
            self.session = aiohttp.ClientSession(
                headers=self.headers,
                connector=connector,
                timeout=timeout,
                cookie_jar=aiohttp.CookieJar()
            )
            
            logger.info("✅ 기업마당 스크래퍼 초기화 완료")
    
    async def close(self):
        """스크래퍼 정리"""
        if self.session:
            await self.session.close()
            self.session = None
            logger.info("🔒 기업마당 스크래퍼 세션 정리 완료")
    
    async def get_status(self) -> Dict:
        """스크래퍼 상태 조회"""
        return {
            "scraper": "bizinfo",
            "status": "active" if self.session else "inactive",
            "stats": self.stats.copy(),
            "last_run": await self.db_manager.get_last_scraping_time('bizinfo')
        }
    
    async def scrape_all_programs(self, force_update: bool = False) -> List[Dict]:
        """모든 지원사업 프로그램 스크래핑"""
        self.stats['start_time'] = datetime.now()
        
        if not self.session:
            await self.initialize()
        
        logger.info("🚀 기업마당 전체 스크래핑 시작")
        
        all_programs = []
        
        # 카테고리별 스크래핑
        for category_name, category_code in self.categories.items():
            if category_name == 'all':
                continue
                
            logger.info(f"📂 카테고리 스크래핑 시작: {category_name}")
            
            try:
                programs = await self.scrape_category(category_code, force_update)
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
        logger.info(f"🎉 기업마당 스크래핑 완료: {len(unique_programs)}개 프로그램 ({total_time:.1f}초)")
        
        return unique_programs
    
    async def scrape_category(self, category_code: str, force_update: bool = False) -> List[Dict]:
        """특정 카테고리 스크래핑"""
        programs = []
        page = 1
        
        while page <= self.config.max_pages:
            try:
                # Rate limiting 적용
                await self.rate_limiter.acquire()
                
                # 페이지 스크래핑
                page_programs = await self.scrape_page(category_code, page, force_update)
                
                if not page_programs:
                    logger.info(f"📄 {category_code} 페이지 {page}: 더 이상 프로그램이 없음")
                    break
                
                programs.extend(page_programs)
                logger.info(f"📄 {category_code} 페이지 {page}: {len(page_programs)}개 프로그램")
                
                page += 1
                
            except Exception as e:
                logger.error(f"❌ {category_code} 페이지 {page} 실패: {str(e)}")
                break
        
        return programs
    
    async def scrape_page(self, category_code: str, page: int, force_update: bool) -> List[Dict]:
        """개별 페이지 스크래핑"""
        url = f"{self.config.base_url}/web/lay1/biz/PBIZ_0000000000000.do"
        
        params = {
            'searchCondition': 'TITLE',
            'searchKeyword': '',
            'bizTycd': category_code,
            'pageIndex': page,
            'recordCountPerPage': '20'  # 페이지당 20개
        }
        
        try:
            self.stats['total_requests'] += 1
            
            async with self.session.get(url, params=params) as response:
                if response.status != 200:
                    logger.warning(f"⚠️ HTTP {response.status}: {url}")
                    self.stats['failed_requests'] += 1
                    return []
                
                html = await response.text()
                self.stats['successful_requests'] += 1
                
                # HTML 파싱
                soup = BeautifulSoup(html, 'html.parser')
                
                # 프로그램 목록 추출
                programs = await self.extract_programs_from_page(soup, force_update)
                
                return programs
                
        except asyncio.TimeoutError:
            logger.error(f"⏰ 타임아웃: {url}")
            self.stats['failed_requests'] += 1
            return []
        except Exception as e:
            logger.error(f"❌ 페이지 스크래핑 오류 {url}: {str(e)}")
            self.stats['failed_requests'] += 1
            return []
    
    async def extract_programs_from_page(self, soup: BeautifulSoup, force_update: bool) -> List[Dict]:
        """페이지에서 프로그램 목록 추출"""
        programs = []
        
        # 다양한 셀렉터 시도 (사이트 구조 변경 대응)
        selectors = [
            '.business-item',
            '.biz-item', 
            '.support-item',
            '.list-item',
            'tr[onclick]',  # 테이블 형태
            '.row.border'   # Bootstrap 스타일
        ]
        
        program_elements = []
        for selector in selectors:
            elements = soup.select(selector)
            if elements:
                program_elements = elements
                logger.debug(f"🎯 셀렉터 사용: {selector} ({len(elements)}개)")
                break
        
        if not program_elements:
            logger.warning("⚠️ 프로그램 요소를 찾을 수 없음")
            return []
        
        # 각 프로그램 정보 추출
        tasks = []
        semaphore = asyncio.Semaphore(self.config.max_concurrent)
        
        for element in program_elements:
            task = self.extract_single_program(semaphore, element, force_update)
            tasks.append(task)
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        for result in results:
            if isinstance(result, Exception):
                logger.error(f"❌ 프로그램 추출 오류: {str(result)}")
                continue
            if result:
                programs.append(result)
        
        return programs
    
    async def extract_single_program(self, semaphore: asyncio.Semaphore, element, force_update: bool) -> Optional[Dict]:
        """개별 프로그램 정보 추출"""
        async with semaphore:
            try:
                # 기본 정보 추출
                basic_info = self.extract_basic_info(element)
                
                if not basic_info or not basic_info.get('detail_url'):
                    return None
                
                # 상세 정보가 필요한 경우에만 추가 요청
                if force_update or await self.needs_detail_update(basic_info):
                    detail_info = await self.scrape_program_detail(basic_info['detail_url'])
                    basic_info.update(detail_info)
                
                # 프로그램 ID 생성
                basic_info['program_id'] = self.generate_program_id(basic_info)
                basic_info['hash_value'] = self.generate_content_hash(basic_info)
                basic_info['portal_id'] = 'bizinfo'
                basic_info['scraped_at'] = datetime.now().isoformat()
                
                return basic_info
                
            except Exception as e:
                logger.error(f"❌ 개별 프로그램 추출 실패: {str(e)}")
                return None
    
    def extract_basic_info(self, element) -> Dict:
        """기본 정보 추출"""
        info = {}
        
        try:
            # 제목 추출 (여러 패턴 시도)
            title_selectors = ['.title', 'h3', 'h4', '.subject', '.biz-title', 'strong']
            title = None
            
            for selector in title_selectors:
                title_elem = element.select_one(selector)
                if title_elem:
                    title = self.content_cleaner.clean_text(title_elem.get_text())
                    break
            
            if not title:
                # onclick 이벤트에서 제목 추출 시도
                onclick = element.get('onclick', '')
                if 'bizId' in onclick:
                    title = self.content_cleaner.clean_text(element.get_text())
            
            info['title'] = title or 'N/A'
            
            # 주관기관 추출
            agency_selectors = ['.agency', '.org', '.institution', '.dept']
            agency = 'N/A'
            
            for selector in agency_selectors:
                agency_elem = element.select_one(selector)
                if agency_elem:
                    agency = self.content_cleaner.clean_text(agency_elem.get_text())
                    break
            
            info['agency'] = agency
            
            # 신청기간 추출
            period_selectors = ['.period', '.date', '.term', '.deadline']
            period = 'N/A'
            
            for selector in period_selectors:
                period_elem = element.select_one(selector)
                if period_elem:
                    period = self.content_cleaner.clean_text(period_elem.get_text())
                    break
            
            info['application_period'] = period
            
            # 상태 정보 추출
            status_selectors = ['.status', '.state', '.badge']
            status = 'N/A'
            
            for selector in status_selectors:
                status_elem = element.select_one(selector)
                if status_elem:
                    status = self.content_cleaner.clean_text(status_elem.get_text())
                    break
            
            info['status'] = status
            
            # 상세 링크 추출
            link_elem = element.select_one('a[href]')
            if not link_elem:
                # onclick 이벤트에서 링크 정보 추출
                onclick = element.get('onclick', '')
                biz_id_match = re.search(r'bizId[\'\"]\s*:\s*[\'\"](.*?)[\'\"', onclick)
                if biz_id_match:
                    biz_id = biz_id_match.group(1)
                    info['detail_url'] = f"{self.config.base_url}/web/lay1/biz/PBIZ_0000000000001.do?bizId={biz_id}"
                else:
                    info['detail_url'] = None
            else:
                href = link_elem.get('href')
                if href:
                    info['detail_url'] = urljoin(self.config.base_url, href)
                else:
                    info['detail_url'] = None
            
            return info
            
        except Exception as e:
            logger.error(f"❌ 기본 정보 추출 실패: {str(e)}")
            return {}
    
    async def scrape_program_detail(self, detail_url: str) -> Dict:
        """프로그램 상세 정보 스크래핑"""
        if not detail_url:
            return {}
        
        try:
            await self.rate_limiter.acquire()
            
            async with self.session.get(detail_url) as response:
                if response.status != 200:
                    logger.warning(f"⚠️ 상세 페이지 접근 실패 {response.status}: {detail_url}")
                    return {}
                
                html = await response.text()
                soup = BeautifulSoup(html, 'html.parser')
                
                # 상세 정보 추출
                detail_info = {
                    'support_details': self.extract_support_details(soup),
                    'target_audience': self.extract_target_audience(soup),
                    'required_documents': self.extract_required_documents(soup),
                    'evaluation_criteria': self.extract_evaluation_criteria(soup),
                    'contact_info': self.extract_contact_info(soup),
                    'attachments': self.extract_attachments(soup),
                    'detailed_description': self.extract_detailed_description(soup)
                }
                
                return detail_info
                
        except Exception as e:
            logger.error(f"❌ 상세 정보 스크래핑 실패 {detail_url}: {str(e)}")
            return {}
    
    def extract_support_details(self, soup: BeautifulSoup) -> Dict:
        """지원 내용 추출"""
        support_info = {}
        
        try:
            # 지원 내용 섹션 찾기
            support_section = soup.select_one('.support-content, .biz-content, .detail-content')
            
            if support_section:
                content_text = self.content_cleaner.clean_text(support_section.get_text())
                
                # 패턴 매칭으로 구조화된 정보 추출
                support_info['raw_content'] = content_text
                support_info['support_amount'] = self.extract_support_amount(content_text)
                support_info['support_period'] = self.extract_support_period(content_text)
                support_info['support_type'] = self.extract_support_type(content_text)
            
        except Exception as e:
            logger.error(f"❌ 지원 내용 추출 실패: {str(e)}")
        
        return support_info
    
    def extract_support_amount(self, text: str) -> str:
        """지원 금액 추출"""
        patterns = [
            r'(\d{1,3}(?:,\d{3})*(?:\.\d+)?)\s*(?:억|만원|원|백만원)',
            r'최대\s*(\d{1,3}(?:,\d{3})*(?:\.\d+)?)\s*(?:억|만원|원)',
            r'(\d{1,3}(?:,\d{3})*(?:\.\d+)?)\s*(?:천만원|백만원)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                return match.group(0)
        
        return 'N/A'
    
    def extract_support_period(self, text: str) -> str:
        """지원 기간 추출"""
        patterns = [
            r'(\d+)\s*개월',
            r'(\d+)\s*년',
            r'(\d{4})\s*년\s*(\d{1,2})\s*월',
            r'(\d{1,2})\s*월\s*~\s*(\d{1,2})\s*월'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                return match.group(0)
        
        return 'N/A'
    
    def extract_support_type(self, text: str) -> str:
        """지원 방식 추출"""
        types = ['융자', '보조금', '지원금', '바우처', '세액공제', '컨설팅', '멘토링', '교육']
        
        found_types = []
        for support_type in types:
            if support_type in text:
                found_types.append(support_type)
        
        return ', '.join(found_types) if found_types else 'N/A'
    
    def extract_target_audience(self, soup: BeautifulSoup) -> str:
        """지원 대상 추출"""
        try:
            target_section = soup.select_one('.target, .audience, .subject-area')
            if target_section:
                return self.content_cleaner.clean_text(target_section.get_text())
        except:
            pass
        
        return 'N/A'
    
    def extract_required_documents(self, soup: BeautifulSoup) -> List[str]:
        """필수 서류 추출"""
        documents = []
        
        try:
            # 서류 목록 섹션 찾기
            docs_section = soup.select_one('.documents, .attachments, .requirements')
            if docs_section:
                # 리스트 항목 추출
                items = docs_section.select('li, .item, .doc-item')
                for item in items:
                    doc_text = self.content_cleaner.clean_text(item.get_text())
                    if doc_text and len(doc_text) > 3:  # 의미있는 텍스트만
                        documents.append(doc_text)
        except:
            pass
        
        return documents
    
    def extract_evaluation_criteria(self, soup: BeautifulSoup) -> List[str]:
        """평가 기준 추출"""
        criteria = []
        
        try:
            eval_section = soup.select_one('.evaluation, .criteria, .assessment')
            if eval_section:
                items = eval_section.select('li, .item, .criteria-item')
                for item in items:
                    criteria_text = self.content_cleaner.clean_text(item.get_text())
                    if criteria_text and len(criteria_text) > 5:
                        criteria.append(criteria_text)
        except:
            pass
        
        return criteria
    
    def extract_contact_info(self, soup: BeautifulSoup) -> Dict:
        """연락처 정보 추출"""
        contact = {}
        
        try:
            contact_section = soup.select_one('.contact, .info, .inquiry')
            if contact_section:
                text = contact_section.get_text()
                
                # 전화번호 추출
                phone_match = re.search(r'(\d{2,3}-\d{3,4}-\d{4})', text)
                if phone_match:
                    contact['phone'] = phone_match.group(1)
                
                # 이메일 추출
                email_match = re.search(r'([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})', text)
                if email_match:
                    contact['email'] = email_match.group(1)
        except:
            pass
        
        return contact
    
    def extract_attachments(self, soup: BeautifulSoup) -> List[Dict]:
        """첨부 파일 정보 추출"""
        attachments = []
        
        try:
            # 첨부파일 링크 찾기
            file_links = soup.select('a[href*="download"], a[href*=".pdf"], a[href*=".doc"], a[href*=".hwp"]')
            
            for link in file_links:
                href = link.get('href')
                if href:
                    attachments.append({
                        'filename': self.content_cleaner.clean_text(link.get_text()),
                        'url': urljoin(self.config.base_url, href)
                    })
        except:
            pass
        
        return attachments
    
    def extract_detailed_description(self, soup: BeautifulSoup) -> str:
        """상세 설명 전체 텍스트 추출"""
        try:
            # 주요 콘텐츠 영역 추출
            content_section = soup.select_one('.content, .detail, .description, .main-content')
            if content_section:
                return self.content_cleaner.clean_text(content_section.get_text())
        except:
            pass
        
        return 'N/A'
    
    async def needs_detail_update(self, basic_info: Dict) -> bool:
        """상세 정보 업데이트 필요 여부 확인"""
        try:
            existing_program = await self.db_manager.get_program_by_id(basic_info.get('program_id'))
            if not existing_program:
                return True  # 새로운 프로그램
            
            # 해시값 비교로 변경 확인
            new_hash = self.generate_content_hash(basic_info)
            return existing_program.get('hash_value') != new_hash
            
        except:
            return True  # 오류시 업데이트
    
    def generate_program_id(self, program_info: Dict) -> str:
        """프로그램 고유 ID 생성"""
        # 제목 + 기관 + URL 기반 해시
        content = f"{program_info.get('title', '')}{program_info.get('agency', '')}{program_info.get('detail_url', '')}"
        return f"bizinfo_{hashlib.md5(content.encode()).hexdigest()[:12]}"
    
    def generate_content_hash(self, program_info: Dict) -> str:
        """콘텐츠 변경 감지용 해시"""
        # 주요 필드들로 해시 생성
        key_fields = ['title', 'agency', 'application_period', 'status']
        content = ''.join(str(program_info.get(field, '')) for field in key_fields)
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