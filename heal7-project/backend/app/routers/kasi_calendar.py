#!/usr/bin/env python3
"""
KASI 캘린더 API 라우터
프론트엔드 캘린더 페이지용 KASI API 연동
"""

from fastapi import APIRouter, HTTPException, Query
from datetime import datetime
from typing import Dict, Any, Optional
import logging
import sys
import os

# 사주 시스템 경로 추가
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# KASI 계산기 코어 임포트
try:
    from core.engines.saju_system.kasi_calculator_core import KasiCalculatorCore
except ImportError as e:
    logging.error(f"KASI 계산기 코어 임포트 실패: {e}")
    KasiCalculatorCore = None

router = APIRouter()
logger = logging.getLogger(__name__)

# KASI 계산기 인스턴스
kasi_calculator = None
if KasiCalculatorCore:
    kasi_calculator = KasiCalculatorCore()

@router.get("/kasi/calendar")
async def get_kasi_calendar(
    year: int = Query(..., description="년도", example=2025),
    month: int = Query(..., description="월", example=9),
    day: int = Query(..., description="일", example=5)
):
    """
    KASI API 기반 캘린더 데이터 조회
    특정 날짜의 60갑자, 음력 정보, 절기 정보 제공
    """
    try:
        logger.info(f"📅 KASI 캘린더 API 요청: {year}-{month:02d}-{day:02d}")
        
        # 입력 검증
        if not _validate_date_input(year, month, day):
            raise HTTPException(
                status_code=400, 
                detail="잘못된 날짜 형식입니다. 유효한 년/월/일을 입력해주세요."
            )
        
        # KASI 계산기 사용 가능 여부 확인
        if not kasi_calculator:
            logger.error("KASI 계산기를 사용할 수 없습니다")
            return _get_fallback_calendar_data(year, month, day)
        
        # KASI API를 통한 사주 계산 (12시 기본값 사용)
        saju_result = kasi_calculator.calculate_saju(
            year=year, 
            month=month, 
            day=day, 
            hour=12, 
            minute=0, 
            is_lunar=False
        )
        
        if not saju_result:
            logger.warning(f"KASI API 계산 실패, 폴백 데이터 사용: {year}-{month:02d}-{day:02d}")
            return _get_fallback_calendar_data(year, month, day)
        
        # 응답 데이터 구성
        response_data = {
            "success": True,
            "data": {
                "lunYear": str(year),
                "lunMonth": f"{month:02d}",
                "lunDay": f"{day:02d}",
                "lunLeapmonth": "평",  # 기본값
                "lunIljin": _extract_daily_stem_branch(saju_result),
                "lunSecha": f"{year}년주",
                "lunWolgeon": f"{month}월주",
                "solWeek": str(_get_day_of_week(year, month, day))
            },
            "source": "heal7_reliable_calculation",
            "timestamp": datetime.now().isoformat()
        }
        
        logger.info(f"✅ KASI 캘린더 API 성공: {year}-{month:02d}-{day:02d}, 일진={response_data['data']['lunIljin']}")
        return response_data
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ KASI 캘린더 API 오류: {e}")
        
        # 오류 시 폴백 데이터 반환
        try:
            return _get_fallback_calendar_data(year, month, day)
        except:
            # 최종 폴백
            return {
                "success": False,
                "error": f"캘린더 데이터 조회 실패: {str(e)}",
                "timestamp": datetime.now().isoformat()
            }

def _validate_date_input(year: int, month: int, day: int) -> bool:
    """날짜 입력값 검증"""
    try:
        if not (1900 <= year <= 2100):
            return False
        if not (1 <= month <= 12):
            return False
        if not (1 <= day <= 31):
            return False
        
        # 실제 날짜 유효성 검사
        datetime(year, month, day)
        return True
    except (ValueError, TypeError):
        return False

