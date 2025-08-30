"""
HEAL7 운세 콘텐츠 API
사주 기반 종합 운세 서비스 (연애운, 결혼운, 궁합, 12지신 등)
"""

from fastapi import APIRouter, HTTPException, Query, Depends
from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Literal, Union, Any
from datetime import datetime, date
from enum import Enum

router = APIRouter(prefix="/fortune", tags=["운세 콘텐츠"])

# --- 요청/응답 모델들 ---

class Gender(Enum):
    MALE = "male"
    FEMALE = "female"

class BirthInfo(BaseModel):
    """출생 정보"""
    birth_date: date = Field(..., description="생년월일")
    birth_time: str = Field(..., description="출생시간 (HH:MM)")
    gender: Gender = Field(..., description="성별")
    name: Optional[str] = Field(None, description="이름")
    lunar_calendar: bool = Field(False, description="음력 여부")

class PersonalityProfile(BaseModel):
    """통합 성격 프로파일"""
    mbti_type: str = Field(..., description="MBTI 유형")
    saju_element: str = Field(..., description="사주 오행")
    personality_summary: str = Field(..., description="성격 종합 분석")
    strengths: List[str] = Field(..., description="강점들")
    weaknesses: List[str] = Field(..., description="약점들")
    growth_directions: List[str] = Field(..., description="성장 방향")
    famous_people: List[str] = Field(default_factory=list, description="동일 유형 유명인")

class ZodiacAnalysis(BaseModel):
    """십이지신 분석"""
    zodiac_animal: str = Field(..., description="띠")
    animal_character: str = Field(..., description="동물 캐릭터 설명")
    basic_traits: List[str] = Field(..., description="기본 성향")
    hidden_potential: List[str] = Field(..., description="숨겨진 잠재력")
    career_luck: str = Field(..., description="직업운")
    year_fortune: str = Field(..., description="연도별 총운")
    lucky_colors: List[str] = Field(default_factory=list)
    lucky_numbers: List[int] = Field(default_factory=list)

class SasangConstitution(BaseModel):
    """사상체질 진단"""
    constitution_type: Literal["태양인", "태음인", "소양인", "소음인"]
    characteristics: List[str] = Field(..., description="체질 특징")
    recommended_foods: List[str] = Field(..., description="추천 음식")
    avoid_foods: List[str] = Field(..., description="피해야 할 음식")
    exercise_tips: List[str] = Field(..., description="운동법")
    health_advice: List[str] = Field(..., description="건강 조언")

class DailyFortune(BaseModel):
    """오늘의 운세"""
    date: date = Field(..., description="운세 날짜")
    overall_score: int = Field(..., description="종합운 점수 (1-100)")
    wealth_score: int = Field(..., description="재물운 점수")
    love_score: int = Field(..., description="애정운 점수")
    health_score: int = Field(..., description="건강운 점수")
    advice: str = Field(..., description="오늘의 조언")
    lucky_item: str = Field(..., description="행운의 아이템")
    biorhythm: Dict[str, float] = Field(..., description="바이오리듬 (신체/감성/지성)")

class LoveFortuneAnalysis(BaseModel):
    """연애운 분석"""
    love_tendency: str = Field(..., description="연애 성향")
    ideal_partner_type: str = Field(..., description="이상형")
    meeting_period: str = Field(..., description="인연을 만날 시기")
    love_advice: List[str] = Field(..., description="연애 조언")
    compatibility_tips: List[str] = Field(..., description="궁합 팁")

class MarriageFortuneAnalysis(BaseModel):
    """결혼운 분석"""
    best_marriage_age: str = Field(..., description="최적 결혼 시기")
    ideal_spouse: str = Field(..., description="배우자상")
    marriage_success_factors: List[str] = Field(..., description="결혼 성공 요인")
    potential_challenges: List[str] = Field(..., description="주의사항")
    happiness_tips: List[str] = Field(..., description="행복한 결혼 팁")

class CompatibilityAnalysis(BaseModel):
    """궁합 분석"""
    compatibility_score: int = Field(..., description="궁합 점수 (1-100)")
    overall_assessment: str = Field(..., description="종합 평가")
    strengths: List[str] = Field(..., description="장점")
    challenges: List[str] = Field(..., description="갈등 요소")
    improvement_tips: List[str] = Field(..., description="관계 개선 방법")
    long_term_outlook: str = Field(..., description="장기적 전망")

# --- API 엔드포인트들 ---

