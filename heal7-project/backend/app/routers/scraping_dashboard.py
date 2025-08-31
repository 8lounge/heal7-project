#!/usr/bin/env python3
"""
🔥 실시간 크롤링 대시보드 API
실제 데이터베이스 연동 대시보드 엔드포인트

Author: HEAL7 Development Team
Version: 2.0.0 (실제 DB 연동)
Date: 2025-08-29
"""

import asyncio
import json
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any
import logging

import asyncpg
from fastapi import APIRouter, HTTPException, Query, Depends, BackgroundTasks
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)

# FastAPI 라우터 생성
router = APIRouter(
    prefix="/api/scraping-dashboard",
    tags=["실시간 크롤링 대시보드"],
    responses={404: {"description": "Not found"}},
)

# Pydantic 모델들
class CollectionListResponse(BaseModel):
    success: bool
    data: Dict[str, Any]
    timestamp: str
    message: Optional[str] = None

class StatsResponse(BaseModel):
    success: bool
    data: Dict[str, Any] 
    timestamp: str
    message: Optional[str] = None

class CollectionTriggerRequest(BaseModel):
    portal_ids: List[str] = Field(..., description="수집할 포털 목록 (bizinfo, kstartup)")
    max_pages: int = Field(5, ge=1, le=20, description="최대 페이지 수")
    force_update: bool = Field(False, description="강제 업데이트 여부")

class CollectionTriggerResponse(BaseModel):
    success: bool
    task_id: str
    message: str
    estimated_time: int

# 데이터베이스 연결 설정
class DatabaseManager:
    """실시간 대시보드용 데이터베이스 관리자"""
    
    def __init__(self):
        # PostgreSQL 연결 문자열 (환경 변수에서 가져오거나 기본값 사용)
        self.connection_string = "postgresql://postgres:@localhost:5432/paperworkdb"
        self.connection_pool = None
    
    async def initialize(self):
        """연결 풀 초기화"""
        try:
            self.connection_pool = await asyncpg.create_pool(
                self.connection_string,
                min_size=1,
                max_size=5,
                command_timeout=60
            )
            logger.info("✅ 대시보드 데이터베이스 연결 풀 생성 완료")
        except Exception as e:
            logger.error(f"❌ 데이터베이스 연결 실패: {e}")
            raise
    
    async def get_connection(self):
        """연결 풀에서 연결 가져오기"""
        if not self.connection_pool:
            await self.initialize()
        return self.connection_pool
    
    async def close(self):
        """연결 풀 닫기"""
        if self.connection_pool:
            await self.connection_pool.close()

# 전역 데이터베이스 매니저 
db_manager = DatabaseManager()

