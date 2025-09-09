"""
Atomic Saju Router - 원자 모듈 기반 사주 API
=========================================

새로운 atomic 모듈을 사용하는 사주 계산 API
기존 시스템과 병행하여 점진적 전환

엔드포인트:
- POST /api/atomic/saju/calculate - 완전한 사주 계산
- GET /api/atomic/saju/gapja - 60갑자 계산
- GET /api/atomic/saju/pillars - 사주 기둥 계산  
- GET /api/atomic/saju/lunar-convert - 음력 변환
"""

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field
from datetime import datetime, date
from typing import Optional, Dict, Any
import logging

# atomic 모듈 import
from ..core.atomic import (
    calculate_gapja, get_gapja_by_date,
    solar_to_lunar_sync, lunar_to_solar_sync,
    calculate_year_pillar, calculate_month_pillar, 
    calculate_day_pillar, calculate_time_pillar
)
from ..core.atomic.constants import GANJI_60, CHEONGAN, JIJI

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/atomic/saju", tags=["Atomic Saju"])

# === Request/Response Models ===

class SajuCalculateRequest(BaseModel):
    """사주 계산 요청"""
    year: int = Field(..., ge=1900, le=2100, description="년도")
    month: int = Field(..., ge=1, le=12, description="월")
    day: int = Field(..., ge=1, le=31, description="일")
    hour: int = Field(12, ge=0, le=23, description="시간")
    minute: int = Field(0, ge=0, le=59, description="분")
    use_true_solar_time: bool = Field(False, description="진태양시 사용")
    longitude: float = Field(126.978, description="경도")

class GapjaResponse(BaseModel):
    """갑자 응답"""
    success: bool
    date: str
    gapja: str
    cheongan: str
    jiji: str
    index: int
    source: str = "atomic_module"

class PillarsResponse(BaseModel):
    """사주 기둥 응답"""
    success: bool
    birth_datetime: str
    year_pillar: Dict[str, Any]
    month_pillar: Dict[str, Any]
    day_pillar: Dict[str, Any]
    time_pillar: Dict[str, Any]
    source: str = "atomic_module"

class LunarConvertResponse(BaseModel):
    """음력 변환 응답"""
    success: bool
    solar_date: Optional[Dict[str, Any]] = None
    lunar_date: Optional[Dict[str, Any]] = None
    source: str
    error_message: str = ""

# === API Endpoints ===

@router.post("/calculate", response_model=Dict[str, Any])
async def calculate_complete_saju_api(request: SajuCalculateRequest):
    """
    완전한 사주 계산 API
    
    atomic 모듈을 사용한 정확한 사주 계산
    """
    try:
        # PillarCalculator 설정
        calculator = PillarCalculator(
            use_true_solar_time=request.use_true_solar_time,
            longitude=request.longitude
        )
        
        # 생년월일시 생성
        birth_datetime = datetime(
            request.year, request.month, request.day,
            request.hour, request.minute
        )
        
        # 사주 계산
        saju_result = calculator.calculate_all_pillars(birth_datetime)
        
        # 응답 데이터 구성
        response = {
            "success": True,
            "birth_datetime": birth_datetime.isoformat(),
            "calculation_method": "atomic_module",
            "use_true_solar_time": request.use_true_solar_time,
            "longitude": request.longitude,
            "pillars": {
                "year": {
                    "gapja": saju_result.year_pillar.ganji,
                    "cheongan": saju_result.year_pillar.cheongan,
                    "jiji": saju_result.year_pillar.jiji,
                    "element": saju_result.year_pillar.element,
                    "yin_yang": saju_result.year_pillar.yin_yang
                },
                "month": {
                    "gapja": saju_result.month_pillar.ganji,
                    "cheongan": saju_result.month_pillar.cheongan,
                    "jiji": saju_result.month_pillar.jiji,
                    "element": saju_result.month_pillar.element,
                    "yin_yang": saju_result.month_pillar.yin_yang
                },
                "day": {
                    "gapja": saju_result.day_pillar.ganji,
                    "cheongan": saju_result.day_pillar.cheongan,
                    "jiji": saju_result.day_pillar.jiji,
                    "element": saju_result.day_pillar.element,
                    "yin_yang": saju_result.day_pillar.yin_yang
                },
                "time": {
                    "gapja": saju_result.time_pillar.ganji,
                    "cheongan": saju_result.time_pillar.cheongan,
                    "jiji": saju_result.time_pillar.jiji,
                    "element": saju_result.time_pillar.element,
                    "yin_yang": saju_result.time_pillar.yin_yang
                }
            },
            "summary": {
                "saju_string": str(saju_result),
                "ilgan": saju_result.day_pillar.cheongan,
                "ilji": saju_result.day_pillar.jiji,
                "primary_element": saju_result.day_pillar.element
            }
        }
        
        logger.info(f"Atomic 사주 계산 성공: {birth_datetime}")
        return response
        
    except Exception as e:
        logger.error(f"Atomic 사주 계산 오류: {e}")
        raise HTTPException(
            status_code=500, 
            detail=f"사주 계산 실패: {str(e)}"
        )

@router.get("/gapja", response_model=GapjaResponse)
async def get_gapja_api(
    year: int = Query(..., ge=1900, le=2100),
    month: int = Query(..., ge=1, le=12),
    day: int = Query(..., ge=1, le=31)
):
    """
    60갑자 계산 API
    
    특정 날짜의 갑자를 계산
    """
    try:
        target_date = date(year, month, day)
        gapja = calculate_gapja(target_date)
        
        # 갑자 분해
        cheongan = gapja[0]
        jiji = gapja[1]
        gapja_index = GANJI_60.index(gapja)
        
        response = GapjaResponse(
            success=True,
            date=target_date.isoformat(),
            gapja=gapja,
            cheongan=cheongan,
            jiji=jiji,
            index=gapja_index
        )
        
        logger.info(f"갑자 계산: {target_date} = {gapja}")
        return response
        
    except Exception as e:
        logger.error(f"갑자 계산 오류: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"갑자 계산 실패: {str(e)}"
        )

@router.get("/pillars", response_model=PillarsResponse) 
async def get_pillars_api(
    year: int = Query(..., ge=1900, le=2100),
    month: int = Query(..., ge=1, le=12),
    day: int = Query(..., ge=1, le=31),
    hour: int = Query(12, ge=0, le=23),
    minute: int = Query(0, ge=0, le=59),
    use_true_solar_time: bool = Query(False)
):
    """
    사주 기둥 계산 API
    
    년주/월주/일주/시주를 개별적으로 계산
    """
    try:
        birth_datetime = datetime(year, month, day, hour, minute)
        calculator = PillarCalculator(use_true_solar_time=use_true_solar_time)
        
        # 개별 기둥 계산
        year_pillar = calculator.calculate_year_pillar(birth_datetime)
        month_pillar = calculator.calculate_month_pillar(birth_datetime, year_pillar)
        day_pillar = calculator.calculate_day_pillar(birth_datetime)
        time_pillar = calculator.calculate_time_pillar(birth_datetime, day_pillar)
        
        def pillar_to_dict(pillar):
            return {
                "gapja": pillar.ganji,
                "cheongan": pillar.cheongan,
                "jiji": pillar.jiji,
                "element": pillar.element,
                "yin_yang": pillar.yin_yang
            }
        
        response = PillarsResponse(
            success=True,
            birth_datetime=birth_datetime.isoformat(),
            year_pillar=pillar_to_dict(year_pillar),
            month_pillar=pillar_to_dict(month_pillar),
            day_pillar=pillar_to_dict(day_pillar),
            time_pillar=pillar_to_dict(time_pillar)
        )
        
        logger.info(f"기둥 계산: {birth_datetime}")
        return response
        
    except Exception as e:
        logger.error(f"기둥 계산 오류: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"기둥 계산 실패: {str(e)}"
        )

@router.get("/lunar-convert", response_model=LunarConvertResponse)
async def convert_lunar_api(
    year: int = Query(..., ge=1900, le=2100),
    month: int = Query(..., ge=1, le=12),
    day: int = Query(..., ge=1, le=31),
    direction: str = Query("solar_to_lunar", regex="^(solar_to_lunar|lunar_to_solar)$"),
    is_leap: bool = Query(False, description="윤달 여부 (음력→양력 시)")
):
    """
    음력 변환 API
    
    양력↔음력 상호 변환
    """
    try:
        if direction == "solar_to_lunar":
            # 양력 → 음력
            solar_date = date(year, month, day)
            result = solar_to_lunar_sync(solar_date)
            
            if result.success:
                response_data = {
                    "success": True,
                    "solar_date": {
                        "year": year,
                        "month": month,
                        "day": day,
                        "date_string": f"{year}년 {month}월 {day}일"
                    },
                    "lunar_date": {
                        "year": result.lunar_date.year,
                        "month": result.lunar_date.month,
                        "day": result.lunar_date.day,
                        "is_leap_month": result.lunar_date.is_leap_month,
                        "date_string": str(result.lunar_date)
                    },
                    "source": result.source
                }
            else:
                response_data = {
                    "success": False,
                    "error_message": result.error_message,
                    "source": "error"
                }
                
        else:
            # 음력 → 양력
            result = lunar_to_solar_sync(year, month, day, is_leap)
            
            if result.success:
                response_data = {
                    "success": True,
                    "lunar_date": {
                        "year": year,
                        "month": month,
                        "day": day,
                        "is_leap_month": is_leap,
                        "date_string": f"음력 {year}년 {month}월 {day}일" + (" (윤달)" if is_leap else "")
                    },
                    "solar_date": {
                        "year": result.solar_date.year,
                        "month": result.solar_date.month,
                        "day": result.solar_date.day,
                        "date_string": str(result.solar_date)
                    },
                    "source": result.source
                }
            else:
                response_data = {
                    "success": False,
                    "error_message": result.error_message,
                    "source": "error"
                }
        
        return LunarConvertResponse(**response_data)
        
    except Exception as e:
        logger.error(f"음력 변환 오류: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"음력 변환 실패: {str(e)}"
        )

# === 헬스 체크 및 정보 ===

@router.get("/health")
async def health_check():
    """atomic 모듈 상태 확인"""
    return {
        "status": "healthy",
        "module": "atomic_saju",
        "version": "1.0.0",
        "available_endpoints": [
            "/calculate",
            "/gapja", 
            "/pillars",
            "/lunar-convert"
        ],
        "constants": {
            "gapja_count": len(GANJI_60),
            "cheongan_count": len(CHEONGAN),
            "jiji_count": len(JIJI)
        }
    }

@router.get("/constants")
async def get_constants():
    """사주 상수 조회"""
    return {
        "gapja_60": GANJI_60,
        "cheongan": CHEONGAN,
        "jiji": JIJI,
        "reference_date": "1900-01-31",
        "reference_gapja": "갑진"
    }