@router.post("/zodiac-analysis", summary="십이지신 분석")
async def get_zodiac_analysis(birth_info: BirthInfo) -> ZodiacAnalysis:
    """띠를 통한 기본 성향과 운세를 분석합니다."""
    
    # 띠 계산 로직 (간단화)
    year = birth_info.birth_date.year
    zodiac_animals = ["원숭이", "닭", "개", "돼지", "쥐", "소", "범", "토끼", "용", "뱀", "말", "양"]
    zodiac_animal = zodiac_animals[year % 12]
    
    # 띠별 분석 데이터 (실제로는 DB나 설정에서 가져와야 함)
    zodiac_data = {
        "쥐": {
            "character": "영리하고 기민한 쥐의 성질로 적응력이 뛰어나고 기회를 잘 포착합니다",
            "traits": ["영리함", "기민함", "사교성", "현실적"],
            "potential": ["리더십", "사업가적 기질", "창의력"],
            "career": "다양한 분야에서 성공 가능, 특히 사업이나 기획 분야",
            "year_fortune": "2025년에는 새로운 기회가 많은 해입니다"
        },
        # ... 다른 띠들도 추가
    }
    
    data = zodiac_data.get(zodiac_animal, zodiac_data["쥐"])  # 기본값
    
    return ZodiacAnalysis(
        zodiac_animal=zodiac_animal,
        animal_character=data["character"],
        basic_traits=data["traits"],
        hidden_potential=data["potential"],
        career_luck=data["career"],
        year_fortune=data["year_fortune"],
        lucky_colors=["빨강", "금색"],
        lucky_numbers=[7, 14, 21]
    )

@router.post("/personality-profile", summary="통합 성격 프로파일")
async def get_personality_profile(
    birth_info: BirthInfo,
    mbti_type: str = Query(..., description="MBTI 유형 (예: INFP)")
) -> PersonalityProfile:
    """MBTI와 사주를 결합한 통합 성격 프로파일을 제공합니다."""
    
    # 간단한 사주 오행 계산 (실제로는 복잡한 로직 필요)
    elements = ["목", "화", "토", "금", "수"]
    saju_element = elements[birth_info.birth_date.year % 5]
    
    # MBTI와 사주 오행 조합 분석
    personality_combinations = {
        "INFP": {
            "목": "이상주의적 성향과 성장 지향적 기질이 결합되어 창의적 표현에 뛰어납니다",
            "화": "따뜻한 감성과 열정적 기질로 사람들에게 영감을 주는 존재입니다"
        }
        # ... 다른 조합들
    }
    
    combo_key = f"{mbti_type}_{saju_element}"
    summary = personality_combinations.get(mbti_type, {}).get(saju_element, 
        f"{mbti_type} 유형과 {saju_element}의 기운이 조화를 이루는 독특한 성격입니다")
    
    return PersonalityProfile(
        mbti_type=mbti_type,
        saju_element=saju_element,
        personality_summary=summary,
        strengths=["깊은 내면의 가치관", "창의적 사고", "따뜻한 공감 능력"],
        weaknesses=["과도한 완벽주의", "결정 장애", "스트레스 민감성"],
        growth_directions=["자신감 향상", "현실적 목표 설정", "소통 능력 개발"],
        famous_people=["이효리", "아이유", "김연아"]
    )

@router.post("/sasang-constitution", summary="사상체질 진단")
async def get_sasang_constitution(birth_info: BirthInfo) -> SasangConstitution:
    """간단한 사상체질 진단을 제공합니다."""
    
    # 간단한 체질 분류 로직 (실제로는 더 복잡한 설문이나 계산 필요)
    constitutions = ["태양인", "태음인", "소양인", "소음인"]
    constitution = constitutions[birth_info.birth_date.month % 4]
    
    constitution_data = {
        "소음인": {
            "characteristics": ["소화기가 약함", "몸이 차가움", "내성적 성향", "섬세함"],
            "recommended_foods": ["생강차", "계피차", "따뜻한 음식", "닭고기", "양고기"],
            "avoid_foods": ["찬 음료", "생선회", "돼지고기", "찬 과일"],
            "exercise_tips": ["가벼운 산책", "요가", "스트레칭", "실내 운동"],
            "health_advice": ["몸을 따뜻하게 유지", "충분한 수면", "스트레스 관리", "규칙적인 식사"]
        }
        # ... 다른 체질들
    }
    
    data = constitution_data.get(constitution, constitution_data["소음인"])
    
    return SasangConstitution(
        constitution_type=constitution,
        characteristics=data["characteristics"],
        recommended_foods=data["recommended_foods"],
        avoid_foods=data["avoid_foods"],
        exercise_tips=data["exercise_tips"],
        health_advice=data["health_advice"]
    )

