#!/usr/bin/env python3
"""
🏢 기업마당(bizinfo.go.kr) 실제 수집기 구현
정부 지원사업 실시간 모니터링 및 데이터 수집

Author: HEAL7 Development Team
Version: 1.0.0
Date: 2025-08-29
"""

import asyncio
import logging
import re
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from urllib.parse import urljoin, urlparse, parse_qs

import aiohttp
from bs4 import BeautifulSoup

from core_collection_engine import CoreCollectionEngine, create_collection_engine


logger = logging.getLogger(__name__)


class BizinfoCollector:
    """🏢 기업마당 전용 실제 데이터 수집기"""
    
    def __init__(self, collection_engine: CoreCollectionEngine):
        self.engine = collection_engine
        self.base_url = "https://www.bizinfo.go.kr"
        
        # 기업마당 특화 설정
        self.search_endpoints = {
            'support_programs': '/web/lay1/bbs/S1T122C128/AS/list.do',  # 지원사업
            'funding': '/web/lay1/bbs/S1T122C129/AS/list.do',           # 자금지원  
            'startup': '/web/lay1/bbs/S1T122C130/AS/list.do',          # 창업지원
        }
        
        # 카테고리 매핑
        self.category_mapping = {
            'C128': '지원사업',
            'C129': '자금지원', 
            'C130': '창업지원',
            'C131': '기술개발',
            'C132': '해외진출',
            'C133': '판로개척'
        }
    
    async def collect_support_programs(self, max_pages: int = 10) -> List[Dict]:
        """지원사업 데이터 수집"""
        logger.info(f"🏢 기업마당 지원사업 수집 시작 (최대 {max_pages}페이지)")
        
        all_programs = []
        
        # 각 카테고리별로 수집
        for category_code, category_name in self.category_mapping.items():
            try:
                programs = await self._collect_category_programs(
                    category_code, category_name, max_pages
                )
                all_programs.extend(programs)
                logger.info(f"✅ {category_name} 카테고리: {len(programs)}개 프로그램 수집")
                
                # 요청 간 간격
                await asyncio.sleep(2.0)
                
            except Exception as e:
                logger.error(f"❌ {category_name} 카테고리 수집 실패: {str(e)}")
        
        logger.info(f"🎯 기업마당 총 {len(all_programs)}개 프로그램 수집 완료")
        return all_programs
    
    async def _collect_category_programs(
        self, 
        category_code: str, 
        category_name: str,
        max_pages: int
    ) -> List[Dict]:
        """특정 카테고리의 프로그램 수집"""
        programs = []
        
        for page in range(1, max_pages + 1):
            try:
                page_programs = await self._scrape_category_page(
                    category_code, category_name, page
                )
                
                if not page_programs:
                    logger.info(f"📄 {category_name} {page}페이지: 데이터 없음 (수집 종료)")
                    break
                
                programs.extend(page_programs)
                logger.debug(f"📄 {category_name} {page}페이지: {len(page_programs)}개")
                
                # 페이지 요청 간격
                await asyncio.sleep(1.5)
                
            except Exception as e:
                logger.error(f"❌ {category_name} {page}페이지 실패: {str(e)}")
                break
        
        return programs
    
    async def _scrape_category_page(
        self,
        category_code: str,
        category_name: str, 
        page: int
    ) -> List[Dict]:
        """카테고리 페이지 스크래핑"""
        
        # 기업마당 목록 URL 구성
        list_url = f"{self.base_url}/web/lay1/bbs/S1T122{category_code}/AS/list.do"
        params = {
            'currentPage': str(page),
            'pageSize': '20',  # 한 페이지당 20개 항목
        }
        
        async with self.engine.session.get(list_url, params=params) as response:
            if response.status != 200:
                logger.warning(f"⚠️ HTTP {response.status}: {list_url}")
                return []
            
            html = await response.text()
            soup = BeautifulSoup(html, 'html.parser')
            
            return await self._parse_program_list(soup, category_name)
    
    async def _parse_program_list(self, soup: BeautifulSoup, category_name: str) -> List[Dict]:
        """프로그램 목록 파싱"""
        programs = []
        
        # 기업마당의 게시판 구조 파싱
        # 실제 구조에 맞게 셀렉터 조정 필요
        program_rows = soup.select('table.board-list tbody tr')
        
        if not program_rows:
            # 대체 셀렉터 시도
            program_rows = soup.select('.list-item, .board-item, .program-item')
        
        for row in program_rows:
            try:
                program = await self._parse_single_program(row, category_name)
                if program and program.get('title'):
                    programs.append(program)
                    
            except Exception as e:
                logger.debug(f"프로그램 파싱 오류: {str(e)}")
                continue
        
        # 만약 테이블 구조가 아니라면 다른 방식으로 파싱
        if not programs:
            programs = await self._parse_alternative_structure(soup, category_name)
        
        return programs
    
    async def _parse_single_program(self, row, category_name: str) -> Optional[Dict]:
        """개별 프로그램 정보 파싱"""
        program = {
            'portal_id': 'bizinfo',
            'category': category_name,
            'scraped_at': datetime.now().isoformat(),
        }
        
        try:
            # 제목 추출 (여러 가능한 셀렉터)
            title_element = (
                row.select_one('.title a') or
                row.select_one('.subject a') or  
                row.select_one('td.title a') or
                row.select_one('a[href*="view.do"]')
            )
            
            if title_element:
                program['title'] = title_element.get_text(strip=True)
                program['url'] = urljoin(self.base_url, title_element.get('href', ''))
            
            # 기관명 추출
            agency_element = (
                row.select_one('.agency') or
                row.select_one('.organ') or
                row.select_one('td:nth-child(3)') or
                row.select_one('.institution')
            )
            
            if agency_element:
                program['agency'] = agency_element.get_text(strip=True)
            
            # 기간 정보 추출
            period_element = (
                row.select_one('.period') or
                row.select_one('.date') or
                row.select_one('td:nth-child(4)')
            )
            
            if period_element:
                program['application_period'] = period_element.get_text(strip=True)
            
            # 상세 정보가 있으면 추가 수집
            if program.get('url'):
                detailed_info = await self._collect_program_details(program['url'])
                program.update(detailed_info)
            
            return program
            
        except Exception as e:
            logger.debug(f"개별 프로그램 파싱 실패: {str(e)}")
            return None
    
    async def _parse_alternative_structure(self, soup: BeautifulSoup, category_name: str) -> List[Dict]:
        """대체 구조 파싱 (카드 형태 등)"""
        programs = []
        
        # 다양한 가능한 구조 시도
        selectors_to_try = [
            '.program-card',
            '.support-item',
            '.list-box .item',
            '.program-list .item',
            '[class*="program"]',
            '[class*="support"]'
        ]
        
        for selector in selectors_to_try:
            items = soup.select(selector)
            if items:
                logger.info(f"🔍 대체 구조 발견: {selector} ({len(items)}개)")
                
                for item in items:
                    try:
                        program = {
                            'portal_id': 'bizinfo',
                            'category': category_name,
                            'scraped_at': datetime.now().isoformat(),
                        }
                        
                        # 제목
                        title_link = item.select_one('a')
                        if title_link:
                            program['title'] = title_link.get_text(strip=True)
                            program['url'] = urljoin(self.base_url, title_link.get('href', ''))
                        
                        # 기관명 (다양한 위치 시도)
                        agency_text = (
                            item.select_one('.agency, .organ, .institution') or
                            item.select_one('[class*="agency"], [class*="organ"]')
                        )
                        if agency_text:
                            program['agency'] = agency_text.get_text(strip=True)
                        
                        if program.get('title'):
                            programs.append(program)
                            
                    except Exception as e:
                        continue
                
                if programs:
                    break  # 성공한 셀렉터 찾으면 중단
        
        return programs
    
    async def _collect_program_details(self, detail_url: str) -> Dict:
        """프로그램 상세 정보 수집"""
        try:
            async with self.engine.session.get(detail_url) as response:
                if response.status != 200:
                    return {}
                
                html = await response.text()
                soup = BeautifulSoup(html, 'html.parser')
                
                details = {}
                
                # 지원대상 추출
                target_element = soup.select_one('.target, .object, [class*="target"]')
                if target_element:
                    details['target_audience'] = target_element.get_text(strip=True)
                
                # 지원내용 추출  
                content_element = soup.select_one('.content, .detail, .support-detail')
                if content_element:
                    details['support_content'] = content_element.get_text(strip=True)[:1000]
                
                # 신청기간 추출
                period_element = soup.select_one('.apply-period, .period, [class*="period"]')
                if period_element:
                    details['application_period'] = period_element.get_text(strip=True)
                
                # 담당기관 연락처 추출
                contact_element = soup.select_one('.contact, .phone, [class*="contact"]')
                if contact_element:
                    details['contact_info'] = contact_element.get_text(strip=True)
                
                # 지원규모/예산 추출
                budget_element = soup.select_one('.budget, .scale, [class*="budget"]')
                if budget_element:
                    details['support_scale'] = budget_element.get_text(strip=True)
                
                return details
                
        except Exception as e:
            logger.debug(f"상세정보 수집 실패 {detail_url}: {str(e)}")
            return {}


