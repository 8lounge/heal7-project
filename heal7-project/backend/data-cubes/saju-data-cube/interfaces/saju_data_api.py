"""
🔮 HEAL7 사주 데이터큐브 - REST API 인터페이스

사주명리학 데이터에 대한 표준화된 접근 인터페이스
다른 큐브나 외부 서비스에서 사주 데이터에 접근할 때 사용
"""

from fastapi import APIRouter, HTTPException, Depends, Query
from typing import List, Optional, Dict, Any
from datetime import datetime, date
from pydantic import BaseModel, Field
import uuid

from ..processors.saju_calculator import SajuCalculator
from ..processors.cache_manager import SajuCacheManager
from ..models.saju_models import (
    SajuChartRequest, SajuChartResponse, 
    CompatibilityRequest, CompatibilityResponse,
    FortuneRequest, FortuneResponse
)

# 라우터 초기화
router = APIRouter(prefix="/api/v1/saju", tags=["saju-data-cube"])

# 의존성 주입
def get_saju_calculator():
    return SajuCalculator()

def get_cache_manager():
    return SajuCacheManager()

# =====================================
# 🔮 사주 차트 관련 API
# =====================================

@router.post("/charts", response_model=SajuChartResponse)
async def create_saju_chart(
    request: SajuChartRequest,
    calculator: SajuCalculator = Depends(get_saju_calculator),
    cache_manager: SajuCacheManager = Depends(get_cache_manager)
):
    """
    새로운 사주 차트 계산 및 생성
    
    Args:
        request: 사주 계산 요청 (출생 정보 포함)
        
    Returns:
        계산된 사주 차트 정보
    """
    try:
        # 캐시 확인
        cache_key = f"chart:{request.user_id}:{request.birth_datetime}"
        cached_chart = await cache_manager.get_chart(cache_key)
        
        if cached_chart:
            return SajuChartResponse(**cached_chart)
        
        # 사주 계산
        chart = await calculator.calculate_saju_chart(
            birth_year=request.birth_year,
            birth_month=request.birth_month,
            birth_day=request.birth_day,
            birth_hour=request.birth_hour,
            birth_minute=request.birth_minute or 0,
            user_id=request.user_id
        )
        
        # 캐시 저장
        await cache_manager.set_chart(cache_key, chart.dict(), ttl=604800)  # 7일
        
        return chart
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"사주 계산 오류: {str(e)}")

@router.get("/charts/{chart_id}", response_model=SajuChartResponse)
async def get_saju_chart(
    chart_id: uuid.UUID,
    cache_manager: SajuCacheManager = Depends(get_cache_manager)
):
    """
    기존 사주 차트 조회
    
    Args:
        chart_id: 사주 차트 ID
        
    Returns:
        사주 차트 정보
    """
    try:
        # 캐시에서 먼저 확인
        cached_chart = await cache_manager.get_chart_by_id(str(chart_id))
        
        if cached_chart:
            return SajuChartResponse(**cached_chart)
        
        # DB에서 조회
        chart = await SajuCalculator.get_chart_from_db(chart_id)
        
        if not chart:
            raise HTTPException(status_code=404, detail="사주 차트를 찾을 수 없습니다")
        
        # 캐시에 저장
        cache_key = f"chart_id:{chart_id}"
        await cache_manager.set_chart(cache_key, chart.dict())
        
        return chart
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"사주 차트 조회 오류: {str(e)}")

@router.get("/users/{user_id}/charts", response_model=List[SajuChartResponse])
async def get_user_charts(
    user_id: uuid.UUID,
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0)
):
    """
    특정 사용자의 모든 사주 차트 조회
    
    Args:
        user_id: 사용자 ID
        limit: 조회할 최대 개수
        offset: 조회 시작 위치
        
    Returns:
        사용자의 사주 차트 목록
    """
    try:
        charts = await SajuCalculator.get_user_charts(
            user_id=user_id,
            limit=limit,
            offset=offset
        )
        
        return charts
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"사용자 사주 차트 조회 오류: {str(e)}")

# =====================================
# ⚖️ 궁합 분석 관련 API
# =====================================

@router.post("/compatibility", response_model=CompatibilityResponse)
async def analyze_compatibility(
    request: CompatibilityRequest,
    calculator: SajuCalculator = Depends(get_saju_calculator),
    cache_manager: SajuCacheManager = Depends(get_cache_manager)
):
    """
    두 사주 간의 궁합 분석
    
    Args:
        request: 궁합 분석 요청 (두 차트 ID 포함)
        
    Returns:
        궁합 분석 결과
    """
    try:
        # 캐시 확인 (작은 ID를 앞에 배치)
        chart1_id, chart2_id = sorted([request.chart1_id, request.chart2_id])
        cache_key = f"compatibility:{chart1_id}:{chart2_id}:{request.analysis_type}"
        
        cached_result = await cache_manager.get_compatibility(cache_key)
        if cached_result:
            return CompatibilityResponse(**cached_result)
        
        # 궁합 분석 수행
        compatibility = await calculator.analyze_compatibility(
            chart1_id=request.chart1_id,
            chart2_id=request.chart2_id,
            analysis_type=request.analysis_type
        )
        
        # 캐시 저장
        await cache_manager.set_compatibility(
            cache_key, 
            compatibility.dict(), 
            ttl=1209600  # 14일
        )
        
        return compatibility
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"궁합 분석 오류: {str(e)}")

