#!/usr/bin/env python3
"""
Production Government Portal Scraper
정식 정부 포털 스크래핑 시스템

Version: 1.0.0
Author: HEAL7 Team
"""

import asyncio
import aiohttp
import asyncpg
import logging
import json
import hashlib
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import re
import time

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/tmp/production_scraper.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class ProductionScraper:
    """프로덕션 정부 포털 스크래퍼"""
    
    def __init__(self):
        self.db_pool = None
        self.session = None
        self.download_base_path = "/tmp/downloads"
        
        # 스크래핑 설정
        self.config = {
            'bizinfo': {
                'base_url': 'https://www.bizinfo.go.kr',
                'list_url': 'https://www.bizinfo.go.kr/web/lay1/biz/S1T122C128/AS/main.do?searchCondition=1&searchKeyword=&crtfcKey=',
                'max_pages': 5,
                'delay': 2.0
            },
            'kstartup': {
                'base_url': 'https://www.k-startup.go.kr',
                'list_url': 'https://www.k-startup.go.kr/main.do',
                'max_pages': 3,
                'delay': 3.0
            }
        }
        
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (compatible; HEAL7-Scraper/1.0; +https://paperwork.heal7.com)',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'ko-KR,ko;q=0.8,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive'
        }

    async def initialize(self):
        """시스템 초기화"""
        logger.info("🚀 Production Scraper 초기화 시작")
        
        # 데이터베이스 연결
        try:
            self.db_pool = await asyncpg.create_pool(
                host='localhost',
                database='paperworkdb',
                user='postgres',
                password='postgres',
                min_size=2,
                max_size=10
            )
            logger.info("✅ PostgreSQL 연결 완료")
        except Exception as e:
            logger.error(f"❌ 데이터베이스 연결 실패: {e}")
            raise
        
        # HTTP 세션 초기화
        connector = aiohttp.TCPConnector(limit=10, ttl_dns_cache=300, use_dns_cache=True)
        timeout = aiohttp.ClientTimeout(total=30)
        
        self.session = aiohttp.ClientSession(
            headers=self.headers,
            connector=connector,
            timeout=timeout
        )
        
        # 다운로드 폴더 생성
        os.makedirs(self.download_base_path, exist_ok=True)
        logger.info("✅ Production Scraper 초기화 완료")

    async def cleanup(self):
        """리소스 정리"""
        if self.session:
            await self.session.close()
        if self.db_pool:
            await self.db_pool.close()
        logger.info("🧹 리소스 정리 완료")

    async def scrape_all_portals(self) -> Dict:
        """모든 포털 스크래핑 실행"""
        logger.info("🌐 전체 포털 스크래핑 시작")
        
        results = {
            'total_scraped': 0,
            'total_new': 0,
            'total_updated': 0,
            'portals': {}
        }
        
        # 스크래핑 세션 시작
        session_id = await self.create_scraping_session()
        
        try:
            # 각 포털 스크래핑
            for portal_id in ['bizinfo', 'kstartup']:
                logger.info(f"📡 {portal_id} 포털 스크래핑 시작")
                
                portal_result = await self.scrape_single_portal(portal_id, session_id)
                results['portals'][portal_id] = portal_result
                results['total_scraped'] += portal_result['scraped_count']
                results['total_new'] += portal_result['new_count']
                results['total_updated'] += portal_result['updated_count']
                
                # 포털간 딜레이
                await asyncio.sleep(self.config[portal_id]['delay'])
            
            # 세션 완료
            await self.complete_scraping_session(session_id, results)
            
        except Exception as e:
            logger.error(f"❌ 스크래핑 실패: {e}")
            await self.fail_scraping_session(session_id, str(e))
            raise
        
        logger.info(f"✅ 전체 스크래핑 완료: {results['total_scraped']}개 수집, {results['total_new']}개 신규")
        return results

    async def create_scraping_session(self) -> str:
        """스크래핑 세션 생성"""
        async with self.db_pool.acquire() as conn:
            session_id = await conn.fetchval("""
                INSERT INTO scraping_sessions (portal_id, session_type, started_at, status)
                VALUES ('multi', 'production', CURRENT_TIMESTAMP, 'running')
                RETURNING id
            """)
            return str(session_id)

    async def complete_scraping_session(self, session_id: str, results: Dict):
        """스크래핑 세션 완료"""
        async with self.db_pool.acquire() as conn:
            await conn.execute("""
                UPDATE scraping_sessions 
                SET status = 'completed', 
                    completed_at = CURRENT_TIMESTAMP,
                    items_found = $2,
                    items_processed = $3,
                    items_migrated = $4
                WHERE id = $1
            """, session_id, results['total_scraped'], results['total_new'], results['total_updated'])

    async def fail_scraping_session(self, session_id: str, error_msg: str):
        """스크래핑 세션 실패 처리"""
        async with self.db_pool.acquire() as conn:
            await conn.execute("""
                UPDATE scraping_sessions 
                SET status = 'failed', 
                    completed_at = CURRENT_TIMESTAMP,
                    error_details = $2
                WHERE id = $1
            """, session_id, json.dumps({'error': error_msg}))

    async def scrape_single_portal(self, portal_id: str, session_id: str) -> Dict:
        """개별 포털 스크래핑"""
        portal_config = self.config[portal_id]
        scraped_programs = []
        
        if portal_id == 'bizinfo':
            scraped_programs = await self.scrape_bizinfo()
        elif portal_id == 'kstartup':
            scraped_programs = await self.scrape_kstartup()
        
        # Raw 데이터 저장
        raw_ids = []
        for program in scraped_programs:
            raw_id = await self.save_raw_data(portal_id, program, session_id)
            raw_ids.append(raw_id)
        
        # 정형 데이터로 마이그레이션
        migration_result = await self.migrate_to_structured(raw_ids, portal_id)
        
        return {
            'scraped_count': len(scraped_programs),
            'new_count': migration_result['new_count'],
            'updated_count': migration_result['updated_count'],
            'error_count': migration_result['error_count']
        }

    async def scrape_bizinfo(self) -> List[Dict]:
        """기업마당 스크래핑"""
        logger.info("🏢 기업마당 스크래핑 시작")
        
        try:
            url = self.config['bizinfo']['list_url']
            async with self.session.get(url) as response:
                if response.status != 200:
                    logger.error(f"❌ 기업마당 접근 실패: {response.status}")
                    return []
                
                html = await response.text()
                soup = BeautifulSoup(html, 'html.parser')
                
                programs = []
                
                # 테이블에서 데이터 추출
                table = soup.find('table')
                if not table:
                    logger.warning("⚠️ 기업마당 테이블을 찾을 수 없음")
                    return []
                
                rows = table.find_all('tr')[1:]  # 헤더 제외
                logger.info(f"📋 기업마당 행 발견: {len(rows)}개")
                
                for i, row in enumerate(rows[:20]):  # 최대 20개까지
                    try:
                        cells = row.find_all('td')
                        if len(cells) >= 4:
                            
                            # 제목과 링크 추출
                            title_cell = cells[0]
                            title_link = title_cell.find('a')
                            title = title_link.get_text(strip=True) if title_link else title_cell.get_text(strip=True)
                            detail_url = urljoin(self.config['bizinfo']['base_url'], title_link.get('href', '')) if title_link else ''
                            
                            # 기관명
                            agency = cells[1].get_text(strip=True)
                            
                            # 기간
                            period = cells[2].get_text(strip=True)
                            
                            # 상태
                            status = cells[3].get_text(strip=True)
                            
                            # 프로그램 ID 생성
                            program_id = f"BIZ_{datetime.now().strftime('%Y%m%d')}_{i+1:03d}"
                            
                            program = {
                                'program_id': program_id,
                                'title': title,
                                'implementing_agency': agency,
                                'application_period': period,
                                'application_status': 'active' if '접수중' in status else 'closed',
                                'detail_url': detail_url,
                                'scraped_at': datetime.now().isoformat(),
                                'portal_name': '정부지원사업통합정보시스템',
                                'quality_score': self.calculate_quality_score(title, agency, period)
                            }
                            
                            programs.append(program)
                            logger.info(f"✅ 기업마당 프로그램 {i+1}: {title[:50]}...")
                    
                    except Exception as e:
                        logger.error(f"❌ 기업마당 행 처리 실패 {i+1}: {e}")
                        continue
                
                logger.info(f"🏢 기업마당 수집 완료: {len(programs)}개")
                return programs
                
        except Exception as e:
            logger.error(f"❌ 기업마당 스크래핑 실패: {e}")
            return []

    async def scrape_kstartup(self) -> List[Dict]:
        """K-Startup 스크래핑"""
        logger.info("🚀 K-Startup 스크래핑 시작")
        
        try:
            url = self.config['kstartup']['list_url']
            async with self.session.get(url) as response:
                if response.status != 200:
                    logger.error(f"❌ K-Startup 접근 실패: {response.status}")
                    return []
                
                html = await response.text()
                soup = BeautifulSoup(html, 'html.parser')
                
                programs = []
                
                # 다양한 셀렉터로 시도
                selectors = [
                    'ul li a',
                    '.list-item a',
                    '.board-list a',
                    'table tr td a'
                ]
                
                items = []
                for selector in selectors:
                    items = soup.select(selector)
                    if len(items) > 5:
                        logger.info(f"✅ K-Startup 셀렉터 '{selector}' 사용: {len(items)}개 아이템")
                        break
                
                if not items:
                    logger.warning("⚠️ K-Startup 아이템을 찾을 수 없음")
                    return []
                
                for i, item in enumerate(items[:15]):  # 최대 15개
                    try:
                        title = item.get_text(strip=True)
                        # 의미있는 제목만 필터링 (SNS 링크, 외부 링크 제외)
                        if (title and len(title) > 10 and 
                            not any(skip_word in title for skip_word in 
                                   ['새창으로 열기', '페이스북', '블로그', '유튜브', '인스타그램', 
                                    'facebook', 'blog', 'youtube', 'instagram']) and
                            not title.startswith(('http', 'www.')) and
                            ('창업' in title or '지원' in title or '사업' in title or '공고' in title)):
                            detail_url = urljoin(self.config['kstartup']['base_url'], item.get('href', ''))
                            
                            # 프로그램 ID 생성
                            program_id = f"KST_{datetime.now().strftime('%Y%m%d')}_{i+1:03d}"
                            
                            program = {
                                'program_id': program_id,
                                'title': title,
                                'implementing_agency': '중소벤처기업부',
                                'application_period': f"{datetime.now().strftime('%Y-%m-%d')} ~ 상시",
                                'application_status': 'active',
                                'detail_url': detail_url,
                                'scraped_at': datetime.now().isoformat(),
                                'portal_name': 'K-Startup',
                                'quality_score': self.calculate_quality_score(title, '중소벤처기업부', '상시')
                            }
                            
                            programs.append(program)
                            logger.info(f"✅ K-Startup 프로그램 {i+1}: {title[:50]}...")
                    
                    except Exception as e:
                        logger.error(f"❌ K-Startup 아이템 처리 실패 {i+1}: {e}")
                        continue
                
                logger.info(f"🚀 K-Startup 수집 완료: {len(programs)}개")
                return programs
                
        except Exception as e:
            logger.error(f"❌ K-Startup 스크래핑 실패: {e}")
            return []

    def calculate_quality_score(self, title: str, agency: str, period: str) -> float:
        """데이터 품질 점수 계산"""
        score = 5.0  # 기본 점수
        
        # 제목 품질 검사
        if title and len(title) > 10:
            score += 1.5
        if title and any(keyword in title for keyword in ['지원', '사업', '모집', '공고']):
            score += 1.0
            
        # 기관명 품질 검사
        if agency and len(agency) > 3:
            score += 1.0
        if agency and any(keyword in agency for keyword in ['부', '청', '원', '단체']):
            score += 0.5
            
        # 기간 품질 검사
        if period and '~' in period:
            score += 1.0
        if period and re.search(r'\d{4}-\d{2}-\d{2}', period):
            score += 0.5
        
        return min(10.0, score)

    async def save_raw_data(self, portal_id: str, program: Dict, session_id: str) -> int:
        """Raw 데이터 저장"""
        async with self.db_pool.acquire() as conn:
            raw_id = await conn.fetchval("""
                INSERT INTO raw_scraped_data (
                    portal_id, url, scraping_session_id, raw_data, 
                    processing_status, quality_score, scraped_at
                ) VALUES ($1, $2, $3, $4, $5, $6, $7)
                RETURNING id
            """, 
            portal_id, 
            program.get('detail_url', ''), 
            session_id,
            json.dumps(program),
            'pending',
            program.get('quality_score', 5.0),
            datetime.now()
            )
            return raw_id

    async def migrate_to_structured(self, raw_ids: List[int], portal_id: str) -> Dict:
        """정형 데이터로 마이그레이션"""
        logger.info(f"🔄 {portal_id} 데이터 마이그레이션 시작: {len(raw_ids)}개")
        
        new_count = 0
        updated_count = 0
        error_count = 0
        
        async with self.db_pool.acquire() as conn:
            for raw_id in raw_ids:
                try:
                    # Raw 데이터 조회
                    raw_row = await conn.fetchrow("""
                        SELECT raw_data FROM raw_scraped_data WHERE id = $1
                    """, raw_id)
                    
                    if not raw_row:
                        continue
                    
                    # JSON 데이터 파싱 (이미 dict인 경우와 string인 경우 모두 처리)
                    raw_data = raw_row['raw_data']
                    if isinstance(raw_data, str):
                        program_data = json.loads(raw_data)
                    elif isinstance(raw_data, dict):
                        program_data = raw_data
                    else:
                        logger.error(f"❌ 예상치 못한 데이터 타입: {type(raw_data)}")
                        continue
                    
                    # 중복 체크
                    existing = await conn.fetchval("""
                        SELECT id FROM support_programs WHERE program_id = $1
                    """, program_data['program_id'])
                    
                    if existing:
                        # 업데이트
                        await conn.execute("""
                            UPDATE support_programs SET
                                title = $2,
                                implementing_agency = $3,
                                application_period = $4,
                                application_status = $5,
                                detail_url = $6,
                                portal_id = $7,
                                data_quality_score = $8,
                                updated_at = CURRENT_TIMESTAMP
                            WHERE program_id = $1
                        """, 
                        program_data['program_id'],
                        program_data.get('title'),
                        program_data.get('implementing_agency'),
                        program_data.get('application_period'),
                        program_data.get('application_status', 'active'),
                        program_data.get('detail_url'),
                        portal_id,
                        program_data.get('quality_score', 5.0)
                        )
                        updated_count += 1
                    else:
                        # 신규 추가
                        await conn.execute("""
                            INSERT INTO support_programs (
                                program_id, portal_id, original_raw_id, title,
                                implementing_agency, application_period, application_status,
                                detail_url, data_quality_score, created_at, updated_at
                            ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
                        """,
                        program_data['program_id'],
                        portal_id,
                        raw_id,
                        program_data.get('title'),
                        program_data.get('implementing_agency'),
                        program_data.get('application_period'),
                        program_data.get('application_status', 'active'),
                        program_data.get('detail_url'),
                        program_data.get('quality_score', 5.0)
                        )
                        new_count += 1
                    
                    # Raw 데이터 처리 완료 표시
                    await conn.execute("""
                        UPDATE raw_scraped_data 
                        SET processing_status = 'completed', processed_at = CURRENT_TIMESTAMP
                        WHERE id = $1
                    """, raw_id)
                    
                except Exception as e:
                    logger.error(f"❌ 마이그레이션 실패 raw_id={raw_id}: {e}")
                    error_count += 1
                    
                    # 오류 상태 저장
                    await conn.execute("""
                        UPDATE raw_scraped_data 
                        SET processing_status = 'failed', 
                            validation_errors = $2,
                            processed_at = CURRENT_TIMESTAMP
                        WHERE id = $1
                    """, raw_id, json.dumps({'error': str(e)}))
        
        logger.info(f"✅ {portal_id} 마이그레이션 완료: 신규 {new_count}, 업데이트 {updated_count}, 오류 {error_count}")
        
        return {
            'new_count': new_count,
            'updated_count': updated_count,
            'error_count': error_count
        }

    async def get_current_stats(self) -> Dict:
        """현재 통계 조회"""
        async with self.db_pool.acquire() as conn:
            stats = await conn.fetchrow("""
                SELECT 
                    COUNT(*) as total_programs,
                    COUNT(*) FILTER (WHERE portal_id = 'bizinfo') as bizinfo_count,
                    COUNT(*) FILTER (WHERE portal_id = 'kstartup') as kstartup_count,
                    AVG(data_quality_score) as avg_quality,
                    COUNT(*) FILTER (WHERE application_status = 'active') as active_count,
                    COUNT(*) FILTER (WHERE created_at::date = CURRENT_DATE) as today_count
                FROM support_programs
            """)
            return dict(stats)

async def main():
    """메인 실행 함수"""
    scraper = ProductionScraper()
    
    try:
        # 시스템 초기화
        await scraper.initialize()
        
        # 이전 통계 확인
        before_stats = await scraper.get_current_stats()
        logger.info(f"📊 스크래핑 전 통계: {before_stats}")
        
        # 전체 포털 스크래핑 실행
        results = await scraper.scrape_all_portals()
        
        # 이후 통계 확인
        after_stats = await scraper.get_current_stats()
        logger.info(f"📈 스크래핑 후 통계: {after_stats}")
        
        # 결과 출력
        print("\n" + "="*60)
        print("🎉 PRODUCTION SCRAPING COMPLETE")
        print("="*60)
        print(f"📊 총 수집: {results['total_scraped']}개")
        print(f"🆕 신규 추가: {results['total_new']}개") 
        print(f"🔄 업데이트: {results['total_updated']}개")
        print(f"📈 전체 프로그램: {before_stats['total_programs']} → {after_stats['total_programs']}")
        print(f"⭐ 평균 품질점수: {after_stats['avg_quality']:.2f}")
        print("="*60)
        
        # 포털별 결과
        for portal_id, portal_result in results['portals'].items():
            print(f"🌐 {portal_id.upper()}: {portal_result['scraped_count']}개 수집, {portal_result['new_count']}개 신규")
        
    except Exception as e:
        logger.error(f"💥 실행 실패: {e}")
        raise
    finally:
        await scraper.cleanup()

if __name__ == "__main__":
    asyncio.run(main())