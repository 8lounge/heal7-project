"""
HEAL7 꿈풀이/해몽 API 엔드포인트 - SQLAlchemy 2.0 현대화 버전
최신 SQLAlchemy 2.0 패턴과 모범 사례 적용

@author HEAL7 Team  
@version 2.0.0
@updated 2025-08-31
"""

from fastapi import APIRouter, HTTPException, Depends, Query, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from sqlalchemy import text, select, func, and_, or_, desc, update
from typing import List, Optional, Dict, Any, Union
from pydantic import BaseModel, Field
import asyncio
from datetime import datetime, date

# Import our modern database utilities
from ....shared.database_utils import get_db, get_async_db, with_async_db_session
from ....shared.database_models_v2 import (
    DreamInterpretation, DreamCategory, DreamSearchStats, UserDream,
    Base
)

# Router 설정
router = APIRouter(prefix="/api/v2/dream-interpretation", tags=["dream-interpretation-v2"])

# ====================================
# 🌙 Enhanced Pydantic Models
# ====================================

class DreamKeywordSearchRequest(BaseModel):
    """꿈 키워드 검색 요청 - 향상된 버전"""
    keywords: List[str] = Field(..., min_items=1, max_items=10, description="검색할 꿈 키워드들")
    search_mode: str = Field("any", regex="^(any|all|fuzzy)$", description="검색 모드")
    category_filters: Optional[List[str]] = Field(None, description="카테고리 필터")
    fortune_filter: Optional[str] = Field(None, regex="^(positive|negative|neutral)$")
    confidence_threshold: Optional[float] = Field(0.0, ge=0.0, le=1.0, description="최소 신뢰도")
    include_variants: bool = Field(True, description="키워드 변형 포함 여부")
    limit: int = Field(20, ge=1, le=100, description="최대 결과 수")

class DreamInterpretationResponse(BaseModel):
    """꿈풀이 응답 - 완전한 정보 포함"""
    id: int
    keyword: str
    emoji: Optional[str] = None
    category_name: Optional[str]
    traditional_meaning: str
    modern_meaning: str
    psychological_meaning: Optional[str]
    fortune_aspect: str
    confidence_score: float
    accuracy_rating: Optional[float]
    related_keywords: List[str] = []
    lucky_numbers: List[int] = []
    search_frequency: int = 0
    user_rating_avg: Optional[float] = None
    data_source: Optional[str] = None
    source_quality: str = "unknown"
    verified: bool = False
    match_score: Optional[float] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

class SearchStatisticsResponse(BaseModel):
    """검색 통계 응답"""
    total_results: int
    processing_time_ms: float
    search_terms: List[str]
    filters_applied: Dict[str, Any]
    recommended_keywords: List[str] = []

class ComprehensiveSearchResponse(BaseModel):
    """종합 검색 응답"""
    results: List[DreamInterpretationResponse]
    statistics: SearchStatisticsResponse
    suggestions: Optional[List[str]] = None

# ====================================
# 🚀 Modern Query Service Class
# ====================================

class DreamQueryServiceV2:
    """SQLAlchemy 2.0 기반 현대적 쿼리 서비스"""
    
    @staticmethod
    async def search_dreams_comprehensive(
        request: DreamKeywordSearchRequest,
        session: AsyncSession
    ) -> ComprehensiveSearchResponse:
        """종합 꿈풀이 검색 - SQLAlchemy 2.0 스타일"""
        import time
        start_time = time.time()
        
        # Base query using modern select() syntax
        base_query = (
            select(
                DreamInterpretation.id,
                DreamInterpretation.keyword,
                DreamInterpretation.emoji,
                DreamInterpretation.traditional_meaning,
                DreamInterpretation.modern_meaning,
                DreamInterpretation.psychological_meaning,
                DreamInterpretation.fortune_aspect,
                DreamInterpretation.confidence_score,
                DreamInterpretation.accuracy_rating,
                DreamInterpretation.related_keywords,
                DreamInterpretation.lucky_numbers,
                DreamInterpretation.search_frequency,
                DreamInterpretation.user_rating_avg,
                DreamInterpretation.data_source,
                DreamInterpretation.source_quality,
                DreamInterpretation.verified,
                DreamInterpretation.created_at,
                DreamInterpretation.updated_at,
                DreamCategory.korean_name.label('category_name')
            )
            .outerjoin(DreamCategory, DreamInterpretation.category_id == DreamCategory.id)
        )
        
        # Build dynamic WHERE conditions
        conditions = []
        
        # Keyword search conditions
        if request.search_mode == "all":
            # All keywords must match
            for keyword in request.keywords:
                keyword_condition = or_(
                    DreamInterpretation.keyword.ilike(f"%{keyword}%"),
                    DreamInterpretation.keyword_variants.any(keyword),
                    func.to_tsvector('korean', DreamInterpretation.traditional_meaning + ' ' + 
                                     DreamInterpretation.modern_meaning).op('@@')(
                        func.plainto_tsquery('korean', keyword)
                    )
                )
                conditions.append(keyword_condition)
        
        elif request.search_mode == "fuzzy":
            # Fuzzy matching using similarity
            fuzzy_conditions = []
            for keyword in request.keywords:
                fuzzy_conditions.append(
                    func.similarity(DreamInterpretation.keyword, keyword) > 0.3
                )
            conditions.append(or_(*fuzzy_conditions))
        
        else:  # "any" mode (default)
            keyword_conditions = []
            for keyword in request.keywords:
                keyword_conditions.append(
                    or_(
                        DreamInterpretation.keyword.ilike(f"%{keyword}%"),
                        DreamInterpretation.keyword_variants.any(keyword) if request.include_variants else False
                    )
                )
            conditions.append(or_(*keyword_conditions))
        
        # Category filter
        if request.category_filters:
            conditions.append(DreamCategory.category_code.in_(request.category_filters))
        
        # Fortune filter
        if request.fortune_filter:
            conditions.append(DreamInterpretation.fortune_aspect == request.fortune_filter)
        
        # Confidence threshold
        if request.confidence_threshold > 0.0:
            conditions.append(DreamInterpretation.confidence_score >= request.confidence_threshold)
        
        # Apply all conditions
        if conditions:
            base_query = base_query.where(and_(*conditions))
        
        # Ordering and limiting
        final_query = (
            base_query
            .order_by(
                desc(DreamInterpretation.confidence_score),
                desc(DreamInterpretation.search_frequency),
                desc(DreamInterpretation.accuracy_rating)
            )
            .limit(request.limit)
        )
        
        # Execute query
        result = await session.execute(final_query)
        dream_rows = result.fetchall()
        
        # Convert to response models
        dreams = []
        for row in dream_rows:
            dream = DreamInterpretationResponse(
                id=row.id,
                keyword=row.keyword,
                emoji=row.emoji,
                category_name=row.category_name,
                traditional_meaning=row.traditional_meaning,
                modern_meaning=row.modern_meaning,
                psychological_meaning=row.psychological_meaning,
                fortune_aspect=row.fortune_aspect,
                confidence_score=row.confidence_score,
                accuracy_rating=row.accuracy_rating,
                related_keywords=row.related_keywords or [],
                lucky_numbers=row.lucky_numbers or [],
                search_frequency=row.search_frequency,
                user_rating_avg=row.user_rating_avg,
                data_source=row.data_source,
                source_quality=row.source_quality,
                verified=row.verified,
                created_at=row.created_at,
                updated_at=row.updated_at
            )
            dreams.append(dream)
        
        # Calculate processing time
        processing_time = (time.time() - start_time) * 1000
        
        # Generate statistics
        statistics = SearchStatisticsResponse(
            total_results=len(dreams),
            processing_time_ms=round(processing_time, 2),
            search_terms=request.keywords,
            filters_applied={
                "search_mode": request.search_mode,
                "category_filters": request.category_filters,
                "fortune_filter": request.fortune_filter,
                "confidence_threshold": request.confidence_threshold
            }
        )
        
        return ComprehensiveSearchResponse(
            results=dreams,
            statistics=statistics
        )
    
    @staticmethod
    async def get_dream_by_id(dream_id: int, session: AsyncSession) -> Optional[DreamInterpretationResponse]:
        """ID로 특정 꿈풀이 조회 - SQLAlchemy 2.0"""
        query = (
            select(
                DreamInterpretation.id,
                DreamInterpretation.keyword,
                DreamInterpretation.emoji,
                DreamInterpretation.traditional_meaning,
                DreamInterpretation.modern_meaning,
                DreamInterpretation.psychological_meaning,
                DreamInterpretation.fortune_aspect,
                DreamInterpretation.confidence_score,
                DreamInterpretation.accuracy_rating,
                DreamInterpretation.related_keywords,
                DreamInterpretation.lucky_numbers,
                DreamInterpretation.search_frequency,
                DreamInterpretation.user_rating_avg,
                DreamInterpretation.data_source,
                DreamInterpretation.source_quality,
                DreamInterpretation.verified,
                DreamInterpretation.created_at,
                DreamInterpretation.updated_at,
                DreamCategory.korean_name.label('category_name')
            )
            .outerjoin(DreamCategory)
            .where(DreamInterpretation.id == dream_id)
        )
        
        result = await session.execute(query)
        row = result.first()
        
        if not row:
            return None
        
        return DreamInterpretationResponse(
            id=row.id,
            keyword=row.keyword,
            emoji=row.emoji,
            category_name=row.category_name,
            traditional_meaning=row.traditional_meaning,
            modern_meaning=row.modern_meaning,
            psychological_meaning=row.psychological_meaning,
            fortune_aspect=row.fortune_aspect,
            confidence_score=row.confidence_score,
            accuracy_rating=row.accuracy_rating,
            related_keywords=row.related_keywords or [],
            lucky_numbers=row.lucky_numbers or [],
            search_frequency=row.search_frequency,
            user_rating_avg=row.user_rating_avg,
            data_source=row.data_source,
            source_quality=row.source_quality,
            verified=row.verified,
            created_at=row.created_at,
            updated_at=row.updated_at
        )
    
    @staticmethod
    async def update_search_statistics(keywords: List[str], session: AsyncSession):
        """검색 통계 업데이트 - Modern upsert pattern"""
        for keyword in keywords:
            # Modern ON CONFLICT DO UPDATE pattern
            upsert_query = text("""
                INSERT INTO dream_service.dream_search_stats 
                (keyword, search_count, daily_searches, last_searched_at)
                VALUES (:keyword, 1, 1, CURRENT_TIMESTAMP)
                ON CONFLICT (keyword) DO UPDATE SET
                    search_count = dream_search_stats.search_count + 1,
                    daily_searches = CASE 
                        WHEN DATE(dream_search_stats.last_searched_at) = CURRENT_DATE 
                        THEN dream_search_stats.daily_searches + 1 
                        ELSE 1 
                    END,
                    last_searched_at = CURRENT_TIMESTAMP,
                    trend_score = LEAST(dream_search_stats.trend_score + 0.1, 1.0)
            """)
            
            await session.execute(upsert_query, {"keyword": keyword})

# ====================================
# 🌙 Modern API Endpoints
# ====================================

@router.post("/search", response_model=ComprehensiveSearchResponse)
async def search_dreams_v2(
    search_request: DreamKeywordSearchRequest,
    background_tasks: BackgroundTasks,
    session: AsyncSession = Depends(get_async_db)
):
    """
    꿈풀이 종합 검색 - SQLAlchemy 2.0 현대화 버전
    - 향상된 검색 알고리즘
    - 실시간 통계
    - 성능 최적화
    """
    try:
        # Execute comprehensive search
        search_result = await DreamQueryServiceV2.search_dreams_comprehensive(
            search_request, session
        )
        
        # Update search statistics in background
        background_tasks.add_task(
            DreamQueryServiceV2.update_search_statistics,
            search_request.keywords,
            session
        )
        
        return search_result
        
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"꿈풀이 검색 중 오류 발생: {str(e)}"
        )

@router.get("/dream/{dream_id}", response_model=DreamInterpretationResponse)
async def get_dream_interpretation_v2(
    dream_id: int,
    session: AsyncSession = Depends(get_async_db)
):
    """
    특정 꿈풀이 상세 조회 - SQLAlchemy 2.0
    """
    try:
        dream = await DreamQueryServiceV2.get_dream_by_id(dream_id, session)
        
        if not dream:
            raise HTTPException(status_code=404, detail="꿈풀이를 찾을 수 없습니다")
        
        return dream
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"꿈풀이 조회 중 오류 발생: {str(e)}"
        )

@router.get("/categories", response_model=List[Dict[str, Any]])
async def get_dream_categories_v2(
    include_counts: bool = Query(True, description="꿈 개수 포함 여부"),
    session: AsyncSession = Depends(get_async_db)
):
    """
    꿈 카테고리 목록 조회 - SQLAlchemy 2.0 스타일
    """
    try:
        if include_counts:
            query = (
                select(
                    DreamCategory.id,
                    DreamCategory.category_code,
                    DreamCategory.korean_name,
                    DreamCategory.english_name,
                    DreamCategory.emoji,
                    DreamCategory.description,
                    func.count(DreamInterpretation.id).label('dream_count')
                )
                .outerjoin(DreamInterpretation)
                .where(DreamCategory.is_active == True)
                .group_by(DreamCategory.id)
                .order_by(DreamCategory.sort_order, DreamCategory.korean_name)
            )
        else:
            query = (
                select(DreamCategory)
                .where(DreamCategory.is_active == True)
                .order_by(DreamCategory.sort_order, DreamCategory.korean_name)
            )
        
        result = await session.execute(query)
        categories = result.fetchall()
        
        return [
            {
                "id": cat.id,
                "category_code": cat.category_code,
                "korean_name": cat.korean_name,
                "english_name": cat.english_name,
                "emoji": cat.emoji,
                "description": cat.description,
                "dream_count": getattr(cat, 'dream_count', 0) if include_counts else None
            }
            for cat in categories
        ]
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"카테고리 조회 중 오류 발생: {str(e)}"
        )

@router.get("/trending", response_model=List[Dict[str, Any]])
async def get_trending_dreams_v2(
    period_hours: int = Query(24, ge=1, le=168, description="분석 기간 (시간)"),
    limit: int = Query(20, ge=1, le=50),
    session: AsyncSession = Depends(get_async_db)
):
    """
    트렌딩 꿈풀이 키워드 - SQLAlchemy 2.0 집계 쿼리
    """
    try:
        # Modern window function query
        trending_query = text("""
            SELECT 
                dss.keyword,
                dss.search_count,
                dss.daily_searches,
                dss.trend_score,
                di.emoji,
                dc.korean_name as category_name,
                SUBSTRING(di.modern_meaning, 1, 100) as brief_meaning,
                RANK() OVER (ORDER BY dss.trend_score DESC, dss.search_count DESC) as trend_rank
            FROM dream_service.dream_search_stats dss
            LEFT JOIN dream_service.dream_interpretations di ON dss.keyword = di.keyword
            LEFT JOIN dream_service.dream_categories dc ON di.category_id = dc.id
            WHERE dss.last_searched_at >= NOW() - INTERVAL :period_hours
            ORDER BY dss.trend_score DESC, dss.search_count DESC
            LIMIT :limit
        """)
        
        result = await session.execute(
            trending_query, 
            {"period_hours": f"{period_hours} hours", "limit": limit}
        )
        
        trending = result.fetchall()
        
        return [
            {
                "keyword": item.keyword,
                "search_count": item.search_count,
                "daily_searches": item.daily_searches,
                "trend_score": float(item.trend_score),
                "trend_rank": item.trend_rank,
                "emoji": item.emoji,
                "category_name": item.category_name,
                "brief_meaning": item.brief_meaning or "해석을 확인해보세요"
            }
            for item in trending
        ]
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"트렌딩 분석 중 오류 발생: {str(e)}"
        )

@router.get("/health", response_model=Dict[str, Any])
async def health_check_v2(session: AsyncSession = Depends(get_async_db)):
    """
    꿈풀이 서비스 헬스 체크 - SQLAlchemy 2.0
    """
    try:
        # Database connectivity check
        db_check = await session.execute(text("SELECT 1"))
        db_ok = db_check.scalar() == 1
        
        # Count total dreams
        count_query = select(func.count(DreamInterpretation.id))
        total_dreams_result = await session.execute(count_query)
        total_dreams = total_dreams_result.scalar()
        
        # Average confidence score
        avg_confidence_query = select(func.avg(DreamInterpretation.confidence_score))
        avg_confidence_result = await session.execute(avg_confidence_query)
        avg_confidence = avg_confidence_result.scalar()
        
        return {
            "service": "dream-interpretation-v2",
            "status": "healthy" if db_ok else "unhealthy",
            "database_connected": db_ok,
            "total_dreams": total_dreams,
            "average_confidence": round(float(avg_confidence or 0), 3),
            "sqlalchemy_version": "2.0.43",
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        return {
            "service": "dream-interpretation-v2",
            "status": "unhealthy",
            "error": str(e),
            "timestamp": datetime.utcnow().isoformat()
        }

# ====================================
# 🎯 Background Tasks & Utilities
# ====================================

@with_async_db_session
async def cleanup_old_search_stats(session: AsyncSession, days_old: int = 30):
    """오래된 검색 통계 정리"""
    cleanup_query = text("""
        DELETE FROM dream_service.dream_search_stats 
        WHERE last_searched_at < NOW() - INTERVAL :days_old
        AND search_count < 5
    """)
    
    result = await session.execute(cleanup_query, {"days_old": f"{days_old} days"})
    return result.rowcount

@router.post("/admin/cleanup-stats")
async def admin_cleanup_stats(
    days_old: int = Query(30, description="정리할 통계 데이터 기간(일)"),
    session: AsyncSession = Depends(get_async_db)
):
    """관리자: 오래된 검색 통계 정리"""
    try:
        cleaned_count = await cleanup_old_search_stats(session, days_old)
        return {
            "message": f"{cleaned_count}개의 오래된 검색 통계가 정리되었습니다",
            "cleaned_records": cleaned_count,
            "days_threshold": days_old
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"통계 정리 중 오류 발생: {str(e)}"
        )