@router.get("/daily-fortune", summary="오늘의 운세")
async def get_daily_fortune(
    birth_date: date = Query(..., description="생년월일"),
    target_date: Optional[date] = Query(None, description="운세를 볼 날짜")
) -> DailyFortune:
    """특정 날짜의 개인 맞춤 운세를 제공합니다."""
    
    # 간단한 운세 계산 (실제로는 복잡한 사주 계산 필요)
    if target_date is None:
        target_date = date.today()
    
    import random
    random.seed(hash(str(birth_date) + str(target_date)))
    
    overall_score = random.randint(60, 95)
    wealth_score = random.randint(50, 90)
    love_score = random.randint(55, 88)
    health_score = random.randint(65, 95)
    
    return DailyFortune(
        date=target_date,
        overall_score=overall_score,
        wealth_score=wealth_score,
        love_score=love_score,
        health_score=health_score,
        advice="오늘은 새로운 시작에 좋은 날입니다. 계획했던 일들을 실행에 옮겨보세요.",
        lucky_item="빨간색 액세서리",
        biorhythm={
            "physical": random.uniform(0.3, 0.9),
            "emotional": random.uniform(0.4, 0.8), 
            "intellectual": random.uniform(0.5, 0.9)
        }
    )

@router.post("/love-fortune", summary="연애운 분석")
async def get_love_fortune(birth_info: BirthInfo) -> LoveFortuneAnalysis:
    """개인의 연애 성향과 연애운을 분석합니다."""
    
    return LoveFortuneAnalysis(
        love_tendency="진실하고 깊은 사랑을 추구하는 타입으로, 상대방과의 정신적 교감을 중요시합니다.",
        ideal_partner_type="지적이고 따뜻한 성격의 파트너, 서로의 꿈을 응원해주는 관계",
        meeting_period="2025년 봄~여름이 새로운 인연을 만나기에 좋은 시기입니다.",
        love_advice=[
            "자신의 매력에 자신감을 가지세요",
            "상대방의 이야기를 진심으로 들어주세요", 
            "완벽함보다는 진실함을 추구하세요"
        ],
        compatibility_tips=[
            "공통의 관심사를 찾아보세요",
            "서로의 차이점을 인정하고 받아들이세요",
            "소통을 통해 오해를 풀어나가세요"
        ]
    )

@router.post("/marriage-fortune", summary="결혼운 분석") 
async def get_marriage_fortune(birth_info: BirthInfo) -> MarriageFortuneAnalysis:
    """결혼 시기와 배우자상, 결혼 생활에 대한 분석을 제공합니다."""
    
    age = datetime.now().year - birth_info.birth_date.year + 1
    best_age_range = f"{age + 2}-{age + 5}세"
    
    return MarriageFortuneAnalysis(
        best_marriage_age=best_age_range,
        ideal_spouse="신중하고 책임감 있는 성격으로, 가정을 소중히 여기는 파트너",
        marriage_success_factors=[
            "서로에 대한 깊은 이해와 배려",
            "공통된 가치관과 목표",
            "원활한 소통과 갈등 해결 능력"
        ],
        potential_challenges=[
            "과도한 완벽주의로 인한 갈등",
            "가족 간의 의견 차이",
            "경제적 가치관의 차이"
        ],
        happiness_tips=[
            "서로의 개성을 존중하고 인정하기",
            "정기적인 대화 시간 갖기", 
            "함께 할 수 있는 취미 찾기"
        ]
    )

@router.post("/compatibility", summary="궁합 분석")
async def get_compatibility_analysis(
    person1: BirthInfo = Field(..., description="첫 번째 사람 정보"),
    person2: BirthInfo = Field(..., description="두 번째 사람 정보"),
    relationship_type: Literal["연인", "부부", "가족", "친구", "동료"] = Query("연인", description="관계 유형")
) -> CompatibilityAnalysis:
    """두 사람의 궁합을 상세히 분석합니다."""
    
    # 간단한 궁합 계산 (실제로는 복잡한 사주 계산 필요)
    import random
    seed = hash(str(person1.birth_date) + str(person2.birth_date))
    random.seed(seed)
    
    compatibility_score = random.randint(65, 95)
    
    return CompatibilityAnalysis(
        compatibility_score=compatibility_score,
        overall_assessment="두 분은 서로 다른 매력을 가지고 있어 상호 보완적인 관계를 만들어갈 수 있습니다.",
        strengths=[
            "서로의 장점을 잘 보완함",
            "깊은 정신적 교감 가능", 
            "함께 성장할 수 있는 관계"
        ],
        challenges=[
            "성격 차이로 인한 초기 갈등",
            "의사소통 방식의 차이",
            "가치관의 미묘한 차이"
        ],
        improvement_tips=[
            "서로의 차이점을 인정하고 받아들이기",
            "정기적인 진솔한 대화 시간 갖기",
            "공통의 목표와 관심사 만들기"
        ],
        long_term_outlook="시간이 지날수록 더욱 깊어지는 관계로 발전할 가능성이 높습니다."
    )

