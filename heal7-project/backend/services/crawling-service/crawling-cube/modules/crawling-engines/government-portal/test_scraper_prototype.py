#!/usr/bin/env python3
"""
정부 포털 스크래핑 프로토타입 테스트
실제 사이트 구조 기반 데이터 수집 검증

Author: Paperwork AI Team
Date: 2025-08-23
"""

import asyncio
import aiohttp
from bs4 import BeautifulSoup
import logging
from typing import List, Dict, Optional
from urllib.parse import urljoin
import time

# 로깅 설정
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class PortalScraperPrototype:
    """정부 포털 스크래퍼 프로토타입"""
    
    def __init__(self):
        self.session = None
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (compatible; PaperworkAI-Test/1.0)',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'ko-KR,ko;q=0.8,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive'
        }
        
    async def __aenter__(self):
        """비동기 컨텍스트 매니저 진입"""
        connector = aiohttp.TCPConnector(limit=3, ttl_dns_cache=300)
        timeout = aiohttp.ClientTimeout(total=30)
        
        self.session = aiohttp.ClientSession(
            headers=self.headers,
            connector=connector,
            timeout=timeout
        )
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """비동기 컨텍스트 매니저 종료"""
        if self.session:
            await self.session.close()

    async def test_bizinfo_scraping(self) -> List[Dict]:
        """기업마당 스크래핑 테스트"""
        logger.info("🏢 기업마당 스크래핑 테스트 시작")
        
        url = "https://www.bizinfo.go.kr/web/lay1/bbs/S1T122C128/AS/74/list.do"
        programs = []
        
        try:
            # 첫 페이지만 테스트
            params = {"cpage": 1}
            
            async with self.session.get(url, params=params) as response:
                if response.status != 200:
                    logger.error(f"❌ HTTP 오류: {response.status}")
                    return []
                
                html = await response.text()
                soup = BeautifulSoup(html, 'html.parser')
                
                logger.info(f"✅ 페이지 로드 성공: {len(html)} bytes")
                
                # 테이블 구조 분석
                table = soup.select_one('table')
                if not table:
                    logger.error("❌ 테이블을 찾을 수 없음")
                    return []
                
                logger.info("✅ 테이블 요소 발견")
                
                # 테이블 행 추출
                rows = table.select('tbody tr')
                if not rows:
                    # tbody가 없는 경우 직접 tr 찾기
                    rows = table.select('tr')
                    if rows:
                        rows = rows[1:]  # 헤더 행 제외
                
                logger.info(f"📋 테이블 행 발견: {len(rows)}개")
                
                for i, row in enumerate(rows[:5]):  # 처음 5개만 테스트
                    cells = row.select('td')
                    if len(cells) >= 6:
                        program = self.extract_bizinfo_program(cells, i + 1)
                        if program:
                            programs.append(program)
                            logger.info(f"✅ 프로그램 {i+1}: {program['title'][:50]}...")
                
        except Exception as e:
            logger.error(f"❌ 기업마당 스크래핑 오류: {str(e)}")
        
        return programs

    def extract_bizinfo_program(self, cells: List, index: int) -> Optional[Dict]:
        """기업마당 프로그램 정보 추출"""
        try:
            # 컬럼: 번호, 지원분야, 지원사업명, 신청기간, 소관부처, 사업수행기관, 등록일, 조회수
            if len(cells) < 6:
                return None
                
            program = {
                'index': index,
                'support_field': self.clean_text(cells[1].get_text()) if len(cells) > 1 else 'N/A',
                'title': self.clean_text(cells[2].get_text()) if len(cells) > 2 else 'N/A', 
                'application_period': self.clean_text(cells[3].get_text()) if len(cells) > 3 else 'N/A',
                'jurisdiction': self.clean_text(cells[4].get_text()) if len(cells) > 4 else 'N/A',
                'implementing_agency': self.clean_text(cells[5].get_text()) if len(cells) > 5 else 'N/A',
                'registration_date': self.clean_text(cells[6].get_text()) if len(cells) > 6 else 'N/A',
                'view_count': self.clean_text(cells[7].get_text()) if len(cells) > 7 else 'N/A'
            }
            
            # 상세 링크 추출
            link_elem = cells[2].select_one('a[href]') if len(cells) > 2 else None
            if link_elem:
                href = link_elem.get('href')
                program['detail_url'] = urljoin('https://www.bizinfo.go.kr', href)
            else:
                program['detail_url'] = None
                
            return program
            
        except Exception as e:
            logger.error(f"❌ 프로그램 정보 추출 실패 {index}: {str(e)}")
            return None

    async def test_kstartup_scraping(self) -> List[Dict]:
        """K-Startup 스크래핑 테스트"""
        logger.info("🚀 K-Startup 스크래핑 테스트 시작")
        
        url = "https://www.k-startup.go.kr/web/contents/bizpbanc-ongoing.do"
        programs = []
        
        try:
            async with self.session.get(url) as response:
                if response.status != 200:
                    logger.error(f"❌ HTTP 오류: {response.status}")
                    return []
                
                html = await response.text()
                soup = BeautifulSoup(html, 'html.parser')
                
                logger.info(f"✅ 페이지 로드 성공: {len(html)} bytes")
                
                # 다양한 셀렉터로 리스트 아이템 찾기
                selectors = [
                    '.list-item',
                    '.announcement-item', 
                    '.business-item',
                    '.program-item',
                    'ul li',
                    '.content li'
                ]
                
                items = []
                for selector in selectors:
                    items = soup.select(selector)
                    if items and len(items) > 5:  # 의미 있는 수의 아이템이 있는 경우
                        logger.info(f"✅ 셀렉터 '{selector}' 사용: {len(items)}개 아이템")
                        break
                
                if not items:
                    logger.warning("⚠️ 리스트 아이템을 찾을 수 없음. 페이지 구조 분석...")
                    # 페이지 구조 분석을 위해 주요 요소들 출력
                    self.analyze_page_structure(soup)
                    return []
                
                # 처음 5개 아이템만 분석
                for i, item in enumerate(items[:5]):
                    program = self.extract_kstartup_program(item, i + 1)
                    if program:
                        programs.append(program)
                        logger.info(f"✅ 프로그램 {i+1}: {program['title'][:50]}...")
                
        except Exception as e:
            logger.error(f"❌ K-Startup 스크래핑 오류: {str(e)}")
        
        return programs

    def extract_kstartup_program(self, item, index: int) -> Optional[Dict]:
        """K-Startup 프로그램 정보 추출"""
        try:
            # 제목 추출
            title_selectors = ['.title', 'h3', 'h4', '.subject', 'strong', 'a']
            title = 'N/A'
            
            for selector in title_selectors:
                title_elem = item.select_one(selector)
                if title_elem:
                    title = self.clean_text(title_elem.get_text())
                    if title and len(title) > 5:  # 의미 있는 제목
                        break
            
            # 기본 텍스트 추출 (제목을 찾지 못한 경우)
            if title == 'N/A' or len(title) <= 5:
                title = self.clean_text(item.get_text())
                if len(title) > 100:  # 너무 긴 경우 앞부분만
                    title = title[:100] + '...'
            
            program = {
                'index': index,
                'title': title,
                'raw_html': str(item)[:200] + '...',  # 디버깅용
            }
            
            # 추가 정보 추출 시도
            for attr, selectors in {
                'status': ['.status', '.state', '.badge', '.label'],
                'organization': ['.org', '.agency', '.department'],
                'period': ['.period', '.date', '.deadline'],
                'category': ['.category', '.tag', '.type']
            }.items():
                
                value = 'N/A'
                for selector in selectors:
                    elem = item.select_one(selector)
                    if elem:
                        value = self.clean_text(elem.get_text())
                        if value and len(value) > 2:
                            break
                
                program[attr] = value
            
            return program if title != 'N/A' and len(title) > 5 else None
            
        except Exception as e:
            logger.error(f"❌ K-Startup 프로그램 추출 실패 {index}: {str(e)}")
            return None

    def analyze_page_structure(self, soup: BeautifulSoup):
        """페이지 구조 분석 (디버깅용)"""
        logger.info("🔍 페이지 구조 분석 시작")
        
        # 주요 컨테이너 요소들 확인
        containers = [
            'main', '.main', '#main',
            '.content', '#content', 
            '.container', '.wrapper',
            '.list', '.items', '.announcements'
        ]
        
        for container in containers:
            elem = soup.select_one(container)
            if elem:
                logger.info(f"📦 컨테이너 발견: {container}")
                # 하위 요소들 분석
                children = elem.find_all(['ul', 'ol', 'div', 'section'], limit=10)
                for child in children:
                    if child.get('class'):
                        logger.info(f"  └─ 하위 요소: {child.name}.{'.'.join(child.get('class'))}")

    def clean_text(self, text: str) -> str:
        """텍스트 정리"""
        if not text:
            return 'N/A'
        
        # 공백 문자 정리
        cleaned = ' '.join(text.strip().split())
        
        # 빈 문자열 처리
        return cleaned if cleaned else 'N/A'

