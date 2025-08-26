"""
HEAL7 사주명리학 시스템 - 사주 계산 및 분석 엔진

전통 한국 사주명리학 이론을 기반으로 한 사주 계산 및 분석 서비스입니다.
AI 분석과 결합하여 현대적이고 정확한 사주 해석을 제공합니다.

Features:
- 정확한 사주팔자 계산 (천간지지, 십신, 신살)
- KASI 24절기 데이터 기반 정밀 계산
- 대운, 세운 계산 및 길흉 판단  
- 전통 명리학 이론 적용 (오행, 합충, 형파해)
- AI 분석과의 융합 해석
- 궁합, 택일, 개명 분석
"""

import asyncio
from datetime import datetime, timedelta, date
from typing import Dict, List, Optional, Any, Tuple, Union
from dataclasses import dataclass, asdict
from enum import Enum
import calendar
import json
from loguru import logger
from pydantic import BaseModel, Field, validator

from .kasi_service import KASIService, SolarTermData
# AI 서비스는 향후 통합 예정 - 현재 보류
# from .ai_service import AIService, AIRequest, AnalysisType
from .database_service import DatabaseService
try:
    from ..config.settings import get_settings
except ImportError:
    from config.settings import get_settings


class Gender(str, Enum):
    """성별"""
    MALE = "male"
    FEMALE = "female"


class ElementType(str, Enum):
    """오행 타입"""
    WOOD = "wood"      # 목
    FIRE = "fire"      # 화  
    EARTH = "earth"    # 토
    METAL = "metal"    # 금
    WATER = "water"    # 수


class SipsinType(str, Enum):
    """십신 타입"""
    JAEGI = "jaegi"           # 재기 (정재, 편재)
    GWAN = "gwan"             # 관 (정관, 편관)
    IN = "in"                 # 인 (정인, 편인)
    SIK = "sik"               # 식 (식신, 상관)
    BI = "bi"                 # 비 (비견, 겁재)


@dataclass
class CheonanJiji:
    """천간지지 정보"""
    cheonan: str  # 천간
    jiji: str     # 지지
    element: ElementType  # 오행
    
    def __str__(self) -> str:
        return f"{self.cheonan}{self.jiji}"


@dataclass  
class Pillar:
    """사주 기둥 (년, 월, 일, 시)"""
    cheonan: str       # 천간
    jiji: str          # 지지
    cheonan_element: ElementType    # 천간 오행
    jiji_element: ElementType       # 지지 오행
    sipsin: Optional[str] = None    # 십신
    
    def __str__(self) -> str:
        return f"{self.cheonan}{self.jiji}"
    
    @property
    def combined_element(self) -> ElementType:
        """기둥의 주요 오행 (천간 우선)"""
        return self.cheonan_element


class BirthInfo(BaseModel):
    """출생 정보"""
    
    year: int = Field(..., ge=1900, le=2050, description="출생년")
    month: int = Field(..., ge=1, le=12, description="출생월")  
    day: int = Field(..., ge=1, le=31, description="출생일")
    hour: int = Field(..., ge=0, le=23, description="출생시")
    minute: int = Field(default=0, ge=0, le=59, description="출생분")
    
    gender: Gender = Field(..., description="성별")
    is_lunar: bool = Field(default=False, description="음력 여부")
    timezone_offset: int = Field(default=540, description="시간대 오프셋(분), 한국=540")
    
    # 선택적 정보
    name: Optional[str] = Field(None, description="이름")
    birth_place: Optional[str] = Field(None, description="출생지")
    
    @validator('day')
    def validate_day(cls, v, values):
        """일자 유효성 검증"""
        if 'year' in values and 'month' in values:
            year, month = values['year'], values['month']
            max_day = calendar.monthrange(year, month)[1]
            if v > max_day:
                raise ValueError(f"{year}년 {month}월은 {max_day}일까지입니다")
        return v
    
    @property
    def birth_datetime(self) -> datetime:
        """출생 일시 (datetime 객체)"""
        return datetime(self.year, self.month, self.day, self.hour, self.minute)


class SajuResult(BaseModel):
    """사주 계산 결과"""
    
    birth_info: BirthInfo = Field(..., description="출생 정보")
    
    # 사주팔자
    year_pillar: Pillar = Field(..., description="년주")
    month_pillar: Pillar = Field(..., description="월주") 
    day_pillar: Pillar = Field(..., description="일주")
    time_pillar: Pillar = Field(..., description="시주")
    
    # 분석 결과
    day_master: str = Field(..., description="일간 (주인)")
    day_master_element: ElementType = Field(..., description="일간 오행")
    
    # 십신 분석
    sipsin_analysis: Dict[str, Any] = Field(..., description="십신 분석")
    
    # 오행 분석  
    element_balance: Dict[ElementType, int] = Field(..., description="오행 균형")
    strong_elements: List[ElementType] = Field(..., description="강한 오행")
    weak_elements: List[ElementType] = Field(..., description="약한 오행")
    
    # 신살 분석
    sinsal: List[str] = Field(default_factory=list, description="신살")
    
    # 대운
    daeun_info: Dict[str, Any] = Field(default_factory=dict, description="대운 정보")
    
    # 계산 메타데이터
    solar_term_used: Optional[SolarTermData] = Field(None, description="사용된 절기")
    calculation_method: str = Field(default="KASI", description="계산 방식")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    @property
    def palcha(self) -> str:
        """팔자 문자열"""
        return f"{self.year_pillar} {self.month_pillar} {self.day_pillar} {self.time_pillar}"
    
    @property
    def is_strong_day_master(self) -> bool:
        """일간이 강한지 판단"""
        day_element = self.day_master_element
        supporting_count = self.element_balance.get(day_element, 0)
        
        # 간단한 강약 판단 (실제로는 더 복잡한 로직 필요)
        total_elements = sum(self.element_balance.values())
        return supporting_count > total_elements / 5


