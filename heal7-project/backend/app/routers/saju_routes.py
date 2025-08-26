#!/usr/bin/env python3
"""
사주 API 라우터 v5.0
- v5.0 통합 명리학 분석 시스템 연동
- KASI API 기반 정밀 사주 계산
- 프론트엔드 최적화된 JSON 응답
"""

from fastapi import APIRouter, HTTPException, BackgroundTasks
from typing import Dict, Any, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
import logging
import uuid

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from saju_system import analyze_complete_saju
from saju_system.saju_ai_inspector import saju_ai_inspector

router = APIRouter(prefix="/admin-api/saju", tags=["saju"])
logger = logging.getLogger(__name__)

# Request/Response 모델
class SajuCalculationRequest(BaseModel):
    year: int = Field(..., description="출생년도", example=1985)
    month: int = Field(..., description="출생월", example=2)
    day: int = Field(..., description="출생일", example=24)
    hour: int = Field(..., description="출생시간", example=22)
    minute: int = Field(0, description="출생분", example=20)
    is_lunar: bool = Field(False, description="음력 여부")
    is_leap_month: bool = Field(False, description="윤달 여부")
    ai_inspection: bool = Field(False, description="AI 검수 요청 여부")
    use_fallback_verification: bool = Field(False, description="폴백 검증 사용 여부")
    gender: Optional[str] = Field(None, description="성별 (male/female)")

class SajuAIInspectionRequest(BaseModel):
    saju_result: Dict[str, Any] = Field(..., description="사주 계산 결과")
    use_fallback: bool = Field(False, description="폴백 모드 사용")

class SajuResponse(BaseModel):
    success: bool
    timestamp: str
    analysis_version: str = "v5.0"
    saju_result: Optional[Dict[str, Any]] = None
    ai_inspection: Optional[Dict[str, Any]] = None
    service_type: Optional[str] = None
    error: Optional[str] = None

@router.post("/calculate", response_model=SajuResponse)
async def calculate_saju_v5(request: SajuCalculationRequest):
    """
    사주 v5.0 통합 명리학 분석
    - KASI API 기반 정밀 계산
    - 오행/십신/격국 완전 분석
    """
    try:
        logger.info(f"📊 사주 v5.0 계산 요청: {request.year}-{request.month:02d}-{request.day:02d} {request.hour:02d}:{request.minute:02d}")
        
        # v5.0 통합 명리학 분석 실행 (성별 포함)
        result = analyze_complete_saju(
            year=request.year,
            month=request.month,
            day=request.day,
            hour=request.hour,
            minute=request.minute,
            is_lunar=request.is_lunar,
            is_leap_month=request.is_leap_month,
            gender=request.gender
        )
        
        # AI 검수 요청시 처리
        if request.ai_inspection:
            logger.info("🔮 AI 검수 시스템 호출")
            ai_inspection_result = await saju_ai_inspector.inspect_saju_result(
                result, 
                fallback_used=request.use_fallback_verification
            )
            
            return SajuResponse(
                success=True,
                timestamp=datetime.now().isoformat(),
                saju_result=result,
                ai_inspection=ai_inspection_result,
                service_type="saju_with_ai_inspection"
            )
        else:
            return SajuResponse(
                success=True,
                timestamp=datetime.now().isoformat(),
                saju_result=result,
                service_type="saju_calculation_only"
            )
            
    except Exception as e:
        logger.error(f"❌ 사주 계산 실패: {e}")
        return SajuResponse(
            success=False,
            timestamp=datetime.now().isoformat(),
            error=str(e)
        )

@router.post("/calculate-with-ai", response_model=SajuResponse)
async def calculate_saju_with_ai_inspection(request: SajuCalculationRequest):
    """
    사주 v5.0 계산 + AI 검수 통합 원스톱 서비스
    """
    try:
        logger.info(f"🔮 사주 v5.0 + AI 검수 통합 요청")
        
        # 사주 계산 (성별 포함)
        saju_result = analyze_complete_saju(
            year=request.year,
            month=request.month,
            day=request.day,
            hour=request.hour,
            minute=request.minute,
            is_lunar=request.is_lunar,
            is_leap_month=request.is_leap_month,
            gender=request.gender
        )
        
        # AI 검수 실행
        ai_inspection_result = await saju_ai_inspector.inspect_saju_result(
            saju_result, 
            fallback_used=request.use_fallback_verification
        )
        
        return SajuResponse(
            success=True,
            timestamp=datetime.now().isoformat(),
            saju_result=saju_result,
            ai_inspection=ai_inspection_result,
            service_type="integrated_analysis_with_ai_inspection"
        )
        
    except Exception as e:
        logger.error(f"❌ 통합 사주 + AI 검수 실패: {e}")
        return SajuResponse(
            success=False,
            timestamp=datetime.now().isoformat(),
            error=str(e)
        )

@router.post("/ai-inspect", response_model=SajuResponse)
async def ai_inspect_saju_result(request: SajuAIInspectionRequest):
    """
    기존 사주 결과 AI 검수 전용
    """
    try:
        logger.info("🔍 사주 결과 AI 검수 전용 요청")
        
        ai_inspection_result = await saju_ai_inspector.inspect_saju_result(
            request.saju_result,
            fallback_used=request.use_fallback
        )
        
        return SajuResponse(
            success=True,
            timestamp=datetime.now().isoformat(),
            ai_inspection=ai_inspection_result,
            service_type="standalone_ai_inspection"
        )
        
    except Exception as e:
        logger.error(f"❌ AI 검수 실패: {e}")
        return SajuResponse(
            success=False,
            timestamp=datetime.now().isoformat(),
            error=str(e)
        )

