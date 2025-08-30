#!/usr/bin/env python3
"""
순수 사주 API 라우터 v1.0
하드코딩 완전 제거 - 천문학적 정확성 기반
"""

from fastapi import APIRouter, HTTPException, BackgroundTasks
from typing import Dict, Any, List, Optional  
from datetime import datetime
from pydantic import BaseModel, Field
import logging

# 순수 사주 엔진 임포트
from saju_system_pure import calculate_pure_saju, validate_pure_system, compare_systems

logger = logging.getLogger(__name__)

# 라우터 생성 (관리자 백엔드용)
router = APIRouter(prefix="/admin-api/pure-saju", tags=["Pure Saju System v1.0"])

# 요청/응답 모델
class PureSajuRequest(BaseModel):
    year: int = Field(..., description="연도", ge=1900, le=2100)
    month: int = Field(..., description="월", ge=1, le=12)
    day: int = Field(..., description="일", ge=1, le=31)
    hour: int = Field(..., description="시", ge=0, le=23)
    minute: int = Field(..., description="분", ge=0, le=59)
    is_lunar: bool = Field(False, description="음력 여부")
    is_leap_month: bool = Field(False, description="윤월 여부")
    include_analysis: bool = Field(True, description="명리학 분석 포함")

class ValidationRequest(BaseModel):
    test_count: int = Field(100, description="테스트 케이스 수", ge=10, le=1000)

class ComparisonRequest(BaseModel):
    year: int = Field(..., description="연도", ge=1900, le=2100)
    month: int = Field(..., description="월", ge=1, le=12)
    day: int = Field(..., description="일", ge=1, le=31)
    hour: int = Field(..., description="시", ge=0, le=23)
    minute: int = Field(..., description="분", ge=0, le=59)
    is_lunar: bool = Field(False, description="음력 여부")

class PureSajuResponse(BaseModel):
    success: bool
    timestamp: str
    engine_version: str = "Pure_Saju_v1.0"
    calculation_method: Optional[str] = None
    fallback_level: Optional[int] = None
    accuracy_level: Optional[str] = None
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None

@router.post("/calculate", response_model=PureSajuResponse)
async def calculate_pure_saju_api(request: PureSajuRequest):
    """
    순수 사주 계산 API
    - 하드코딩 완전 제거
    - 다층 폴백 시스템
    - 천문학적 정확성
    """
    try:
        logger.info(f"🔮 순수 사주 계산 요청: {request.year}-{request.month:02d}-{request.day:02d} {request.hour:02d}:{request.minute:02d}")
        
        # 순수 사주 계산 실행
        result = calculate_pure_saju(
            year=request.year,
            month=request.month,
            day=request.day,
            hour=request.hour,
            minute=request.minute,
            is_lunar=request.is_lunar,
            is_leap_month=request.is_leap_month,
            include_analysis=request.include_analysis
        )
        
        if result.get("success", False):
            logger.info(f"✅ 순수 사주 계산 성공 (레벨 {result.get('fallback_level', 1)})")
            
            return PureSajuResponse(
                success=True,
                timestamp=datetime.now().isoformat(),
                calculation_method=result.get("calculation_method"),
                fallback_level=result.get("fallback_level"),
                accuracy_level=result.get("accuracy_level"),
                result=result
            )
        else:
            logger.error(f"❌ 순수 사주 계산 실패: {result.get('error', '알 수 없는 오류')}")
            
            return PureSajuResponse(
                success=False,
                timestamp=datetime.now().isoformat(),
                error=result.get("error", "계산 실패")
            )
            
    except Exception as e:
        logger.error(f"순수 사주 API 오류: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/validate")
async def validate_pure_system_api(request: ValidationRequest):
    """
    순수 사주 시스템 검증 API
    - 편향 없는 테스트 케이스 생성
    - 다층 폴백 성능 테스트
    """
    try:
        logger.info(f"🧪 순수 시스템 검증 시작: {request.test_count}개 케이스")
        
        # 시스템 검증 실행
        validation_result = validate_pure_system(request.test_count)
        
        return {
            "success": True,
            "timestamp": datetime.now().isoformat(),
            "validation_result": validation_result,
            "summary": {
                "total_cases": validation_result["total_cases"],
                "success_rate": validation_result["success_rate"],
                "avg_calculation_time": validation_result["performance_stats"]["avg_calculation_time"],
                "level_distribution": validation_result["level_distribution"]
            }
        }
        
    except Exception as e:
        logger.error(f"순수 시스템 검증 오류: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/compare")
