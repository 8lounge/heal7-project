"""
Simple Saju Basic API
기본적인 사주 계산 API (사주.heal7.com용)
"""

from fastapi import APIRouter, HTTPException, Query, Path
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime, date
import random

router = APIRouter(prefix="/fortune/saju", tags=["사주"])

class SajuBasicInfo(BaseModel):
    """사주 기본 정보"""
    birth_date: date = Field(..., description="생년월일")
    birth_time: str = Field(..., description="출생시간 (HH:MM)")
    gender: str = Field(..., description="성별 (male/female)")
    name: Optional[str] = Field(None, description="이름")
    lunar_calendar: bool = Field(False, description="음력 여부")

class SajuResult(BaseModel):
    """사주 계산 결과"""
    name: Optional[str]
    birth_info: SajuBasicInfo
    saju_pillars: dict = Field(..., description="사주 사주 (년주, 월주, 일주, 시주)")
    five_elements: dict = Field(..., description="오행 분석")
    ten_gods: dict = Field(..., description="십신 분석")
    overall_fortune: str = Field(..., description="종합 운세")
    personality: List[str] = Field(..., description="성격 특징")
    career_luck: str = Field(..., description="직업운")
    love_luck: str = Field(..., description="애정운")
    wealth_luck: str = Field(..., description="재물운")
    health_advice: str = Field(..., description="건강 조언")

# 간단한 사주 데이터 (실제로는 복잡한 계산 필요)
HEAVENLY_STEMS = ["갑", "을", "병", "정", "무", "기", "경", "신", "임", "계"]
EARTHLY_BRANCHES = ["자", "축", "인", "묘", "진", "사", "오", "미", "신", "유", "술", "해"]
ZODIAC_ANIMALS = ["쥐", "소", "범", "토끼", "용", "뱀", "말", "양", "원숭이", "닭", "개", "돼지"]
FIVE_ELEMENTS = ["목", "화", "토", "금", "수"]

@router.post("/basic", summary="기본 사주 계산")
async def get_basic_saju(saju_info: SajuBasicInfo) -> SajuResult:
    """기본적인 사주 계산과 해석을 제공합니다."""
    
    # 간단한 사주 계산 (실제로는 KASI API나 복잡한 계산 필요)
    year = saju_info.birth_date.year
    month = saju_info.birth_date.month
    day = saju_info.birth_date.day
    
    # 시간 파싱
    try:
        hour = int(saju_info.birth_time.split(':')[0])
    except:
        hour = 12  # 기본값
    
    # 간단한 사주 계산 (실제로는 복잡한 음양오행 계산)
    year_pillar = {
        "heavenly_stem": HEAVENLY_STEMS[year % 10],
        "earthly_branch": EARTHLY_BRANCHES[year % 12],
        "zodiac": ZODIAC_ANIMALS[year % 12]
    }
    
    month_pillar = {
        "heavenly_stem": HEAVENLY_STEMS[month % 10],
        "earthly_branch": EARTHLY_BRANCHES[month % 12]
    }
    
    day_pillar = {
        "heavenly_stem": HEAVENLY_STEMS[day % 10],
        "earthly_branch": EARTHLY_BRANCHES[day % 12]
    }
    
    hour_pillar = {
        "heavenly_stem": HEAVENLY_STEMS[hour % 10],
        "earthly_branch": EARTHLY_BRANCHES[hour % 12]
    }
    
    saju_pillars = {
        "year_pillar": year_pillar,
        "month_pillar": month_pillar, 
        "day_pillar": day_pillar,
        "hour_pillar": hour_pillar
    }
    
    # 오행 분석 (간단화)
    elements_count = {element: 0 for element in FIVE_ELEMENTS}
    # 임의로 오행 분포 생성
    random.seed(hash(str(saju_info.birth_date)))
    for _ in range(8):  # 사주 8자
        element = random.choice(FIVE_ELEMENTS)
        elements_count[element] += 1
    
    five_elements = {
        "distribution": elements_count,
        "dominant_element": max(elements_count, key=elements_count.get),
        "lacking_element": min(elements_count, key=elements_count.get) if min(elements_count.values()) == 0 else None
    }
    
    # 십신 분석 (간단화)
    ten_gods = {
        "main_god": random.choice(["정관", "편관", "정인", "편인", "비견", "겁재", "식신", "상관", "정재", "편재"]),
        "characteristics": ["책임감이 강함", "리더십이 있음", "창의적 사고"]
    }
    
    # 성격 특징
    personality_traits = {
        "목": ["성장 지향적", "유연한 사고", "창의적"],
        "화": ["열정적", "사교적", "활발함"],
        "토": ["안정적", "신중함", "포용력"],
        "금": ["의지가 강함", "결단력", "정의감"],
        "수": ["지혜로움", "적응력", "직관력"]
    }
    
    personality = personality_traits.get(five_elements["dominant_element"], ["균형잡힌 성격"])
    
    # 운세 해석 생성
    overall_fortune = f"{year}년생 {year_pillar['zodiac']}띠로서 {five_elements['dominant_element']}의 기운이 강한 사주입니다. 전체적으로 균형잡힌 운세를 가지고 있습니다."
    
    career_luck = f"{five_elements['dominant_element']} 기운이 강해 창의적이고 지속적인 발전이 가능한 직업이 적합합니다."
    
    love_luck = "진실하고 깊은 관계를 추구하는 성향으로, 신중한 선택을 통해 좋은 인연을 만날 수 있습니다."
    
    wealth_luck = "꾸준한 노력을 통해 안정적인 재물운을 가질 수 있으며, 무리한 투자보다는 착실한 저축이 유리합니다."
    
    health_advice = f"{five_elements['dominant_element']} 기운에 맞는 음식과 생활습관을 유지하고, 스트레스 관리에 주의하세요."
    
    return SajuResult(
        name=saju_info.name,
        birth_info=saju_info,
        saju_pillars=saju_pillars,
        five_elements=five_elements,
        ten_gods=ten_gods,
        overall_fortune=overall_fortune,
        personality=personality,
        career_luck=career_luck,
        love_luck=love_luck,
        wealth_luck=wealth_luck,
        health_advice=health_advice
    )