async def get_collection_data(
    portal_id: Optional[str] = None,
    limit: int = 20,
    offset: int = 0,
    date_from: Optional[str] = None,
    date_to: Optional[str] = None
) -> Dict[str, Any]:
    """🔥 실제 수집 데이터 조회 (실시간 DB 연동)"""
    
    try:
        # 기본 날짜 설정
        if not date_from:
            date_from = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
        if not date_to:
            date_to = datetime.now().strftime('%Y-%m-%d')
        
        # 데이터베이스 연결
        pool = await db_manager.get_connection()
        
        # WHERE 조건 구성
        where_conditions = ["scraped_at BETWEEN $1 AND $2"]
        params = [f"{date_from} 00:00:00", f"{date_to} 23:59:59"]
        param_count = 2
        
        if portal_id:
            param_count += 1
            where_conditions.append(f"portal_id = ${param_count}")
            params.append(portal_id)
        
        where_clause = " AND ".join(where_conditions)
        
        # 메인 데이터 조회
        query = f"""
            SELECT 
                id,
                portal_id,
                title,
                agency,
                category,
                scraped_at,
                quality_score,
                processing_status as status,
                url,
                raw_data
            FROM raw_scraped_data 
            WHERE {where_clause}
            AND processing_status != 'failed'
            ORDER BY scraped_at DESC
            LIMIT ${param_count + 1} OFFSET ${param_count + 2}
        """
        
        params.extend([limit, offset])
        
        # 총 카운트 조회
        count_query = f"""
            SELECT COUNT(*) as total_count
            FROM raw_scraped_data 
            WHERE {where_clause}
            AND processing_status != 'failed'
        """
        
        async with pool.acquire() as conn:
            # 메인 데이터 조회
            rows = await conn.fetch(query, *params)
            
            # 총 카운트 조회
            count_row = await conn.fetchrow(count_query, *params[:-2])
            total_count = count_row['total_count'] if count_row else 0
            
            # 데이터 변환
            items = []
            for row in rows:
                item = {
                    'id': row['id'],
                    'portal_id': row['portal_id'],
                    'title': row['title'],
                    'agency': row['agency'] or '미분류',
                    'category': row['category'] or '일반',
                    'scraped_at': row['scraped_at'].strftime('%Y-%m-%d %H:%M:%S'),
                    'quality_score': float(row['quality_score'] or 0),
                    'status': row['status'],
                    'url': row['url'] or ''
                }
                
                # 추가 정보가 raw_data에 있으면 포함
                if row['raw_data']:
                    try:
                        raw_data = json.loads(row['raw_data']) if isinstance(row['raw_data'], str) else row['raw_data']
                        item['support_content'] = raw_data.get('support_content', '')[:200] + '...' if raw_data.get('support_content') else ''
                        item['target_audience'] = raw_data.get('target_audience', '')
                    except:
                        pass
                
                items.append(item)
            
            return {
                'items': items,
                'total_count': total_count,
                'filtered_count': len(items),
                'has_more': (offset + limit) < total_count,
                'page_info': {
                    'current_offset': offset,
                    'current_limit': limit,
                    'next_offset': offset + limit if (offset + limit) < total_count else None
                }
            }
            
    except Exception as e:
        logger.error(f"❌ 실제 데이터 조회 실패: {e}")
        # DB 오류 시 빈 데이터 반환
        return {
            'items': [],
            'total_count': 0,
            'filtered_count': 0,
            'has_more': False,
            'error': str(e)
        }

def get_simulation_data(portal_id: Optional[str], limit: int, offset: int) -> Dict[str, Any]:
    """시뮬레이션 데이터 생성"""
    
    programs = [
        '청년창업사관학교', 'K-Global 300 프로그램', '중소기업 기술혁신 지원사업',
        '스마트 제조혁신 추진단', 'AI 기반 스타트업 육성', '글로벌 진출 지원 프로그램',
        '디지털 뉴딜 창업지원', '그린뉴딜 기술개발', '바이오헬스 R&D 지원',
        '지역혁신 창업생태계', '소셜벤처 성장지원', '여성기업 창업지원',
        '시니어 창업 아카데미', '농식품 스타트업 육성', '문화콘텐츠 창업지원'
    ]

    agencies = [
        '중소벤처기업부', '과학기술정보통신부', '산업통상자원부',
        '기업진흥원', '창업진흥원', '연구개발특구진흥재단',
        '정보통신산업진흥원', '농림축산식품부', '문화체육관광부'
    ]

    import random
    
    # 필터링된 포털별 데이터 생성
    filtered_portals = [portal_id] if portal_id else ['bizinfo', 'kstartup']
    
    items = []
    for i in range(limit):
        selected_portal = random.choice(filtered_portals)
        random_program = random.choice(programs)
        random_agency = random.choice(agencies)
        
        # 최근 시간 생성
        hours_ago = random.randint(1, 168)  # 1시간~7일 전
        scraped_time = (datetime.now() - timedelta(hours=hours_ago)).strftime('%Y-%m-%d %H:%M:%S')
        
        items.append({
            'id': offset + i + 1,
            'portal_id': selected_portal,
            'title': f"{random_program} {random.choice([2024, 2025])}년 {random.randint(1, 4)}차",
            'agency': random_agency,
            'category': random.choice(['창업지원', '기술개발', '마케팅지원', 'R&D', 'AI/디지털', '글로벌진출']),
            'scraped_at': scraped_time,
            'quality_score': round(random.uniform(6.5, 9.8), 1),
            'status': random.choice(['completed', 'processing', 'completed', 'completed'])  # completed 확률 높임
        })

    total_count = random.randint(1200, 4800)
    return {
        'items': items,
        'total_count': total_count,
        'filtered_count': len(items),
        'has_more': (offset + limit) < total_count
    }