async def main():
    """메인 테스트 함수"""
    logger.info("🚀 정부 포털 스크래핑 프로토타입 테스트 시작")
    
    async with PortalScraperPrototype() as scraper:
        # 기업마당 테스트
        bizinfo_programs = await scraper.test_bizinfo_scraping()
        logger.info(f"🏢 기업마당 수집 결과: {len(bizinfo_programs)}개 프로그램")
        
        if bizinfo_programs:
            logger.info("📋 기업마당 샘플 데이터:")
            for i, program in enumerate(bizinfo_programs[:3]):
                logger.info(f"  {i+1}. {program['title']}")
                logger.info(f"     기관: {program['implementing_agency']}")
                logger.info(f"     기간: {program['application_period']}")
        
        await asyncio.sleep(2)  # 요청 간격
        
        # K-Startup 테스트
        kstartup_programs = await scraper.test_kstartup_scraping()
        logger.info(f"🚀 K-Startup 수집 결과: {len(kstartup_programs)}개 프로그램")
        
        if kstartup_programs:
            logger.info("📋 K-Startup 샘플 데이터:")
            for i, program in enumerate(kstartup_programs[:3]):
                logger.info(f"  {i+1}. {program['title']}")
                if program.get('organization') != 'N/A':
                    logger.info(f"     기관: {program['organization']}")
                if program.get('period') != 'N/A':
                    logger.info(f"     기간: {program['period']}")
    
    logger.info("✅ 프로토타입 테스트 완료")

if __name__ == "__main__":
    asyncio.run(main())