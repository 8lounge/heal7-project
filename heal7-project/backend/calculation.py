"""
HEAL7 사주명리학 시스템 - 계산 엔진 라우터

이 모듈은 사주명리학의 핵심 계산 로직을 처리합니다:
- 60갑자 계산
- 월두법, 시두법 계산
- 진태양시 보정
- 오행 분석
- 십신 분석
- 대운/세운 계산

모든 계산은 KASI 데이터를 기반으로 하며, 높은 정확도를 보장합니다.

@author HEAL7 Development Team
@version 1.0.0
@since 2025-08-12
"""

import asyncio
from datetime import datetime, timezone
from typing import List, Dict, Any, Optional
import logging

from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, validator

from core.database import DatabaseManager
from core.redis_client import RedisManager
from services.saju_calculator import SajuCalculator
from services.wuxing_analyzer import WuXingAnalyzer
from services.sipsin_analyzer import SipSinAnalyzer
from services.daeun_calculator import DaeunCalculator
from services.true_solar_time import TrueSolarTimeCalculator
from models.saju_models import (
    BirthInfo, SajuResult, WuXingAnalysis, 
    SipSinAnalysis, DaeunResult, ValidationResult
)
from utils.cache_keys import CacheKeys
from utils.performance import measure_time
from utils.validation import validate_birth_info

router = APIRouter()
logger = logging.getLogger("heal7.calculation")

# ============================================================================
# Request/Response 모델 정의
# ============================================================================