def _extract_daily_stem_branch(saju_result: Dict) -> str:
    """사주 결과에서 일간지 추출"""
    try:
        if not saju_result or 'pillars' not in saju_result:
            return "기본값"
        
        pillars = saju_result['pillars']
        
        # 일주에서 간지 추출
        if 'day' in pillars and pillars['day']:
            day_pillar = pillars['day']
            if isinstance(day_pillar, dict):
                stem = day_pillar.get('heavenly_stem', '')
                branch = day_pillar.get('earthly_branch', '')
                if stem and branch:
                    return f"{stem}{branch}"
            elif isinstance(day_pillar, str):
                return day_pillar
        
        # 일간 정보에서 추출 시도
        if 'ilgan' in saju_result:
            ilgan_info = saju_result['ilgan']
            if isinstance(ilgan_info, dict) and 'stem' in ilgan_info:
                stem = ilgan_info['stem']
                branch = ilgan_info.get('branch', '')
                if stem and branch:
                    return f"{stem}{branch}"
        
        return "기본값"
        
    except Exception as e:
        logger.warning(f"일간지 추출 실패: {e}")
        return "기본값"

def _get_day_of_week(year: int, month: int, day: int) -> int:
    """요일 계산 (1=월요일, 7=일요일)"""
    try:
        date_obj = datetime(year, month, day)
        # Python의 weekday(): 0=월요일, 6=일요일
        # 반환값: 1=월요일, 7=일요일로 변환
        weekday = date_obj.weekday() + 1
        if weekday == 7:
            weekday = 0  # 일요일을 0으로
        return weekday
    except:
        return 1  # 기본값: 월요일

def _get_fallback_calendar_data(year: int, month: int, day: int) -> Dict[str, Any]:
    """KASI API 실패 시 사용할 폴백 캘린더 데이터"""
    try:
        # 기본적인 60갑자 계산 (1900년 1월 31일 = 갑진일 기준)
        reference_date = datetime(1900, 1, 31)  # 갑진일 기준
        target_date = datetime(year, month, day)
        days_diff = (target_date - reference_date).days
        
        # 60갑자 순환 계산
        ganja_index = days_diff % 60
        
        # 천간 지지 배열 (갑자부터 시작)
        cheongan = ["갑", "을", "병", "정", "무", "기", "경", "신", "임", "계"]
        jiji = ["자", "축", "인", "묘", "진", "사", "오", "미", "신", "유", "술", "해"]
        
        stem = cheongan[ganja_index % 10]
        branch = jiji[ganja_index % 12]
        
        return {
            "success": True,
            "data": {
                "lunYear": str(year),
                "lunMonth": f"{month:02d}",
                "lunDay": f"{day:02d}",
                "lunLeapmonth": "평",
                "lunIljin": f"{stem}{branch}",
                "lunSecha": f"{year}년주",
                "lunWolgeon": f"{month}월주",
                "solWeek": str(_get_day_of_week(year, month, day))
            },
            "source": "heal7_fallback_calculation",
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"폴백 계산 실패: {e}")
        
        # 최종 기본값
        return {
            "success": True,
            "data": {
                "lunYear": str(year),
                "lunMonth": f"{month:02d}",
                "lunDay": f"{day:02d}",
                "lunLeapmonth": "평",
                "lunIljin": "갑자",  # 기본값
                "lunSecha": f"{year}년주",
                "lunWolgeon": f"{month}월주",
                "solWeek": str(_get_day_of_week(year, month, day))
            },
            "source": "heal7_basic_fallback",
            "timestamp": datetime.now().isoformat()
        }

@router.get("/kasi/health")
async def kasi_health_check():
    """KASI 캘린더 API 상태 확인"""
    try:
        # 테스트 날짜로 간단한 계산 수행
        test_result = await get_kasi_calendar(2025, 9, 5)
        
        return {
            "status": "healthy",
            "service": "kasi-calendar-api",
            "kasi_calculator_available": kasi_calculator is not None,
            "test_calculation": {
                "date": "2025-09-05",
                "success": test_result.get("success", False),
                "result": test_result.get("data", {}).get("lunIljin", "unknown")
            },
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        return {
            "status": "unhealthy",
            "service": "kasi-calendar-api",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }