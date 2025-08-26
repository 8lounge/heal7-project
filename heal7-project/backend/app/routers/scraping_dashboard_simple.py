#!/usr/bin/env python3
"""
정부포털 수집 대시보드 FastAPI 라우터 (간소화 버전)
실시간 수집 데이터 API 엔드포인트
"""

import random
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any
import logging

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel

logger = logging.getLogger(__name__)

# FastAPI 라우터 생성
router = APIRouter(
    prefix="/api/scraping-dashboard",
    tags=["scraping-dashboard"],
)

# Pydantic 모델들
class CollectionListResponse(BaseModel):
    success: bool
    data: Dict[str, Any]
    timestamp: str

class StatsResponse(BaseModel):
    success: bool
    data: Dict[str, Any]
    timestamp: str

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

def get_stats_data() -> Dict[str, Any]:
    """통계 데이터 생성"""
    return {
        'total_storage_mb': 29.1,
        'kstartup_count': random.randint(1200, 1300),
        'bizinfo_count': random.randint(3800, 4000),
        'today_collected': random.randint(80, 150),
        'success_rate': round(random.uniform(95.0, 99.0), 1),
        'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'duplicate_filtered_today': random.randint(15, 35),
        'processing_speed_avg': f"{round(random.uniform(1.2, 1.8), 1)} items/min"
    }

# API 엔드포인트들

@router.get("/collection-list")
async def get_collection_list(
    portal_id: Optional[str] = Query(None, description="포털 ID (bizinfo, kstartup)"),
    limit: int = Query(20, ge=1, le=100, description="페이지 크기"),
    offset: int = Query(0, ge=0, description="오프셋"),
    date_from: Optional[str] = Query(None, description="시작 날짜 (YYYY-MM-DD)"),
    date_to: Optional[str] = Query(None, description="종료 날짜 (YYYY-MM-DD)")
):
    """실시간 수집 데이터 리스트 조회"""
    try:
        data = get_simulation_data(portal_id, limit, offset)
        
        return {
            "success": True,
            "data": data,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Collection list error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/stats")
async def get_collection_stats():
    """수집 통계 조회"""
    try:
        data = get_stats_data()
        
        return {
            "success": True,
            "data": data,
            "timestamp": datetime.now().isoformat()
        }
        
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

# 기존 PHP API 호환성을 위한 엔드포인트
@router.get("")
async def legacy_endpoint(
    action: str = Query(..., description="액션 타입"),
    portal_id: Optional[str] = Query(None),
    limit: int = Query(20),
    offset: int = Query(0)
):
    """기존 PHP API와 호환되는 엔드포인트"""
    if action == "collection_list":
        return await get_collection_list(portal_id=portal_id, limit=limit, offset=offset)
    elif action == "stats":
        return await get_collection_stats()
    else:
        raise HTTPException(status_code=400, detail=f"Invalid action: {action}")