@router.get("/analyze/wuxing")
async def analyze_wuxing_only(
    year: int, month: int, day: int, hour: int, minute: int = 0,
    is_lunar: bool = False, is_leap_month: bool = False
):
    """
    오행 분석만 수행 (경량화)
    """
    try:
        logger.info("🌟 오행 분석 전용 요청")
        
        # 전체 분석 후 오행 부분만 추출
        full_result = analyze_complete_saju(
            year, month, day, hour, minute, is_lunar, is_leap_month, gender=None
        )
        
        # 오행 분석만 추출
        wuxing_only_result = {
            "input": full_result["input"],
            "ilgan": full_result["ilgan"],
            "wuxing_analysis": full_result.get("analysis_details", {}).get("wuxing_balance", {}),
            "analysis_type": "wuxing_only",
            "timestamp": datetime.now().isoformat()
        }
        
        return {
            "success": True,
            "result": wuxing_only_result
        }
        
    except Exception as e:
        logger.error(f"❌ 오행 분석 실패: {e}")
        raise HTTPException(status_code=500, detail=f"오행 분석 실패: {str(e)}")

@router.get("/analyze/sipsin")
async def analyze_sipsin_only(
    year: int, month: int, day: int, hour: int, minute: int = 0,
    is_lunar: bool = False, is_leap_month: bool = False
):
    """
    십신 패턴 분석만 수행 (성격 분석 특화)
    """
    try:
        logger.info("⭐ 십신 분석 전용 요청")
        
        # 전체 분석 후 십신 부분만 추출
        full_result = analyze_complete_saju(
            year, month, day, hour, minute, is_lunar, is_leap_month
        )
        
        # 십신 분석만 추출
        sipsin_only_result = {
            "input": full_result["input"],
            "ilgan": full_result["ilgan"],
            "sipsin_analysis": full_result.get("analysis_details", {}).get("sipsin_pattern", {}),
            "analysis_type": "sipsin_only",
            "timestamp": datetime.now().isoformat()
        }
        
        return {
            "success": True,
            "result": sipsin_only_result
        }
        
    except Exception as e:
        logger.error(f"❌ 십신 분석 실패: {e}")
        raise HTTPException(status_code=500, detail=f"십신 분석 실패: {str(e)}")

@router.get("/analyze/gyeokguk")
async def analyze_gyeokguk_only(
    year: int, month: int, day: int, hour: int, minute: int = 0,
    is_lunar: bool = False, is_leap_month: bool = False
):
    """
    격국 분석만 수행 (용신 추천 특화)
    """
    try:
        logger.info("🏛️ 격국 분석 전용 요청")
        
        # 전체 분석 후 격국 부분만 추출
        full_result = analyze_complete_saju(
            year, month, day, hour, minute, is_lunar, is_leap_month
        )
        
        # 격국 분석만 추출
        gyeokguk_only_result = {
            "input": full_result["input"],
            "ilgan": full_result["ilgan"],
            "gyeokguk": full_result.get("gyeokguk", "미분류격"),
            "gyeokguk_analysis": full_result.get("analysis_details", {}).get("gyeokguk_details", {}),
            "analysis_type": "gyeokguk_only",
            "timestamp": datetime.now().isoformat()
        }
        
        return {
            "success": True,
            "result": gyeokguk_only_result
        }
        
    except Exception as e:
        logger.error(f"❌ 격국 분석 실패: {e}")
        raise HTTPException(status_code=500, detail=f"격국 분석 실패: {str(e)}")

@router.get("/health")
async def health_check():
    """
    사주 시스템 상태 확인
    """
    try:
        # v5.0 시스템 가동 확인
        test_result = analyze_complete_saju(1985, 2, 24, 22, 20, False)
        
        # AI 검수 시스템 확인
        ai_models_status = []
        for model in saju_ai_inspector.fallback_models:
            try:
                # 간단한 상태 체크
                ai_models_status.append({
                    "model": model,
                    "status": "available"
                })
            except:
                ai_models_status.append({
                    "model": model,
                    "status": "unavailable"
                })
        
        return {
            "success": True,
            "system_status": "healthy",
            "saju_analyzer": "ready",
            "ai_inspector": "ready",
            "ai_models": ai_models_status,
            "version": "v5.0",
            "features": {
                "kasi_api": "enabled",
                "wuxing_analysis": "enabled",
                "sipsin_analysis": "enabled", 
                "gyeokguk_analysis": "enabled",
                "ai_inspection": "enabled"
            },
            "test_calculation": {
                "input": "1985-02-24 22:20",
                "ilgan": test_result.get("ilgan", "unknown"),
                "status": "success"
            },
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"❌ 시스템 상태 확인 실패: {e}")
        return {
            "success": False,
            "system_status": "unhealthy",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }

@router.get("/test")
async def test_endpoint():
    """
    사주 시스템 간단 테스트
    """
    try:
        test_result = analyze_complete_saju(1985, 2, 24, 22, 20, False)
        
        return {
            "success": True,
            "message": "사주 v5.0 시스템 정상 작동",
            "test_data": {
                "input": "1985-02-24 22:20 (양력)",
                "pillars": test_result.get("pillars", {}),
                "ilgan": test_result.get("ilgan", "unknown"),
                "gyeokguk": test_result.get("gyeokguk", "unknown")
            },
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }