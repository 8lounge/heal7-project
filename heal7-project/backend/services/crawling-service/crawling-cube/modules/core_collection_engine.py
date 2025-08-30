#!/usr/bin/env python3
"""
🎯 핵심 수집 엔진 - 크롤링 시스템 공통 모듈
실시간 데이터 수집 및 처리를 위한 통합 엔진

Author: HEAL7 Development Team  
Version: 1.0.0
Date: 2025-08-29
"""

import asyncio
import logging
import hashlib
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, asdict
from enum import Enum

import aiohttp
import asyncpg
from bs4 import BeautifulSoup


logger = logging.getLogger(__name__)


class CollectionStatus(Enum):
    """수집 상태 열거형"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    DUPLICATE = "duplicate"
    PROCESSING = "processing"


@dataclass
class CollectionItem:
    """수집된 개별 아이템 데이터 구조"""
    id: Optional[str] = None
    portal_id: str = ""
    title: str = ""
    agency: str = ""
    category: str = ""
    content: Dict[str, Any] = None
    url: str = ""
    scraped_at: datetime = None
    quality_score: float = 0.0
    status: CollectionStatus = CollectionStatus.PENDING
    hash_key: str = ""
    
    def __post_init__(self):
        if self.scraped_at is None:
            self.scraped_at = datetime.now()
        if not self.hash_key:
            self.hash_key = self.generate_hash()
        if self.content is None:
            self.content = {}
    
    def generate_hash(self) -> str:
        """컨텐츠 해시 생성 (중복 감지용)"""
        content_str = f"{self.portal_id}_{self.title}_{self.agency}_{self.url}"
        return hashlib.md5(content_str.encode('utf-8')).hexdigest()


@dataclass 
class CollectionResult:
    """수집 결과 데이터"""
    portal_id: str
    success: bool
    items_found: int
    new_items: int
    duplicates: int
    errors: int
    processing_time: float
    start_time: datetime
    end_time: datetime
    error_messages: List[str] = None
    
    def __post_init__(self):
        if self.error_messages is None:
            self.error_messages = []


class CoreCollectionEngine:
    """🎯 핵심 수집 엔진 - 모든 크롤러의 공통 기반"""
    
    def __init__(self, db_connection_string: str):
        self.db_connection_string = db_connection_string
        self.db_pool = None
        
        # 수집 설정
        self.max_concurrent = 5
        self.request_timeout = 30
        self.max_retries = 3
        self.duplicate_check_days = 7
        
        # 통계
        self.total_requests = 0
        self.successful_requests = 0
        self.failed_requests = 0
        
        # HTTP 세션
        self.session = None
        self.default_headers = {
            'User-Agent': 'HEAL7-CollectionBot/1.0 (+https://heal7.com/crawler)',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'ko-KR,ko;q=0.8,en-US;q=0.5',
            'Connection': 'keep-alive'
        }
    
    async def initialize(self):
        """엔진 초기화"""
        logger.info("🚀 Core Collection Engine 초기화 시작")
        
        # 데이터베이스 연결 풀 생성
        try:
            self.db_pool = await asyncpg.create_pool(
                self.db_connection_string,
                min_size=2,
                max_size=10,
                command_timeout=30
            )
            logger.info("✅ 데이터베이스 연결 풀 생성 완료")
        except Exception as e:
            logger.error(f"❌ 데이터베이스 연결 실패: {e}")
            raise
        
        # HTTP 세션 생성
        connector = aiohttp.TCPConnector(
            limit=self.max_concurrent,
            limit_per_host=3,
            ttl_dns_cache=300
        )
        
        timeout = aiohttp.ClientTimeout(total=self.request_timeout)
        
        self.session = aiohttp.ClientSession(
            headers=self.default_headers,
            connector=connector, 
            timeout=timeout,
            cookie_jar=aiohttp.CookieJar()
        )
        
        logger.info("✅ HTTP 세션 초기화 완료")
        
        # 데이터베이스 스키마 초기화
        await self.initialize_database_schema()
        
        logger.info("🎯 Core Collection Engine 초기화 완료")
    
    async def close(self):
        """엔진 정리"""
        if self.session:
            await self.session.close()
        
        if self.db_pool:
            await self.db_pool.close()
        
        logger.info("🛑 Core Collection Engine 정리 완료")
    
    async def initialize_database_schema(self):
        """데이터베이스 스키마 초기화"""
        schema_sql = """
        -- 크롤링 데이터 저장 테이블
        CREATE TABLE IF NOT EXISTS raw_scraped_data (
            id SERIAL PRIMARY KEY,
            portal_id VARCHAR(50) NOT NULL,
            title TEXT NOT NULL,
            agency VARCHAR(200),
            category VARCHAR(100),
            raw_data JSONB NOT NULL,
            url TEXT,
            hash_key VARCHAR(32) UNIQUE NOT NULL,
            quality_score DECIMAL(3,1) DEFAULT 0.0,
            scraped_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
            processing_status VARCHAR(20) DEFAULT 'pending',
            created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
            updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
        );
        
        -- 인덱스 생성
        CREATE INDEX IF NOT EXISTS idx_raw_scraped_portal_id ON raw_scraped_data(portal_id);
        CREATE INDEX IF NOT EXISTS idx_raw_scraped_scraped_at ON raw_scraped_data(scraped_at);
        CREATE INDEX IF NOT EXISTS idx_raw_scraped_status ON raw_scraped_data(processing_status);
        CREATE INDEX IF NOT EXISTS idx_raw_scraped_hash ON raw_scraped_data(hash_key);
        
        -- 수집 통계 테이블
        CREATE TABLE IF NOT EXISTS collection_stats (
            id SERIAL PRIMARY KEY,
            portal_id VARCHAR(50) NOT NULL,
            collection_date DATE NOT NULL,
            items_found INTEGER DEFAULT 0,
            items_new INTEGER DEFAULT 0,
            items_duplicate INTEGER DEFAULT 0,
            items_failed INTEGER DEFAULT 0,
            processing_time_seconds DECIMAL(10,2) DEFAULT 0,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
            UNIQUE(portal_id, collection_date)
        );
        """
        
        async with self.db_pool.acquire() as conn:
            await conn.execute(schema_sql)
        
        logger.info("✅ 데이터베이스 스키마 초기화 완료")
    
    async def collect_from_portal(
        self, 
        portal_id: str,
        extractor_func: Callable,
        pages_to_scan: int = 10,
        force_update: bool = False
    ) -> CollectionResult:
        """포털에서 데이터 수집 실행"""
        start_time = datetime.now()
        
        logger.info(f"🕷️ 수집 시작: {portal_id} (페이지: {pages_to_scan})")
        
        collected_items = []
        errors = []
        
        try:
            # 1단계: 데이터 추출
            raw_items = await extractor_func(pages_to_scan)
            logger.info(f"📊 원본 데이터 {len(raw_items)}개 추출 완료")
            
            # 2단계: 데이터 정제 및 구조화
            for raw_item in raw_items:
                try:
                    item = CollectionItem(
                        portal_id=portal_id,
                        title=raw_item.get('title', ''),
                        agency=raw_item.get('agency', ''),
                        category=raw_item.get('category', ''),
                        content=raw_item,
                        url=raw_item.get('url', ''),
                        quality_score=self.calculate_quality_score(raw_item)
                    )
                    collected_items.append(item)
                except Exception as e:
                    errors.append(f"아이템 처리 실패: {str(e)}")
            
            # 3단계: 중복 검사
            if not force_update:
                collected_items = await self.filter_duplicates(collected_items)
            
            # 4단계: 데이터베이스 저장
            save_result = await self.save_items_to_database(collected_items)
            
            # 5단계: 통계 업데이트
            await self.update_collection_stats(
                portal_id=portal_id,
                items_found=len(raw_items),
                items_new=save_result['new_count'], 
                items_duplicate=save_result['duplicate_count'],
                processing_time=(datetime.now() - start_time).total_seconds()
            )
            
            end_time = datetime.now()
            processing_time = (end_time - start_time).total_seconds()
            
            result = CollectionResult(
                portal_id=portal_id,
                success=True,
                items_found=len(raw_items),
                new_items=save_result['new_count'],
                duplicates=save_result['duplicate_count'],
                errors=len(errors),
                processing_time=processing_time,
                start_time=start_time,
                end_time=end_time,
                error_messages=errors
            )
            
            logger.info(f"✅ 수집 완료: {portal_id} | 신규 {result.new_items}개 | 중복 {result.duplicates}개 | {processing_time:.1f}초")
            
            return result
            
        except Exception as e:
            end_time = datetime.now() 
            processing_time = (end_time - start_time).total_seconds()
            
            logger.error(f"❌ 수집 실패: {portal_id} - {str(e)}")
            
            return CollectionResult(
                portal_id=portal_id,
                success=False,
                items_found=0,
                new_items=0,
                duplicates=0,
                errors=1,
                processing_time=processing_time,
                start_time=start_time,
                end_time=end_time,
                error_messages=[str(e)]
            )
    
    async def filter_duplicates(self, items: List[CollectionItem]) -> List[CollectionItem]:
        """중복 항목 필터링"""
        if not items:
            return items
        
        # 해시키 기반으로 기존 데이터 확인
        hash_keys = [item.hash_key for item in items]
        
        async with self.db_pool.acquire() as conn:
            existing_hashes = await conn.fetch(
                """
                SELECT hash_key FROM raw_scraped_data 
                WHERE hash_key = ANY($1::text[])
                AND scraped_at >= $2
                """,
                hash_keys,
                datetime.now() - timedelta(days=self.duplicate_check_days)
            )
        
        existing_hash_set = {row['hash_key'] for row in existing_hashes}
        
        # 중복되지 않은 항목만 반환
        unique_items = []
        for item in items:
            if item.hash_key not in existing_hash_set:
                unique_items.append(item)
            else:
                item.status = CollectionStatus.DUPLICATE
        
        logger.info(f"🔍 중복 필터링: {len(items)} → {len(unique_items)} (중복 {len(items) - len(unique_items)}개)")
        
        return unique_items
    
    async def save_items_to_database(self, items: List[CollectionItem]) -> Dict[str, int]:
        """데이터베이스에 아이템 저장"""
        if not items:
            return {'new_count': 0, 'duplicate_count': 0}
        
        new_count = 0
        duplicate_count = 0
        
        async with self.db_pool.acquire() as conn:
            for item in items:
                try:
                    await conn.execute(
                        """
                        INSERT INTO raw_scraped_data 
                        (portal_id, title, agency, category, raw_data, url, hash_key, 
                         quality_score, scraped_at, processing_status)
                        VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10)
                        ON CONFLICT (hash_key) DO NOTHING
                        """,
                        item.portal_id,
                        item.title,
                        item.agency, 
                        item.category,
                        json.dumps(item.content, ensure_ascii=False),
                        item.url,
                        item.hash_key,
                        item.quality_score,
                        item.scraped_at,
                        item.status.value
                    )
                    new_count += 1
                    item.status = CollectionStatus.COMPLETED
                    
                except Exception as e:
                    if "duplicate key" in str(e).lower():
                        duplicate_count += 1
                        item.status = CollectionStatus.DUPLICATE
                    else:
                        logger.error(f"❌ 저장 실패: {item.title} - {str(e)}")
                        item.status = CollectionStatus.FAILED
        
        logger.info(f"💾 데이터 저장 완료: 신규 {new_count}개, 중복 {duplicate_count}개")
        
        return {'new_count': new_count, 'duplicate_count': duplicate_count}
    
    async def update_collection_stats(
        self,
        portal_id: str,
        items_found: int,
        items_new: int, 
        items_duplicate: int,
        processing_time: float
    ):
        """수집 통계 업데이트"""
        today = datetime.now().date()
        
        async with self.db_pool.acquire() as conn:
            await conn.execute(
                """
                INSERT INTO collection_stats 
                (portal_id, collection_date, items_found, items_new, 
                 items_duplicate, processing_time_seconds)
                VALUES ($1, $2, $3, $4, $5, $6)
                ON CONFLICT (portal_id, collection_date)
                DO UPDATE SET
                    items_found = collection_stats.items_found + EXCLUDED.items_found,
                    items_new = collection_stats.items_new + EXCLUDED.items_new,
                    items_duplicate = collection_stats.items_duplicate + EXCLUDED.items_duplicate,
                    processing_time_seconds = collection_stats.processing_time_seconds + EXCLUDED.processing_time_seconds
                """,
                portal_id,
                today,
                items_found,
                items_new,
                items_duplicate,
                processing_time
            )
    
    def calculate_quality_score(self, raw_item: Dict[str, Any]) -> float:
        """데이터 품질 점수 계산 (0.0~10.0)"""
        score = 0.0
        
        # 기본 정보 존재 여부 (40%)
        if raw_item.get('title'):
            score += 2.0
        if raw_item.get('agency'):
            score += 1.5
        if raw_item.get('category'):
            score += 1.0
        if raw_item.get('url'):
            score += 0.5
        
        # 내용 충실도 (40%)
        content_length = len(str(raw_item.get('content', '')))
        if content_length > 100:
            score += 2.0
        elif content_length > 50:
            score += 1.0
        
        if raw_item.get('application_period'):
            score += 1.0
        if raw_item.get('target_audience'):
            score += 1.0
        
        # 구조화 정도 (20%)
        if isinstance(raw_item.get('support_details'), dict):
            score += 1.0
        if raw_item.get('contact_info'):
            score += 1.0
        
        return min(score, 10.0)  # 최대 10점
    
    async def get_recent_collections(
        self,
        portal_id: Optional[str] = None,
        days: int = 7,
        limit: int = 100
    ) -> List[Dict]:
        """최근 수집 데이터 조회"""
        since_date = datetime.now() - timedelta(days=days)
        
        query = """
            SELECT 
                id, portal_id, title, agency, category,
                raw_data, url, quality_score, scraped_at, processing_status
            FROM raw_scraped_data
            WHERE scraped_at >= $1
        """
        params = [since_date]
        
        if portal_id:
            query += " AND portal_id = $2"
            params.append(portal_id)
        
        query += " ORDER BY scraped_at DESC LIMIT ${}".format(len(params) + 1)
        params.append(limit)
        
        async with self.db_pool.acquire() as conn:
            rows = await conn.fetch(query, *params)
        
        return [dict(row) for row in rows]
    
    async def get_collection_statistics(self, portal_id: Optional[str] = None) -> Dict:
        """수집 통계 조회"""
        today = datetime.now().date()
        
        base_query = """
            SELECT 
                portal_id,
                COUNT(*) as total_items,
                COUNT(CASE WHEN DATE(scraped_at) = $1 THEN 1 END) as today_items,
                AVG(quality_score) as avg_quality,
                COUNT(CASE WHEN processing_status = 'duplicate' THEN 1 END) as duplicate_items,
                MIN(scraped_at) as first_scraped,
                MAX(scraped_at) as last_scraped
            FROM raw_scraped_data
            WHERE processing_status != 'failed'
        """
        
        params = [today]
        
        if portal_id:
            base_query += " AND portal_id = $2 GROUP BY portal_id"
            params.append(portal_id)
        else:
            base_query += " GROUP BY portal_id"
        
        async with self.db_pool.acquire() as conn:
            rows = await conn.fetch(base_query, *params)
        
        stats = {}
        total_items = 0
        total_today = 0
        
        for row in rows:
            portal_stats = {
                'total_items': row['total_items'],
                'today_items': row['today_items'],
                'avg_quality': float(row['avg_quality'] or 0),
                'duplicate_items': row['duplicate_items'],
                'first_scraped': row['first_scraped'].isoformat() if row['first_scraped'] else None,
                'last_scraped': row['last_scraped'].isoformat() if row['last_scraped'] else None
            }
            
            stats[row['portal_id']] = portal_stats
            total_items += row['total_items']
            total_today += row['today_items']
        
        return {
            'portals': stats,
            'summary': {
                'total_items': total_items,
                'today_items': total_today,
                'active_portals': len(stats),
                'last_updated': datetime.now().isoformat()
            }
        }


# 유틸리티 함수들

async def create_collection_engine(db_connection_string: str) -> CoreCollectionEngine:
    """수집 엔진 생성 및 초기화"""
    engine = CoreCollectionEngine(db_connection_string)
    await engine.initialize()
    return engine


def extract_text_safely(element, default: str = "") -> str:
    """BeautifulSoup 요소에서 안전하게 텍스트 추출"""
    if element:
        return element.get_text(strip=True) or default
    return default


def clean_korean_text(text: str) -> str:
    """한국어 텍스트 정제"""
    if not text:
        return ""
    
    # 불필요한 공백 제거
    text = ' '.join(text.split())
    
    # 특수문자 정리
    text = text.replace('\xa0', ' ')  # Non-breaking space
    text = text.replace('\u200b', '')  # Zero-width space
    
    return text.strip()