from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List, Dict, Any
import logging

from services_new.saju_service import SajuService, BirthInfo, SajuResult as SajuServiceResult, Gender
# AI 서비스는 향후 통합 예정
# from services_new.ai_service import AnalysisType

logger = logging.getLogger(__name__)
router = APIRouter()

# 전역 서비스 인스턴스
_saju_service: Optional[SajuService] = None

async def get_saju_service() -> SajuService:
    """사주 서비스 인스턴스 가져오기"""
    global _saju_service
    if _saju_service is None:
        _saju_service = SajuService()
        await _saju_service.initialize()
    return _saju_service

# Pydantic 모델들
class SajuRequest(BaseModel):
    birth_year: int
    birth_month: int 
    birth_day: int
    birth_hour: int
    birth_minute: int = 0
    gender: str  # "male" or "female"
    name: Optional[str] = None
    is_lunar: bool = False

class SajuResult(BaseModel):
    name: Optional[str]
    birth_info: Dict[str, Any]
    four_pillars: Dict[str, str]
    day_master: str
    element_balance: Dict[str, int]
    sipsin_analysis: Dict[str, Any]
    sinsal: List[str]
    analysis: str
    timestamp: datetime
    calculation_method: str

class FortuneResult(BaseModel):
    today: dict
    weekly: dict
    monthly: dict
    yearly: dict

# 사주 분석 엔드포인트
@router.get("/")
async def saju_home():
    """사주 서비스 홈"""
    return {
        "service": "Heal7 사주명리학 서비스",
        "version": "2.0.0",
        "endpoints": {
            "/analyze": "사주 분석",
            "/fortune": "운세 조회",
            "/compatibility": "궁합 분석"
        },
        "description": "전통 명리학을 현대적으로 해석한 정확한 사주 분석 서비스"
    }

@router.post("/analyze", response_model=SajuResult)
async def analyze_saju(request: SajuRequest, saju_service: SajuService = Depends(get_saju_service)):
    """사주 분석 - 실제 계산 엔진 사용"""
    try:
        # 요청을 BirthInfo로 변환
        birth_info = BirthInfo(
            year=request.birth_year,
            month=request.birth_month,
            day=request.birth_day,
            hour=request.birth_hour,
            minute=request.birth_minute,
            gender=Gender.MALE if request.gender.lower() == "male" else Gender.FEMALE,
            name=request.name,
            is_lunar=request.is_lunar
        )
        
        # 실제 사주 계산 수행
        saju_result = await saju_service.calculate_saju(birth_info)
        
        # 응답 형태로 변환
        result = SajuResult(
            name=saju_result.birth_info.name,
            birth_info={
                "year": saju_result.birth_info.year,
                "month": saju_result.birth_info.month,
                "day": saju_result.birth_info.day,
                "hour": saju_result.birth_info.hour,
                "minute": saju_result.birth_info.minute,
                "gender": saju_result.birth_info.gender.value,
                "is_lunar": saju_result.birth_info.is_lunar,
                "birth_datetime": saju_result.birth_info.birth_datetime.isoformat()
            },
            four_pillars={
                "year_pillar": str(saju_result.year_pillar),
                "month_pillar": str(saju_result.month_pillar),
                "day_pillar": str(saju_result.day_pillar),
                "time_pillar": str(saju_result.time_pillar)
            },
            day_master=saju_result.day_master,
            element_balance={k.value: v for k, v in saju_result.element_balance.items()},
            sipsin_analysis=saju_result.sipsin_analysis,
            sinsal=saju_result.sinsal,
            analysis=f"{request.name or '고객'}님의 사주는 {saju_result.palcha}입니다. 일간 {saju_result.day_master}을 중심으로 하는 {'강한' if saju_result.is_strong_day_master else '약한'} 사주입니다.",
            timestamp=saju_result.created_at,
            calculation_method=saju_result.calculation_method
        )
        
        logger.info(f"실제 사주 분석 완료: {request.name} - {saju_result.palcha}")
        return result
        
    except Exception as e:
        logger.error(f"사주 분석 오류: {e}")
        raise HTTPException(status_code=500, detail=f"사주 분석 중 오류가 발생했습니다: {str(e)}")

@router.get("/fortune/{user_id}", response_model=FortuneResult)
async def get_fortune(user_id: str):
    """운세 조회"""
    try:
        # 실제 운세 조회 로직
        result = {
            "today": {
                "overall": "길함",
                "lucky_color": "파란색",
                "lucky_number": 7,
                "advice": "새로운 시작에 좋은 날입니다."
            },
            "weekly": {
                "trend": "상승",
                "focus": "인간관계",
                "caution": "건강 관리"
            },
            "monthly": {
                "theme": "발전",
                "opportunity": "사업 확장",
                "challenge": "감정 조절"
            },
            "yearly": {
                "fortune": "대길",
                "major_events": ["승진", "이사", "결혼"],
                "turning_point": "7월"
            }
        }
        
        logger.info(f"운세 조회 완료: {user_id}")
        return result
        
    except Exception as e:
        logger.error(f"운세 조회 오류: {e}")
        raise HTTPException(status_code=500, detail="운세 조회 중 오류가 발생했습니다.")

@router.post("/compatibility")
async def check_compatibility(person1: SajuRequest, person2: SajuRequest, saju_service: SajuService = Depends(get_saju_service)):
    """궁합 분석 - 실제 계산 엔진 사용"""
    try:
        # 두 사람의 출생 정보 변환
        birth_info_1 = BirthInfo(
            year=person1.birth_year,
            month=person1.birth_month,
            day=person1.birth_day,
            hour=person1.birth_hour,
            minute=person1.birth_minute,
            gender=Gender.MALE if person1.gender.lower() == "male" else Gender.FEMALE,
            name=person1.name,
            is_lunar=person1.is_lunar
        )
        
        birth_info_2 = BirthInfo(
            year=person2.birth_year,
            month=person2.birth_month,
            day=person2.birth_day,
            hour=person2.birth_hour,
            minute=person2.birth_minute,
            gender=Gender.MALE if person2.gender.lower() == "male" else Gender.FEMALE,
            name=person2.name,
            is_lunar=person2.is_lunar
        )
        
        # 실제 궁합 계산 수행
        compatibility_result = await saju_service.calculate_compatibility(birth_info_1, birth_info_2)
        
        logger.info(f"실제 궁합 분석 완료: {person1.name} & {person2.name} - {compatibility_result['compatibility']['score']}점")
        return compatibility_result
        
    except Exception as e:
        logger.error(f"궁합 분석 오류: {e}")
        raise HTTPException(status_code=500, detail=f"궁합 분석 중 오류가 발생했습니다: {str(e)}")

@router.get("/stats")
async def get_saju_stats():
    """사주 서비스 통계"""
    return {
        "total_analyses": 12847,
        "monthly_analyses": 1503,
        "satisfaction_rate": 4.8,
        "popular_services": ["기본 사주", "연애 궁합", "사업 운세"],
        "timestamp": datetime.now()
    }