async def get_stats_data() -> Dict[str, Any]:
    """🔥 실시간 통계 데이터 조회 (실제 DB 연동)"""
    
    try:
        pool = await db_manager.get_connection()
        today = datetime.now().date()
        
        async with pool.acquire() as conn:
            # 포털별 통계 조회
            portal_stats_query = """
                SELECT 
                    portal_id,
                    COUNT(*) as total_count,
                    COUNT(CASE WHEN DATE(scraped_at) = $1 THEN 1 END) as today_count,
                    AVG(quality_score) as avg_quality,
                    COUNT(CASE WHEN processing_status = 'duplicate' THEN 1 END) as duplicate_count,
                    MAX(scraped_at) as last_scraped
                FROM raw_scraped_data 
                WHERE processing_status IN ('completed', 'duplicate', 'processing')
                GROUP BY portal_id
            """
            
            portal_rows = await conn.fetch(portal_stats_query, today)
            
            # 전체 통계 조회  
            overall_stats_query = """
                SELECT 
                    COUNT(*) as total_items,
                    COUNT(CASE WHEN DATE(scraped_at) = $1 THEN 1 END) as today_items,
                    AVG(quality_score) as overall_quality,
                    COUNT(DISTINCT portal_id) as active_portals,
                    pg_size_pretty(pg_total_relation_size('raw_scraped_data')) as table_size
                FROM raw_scraped_data 
                WHERE processing_status IN ('completed', 'duplicate', 'processing')
            """
            
            overall_row = await conn.fetchrow(overall_stats_query, today)
            
            # 최근 7일간 수집 추세
            trend_query = """
                SELECT 
                    DATE(scraped_at) as collection_date,
                    COUNT(*) as daily_count,
                    COUNT(DISTINCT portal_id) as portals_active
                FROM raw_scraped_data 
                WHERE scraped_at >= $1 
                AND processing_status IN ('completed', 'duplicate')
                GROUP BY DATE(scraped_at)
                ORDER BY collection_date DESC
                LIMIT 7
            """
            
            trend_rows = await conn.fetch(trend_query, today - timedelta(days=6))
            
            # 품질별 분포
            quality_query = """
                SELECT 
                    CASE 
                        WHEN quality_score >= 8.0 THEN 'excellent'
                        WHEN quality_score >= 6.0 THEN 'good'
                        WHEN quality_score >= 4.0 THEN 'fair'
                        ELSE 'poor'
                    END as quality_tier,
                    COUNT(*) as count
                FROM raw_scraped_data 
                WHERE processing_status = 'completed'
                GROUP BY quality_tier
            """
            
            quality_rows = await conn.fetch(quality_query)
        
        # 포털별 데이터 정리
        portal_data = {}
        total_items = 0
        total_today = 0
        total_duplicates = 0
        
        for row in portal_rows:
            portal_id = row['portal_id']
            portal_data[portal_id] = {
                'total_count': int(row['total_count']),
                'today_count': int(row['today_count']),
                'avg_quality': round(float(row['avg_quality'] or 0), 1),
                'duplicate_count': int(row['duplicate_count']),
                'last_scraped': row['last_scraped'].strftime('%Y-%m-%d %H:%M:%S') if row['last_scraped'] else None
            }
            
            total_items += int(row['total_count'])
            total_today += int(row['today_count'])
            total_duplicates += int(row['duplicate_count'])
        
        # 성공률 계산
        success_rate = round(((total_items - total_duplicates) / total_items * 100), 1) if total_items > 0 else 0
        
        # 7일 추세 데이터
        trend_data = []
        for row in trend_rows:
            trend_data.append({
                'date': row['collection_date'].strftime('%Y-%m-%d'),
                'count': int(row['daily_count']),
                'active_portals': int(row['portals_active'])
            })
        
        # 품질 분포
        quality_distribution = {}
        for row in quality_rows:
            quality_distribution[row['quality_tier']] = int(row['count'])
        
        return {
            'summary': {
                'total_items': total_items,
                'today_collected': total_today,
                'success_rate': success_rate,
                'active_portals': len(portal_data),
                'duplicate_filtered_today': total_duplicates,
                'overall_quality': round(float(overall_row['overall_quality'] or 0), 1) if overall_row else 0,
                'storage_size': overall_row['table_size'] if overall_row else 'N/A',
                'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            },
            'portals': portal_data,
            'trends': {
                'daily_collection': trend_data,
                'quality_distribution': quality_distribution
            },
            'performance': {
                'avg_quality_threshold': 6.0,
                'collection_efficiency': round((total_today / max(total_items / 30, 1)), 2),  # 일일 평균 대비
                'quality_pass_rate': round((quality_distribution.get('excellent', 0) + quality_distribution.get('good', 0)) / max(sum(quality_distribution.values()), 1) * 100, 1)
            }
        }
        
    except Exception as e:
        logger.error(f"❌ 실시간 통계 조회 실패: {e}")
        # DB 오류 시 기본 구조 반환
        return {
            'summary': {
                'total_items': 0,
                'today_collected': 0,
                'success_rate': 0,
                'active_portals': 0,
                'duplicate_filtered_today': 0,
                'overall_quality': 0,
                'storage_size': 'Error',
                'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            },
            'portals': {},
            'trends': {'daily_collection': [], 'quality_distribution': {}},
            'performance': {'avg_quality_threshold': 6.0, 'collection_efficiency': 0, 'quality_pass_rate': 0},
            'error': str(e)
        }

# API 엔드포인트들

@router.get("/collection-list", response_model=CollectionListResponse)
async def get_collection_list(
    portal_id: Optional[str] = Query(None, description="포털 ID (bizinfo, kstartup)"),
    limit: int = Query(20, ge=1, le=100, description="페이지 크기"),
    offset: int = Query(0, ge=0, description="오프셋"),
    date_from: Optional[str] = Query(None, description="시작 날짜 (YYYY-MM-DD)"),
    date_to: Optional[str] = Query(None, description="종료 날짜 (YYYY-MM-DD)")
):
    """실시간 수집 데이터 리스트 조회"""
    try:
        data = await get_collection_data(
            portal_id=portal_id,
            limit=limit,
            offset=offset,
            date_from=date_from,
            date_to=date_to
        )
        
        return CollectionListResponse(
            success=True,
            data=data,
            timestamp=datetime.now().isoformat()
        )
        
    except Exception as e:
        logger.error(f"Collection list error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/stats", response_model=StatsResponse)
async def get_collection_stats():
    """수집 통계 조회"""
    try:
        data = await get_stats_data()
        
        return StatsResponse(
            success=True,
            data=data,
            timestamp=datetime.now().isoformat()
        )
        
    except Exception as e:
        logger.error(f"Stats error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/health")
async def health_check():
    """헬스 체크"""
    return {
        "status": "healthy",
        "service": "Scraping Dashboard API",
        "timestamp": datetime.now().isoformat()
    }

# 🔥 새로운 실시간 기능들

@router.post("/trigger-collection", response_model=CollectionTriggerResponse)
async def trigger_manual_collection(
    request: CollectionTriggerRequest,
    background_tasks: BackgroundTasks
):
    """🚀 수동 수집 트리거 (백그라운드 실행)"""
    try:
        # 작업 ID 생성
        import uuid
        task_id = str(uuid.uuid4())[:8]
        
        # 예상 시간 계산 (페이지당 약 3초)
        estimated_time = len(request.portal_ids) * request.max_pages * 3
        
        # 백그라운드에서 수집 실행
        background_tasks.add_task(
            run_background_collection,
            task_id,
            request.portal_ids,
            request.max_pages,
            request.force_update
        )
        
        logger.info(f"🚀 수집 작업 시작: {task_id} | 포털: {request.portal_ids} | 페이지: {request.max_pages}")
        
        return CollectionTriggerResponse(
            success=True,
            task_id=task_id,
            message=f"{len(request.portal_ids)}개 포털에서 수집 시작",
            estimated_time=estimated_time
        )
        
    except Exception as e:
        logger.error(f"❌ 수집 트리거 실패: {str(e)}")
        raise HTTPException(status_code=500, detail=f"수집 트리거 실패: {str(e)}")

@router.get("/collection-status/{task_id}")
async def get_collection_status(task_id: str):
    """수집 작업 상태 조회"""
    # 실제로는 Redis나 별도 저장소에서 상태를 확인해야 함
    # 여기서는 기본 구현만
    return {
        "task_id": task_id,
        "status": "running",
        "progress": 45,
        "message": "기업마당 데이터 수집 중...",
        "timestamp": datetime.now().isoformat()
    }

@router.get("/real-time-stats") 
async def get_real_time_stats():
    """⚡ 실시간 통계 (1분마다 갱신되는 핵심 지표)"""
    try:
        pool = await db_manager.get_connection()
        
        async with pool.acquire() as conn:
            # 최근 1시간 수집 현황
            recent_query = """
                SELECT 
                    COUNT(*) as recent_count,
                    COUNT(DISTINCT portal_id) as active_portals,
                    AVG(quality_score) as avg_quality,
                    MAX(scraped_at) as last_activity
                FROM raw_scraped_data
                WHERE scraped_at >= NOW() - INTERVAL '1 hour'
                AND processing_status = 'completed'
            """
            
            recent_row = await conn.fetchrow(recent_query)
            
            # 실시간 처리 상태
            processing_query = """
                SELECT 
                    processing_status,
                    COUNT(*) as count
                FROM raw_scraped_data 
                WHERE scraped_at >= NOW() - INTERVAL '10 minutes'
                GROUP BY processing_status
            """
            
            processing_rows = await conn.fetch(processing_query)
            
        processing_status = {}
        for row in processing_rows:
            processing_status[row['processing_status']] = int(row['count'])
        
        return {
            "real_time": {
                "recent_hour_collected": int(recent_row['recent_count']) if recent_row else 0,
                "active_portals": int(recent_row['active_portals']) if recent_row else 0,
                "current_avg_quality": round(float(recent_row['avg_quality'] or 0), 1) if recent_row else 0,
                "last_activity": recent_row['last_activity'].strftime('%Y-%m-%d %H:%M:%S') if recent_row and recent_row['last_activity'] else None,
                "processing_status": processing_status,
                "system_health": "healthy" if processing_status.get('completed', 0) > 0 else "idle"
            },
            "timestamp": datetime.now().isoformat(),
            "refresh_interval": 60  # 60초마다 갱신 권장
        }
        
    except Exception as e:
        logger.error(f"❌ 실시간 통계 조회 실패: {str(e)}")
        return {
            "real_time": {
                "recent_hour_collected": 0,
                "active_portals": 0,
                "current_avg_quality": 0,
                "last_activity": None,
                "processing_status": {},
                "system_health": "error"
            },
            "timestamp": datetime.now().isoformat(),
            "error": str(e)
        }

@router.get("/portal-comparison")
async def get_portal_comparison(days: int = Query(7, ge=1, le=30)):
    """📊 포털간 수집 성과 비교 분석"""
    try:
        pool = await db_manager.get_connection()
        since_date = datetime.now() - timedelta(days=days)
        
        async with pool.acquire() as conn:
            comparison_query = """
                SELECT 
                    portal_id,
                    COUNT(*) as total_collected,
                    COUNT(CASE WHEN processing_status = 'completed' THEN 1 END) as successful,
                    COUNT(CASE WHEN processing_status = 'duplicate' THEN 1 END) as duplicates,
                    AVG(quality_score) as avg_quality,
                    MIN(scraped_at) as first_collection,
                    MAX(scraped_at) as latest_collection,
                    COUNT(DISTINCT DATE(scraped_at)) as active_days
                FROM raw_scraped_data 
                WHERE scraped_at >= $1
                GROUP BY portal_id
                ORDER BY total_collected DESC
            """
            
            rows = await conn.fetch(comparison_query, since_date)
        
        comparisons = []
        for row in rows:
            success_rate = round((int(row['successful']) / max(int(row['total_collected']), 1)) * 100, 1)
            daily_avg = round(int(row['total_collected']) / max(int(row['active_days']), 1), 1)
            
            comparisons.append({
                'portal_id': row['portal_id'],
                'total_collected': int(row['total_collected']),
                'successful': int(row['successful']),
                'duplicates': int(row['duplicates']),
                'success_rate': success_rate,
                'avg_quality': round(float(row['avg_quality'] or 0), 1),
                'daily_average': daily_avg,
                'active_days': int(row['active_days']),
                'consistency': round((int(row['active_days']) / days) * 100, 1),
                'latest_collection': row['latest_collection'].strftime('%Y-%m-%d %H:%M:%S') if row['latest_collection'] else None
            })
        
        return {
            'comparison_period': f"{days} days",
            'portals': comparisons,
            'summary': {
                'best_performer': comparisons[0]['portal_id'] if comparisons else None,
                'total_portals': len(comparisons),
                'average_success_rate': round(sum(p['success_rate'] for p in comparisons) / max(len(comparisons), 1), 1),
                'average_quality': round(sum(p['avg_quality'] for p in comparisons) / max(len(comparisons), 1), 1)
            }
        }
        
    except Exception as e:
        logger.error(f"❌ 포털 비교 분석 실패: {str(e)}")
        raise HTTPException(status_code=500, detail=f"포털 비교 분석 실패: {str(e)}")

async def run_background_collection(
    task_id: str,
    portal_ids: List[str], 
    max_pages: int,
    force_update: bool
):
    """백그라운드 수집 실행"""
    try:
        logger.info(f"🔄 백그라운드 수집 시작: {task_id}")
        
        # 실제 수집기 import 및 실행
        from bizinfo_collector import run_comprehensive_collection
        
        # 데이터베이스 연결 문자열 
        db_conn = "postgresql://postgres:@localhost:5432/paperworkdb"
        
        # 수집 실행
        results = await run_comprehensive_collection(
            db_connection_string=db_conn,
            portals=portal_ids,
            max_pages=max_pages
        )
        
        # 결과 로깅
        total_new = sum(r.new_items for r in results)
        total_time = sum(r.processing_time for r in results)
        
        logger.info(f"✅ 백그라운드 수집 완료: {task_id} | 신규 {total_new}개 | {total_time:.1f}초")
        
        # 실제로는 결과를 Redis나 별도 저장소에 저장해야 함
        
    except Exception as e:
        logger.error(f"❌ 백그라운드 수집 실패: {task_id} - {str(e)}")

# 이전 PHP 호환성을 위한 엔드포인트 (기존 프론트엔드와 호환)
@router.get("")
async def legacy_endpoint(action: str = Query(..., description="액션 타입")):
    """기존 PHP API와 호환되는 엔드포인트"""
    if action == "collection_list":
        return await get_collection_list()
    elif action == "stats":
        return await get_collection_stats()
    else:
        raise HTTPException(status_code=400, detail=f"Invalid action: {action}")