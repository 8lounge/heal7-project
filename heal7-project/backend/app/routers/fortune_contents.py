"""
HEAL7 운세 콘텐츠 API
사주 기반 종합 운세 서비스 (연애운, 결혼운, 궁합, 12지신 등)
"""

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Any
from datetime import datetime, date

router = APIRouter(prefix="/fortune", tags=["운세 콘텐츠"])

# --- 요청/응답 모델들 (간소화) ---

class ZodiacSign(BaseModel):
    """12지신 띠 정보"""
    id: str
    name: str
    chinese_name: str
    emoji: str
    image: str
    element: str
    years: List[int]
    characteristics: List[str]
    personality_traits: List[str]
    suitable_jobs: List[str]
    lucky_colors: List[str]
    lucky_numbers: List[int]
    compatibility: Dict[str, List[str]]
    fortune_2025: Dict[str, str]

class ZodiacCompatibility(BaseModel):
    """띠 궁합 분석"""
    zodiac1: str
    zodiac2: str
    compatibility_score: int
    compatibility_level: str
    analysis: str
    advantages: List[str]
    challenges: List[str]
    advice: List[str]

# --- 12지신 데이터 ---
def get_zodiac_data():
    """12지신 띠 데이터 반환"""
    from app.data.zodiac_data import ZODIAC_DATA, calculate_zodiac, check_compatibility, get_all_zodiac_signs
    return ZODIAC_DATA, calculate_zodiac, check_compatibility, get_all_zodiac_signs

# --- API 엔드포인트들 ---

@router.get("/zodiac-signs", response_model=List[Dict])
async def get_all_zodiac_signs():
    """모든 12지신 띠 정보 조회"""
    try:
        _, _, _, all_signs_func = get_zodiac_data()
        return all_signs_func()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"띠 정보 조회 오류: {str(e)}")

@router.get("/zodiac-by-year/{year}")
async def get_zodiac_by_year(year: int):
    """출생년도로 띠 조회"""
    try:
        zodiac_data, calculate_func, _, _ = get_zodiac_data()
        zodiac_id = calculate_func(year)
        if zodiac_id in zodiac_data:
            return zodiac_data[zodiac_id]
        else:
            raise HTTPException(status_code=404, detail="해당 년도의 띠 정보를 찾을 수 없습니다.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"띠 계산 오류: {str(e)}")

@router.get("/zodiac-compatibility")
async def get_zodiac_compatibility(
    zodiac1: str = Query(..., description="첫 번째 띠"),
    zodiac2: str = Query(..., description="두 번째 띠")
):
    """두 띠 간의 궁합 분석"""
    try:
        _, _, compatibility_func, _ = get_zodiac_data()
        compatibility = compatibility_func(zodiac1, zodiac2)
        return {"zodiac1": zodiac1, "zodiac2": zodiac2, "compatibility": compatibility}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"궁합 분석 오류: {str(e)}")

@router.get("/zodiac-fortune-2025/{zodiac_id}")
async def get_zodiac_fortune_2025(zodiac_id: str):
    """2025년 띠별 운세"""
    try:
        zodiac_data, _, _, _ = get_zodiac_data()
        if zodiac_id not in zodiac_data:
            raise HTTPException(status_code=404, detail="해당 띠를 찾을 수 없습니다.")
        
        zodiac = zodiac_data[zodiac_id]
        return {
            "zodiac_id": zodiac_id,
            "zodiac_name": zodiac.get("name", zodiac_id),
            "year": 2025,
            "fortune": zodiac.get("fortune_2025", {})
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"2025년 운세 조회 오류: {str(e)}")

@router.get("/health")
async def health_check():
    """운세 서비스 헬스 체크"""
    return {"status": "healthy", "service": "fortune_contents", "timestamp": datetime.now().isoformat()}