@router.get("/compatibility/{compatibility_id}", response_model=CompatibilityResponse)
async def get_compatibility_analysis(
    compatibility_id: uuid.UUID
):
    """
    기존 궁합 분석 결과 조회
    
    Args:
        compatibility_id: 궁합 분석 ID
        
    Returns:
        궁합 분석 결과
    """
    try:
        compatibility = await SajuCalculator.get_compatibility_from_db(compatibility_id)
        
        if not compatibility:
            raise HTTPException(status_code=404, detail="궁합 분석 결과를 찾을 수 없습니다")
        
        return compatibility
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"궁합 분석 조회 오류: {str(e)}")

# =====================================
# 🔮 운세 관련 API
# =====================================

@router.post("/fortune", response_model=FortuneResponse)
async def get_fortune(
    request: FortuneRequest,
    calculator: SajuCalculator = Depends(get_saju_calculator),
    cache_manager: SajuCacheManager = Depends(get_cache_manager)
):
    """
    사주 기반 운세 조회
    
    Args:
        request: 운세 조회 요청 (차트 ID, 날짜, 유형 포함)
        
    Returns:
        운세 정보
    """
    try:
        # 캐시 확인
        cache_key = f"fortune:{request.chart_id}:{request.target_date}:{request.fortune_type}"
        
        cached_fortune = await cache_manager.get_fortune(cache_key)
        if cached_fortune:
            return FortuneResponse(**cached_fortune)
        
        # 운세 계산
        fortune = await calculator.calculate_fortune(
            chart_id=request.chart_id,
            target_date=request.target_date,
            fortune_type=request.fortune_type
        )
        
        # 캐시 저장 (운세는 하루 단위로 캐시)
        ttl = 86400 if request.fortune_type == "daily" else 2592000  # 1일 또는 30일
        await cache_manager.set_fortune(cache_key, fortune.dict(), ttl=ttl)
        
        return fortune
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"운세 조회 오류: {str(e)}")

# =====================================
# 🔧 캐시 관리 API
# =====================================

@router.delete("/cache/{user_id}")
async def clear_user_cache(
    user_id: uuid.UUID,
    cache_manager: SajuCacheManager = Depends(get_cache_manager)
):
    """
    특정 사용자의 사주 관련 캐시 삭제
    
    Args:
        user_id: 사용자 ID
        
    Returns:
        삭제 결과
    """
    try:
        deleted_count = await cache_manager.clear_user_cache(str(user_id))
        
        return {
            "message": f"사용자 {user_id}의 캐시 삭제 완료",
            "deleted_keys": deleted_count
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"캐시 삭제 오류: {str(e)}")

@router.post("/cache/warm")
async def warm_cache(
    popular_charts: List[uuid.UUID],
    cache_manager: SajuCacheManager = Depends(get_cache_manager)
):
    """
    인기 사주 차트들에 대한 캐시 워밍
    
    Args:
        popular_charts: 인기 사주 차트 ID 목록
        
    Returns:
        캐시 워밍 결과
    """
    try:
        warmed_count = await cache_manager.warm_popular_charts(popular_charts)
        
        return {
            "message": "캐시 워밍 완료",
            "warmed_charts": warmed_count
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"캐시 워밍 오류: {str(e)}")

# =====================================
# 📊 통계 및 메트릭 API
# =====================================

@router.get("/metrics/performance")
async def get_performance_metrics():
    """
    사주 데이터큐브 성능 지표 조회
    
    Returns:
        성능 메트릭 정보
    """
    try:
        metrics = await SajuCalculator.get_performance_metrics()
        
        return {
            "calculation_performance": {
                "average_calculation_time": metrics.get("avg_calc_time"),
                "total_calculations_today": metrics.get("calc_count_today"),
                "cache_hit_rate": metrics.get("cache_hit_rate")
            },
            "database_performance": {
                "active_connections": metrics.get("db_connections"),
                "average_query_time": metrics.get("avg_query_time")
            },
            "redis_performance": {
                "memory_usage": metrics.get("redis_memory"),
                "keyspace_hits": metrics.get("redis_hits"),
                "keyspace_misses": metrics.get("redis_misses")
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"메트릭 조회 오류: {str(e)}")

# =====================================
# 🔍 헬스체크 API
# =====================================

@router.get("/health")
async def health_check():
    """
    사주 데이터큐브 상태 확인
    
    Returns:
        큐브 상태 정보
    """
    try:
        # PostgreSQL 연결 확인
        db_status = await SajuCalculator.check_database_health()
        
        # Redis 연결 확인
        cache_status = await SajuCacheManager.check_redis_health()
        
        # KASI API 연결 확인
        kasi_status = await SajuCalculator.check_kasi_api_health()
        
        overall_status = "healthy" if all([
            db_status.get("status") == "healthy",
            cache_status.get("status") == "healthy",
            kasi_status.get("status") == "healthy"
        ]) else "unhealthy"
        
        return {
            "cube_name": "saju-data-cube",
            "version": "2.0.0", 
            "status": overall_status,
            "timestamp": datetime.utcnow().isoformat(),
            "components": {
                "database": db_status,
                "cache": cache_status,
                "external_api": kasi_status
            }
        }
        
    except Exception as e:
        return {
            "cube_name": "saju-data-cube",
            "version": "2.0.0",
            "status": "error",
            "timestamp": datetime.utcnow().isoformat(),
            "error": str(e)
        }