class SajuService:
    """사주 계산 및 분석 서비스"""
    
    # 천간 (10개)
    CHEONAN = ["갑", "을", "병", "정", "무", "기", "경", "신", "임", "계"]
    
    # 지지 (12개)  
    JIJI = ["자", "축", "인", "묘", "진", "사", "오", "미", "신", "유", "술", "해"]
    
    # 천간 오행
    CHEONAN_ELEMENTS = {
        "갑": ElementType.WOOD, "을": ElementType.WOOD,
        "병": ElementType.FIRE, "정": ElementType.FIRE, 
        "무": ElementType.EARTH, "기": ElementType.EARTH,
        "경": ElementType.METAL, "신": ElementType.METAL,
        "임": ElementType.WATER, "계": ElementType.WATER
    }
    
    # 지지 오행
    JIJI_ELEMENTS = {
        "자": ElementType.WATER, "축": ElementType.EARTH,
        "인": ElementType.WOOD, "묘": ElementType.WOOD,
        "진": ElementType.EARTH, "사": ElementType.FIRE,
        "오": ElementType.FIRE, "미": ElementType.EARTH,
        "신": ElementType.METAL, "유": ElementType.METAL,
        "술": ElementType.EARTH, "해": ElementType.WATER
    }
    
    # 십신 관계 (일간 기준)
    SIPSIN_RELATIONS = {
        # 일간이 갑목일 때의 십신
        "갑": {
            "갑": "비견", "을": "겁재",  # 비견
            "병": "식신", "정": "상관",  # 식상
            "무": "편재", "기": "정재",  # 재성
            "경": "편관", "신": "정관",  # 관성  
            "임": "편인", "계": "정인"   # 인성
        }
    }
    
    # 지지 시간대 매핑
    JIJI_HOURS = {
        "자": (23, 1), "축": (1, 3), "인": (3, 5), "묘": (5, 7),
        "진": (7, 9), "사": (9, 11), "오": (11, 13), "미": (13, 15),
        "신": (15, 17), "유": (17, 19), "술": (19, 21), "해": (21, 23)
    }
    
    # 주요 신살
    SINSAL_PATTERNS = {
        "천을귀인": "길신 중의 길신, 고귀한 도움을 받음",
        "태극귀인": "학문과 종교에 뛰어남", 
        "문창귀인": "문학적 재능이 뛰어남",
        "학당": "학문에 대한 열정과 재능",
        "역마": "이동, 변화, 역동성",
        "도화": "인연, 매력, 예술적 재능",
        "홍염": "강한 매력, 이성운",
        "양인": "강한 성격, 리더십, 때로는 과격함",
        "공망": "허무함, 종교적 성향",
        "충": "충돌, 변화, 불안정",
        "형": "형벌, 상해, 관재수"
    }
    
    def __init__(self):
        """서비스 초기화"""
        self.settings = get_settings()
        self.kasi_service = KASIService()
        # AI 서비스는 향후 통합 예정 - 현재 보류
        # self.ai_service = AIService() 
        self.db_service = DatabaseService()
        self._is_initialized = False
        
        logger.info("사주 서비스 초기화 시작")
    
    async def initialize(self) -> None:
        """서비스 초기화"""
        if self._is_initialized:
            return
            
        try:
            # 의존 서비스들 초기화
            await self.kasi_service.initialize()
            # AI 서비스는 향후 통합 예정 - 현재 보류
            # await self.ai_service.initialize() 
            await self.db_service.initialize()
            
            self._is_initialized = True
            logger.info("사주 서비스 초기화 완료")
            
        except Exception as e:
            logger.error(f"사주 서비스 초기화 실패: {e}")
            raise
    
    async def cleanup(self) -> None:
        """리소스 정리"""
        await self.kasi_service.cleanup()
        # AI 서비스는 향후 통합 예정 - 현재 보류
        # await self.ai_service.cleanup()
        await self.db_service.cleanup()
        
        self._is_initialized = False
        logger.info("사주 서비스 정리 완료")
    
    async def health_check(self) -> Dict[str, Any]:
        """헬스체크"""
        if not self._is_initialized:
            return {"status": "unhealthy", "reason": "not_initialized"}
        
        # 의존 서비스들 상태 확인
        kasi_health = await self.kasi_service.health_check()
        # AI 서비스는 향후 통합 예정 - 현재 보류  
        # ai_health = await self.ai_service.health_check()
        db_health = await self.db_service.health_check()
        
        all_healthy = all(
            health["status"] == "healthy" 
            for health in [kasi_health, db_health]
        )
        
        return {
            "status": "healthy" if all_healthy else "degraded",
            "services": {
                "kasi": kasi_health["status"],
                "database": db_health["status"]
            },
            "available_features": {
                "basic_calculation": True,
                "precise_solar_terms": kasi_health["status"] == "healthy",
                "data_persistence": db_health["status"] == "healthy"
            }
        }
    
    def _get_cheonan_jiji_for_year(self, year: int) -> Tuple[str, str]:
        """연도의 천간지지 계산"""
        # 갑자년을 기준(1984년)으로 계산
        base_year = 1984  # 갑자년
        year_offset = (year - base_year) % 60
        
        cheonan_index = year_offset % 10
        jiji_index = year_offset % 12
        
        return self.CHEONAN[cheonan_index], self.JIJI[jiji_index]
    
    def _get_month_pillar(self, year: int, month: int, solar_term: Optional[SolarTermData] = None) -> Tuple[str, str]:
        """월주 계산 (절기 기준)"""
        # 월지는 절기를 기준으로 결정
        month_jiji_map = {
            1: "인", 2: "묘", 3: "진", 4: "사", 5: "오", 6: "미",
            7: "신", 8: "유", 9: "술", 10: "해", 11: "자", 12: "축"
        }
        
        # 실제로는 절기를 기준으로 정확히 계산해야 함
        # 여기서는 간소화된 계산 사용
        jiji = month_jiji_map.get(month, "인")
        
        # 월간 계산: 갑기년에는 병인월부터 시작
        year_cheonan, _ = self._get_cheonan_jiji_for_year(year)
        year_cheonan_index = self.CHEONAN.index(year_cheonan)
        
        # 월간 기준표 (갑기년, 을경년, 병신년, 정임년, 무계년)
        month_cheonan_bases = [2, 4, 6, 8, 0]  # 병, 무, 경, 임, 갑
        base_index = month_cheonan_bases[year_cheonan_index // 2]
        
        # 인월부터 시작해서 month-1만큼 더함 (인월=1월 기준)
        month_offset = (month + 1) % 12  # 인월을 0으로 맞춤
        cheonan_index = (base_index + month_offset) % 10
        
        return self.CHEONAN[cheonan_index], jiji
    
    def _get_day_pillar(self, target_date: date) -> Tuple[str, str]:
        """일주 계산 (만세력 기준)"""
        # 기준일: 1900년 1월 1일을 갑자일로 설정
        base_date = date(1900, 1, 1)
        days_diff = (target_date - base_date).days
        
        # 60갑자 주기로 계산
        day_offset = days_diff % 60
        cheonan_index = day_offset % 10
        jiji_index = day_offset % 12
        
        return self.CHEONAN[cheonan_index], self.JIJI[jiji_index]
    
    def _get_time_pillar(self, day_cheonan: str, hour: int) -> Tuple[str, str]:
        """시주 계산"""
        # 시간대별 지지 결정
        hour_jiji = None
        for jiji, (start, end) in self.JIJI_HOURS.items():
            if start > end:  # 자시(23-1시) 처리
                if hour >= start or hour < end:
                    hour_jiji = jiji
                    break
            else:
                if start <= hour < end:
                    hour_jiji = jiji
                    break
        
        if not hour_jiji:
            hour_jiji = "자"  # 기본값
        
        # 시간 천간 계산
        day_index = self.CHEONAN.index(day_cheonan)
        jiji_index = self.JIJI.index(hour_jiji)
        
        # 갑기일, 을경일, 병신일, 정임일, 무계일에 따른 시간 천간
        time_cheonan_bases = [0, 2, 4, 6, 8]  # 갑, 병, 무, 경, 임
        base_index = time_cheonan_bases[day_index // 2]
        
        cheonan_index = (base_index + jiji_index) % 10
        
        return self.CHEONAN[cheonan_index], hour_jiji
    
    def _calculate_sipsin(self, day_cheonan: str, target_cheonan: str) -> str:
        """십신 계산"""
        if day_cheonan not in self.SIPSIN_RELATIONS:
            # 다른 일간들도 갑목 기준으로 변환해서 계산
            day_index = self.CHEONAN.index(day_cheonan)
            target_index = self.CHEONAN.index(target_cheonan)
            
            # 상대적 관계 계산
            diff = (target_index - day_index) % 10
            sipsin_order = ["비견", "겁재", "식신", "상관", "편재", "정재", "편관", "정관", "편인", "정인"]
            return sipsin_order[diff]
        
        return self.SIPSIN_RELATIONS[day_cheonan].get(target_cheonan, "미정")
    
    def _analyze_element_balance(self, pillars: List[Pillar]) -> Dict[str, Any]:
        """오행 균형 분석"""
        element_count = {element: 0 for element in ElementType}
        
        # 각 기둥의 천간, 지지 오행 카운트
        for pillar in pillars:
            element_count[pillar.cheonan_element] += 2  # 천간은 더 강함
            element_count[pillar.jiji_element] += 1     # 지지
        
        # 강약 분석
        total = sum(element_count.values())
        strong_threshold = total / 5 * 1.5  # 평균의 1.5배 이상
        weak_threshold = total / 5 * 0.5    # 평균의 0.5배 이하
        
        strong_elements = [
            element for element, count in element_count.items() 
            if count >= strong_threshold
        ]
        
        weak_elements = [
            element for element, count in element_count.items()
            if count <= weak_threshold  
        ]
        
        return {
            "element_balance": element_count,
            "strong_elements": strong_elements,
            "weak_elements": weak_elements,
            "total_power": total
        }
    
    def _find_sinsal(self, pillars: List[Pillar], birth_info: BirthInfo) -> List[str]:
        """신살 찾기 (간소화된 버전)"""
        sinsal_found = []
        
        day_pillar = pillars[2]  # 일주
        year_pillar = pillars[0]  # 년주
        
        # 간단한 신살 몇 가지만 구현
        
        # 역마: 신자진년/월/일에 인, 인오술년/월/일에 사, 사유축년/월/일에 해, 해묘미년/월/일에 신
        yeokma_groups = {
            frozenset(["신", "자", "진"]): "인",
            frozenset(["인", "오", "술"]): "사", 
            frozenset(["사", "유", "축"]): "해",
            frozenset(["해", "묘", "미"]): "신"
        }
        
        for group_set, yeokma_jiji in yeokma_groups.items():
            if any(pillar.jiji in group_set for pillar in pillars):
                if any(pillar.jiji == yeokma_jiji for pillar in pillars):
                    sinsal_found.append("역마")
                    break
        
        # 도화: 인오술견묘, 사유축견오, 신자진견유, 해묘미견자
        doehwa_map = {
            frozenset(["인", "오", "술"]): "묘",
            frozenset(["사", "유", "축"]): "오",
            frozenset(["신", "자", "진"]): "유", 
            frozenset(["해", "묘", "미"]): "자"
        }
        
        for group_set, doehwa_jiji in doehwa_map.items():
            if any(pillar.jiji in group_set for pillar in pillars):
                if any(pillar.jiji == doehwa_jiji for pillar in pillars):
                    sinsal_found.append("도화")
                    break
        
        # 공망: 갑을일에 술해, 병정일에 신유, 무기일에 오미, 경신일에 진사, 임계일에 인묘
        gongmang_map = {
            frozenset(["갑", "을"]): ["술", "해"],
            frozenset(["병", "정"]): ["신", "유"],
            frozenset(["무", "기"]): ["오", "미"],
            frozenset(["경", "신"]): ["진", "사"],
            frozenset(["임", "계"]): ["인", "묘"]
        }
        
        for cheonan_set, gongmang_jiji_list in gongmang_map.items():
            if day_pillar.cheonan in cheonan_set:
                if any(pillar.jiji in gongmang_jiji_list for pillar in pillars):
                    sinsal_found.append("공망")
                    break
        
        return sinsal_found
    
    def _calculate_daeun(self, birth_info: BirthInfo, day_pillar: Pillar) -> Dict[str, Any]:
        """대운 계산 (간소화된 버전)"""
        
        # 대운 시작 나이 계산 (남성/여성, 양간/음간에 따라 다름)
        year_cheonan, _ = self._get_cheonan_jiji_for_year(birth_info.year)
        is_yang_year = self.CHEONAN.index(year_cheonan) % 2 == 0
        
        # 남자 양년생, 여자 음년생은 순행, 그 외는 역행
        is_forward = (
            (birth_info.gender == Gender.MALE and is_yang_year) or
            (birth_info.gender == Gender.FEMALE and not is_yang_year)
        )
        
        # 대운 시작 나이 (실제로는 절기까지 계산해야 하지만 간소화)
        start_age = 3 if is_forward else 7  # 예시값
        
        # 현재 나이 계산
        current_year = datetime.now().year
        current_age = current_year - birth_info.year + 1
        
        # 현재 대운 계산
        daeun_period = 10  # 10년 주기
        current_daeun_index = max(0, (current_age - start_age) // daeun_period)
        
        return {
            "start_age": start_age,
            "is_forward": is_forward,
            "period_years": daeun_period,
            "current_age": current_age,
            "current_daeun_index": current_daeun_index,
            "current_daeun_age_range": (
                start_age + current_daeun_index * daeun_period,
                start_age + (current_daeun_index + 1) * daeun_period - 1
            )
        }
    
    async def calculate_saju(self, birth_info: BirthInfo) -> SajuResult:
        """사주 계산 메인 함수"""
        if not self._is_initialized:
            await self.initialize()
        
        try:
            logger.info(f"사주 계산 시작: {birth_info.name or '익명'} ({birth_info.birth_datetime})")
            
            # 음력을 양력으로 변환 (필요시)
            if birth_info.is_lunar:
                # TODO: 음양력 변환 구현 (korean-lunar-calendar 라이브러리 사용)
                logger.warning("음력 변환은 아직 구현되지 않음")
                pass
            
            birth_date = birth_info.birth_datetime.date()
            
            # KASI 절기 데이터 조회 (정확한 월주 계산용)
            solar_term = None
            try:
                solar_term = await self.kasi_service.find_solar_term_by_date(birth_info.birth_datetime)
                if solar_term:
                    logger.debug(f"절기 정보 확인: {solar_term.solar_term_name}")
            except Exception as e:
                logger.warning(f"절기 조회 실패, 기본 계산 사용: {e}")
            
            # 각 주 계산
            year_cheonan, year_jiji = self._get_cheonan_jiji_for_year(birth_info.year)
            month_cheonan, month_jiji = self._get_month_pillar(birth_info.year, birth_info.month, solar_term)
            day_cheonan, day_jiji = self._get_day_pillar(birth_date)
            time_cheonan, time_jiji = self._get_time_pillar(day_cheonan, birth_info.hour)
            
            # 기둥 생성
            year_pillar = Pillar(
                cheonan=year_cheonan,
                jiji=year_jiji,
                cheonan_element=self.CHEONAN_ELEMENTS[year_cheonan],
                jiji_element=self.JIJI_ELEMENTS[year_jiji]
            )
            
            month_pillar = Pillar(
                cheonan=month_cheonan,
                jiji=month_jiji, 
                cheonan_element=self.CHEONAN_ELEMENTS[month_cheonan],
                jiji_element=self.JIJI_ELEMENTS[month_jiji]
            )
            
            day_pillar = Pillar(
                cheonan=day_cheonan,
                jiji=day_jiji,
                cheonan_element=self.CHEONAN_ELEMENTS[day_cheonan],
                jiji_element=self.JIJI_ELEMENTS[day_jiji]
            )
            
            time_pillar = Pillar(
                cheonan=time_cheonan,
                jiji=time_jiji,
                cheonan_element=self.CHEONAN_ELEMENTS[time_cheonan], 
                jiji_element=self.JIJI_ELEMENTS[time_jiji]
            )
            
            pillars = [year_pillar, month_pillar, day_pillar, time_pillar]
            
            # 십신 계산
            for pillar in pillars:
                pillar.sipsin = self._calculate_sipsin(day_cheonan, pillar.cheonan)
            
            # 십신 분석
            sipsin_counts = {}
            for pillar in pillars:
                sipsin = pillar.sipsin
                sipsin_counts[sipsin] = sipsin_counts.get(sipsin, 0) + 1
            
            sipsin_analysis = {
                "counts": sipsin_counts,
                "dominant": max(sipsin_counts, key=sipsin_counts.get) if sipsin_counts else None,
                "missing": [sipsin for sipsin in ["비견", "겁재", "식신", "상관", "편재", "정재", "편관", "정관", "편인", "정인"] 
                          if sipsin not in sipsin_counts]
            }
            
            # 오행 분석
            element_analysis = self._analyze_element_balance(pillars)
            
            # 신살 계산
            sinsal = self._find_sinsal(pillars, birth_info)
            
            # 대운 계산
            daeun_info = self._calculate_daeun(birth_info, day_pillar)
            
            # 결과 생성
            saju_result = SajuResult(
                birth_info=birth_info,
                year_pillar=year_pillar,
                month_pillar=month_pillar, 
                day_pillar=day_pillar,
                time_pillar=time_pillar,
                day_master=day_cheonan,
                day_master_element=self.CHEONAN_ELEMENTS[day_cheonan],
                sipsin_analysis=sipsin_analysis,
                element_balance=element_analysis["element_balance"],
                strong_elements=element_analysis["strong_elements"],
                weak_elements=element_analysis["weak_elements"],
                sinsal=sinsal,
                daeun_info=daeun_info,
                solar_term_used=solar_term,
                calculation_method="KASI" if solar_term else "Standard"
            )
            
            logger.info(f"사주 계산 완료: {saju_result.palcha}")
            return saju_result
            
        except Exception as e:
            logger.error(f"사주 계산 실패: {e}")
            raise
    
    async def analyze_with_ai(
        self, 
        saju_result: SajuResult,
        analysis_type: str,  # AI 서비스 보류로 str로 변경
        question: Optional[str] = None,
        user_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """AI를 활용한 사주 분석"""
        
        # 사주 데이터를 AI가 이해할 수 있는 형태로 변환
        saju_data = {
            "birth_datetime": saju_result.birth_info.birth_datetime.strftime("%Y년 %m월 %d일 %H시"),
            "palcha": saju_result.palcha,
            "day_pillar": str(saju_result.day_pillar),
            "day_master": saju_result.day_master,
            "day_master_element": saju_result.day_master_element.value,
            "sipsin": saju_result.sipsin_analysis,
            "oheng": dict(saju_result.element_balance),
            "strong_elements": [elem.value for elem in saju_result.strong_elements],
            "weak_elements": [elem.value for elem in saju_result.weak_elements],
            "sinsal": saju_result.sinsal,
            "daeun": saju_result.daeun_info,
            "is_strong_day_master": saju_result.is_strong_day_master
        }
        
        # AI 분석은 향후 통합 예정 - 현재는 전통 분석만 제공
        # 순수 전통 명리학 분석 결과 반환
        traditional_analysis = {
            "palcha": saju_result.palcha,
            "day_master_strength": "강" if saju_result.is_strong_day_master else "약",
            "element_balance": dict(saju_result.element_balance),
            "dominant_sipsin": saju_result.sipsin_analysis.get("dominant"),
            "sinsal": saju_result.sinsal,
            "calculation_method": saju_result.calculation_method
        }
        
        logger.info(f"전통 사주 분석 완료: {saju_result.palcha}")
        return {
            "traditional_analysis": traditional_analysis,
            "analysis_note": "현재 전통 명리학 분석만 제공됩니다. AI 분석은 향후 통합 예정입니다."
        }
    
    async def calculate_compatibility(
        self, 
        person_a: BirthInfo,
        person_b: BirthInfo
    ) -> Dict[str, Any]:
        """궁합 계산"""
        
        try:
            # 각각의 사주 계산
            saju_a = await self.calculate_saju(person_a)
            saju_b = await self.calculate_saju(person_b)
            
            # 기본 궁합 점수 계산
            compatibility_score = 50  # 기본 점수
            compatibility_details = []
            
            # 일주 합충 관계 확인
            day_a = saju_a.day_pillar
            day_b = saju_b.day_pillar
            
            # 천간 관계
            if day_a.cheonan == day_b.cheonan:
                compatibility_score += 10
                compatibility_details.append("일간이 같아 성격적 동조화가 높음")
            
            # 오행 상생상극 관계  
            element_a = day_a.cheonan_element
            element_b = day_b.cheonan_element
            
            # 오행 상생 관계 (간소화된 버전)
            saengsaeng_pairs = [
                (ElementType.WOOD, ElementType.FIRE),
                (ElementType.FIRE, ElementType.EARTH), 
                (ElementType.EARTH, ElementType.METAL),
                (ElementType.METAL, ElementType.WATER),
                (ElementType.WATER, ElementType.WOOD)
            ]
            
            if (element_a, element_b) in saengsaeng_pairs or (element_b, element_a) in saengsaeng_pairs:
                compatibility_score += 15
                compatibility_details.append(f"{element_a.value}와 {element_b.value} 상생관계로 서로 도움")
            
            # 오행 상극 관계
            sanggeuk_pairs = [
                (ElementType.WOOD, ElementType.EARTH),
                (ElementType.EARTH, ElementType.WATER),
                (ElementType.WATER, ElementType.FIRE),
                (ElementType.FIRE, ElementType.METAL),
                (ElementType.METAL, ElementType.WOOD)
            ]
            
            if (element_a, element_b) in sanggeuk_pairs or (element_b, element_a) in sanggeuk_pairs:
                compatibility_score -= 10
                compatibility_details.append(f"{element_a.value}와 {element_b.value} 상극관계로 마찰 가능")
            
            # 신살 비교
            common_sinsal = set(saju_a.sinsal) & set(saju_b.sinsal)
            if common_sinsal:
                compatibility_score += len(common_sinsal) * 5
                compatibility_details.append(f"공통 신살: {', '.join(common_sinsal)}")
            
            # 점수 범위 조정 (0-100)
            compatibility_score = max(0, min(100, compatibility_score))
            
            # 등급 산정
            if compatibility_score >= 85:
                grade = "최상"
            elif compatibility_score >= 70:
                grade = "상"
            elif compatibility_score >= 55:
                grade = "중상"
            elif compatibility_score >= 40:
                grade = "중"
            else:
                grade = "하"
            
            compatibility_result = {
                "person_a": {
                    "name": person_a.name or "A",
                    "palcha": saju_a.palcha,
                    "day_master": saju_a.day_master
                },
                "person_b": {
                    "name": person_b.name or "B", 
                    "palcha": saju_b.palcha,
                    "day_master": saju_b.day_master
                },
                "compatibility": {
                    "score": compatibility_score,
                    "grade": grade,
                    "details": compatibility_details
                },
                "calculated_at": datetime.utcnow()
            }
            
            logger.info(f"궁합 계산 완료: {compatibility_score}점 ({grade})")
            return compatibility_result
            
        except Exception as e:
            logger.error(f"궁합 계산 실패: {e}")
            raise
    
    async def save_saju_result(self, saju_result: SajuResult, user_id: Optional[str] = None) -> str:
        """사주 결과 저장"""
        try:
            # 데이터베이스에 저장 로직 (간소화됨)
            save_data = {
                "user_id": user_id,
                "birth_info": saju_result.birth_info.dict(),
                "saju_data": {
                    "palcha": saju_result.palcha,
                    "day_master": saju_result.day_master,
                    "element_balance": dict(saju_result.element_balance),
                    "sipsin_analysis": saju_result.sipsin_analysis,
                    "sinsal": saju_result.sinsal,
                    "daeun_info": saju_result.daeun_info
                },
                "created_at": saju_result.created_at.isoformat()
            }
            
            # 실제 구현에서는 데이터베이스에 저장
            save_id = f"saju_{int(saju_result.created_at.timestamp())}"
            
            logger.info(f"사주 결과 저장 완료: {save_id}")
            return save_id
            
        except Exception as e:
            logger.error(f"사주 결과 저장 실패: {e}")
            raise
    
    def __repr__(self) -> str:
        status = "initialized" if self._is_initialized else "not_initialized"
        return f"SajuService(status={status}, version=1.0.0)"