class KStartupCollector:
    """🚀 K-Startup (k-startup.go.kr) 수집기"""
    
    def __init__(self, collection_engine: CoreCollectionEngine):
        self.engine = collection_engine
        self.base_url = "https://www.k-startup.go.kr"
        
        # K-Startup 특화 설정
        self.api_endpoints = {
            'startup_support': '/api/startup/support',
            'biz_support': '/api/biz/support',
            'contest': '/api/contest/list'
        }
    
    async def collect_startup_programs(self, max_pages: int = 10) -> List[Dict]:
        """K-Startup 창업지원 프로그램 수집"""
        logger.info(f"🚀 K-Startup 프로그램 수집 시작 (최대 {max_pages}페이지)")
        
        all_programs = []
        
        # K-Startup은 주로 Ajax API를 사용하므로 API 호출
        for api_name, endpoint in self.api_endpoints.items():
            try:
                programs = await self._collect_from_api(api_name, endpoint, max_pages)
                all_programs.extend(programs)
                logger.info(f"✅ {api_name}: {len(programs)}개 프로그램 수집")
                
                await asyncio.sleep(2.0)
                
            except Exception as e:
                logger.error(f"❌ {api_name} API 수집 실패: {str(e)}")
        
        # API가 실패하면 웹 스크래핑으로 대체
        if not all_programs:
            all_programs = await self._collect_from_web_pages(max_pages)
        
        logger.info(f"🎯 K-Startup 총 {len(all_programs)}개 프로그램 수집 완료")
        return all_programs
    
    async def _collect_from_api(self, api_name: str, endpoint: str, max_pages: int) -> List[Dict]:
        """K-Startup API에서 데이터 수집"""
        programs = []
        
        for page in range(1, max_pages + 1):
            try:
                api_url = f"{self.base_url}{endpoint}"
                params = {
                    'page': page,
                    'size': 20,
                    'sort': 'regDate,desc'
                }
                
                async with self.engine.session.get(api_url, params=params) as response:
                    if response.status != 200:
                        break
                    
                    try:
                        data = await response.json()
                    except:
                        # JSON이 아니면 HTML 파싱으로 전환
                        break
                    
                    page_programs = await self._parse_api_response(data, api_name)
                    
                    if not page_programs:
                        break
                    
                    programs.extend(page_programs)
                    await asyncio.sleep(1.0)
                    
            except Exception as e:
                logger.debug(f"{api_name} API {page}페이지 실패: {str(e)}")
                break
        
        return programs
    
    async def _parse_api_response(self, data: Dict, api_name: str) -> List[Dict]:
        """API 응답 데이터 파싱"""
        programs = []
        
        # API 응답 구조에 따라 데이터 추출
        items = (
            data.get('content', []) or
            data.get('data', []) or
            data.get('list', []) or
            data.get('items', [])
        )
        
        for item in items:
            try:
                program = {
                    'portal_id': 'kstartup',
                    'category': self._map_api_category(api_name),
                    'title': item.get('title', item.get('name', '')),
                    'agency': item.get('agency', item.get('organization', '중소벤처기업부')),
                    'application_period': item.get('applyPeriod', item.get('period', '')),
                    'target_audience': item.get('target', ''),
                    'support_content': item.get('content', item.get('description', ''))[:1000],
                    'scraped_at': datetime.now().isoformat(),
                }
                
                # URL 구성
                if item.get('id'):
                    program['url'] = f"{self.base_url}/web/contents/view.do?schId={item['id']}"
                
                if program.get('title'):
                    programs.append(program)
                    
            except Exception as e:
                logger.debug(f"API 응답 파싱 오류: {str(e)}")
                continue
        
        return programs
    
    async def _collect_from_web_pages(self, max_pages: int) -> List[Dict]:
        """웹페이지에서 직접 수집 (API 실패 시 대체)"""
        programs = []
        
        # K-Startup 주요 페이지들
        page_urls = [
            '/web/contents/bizListPage.do',  # 사업공고
            '/web/contents/supportListPage.do',  # 지원사업
        ]
        
        for page_url in page_urls:
            try:
                url = f"{self.base_url}{page_url}"
                
                async with self.engine.session.get(url) as response:
                    if response.status != 200:
                        continue
                    
                    html = await response.text()
                    soup = BeautifulSoup(html, 'html.parser')
                    
                    page_programs = await self._parse_kstartup_page(soup)
                    programs.extend(page_programs)
                    
                    logger.info(f"📄 {page_url}: {len(page_programs)}개 수집")
                    await asyncio.sleep(2.0)
                    
            except Exception as e:
                logger.error(f"K-Startup 페이지 수집 실패 {page_url}: {str(e)}")
        
        return programs
    
    async def _parse_kstartup_page(self, soup: BeautifulSoup) -> List[Dict]:
        """K-Startup 페이지 파싱"""
        programs = []
        
        # K-Startup의 게시판 구조 파싱
        program_items = (
            soup.select('.biz-list .item') or
            soup.select('.support-list .item') or
            soup.select('table tbody tr') or
            soup.select('.program-card')
        )
        
        for item in program_items:
            try:
                program = {
                    'portal_id': 'kstartup',
                    'category': '창업지원',
                    'agency': '중소벤처기업부',
                    'scraped_at': datetime.now().isoformat(),
                }
                
                # 제목 및 URL
                title_link = item.select_one('a')
                if title_link:
                    program['title'] = title_link.get_text(strip=True)
                    program['url'] = urljoin(self.base_url, title_link.get('href', ''))
                
                # 기간 정보
                period = item.select_one('.period, .date')
                if period:
                    program['application_period'] = period.get_text(strip=True)
                
                if program.get('title'):
                    programs.append(program)
                    
            except Exception as e:
                continue
        
        return programs
    
    def _map_api_category(self, api_name: str) -> str:
        """API 이름을 카테고리로 매핑"""
        mapping = {
            'startup_support': '창업지원',
            'biz_support': '기업지원',
            'contest': '공모전'
        }
        return mapping.get(api_name, '기타')


# 통합 수집 실행 함수

async def run_comprehensive_collection(
    db_connection_string: str,
    portals: List[str] = ['bizinfo', 'kstartup'],
    max_pages: int = 10
):
    """종합적인 데이터 수집 실행"""
    logger.info("🚀 종합 데이터 수집 시작")
    
    # 수집 엔진 초기화
    engine = await create_collection_engine(db_connection_string)
    
    try:
        results = []
        
        if 'bizinfo' in portals:
            # 기업마당 수집
            bizinfo_collector = BizinfoCollector(engine)
            
            result = await engine.collect_from_portal(
                portal_id='bizinfo',
                extractor_func=bizinfo_collector.collect_support_programs,
                pages_to_scan=max_pages
            )
            results.append(result)
        
        if 'kstartup' in portals:
            # K-Startup 수집
            kstartup_collector = KStartupCollector(engine)
            
            result = await engine.collect_from_portal(
                portal_id='kstartup', 
                extractor_func=kstartup_collector.collect_startup_programs,
                pages_to_scan=max_pages
            )
            results.append(result)
        
        # 수집 결과 요약
        total_new = sum(r.new_items for r in results)
        total_duplicates = sum(r.duplicates for r in results)
        total_time = sum(r.processing_time for r in results)
        
        logger.info(f"🎯 종합 수집 완료: 신규 {total_new}개 | 중복 {total_duplicates}개 | {total_time:.1f}초")
        
        return results
        
    finally:
        await engine.close()


# 테스트 실행 함수
async def test_collection():
    """수집기 테스트"""
    # PostgreSQL 연결 문자열 (실제 환경에 맞게 수정)
    db_conn = "postgresql://postgres:@localhost:5432/paperworkdb"
    
    try:
        results = await run_comprehensive_collection(
            db_connection_string=db_conn,
            portals=['bizinfo'],  # 테스트는 기업마당만
            max_pages=3
        )
        
        for result in results:
            print(f"Portal: {result.portal_id}")
            print(f"Success: {result.success}")
            print(f"New items: {result.new_items}")
            print(f"Duplicates: {result.duplicates}")
            print(f"Time: {result.processing_time:.1f}s")
            print("---")
            
    except Exception as e:
        logger.error(f"테스트 실패: {str(e)}")


if __name__ == "__main__":
    # 로깅 설정
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # 테스트 실행
    asyncio.run(test_collection())