@router.get("/compatibility", summary="사주 궁합")
async def get_saju_compatibility(
    birth1: date = Query(..., description="첫 번째 사람 생년월일"),
    birth2: date = Query(..., description="두 번째 사람 생년월일"),
    gender1: str = Query(..., description="첫 번째 사람 성별"),
    gender2: str = Query(..., description="두 번째 사람 성별")
) -> dict:
    """두 사람의 사주 궁합을 분석합니다."""
    
    # 간단한 궁합 분석
    year1_element = FIVE_ELEMENTS[birth1.year % 5]
    year2_element = FIVE_ELEMENTS[birth2.year % 5]
    
    # 오행 상생상극 관계
    compatible_elements = {
        "목": ["수", "화"],  # 수생목, 목생화
        "화": ["목", "토"],  # 목생화, 화생토  
        "토": ["화", "금"],  # 화생토, 토생금
        "금": ["토", "수"],  # 토생금, 금생수
        "수": ["금", "목"]   # 금생수, 수생목
    }
    
    is_compatible = year2_element in compatible_elements.get(year1_element, [])
    
    compatibility_score = random.randint(65, 95) if is_compatible else random.randint(45, 75)
    
    zodiac1 = ZODIAC_ANIMALS[birth1.year % 12]
    zodiac2 = ZODIAC_ANIMALS[birth2.year % 12]
    
    return {
        "compatibility_score": compatibility_score,
        "element_analysis": {
            "person1_element": year1_element,
            "person2_element": year2_element,
            "relationship": "상생관계" if is_compatible else "중립관계"
        },
        "zodiac_analysis": {
            "person1_zodiac": zodiac1,
            "person2_zodiac": zodiac2,
            "zodiac_compatibility": "좋은 궁합" if compatibility_score > 70 else "보통 궁합"
        },
        "overall_assessment": f"{zodiac1}띠와 {zodiac2}띠의 조합으로 {compatibility_score}점의 궁합을 보입니다.",
        "advice": "서로의 차이점을 인정하고 소통을 통해 관계를 발전시켜나가세요." if compatibility_score > 60 else "더 많은 대화와 이해가 필요한 관계입니다."
    }

@router.get("/yearly-fortune/{year}", summary="연간 운세")
async def get_yearly_fortune(
    year: int,
    birth_date: date = Query(..., description="생년월일"),
    birth_time: str = Query("12:00", description="출생시간")
) -> dict:
    """특정 년도의 개인 운세를 분석합니다."""
    
    birth_year_element = FIVE_ELEMENTS[birth_date.year % 5]
    target_year_element = FIVE_ELEMENTS[year % 5]
    
    # 간단한 연운 분석
    fortune_score = random.randint(55, 90)
    random.seed(hash(str(birth_date) + str(year)))
    
    monthly_fortune = []
    for month in range(1, 13):
        month_score = random.randint(40, 95)
        monthly_fortune.append({
            "month": month,
            "score": month_score,
            "summary": f"{month}월은 {'좋은' if month_score > 70 else '보통' if month_score > 50 else '주의가 필요한'} 운세입니다."
        })
    
    return {
        "year": year,
        "overall_fortune_score": fortune_score,
        "year_element": target_year_element,
        "birth_element": birth_year_element,
        "element_harmony": "조화로움" if target_year_element == birth_year_element else "변화의 시기",
        "yearly_summary": f"{year}년은 {target_year_element}의 해로 전체적으로 {'안정적이고 발전적인' if fortune_score > 70 else '변화가 많은'} 한 해가 될 것입니다.",
        "key_advice": [
            "꾸준한 노력과 인내가 중요한 시기입니다",
            "새로운 도전보다는 기존 일의 완성에 집중하세요",
            "인간관계에서 갈등을 피하고 조화를 추구하세요"
        ],
        "monthly_fortune": monthly_fortune,
        "lucky_months": [m["month"] for m in monthly_fortune if m["score"] > 80],
        "caution_months": [m["month"] for m in monthly_fortune if m["score"] < 60]
    }