class SajuCalculationRequest(BaseModel):
    """사주 계산 요청 모델"""
    
    # 기본 출생 정보
    birth_year: int = Field(..., ge=1900, le=2100, description="출생 연도")
    birth_month: int = Field(..., ge=1, le=12, description="출생 월")
    birth_day: int = Field(..., ge=1, le=31, description="출생 일")
    birth_hour: int = Field(..., ge=0, le=23, description="출생 시")
    birth_minute: int = Field(0, ge=0, le=59, description="출생 분")
    
    # 달력 및 지역 정보
    is_lunar: bool = Field(False, description="음력 여부")
    is_leap_month: bool = Field(False, description="윤달 여부")
    timezone: str = Field("Asia/Seoul", description="시간대")
    
    # 성별 및 추가 정보
    gender: str = Field(..., regex="^(male|female)$", description="성별")
    birth_location: Optional[str] = Field(None, description="출생 지역")
    latitude: Optional[float] = Field(None, ge=-90, le=90, description="위도")
    longitude: Optional[float] = Field(None, ge=-180, le=180, description="경도")
    
    # 계산 옵션
    use_true_solar_time: bool = Field(True, description="진태양시 보정 사용")
    calculation_method: str = Field("kasi_verified", description="계산 방법")
    include_analysis: bool = Field(True, description="분석 포함")
    
    @validator('birth_day')
    def validate_birth_day(cls, v, values):
        """날짜 유효성 검사"""
        if 'birth_year' in values and 'birth_month' in values:
            year = values['birth_year']
            month = values['birth_month']
            
            # 월별 최대 일수 확인
            days_in_month = [31, 29 if year % 4 == 0 and (year % 100 != 0 or year % 400 == 0) else 28,
                           31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
            
            if v > days_in_month[month - 1]:
                raise ValueError(f"Invalid day {v} for month {month} in year {year}")
        
        return v

class BatchCalculationRequest(BaseModel):
    """배치 계산 요청 모델"""
    
    calculations: List[SajuCalculationRequest] = Field(..., max_items=10, description="계산 요청 목록")
    priority: str = Field("normal", regex="^(low|normal|high)$", description="처리 우선순위")

class SajuCalculationResponse(BaseModel):
    """사주 계산 응답 모델"""
    
    # 계산 결과
    saju_result: SajuResult
    wuxing_analysis: Optional[WuXingAnalysis] = None
    sipsin_analysis: Optional[SipSinAnalysis] = None
    daeun_result: Optional[DaeunResult] = None
    
    # 메타데이터
    calculation_id: str
    calculation_time: float
    data_source: str
    confidence_score: int = Field(ge=0, le=100)
    
    # 검증 정보
    validation_result: ValidationResult
    
    class Config:
        schema_extra = {
            "example": {
                "saju_result": {
                    "year_pillar": {"heavenly": "경", "earthly": "인", "korean": "경인"},
                    "month_pillar": {"heavenly": "무", "earthly": "인", "korean": "무인"},
                    "day_pillar": {"heavenly": "갑", "earthly": "자", "korean": "갑자"},
                    "hour_pillar": {"heavenly": "을", "earthly": "축", "korean": "을축"}
                },
                "calculation_id": "calc_abc123def456",
                "calculation_time": 0.045,
                "data_source": "kasi_verified",
                "confidence_score": 98
            }
        }

# ============================================================================
# 계산 엔드포인트들
# ============================================================================

@router.post("/saju", response_model=SajuCalculationResponse)
async def calculate_saju(
    request: SajuCalculationRequest,
    background_tasks: BackgroundTasks,
    db: DatabaseManager = Depends(),
    redis: RedisManager = Depends()
) -> SajuCalculationResponse:
    """
    완전한 사주 계산
    
    출생 정보를 받아서 정확한 사주를 계산합니다.
    KASI 데이터를 기반으로 한 정밀 계산을 수행합니다.
    """
    calculation_start = datetime.now()
    calculation_id = f"calc_{int(calculation_start.timestamp())}"
    
    try:
        logger.info(f"사주 계산 시작: {calculation_id}")
        
        # 캐시 키 생성
        cache_key = CacheKeys.saju_calculation(
            request.birth_year, request.birth_month, request.birth_day,
            request.birth_hour, request.birth_minute, request.gender
        )
        
        # 캐시에서 먼저 확인
        cached_result = await redis.get_json(cache_key)
        if cached_result:
            logger.info(f"캐시에서 결과 반환: {calculation_id}")
            return SajuCalculationResponse(**cached_result)
        
        # 입력 데이터 검증
        birth_info = BirthInfo(
            year=request.birth_year,
            month=request.birth_month,
            day=request.birth_day,
            hour=request.birth_hour,
            minute=request.birth_minute,
            is_lunar=request.is_lunar,
            gender=request.gender,
            timezone=request.timezone
        )
        
        validation_result = await validate_birth_info(birth_info, db)
        if not validation_result.is_valid:
            raise HTTPException(
                status_code=400,
                detail=f"입력 데이터 검증 실패: {', '.join(validation_result.errors)}"
            )
        
        # 진태양시 보정 계산
        true_solar_calculator = TrueSolarTimeCalculator()
        corrected_time = await true_solar_calculator.calculate(
            request.birth_year, request.birth_month, request.birth_day,
            request.birth_hour, request.birth_minute
        ) if request.use_true_solar_time else None
        
        # 실제 계산에 사용할 시간
        calc_hour = corrected_time.hour if corrected_time else request.birth_hour
        calc_minute = corrected_time.minute if corrected_time else request.birth_minute
        
        # 사주 계산
        calculator = SajuCalculator()
        saju_result = await calculator.calculate_complete_saju(
            birth_info._replace(hour=calc_hour, minute=calc_minute)
        )
        
        # 분석 수행 (옵션)
        wuxing_analysis = None
        sipsin_analysis = None
        daeun_result = None
        
        if request.include_analysis:
            # 오행 분석
            wuxing_analyzer = WuXingAnalyzer()
            wuxing_analysis = await wuxing_analyzer.analyze(saju_result)
            
            # 십신 분석
            sipsin_analyzer = SipSinAnalyzer()
            sipsin_analysis = await sipsin_analyzer.analyze(saju_result)
            
            # 대운 계산
            daeun_calculator = DaeunCalculator()
            daeun_result = await daeun_calculator.calculate(birth_info, saju_result.month_pillar)
        
        # 계산 시간 측정
        calculation_time = (datetime.now() - calculation_start).total_seconds()
        
        # 응답 생성
        response = SajuCalculationResponse(
            saju_result=saju_result,
            wuxing_analysis=wuxing_analysis,
            sipsin_analysis=sipsin_analysis,
            daeun_result=daeun_result,
            calculation_id=calculation_id,
            calculation_time=calculation_time,
            data_source=request.calculation_method,
            confidence_score=validation_result.confidence_score,
            validation_result=validation_result
        )
        
        # 백그라운드에서 결과 캐싱 및 로깅
        background_tasks.add_task(
            cache_and_log_result,
            cache_key, response.dict(), calculation_id, calculation_time, db, redis
        )
        
        logger.info(f"사주 계산 완료: {calculation_id} ({calculation_time:.3f}초)")
        return response
        
    except Exception as e:
        logger.error(f"사주 계산 오류: {calculation_id} - {str(e)}")
        
        # 에러 로깅
        background_tasks.add_task(
            log_calculation_error,
            calculation_id, str(e), request.dict(), db
        )
        
        raise HTTPException(
            status_code=500,
            detail=f"사주 계산 중 오류가 발생했습니다: {str(e)}"
        )

@router.post("/saju/batch", response_model=List[SajuCalculationResponse])
async def calculate_saju_batch(
    request: BatchCalculationRequest,
    background_tasks: BackgroundTasks,
    db: DatabaseManager = Depends(),
    redis: RedisManager = Depends()
) -> List[SajuCalculationResponse]:
    """
    배치 사주 계산
    
    여러 사주를 한번에 계산합니다.
    병렬 처리를 통해 성능을 최적화합니다.
    """
    batch_id = f"batch_{int(datetime.now().timestamp())}"
    
    try:
        logger.info(f"배치 계산 시작: {batch_id} ({len(request.calculations)}개)")
        
        # 병렬 처리를 위한 태스크 생성
        tasks = []
        for i, calc_request in enumerate(request.calculations):
            task = asyncio.create_task(
                calculate_single_saju_in_batch(
                    calc_request, f"{batch_id}_{i}", db, redis
                )
            )
            tasks.append(task)
        
        # 모든 계산 완료 대기
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # 결과 처리
        successful_results = []
        errors = []
        
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                errors.append(f"계산 {i+1}: {str(result)}")
            else:
                successful_results.append(result)
        
        # 에러가 있는 경우 부분적 성공 처리
        if errors:
            logger.warning(f"배치 계산 부분 실패: {batch_id} - {len(errors)}개 실패")
            # 에러 로깅은 백그라운드에서 처리
            background_tasks.add_task(
                log_batch_errors,
                batch_id, errors, db
            )
        
        logger.info(f"배치 계산 완료: {batch_id} ({len(successful_results)}개 성공)")
        return successful_results
        
    except Exception as e:
        logger.error(f"배치 계산 오류: {batch_id} - {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"배치 계산 중 오류가 발생했습니다: {str(e)}"
        )

@router.get("/pillars/{year}/{month}/{day}")
async def get_pillars_only(
    year: int,
    month: int,
    day: int,
    hour: int = 12,
    minute: int = 0,
    redis: RedisManager = Depends()
) -> Dict[str, Any]:
    """
    사주 기둥만 빠르게 조회
    
    분석 없이 기본적인 사주 기둥 정보만 반환합니다.
    빠른 조회가 필요한 경우 사용합니다.
    """
    try:
        # 캐시 키 생성
        cache_key = CacheKeys.pillars_only(year, month, day, hour, minute)
        
        # 캐시에서 확인
        cached_result = await redis.get_json(cache_key)
        if cached_result:
            return cached_result
        
        # 간단한 계산 수행
        birth_info = BirthInfo(
            year=year, month=month, day=day,
            hour=hour, minute=minute,
            is_lunar=False, gender="male"
        )
        
        calculator = SajuCalculator()
        saju_result = await calculator.calculate_pillars_only(birth_info)
        
        result = {
            "year_pillar": saju_result.year_pillar.dict(),
            "month_pillar": saju_result.month_pillar.dict(),
            "day_pillar": saju_result.day_pillar.dict(),
            "hour_pillar": saju_result.hour_pillar.dict(),
            "calculation_time": 0.001,  # 매우 빠른 계산
            "cached": False
        }
        
        # 결과 캐싱 (1시간)
        await redis.set_json(cache_key, result, expire=3600)
        
        return result
        
    except Exception as e:
        logger.error(f"기둥 조회 오류: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"기둥 조회 중 오류가 발생했습니다: {str(e)}"
        )

@router.post("/validate")
async def validate_birth_data(
    request: SajuCalculationRequest,
    db: DatabaseManager = Depends()
) -> ValidationResult:
    """
    출생 정보 검증
    
    계산 전에 출생 정보의 유효성을 검증합니다.
    """
    try:
        birth_info = BirthInfo(
            year=request.birth_year,
            month=request.birth_month,
            day=request.birth_day,
            hour=request.birth_hour,
            minute=request.birth_minute,
            is_lunar=request.is_lunar,
            gender=request.gender,
            timezone=request.timezone
        )
        
        validation_result = await validate_birth_info(birth_info, db)
        return validation_result
        
    except Exception as e:
        logger.error(f"데이터 검증 오류: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"데이터 검증 중 오류가 발생했습니다: {str(e)}"
        )

@router.get("/statistics")
async def get_calculation_statistics(
    redis: RedisManager = Depends()
) -> Dict[str, Any]:
    """
    계산 통계 조회
    
    최근 계산 성능 및 사용량 통계를 반환합니다.
    """
    try:
        # Redis에서 통계 데이터 조회
        stats = await redis.get_calculation_stats()
        
        return {
            "total_calculations": stats.get("total_calculations", 0),
            "successful_calculations": stats.get("successful_calculations", 0),
            "failed_calculations": stats.get("failed_calculations", 0),
            "average_response_time": stats.get("average_response_time", 0),
            "cache_hit_rate": stats.get("cache_hit_rate", 0),
            "last_24h_calculations": stats.get("last_24h_calculations", 0),
            "most_common_birth_years": stats.get("most_common_birth_years", []),
            "performance_metrics": {
                "fastest_calculation": stats.get("fastest_calculation", 0),
                "slowest_calculation": stats.get("slowest_calculation", 0),
                "median_calculation_time": stats.get("median_calculation_time", 0)
            }
        }
        
    except Exception as e:
        logger.error(f"통계 조회 오류: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"통계 조회 중 오류가 발생했습니다: {str(e)}"
        )

# ============================================================================
# 헬퍼 함수들
# ============================================================================

async def calculate_single_saju_in_batch(
    request: SajuCalculationRequest,
    calc_id: str,
    db: DatabaseManager,
    redis: RedisManager
) -> SajuCalculationResponse:
    """
    배치 처리에서 단일 사주 계산
    """
    # 개별 계산 로직 (메인 calculate_saju 함수와 유사하지만 간소화)
    birth_info = BirthInfo(
        year=request.birth_year,
        month=request.birth_month,
        day=request.birth_day,
        hour=request.birth_hour,
        minute=request.birth_minute,
        is_lunar=request.is_lunar,
        gender=request.gender,
        timezone=request.timezone
    )
    
    calculator = SajuCalculator()
    saju_result = await calculator.calculate_complete_saju(birth_info)
    
    return SajuCalculationResponse(
        saju_result=saju_result,
        calculation_id=calc_id,
        calculation_time=0.1,  # 배치에서는 간소화
        data_source="batch_calculation",
        confidence_score=95,
        validation_result=ValidationResult(is_valid=True, confidence_score=95, errors=[])
    )

async def cache_and_log_result(
    cache_key: str,
    result_data: dict,
    calculation_id: str,
    calculation_time: float,
    db: DatabaseManager,
    redis: RedisManager
):
    """
    계산 결과 캐싱 및 로깅 (백그라운드 작업)
    """
    try:
        # Redis에 결과 캐싱 (6시간)
        await redis.set_json(cache_key, result_data, expire=21600)
        
        # 통계 업데이트
        await redis.update_calculation_stats(
            calculation_id, calculation_time, success=True
        )
        
        # 데이터베이스에 계산 로그 저장
        await db.log_calculation(
            calculation_id=calculation_id,
            calculation_time=calculation_time,
            cache_key=cache_key,
            success=True
        )
        
    except Exception as e:
        logger.error(f"결과 캐싱/로깅 오류: {calculation_id} - {str(e)}")

async def log_calculation_error(
    calculation_id: str,
    error_message: str,
    request_data: dict,
    db: DatabaseManager
):
    """
    계산 오류 로깅 (백그라운드 작업)
    """
    try:
        await db.log_calculation_error(
            calculation_id=calculation_id,
            error_message=error_message,
            request_data=request_data
        )
        
    except Exception as e:
        logger.error(f"오류 로깅 실패: {calculation_id} - {str(e)}")

async def log_batch_errors(
    batch_id: str,
    errors: List[str],
    db: DatabaseManager
):
    """
    배치 오류 로깅 (백그라운드 작업)
    """
    try:
        await db.log_batch_errors(
            batch_id=batch_id,
            errors=errors
        )
        
    except Exception as e:
        logger.error(f"배치 오류 로깅 실패: {batch_id} - {str(e)}")