@router.post("/family-compatibility", summary="가족 궁합 분석")
async def get_family_compatibility(
    family_members: List[BirthInfo] = Field(..., description="가족 구성원들의 출생 정보")
) -> dict:
    """가족 구성원 전체의 궁합과 역할을 분석합니다."""
    
    if len(family_members) < 2:
        raise HTTPException(status_code=400, detail="최소 2명 이상의 가족 구성원 정보가 필요합니다.")
    
    # 가족 구성원별 역할과 상호작용 분석
    family_analysis = {
        "family_harmony_score": 78,
        "overall_assessment": "가족 구성원들이 서로 다른 강점을 가지고 있어 조화로운 가정을 이룰 수 있습니다.",
        "member_roles": [
            {"name": member.name or f"가족{i+1}", "role": "조화를 이끄는 역할", "contribution": "가족의 균형 유지"}
            for i, member in enumerate(family_members)
        ],
        "family_strengths": [
            "서로 다른 재능으로 상호 보완",
            "깊은 가족 유대감",
            "공통된 가치관"
        ],
        "potential_conflicts": [
            "세대 간 가치관 차이",
            "의사소통 방식의 차이"
        ],
        "harmony_tips": [
            "정기적인 가족 회의 시간 갖기",
            "각자의 개성을 존중하기",
            "함께 할 수 있는 활동 늘리기"
        ]
    }
    
    return family_analysis

# --- 추가 특수 궁합 분석들 ---

@router.post("/in-laws-compatibility", summary="시부모/장서 궁합")
async def get_in_laws_compatibility(
    person: BirthInfo = Field(..., description="본인 정보"),
    in_law: BirthInfo = Field(..., description="시부모/장서 정보")
) -> CompatibilityAnalysis:
    """결혼 후 시부모/장서와의 관계 분석과 소통 방법을 제안합니다."""
    
    return CompatibilityAnalysis(
        compatibility_score=72,
        overall_assessment="서로 다른 세대의 지혜와 활력이 만나 좋은 시너지를 낼 수 있는 관계입니다.",
        strengths=[
            "상호 존중하는 관계",
            "경험과 활력의 조화",
            "가족을 위한 공통된 관심"
        ],
        challenges=[
            "세대 간 가치관 차이",
            "소통 방식의 차이",
            "생활 패턴의 차이"
        ],
        improvement_tips=[
            "상대방의 입장에서 생각해보기",
            "작은 관심과 배려 표현하기",
            "전통과 현대의 절충점 찾기",
            "정기적인 안부 인사하기"
        ],
        long_term_outlook="시간이 지나면서 서로를 더 잘 이해하게 되는 관계로 발전할 것입니다."
    )

@router.post("/workplace-compatibility", summary="직장 동료 궁합")
async def get_workplace_compatibility(
    person1: BirthInfo = Field(..., description="첫 번째 사람"),
    person2: BirthInfo = Field(..., description="두 번째 사람"),
    work_relationship: Literal["동료", "상사-부하", "팀원", "파트너"] = Query("동료")
) -> dict:
    """직장에서의 협업 관계와 시너지 분석을 제공합니다."""
    
    return {
        "collaboration_score": 85,
        "work_synergy": "서로 다른 강점을 가져 업무에서 좋은 보완 관계를 형성할 수 있습니다.",
        "role_suggestions": {
            person1.name or "첫 번째 사람": "아이디어 기획과 전략 수립",
            person2.name or "두 번째 사람": "실행과 마무리 담당"
        },
        "communication_tips": [
            "명확하고 구체적인 의사소통",
            "정기적인 진행 상황 공유",
            "서로의 업무 스타일 이해하기"
        ],
        "conflict_prevention": [
            "역할과 책임 명확히 하기",
            "의견 충돌 시 객관적 근거 제시",
            "개인적 감정과 업무 분리하기"
        ],
        "success_factors": [
            "상호 존중과 신뢰",
            "공통 목표 설정",
            "각자의 전문성 인정"
        ]
    }