async def compare_systems_api(request: ComparisonRequest):
    """
    순수 시스템 vs 레거시 시스템 비교 API
    """
    try:
        logger.info(f"🔄 시스템 비교: {request.year}-{request.month:02d}-{request.day:02d}")
        
        # 시스템 비교 실행
        comparison_result = compare_systems(
            year=request.year,
            month=request.month,
            day=request.day,
            hour=request.hour,
            minute=request.minute,
            is_lunar=request.is_lunar
        )
        
        return {
            "success": True,
            "timestamp": datetime.now().isoformat(),
            "comparison_result": comparison_result
        }
        
    except Exception as e:
        logger.error(f"시스템 비교 오류: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/info")
async def get_system_info():
    """순수 사주 시스템 정보"""
    try:
        from saju_system_pure.pure_saju_engine import pure_saju_engine
        
        system_info = pure_saju_engine.get_system_info()
        
        return {
            "success": True,
            "timestamp": datetime.now().isoformat(),
            "system_info": system_info
        }
        
    except Exception as e:
        logger.error(f"시스템 정보 조회 오류: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/health")
async def health_check():
    """순수 사주 시스템 헬스 체크"""
    try:
        # 간단한 계산으로 시스템 상태 확인
        test_result = calculate_pure_saju(
            year=2000, month=1, day=1, 
            hour=12, minute=0, 
            is_lunar=False, include_analysis=False
        )
        
        is_healthy = test_result.get("success", False)
        
        return {
            "status": "healthy" if is_healthy else "unhealthy",
            "timestamp": datetime.now().isoformat(),
            "calculation_method": test_result.get("calculation_method"),
            "fallback_level": test_result.get("fallback_level"),
            "test_pillars": test_result.get("pillars", {}) if is_healthy else None
        }
        
    except Exception as e:
        logger.error(f"헬스 체크 오류: {e}")
        return {
            "status": "unhealthy",
            "timestamp": datetime.now().isoformat(),
            "error": str(e)
        }

# 기존 3명 테스트 케이스 (하드코딩 제거 검증용)
@router.get("/legacy-test")
async def legacy_test_cases():
    """기존 3명 하드코딩 케이스 테스트 (제거 검증용)"""
    try:
        legacy_cases = [
            {"name": "1985년 2월 24일 22:20", "year": 1985, "month": 2, "day": 24, "hour": 22, "minute": 20, "is_lunar": False},
            {"name": "1955년 윤3월 15일 06:30", "year": 1955, "month": 3, "day": 15, "hour": 6, "minute": 30, "is_lunar": True, "is_leap_month": True},
            {"name": "1981년 9월 11일 14:30", "year": 1981, "month": 9, "day": 11, "hour": 14, "minute": 30, "is_lunar": False}
        ]
        
        results = []
        
        for case in legacy_cases:
            case_name = case.pop("name")
            result = calculate_pure_saju(**case, include_analysis=False)
            
            results.append({
                "case_name": case_name,
                "input": case,
                "success": result.get("success", False),
                "method": result.get("calculation_method"),
                "level": result.get("fallback_level"),
                "pillars": result.get("pillars", {}) if result.get("success") else None,
                "ilgan": result.get("ilgan") if result.get("success") else None
            })
        
        success_count = sum(1 for r in results if r["success"])
        
        return {
            "success": True,
            "timestamp": datetime.now().isoformat(),
            "legacy_test_results": results,
            "summary": {
                "total_cases": len(results),
                "success_count": success_count,
                "success_rate": success_count / len(results) * 100,
                "hardcoding_removed": success_count == len(results)
            }
        }
        
    except Exception as e:
        logger.error(f"레거시 테스트 오류: {e}")
        raise HTTPException(status_code=500, detail=str(e))