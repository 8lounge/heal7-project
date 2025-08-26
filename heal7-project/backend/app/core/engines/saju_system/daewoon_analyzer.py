#!/usr/bin/env python3
"""
대운(大運) 계산 및 분석 모듈
- 성별에 따른 순행/역행 대운 계산
- 24절기 기반 대운 시작점 정확 계산
- 10년 주기 대운 분석
"""

from datetime import datetime, date, timedelta
from typing import Dict, List, Tuple, Optional, Any
import logging
from enum import Enum

from .solar_terms_legacy_adapter import solar_terms_adapter, get_solar_term_for_date
from .myeongrihak_constants import (
    JIJI, CHEONGAN, WuXing, SipSin,
    get_cheongan_wuxing, get_jiji_wuxing, get_sipsin_relation,
    normalize_to_hangul
)

logger = logging.getLogger(__name__)

class Gender(Enum):
    """성별 구분"""
    MALE = "male"
    FEMALE = "female"

class DaewoonDirection(Enum):
    """대운 방향"""
    FORWARD = "forward"    # 순행
    BACKWARD = "backward"  # 역행

class DaewoonAnalyzer:
    """대운 분석기"""
    
    def __init__(self):
        # 천간 음양 구분
        self.cheongan_yinyang = {
            "甲": "양", "乙": "음", "丙": "양", "丁": "음", "戊": "양",
            "己": "음", "庚": "양", "辛": "음", "壬": "양", "癸": "음"
        }
        
        # 지지 음양 구분  
        self.jiji_yinyang = {
            "子": "양", "丑": "음", "寅": "양", "卯": "음", "辰": "양", "巳": "음",
            "午": "양", "未": "음", "申": "양", "酉": "음", "戌": "양", "亥": "음"
        }
    
    def calculate_daewoon(self, birth_date: date, birth_time: Tuple[int, int], 
                         gender: Gender, month_pillar: str, is_lunar: bool = False) -> Dict[str, Any]:
        """대운 계산 메인 함수"""
        
        logger.info(f"🌟 대운 계산 시작: {birth_date} {birth_time} ({gender.value})")
        
        try:
            # 1. 대운 방향 결정 (양남음녀 vs 음남양녀)
            direction = self._determine_daewoon_direction(birth_date.year, gender)
            
            # 2. 대운 시작 나이 계산 (24절기 기준)
            start_age = self._calculate_daewoon_start_age(birth_date, birth_time, direction)
            
            # 3. 10년 주기 대운 계산
            daewoon_periods = self._calculate_daewoon_periods(month_pillar, direction, start_age)
            
            # 4. 현재 대운 확인
            current_age = datetime.now().year - birth_date.year + 1  # 한국 나이
            current_daewoon = self._get_current_daewoon(daewoon_periods, current_age)
            
            result = {
                "birth_info": {
                    "date": birth_date.isoformat(),
                    "time": f"{birth_time[0]:02d}:{birth_time[1]:02d}",
                    "gender": gender.value,
                    "is_lunar": is_lunar
                },
                "daewoon_direction": direction.value,
                "start_age": start_age,
                "periods": daewoon_periods,
                "current_age": current_age,
                "current_daewoon": current_daewoon,
                "analysis_summary": self._generate_analysis_summary(daewoon_periods, current_daewoon)
            }
            
            logger.info(f"✅ 대운 계산 완료: {direction.value} 대운, {start_age}세 시작")
            return result
            
        except Exception as e:
            logger.error(f"❌ 대운 계산 오류: {e}")
            return {
                "error": str(e),
                "birth_info": {
                    "date": birth_date.isoformat(),
                    "gender": gender.value
                }
            }
    
    def _determine_daewoon_direction(self, birth_year: int, gender: Gender) -> DaewoonDirection:
        """대운 방향 결정 (양남음녀 vs 음남양녀)"""
        
        # 출생년도 천간으로 음양 판단
        year_idx = (birth_year - 4) % 60  # 갑자(甲子) = 0번째
        year_cheongan = CHEONGAN[year_idx % 10]
        
        # 한자로 변환해서 사용
        year_cheongan_hanja = normalize_to_hangul(year_cheongan)
        if year_cheongan_hanja in ["갑", "병", "무", "경", "임"]:
            year_yinyang = "양"
        else:
            year_yinyang = "음"
        
        logger.info(f"  출생년 천간: {year_cheongan} ({year_yinyang})")
        
        # 양남음녀: 순행, 음남양녀: 역행
        if (gender == Gender.MALE and year_yinyang == "양") or \
           (gender == Gender.FEMALE and year_yinyang == "음"):
            return DaewoonDirection.FORWARD
        else:
            return DaewoonDirection.BACKWARD
    
    def _calculate_daewoon_start_age(self, birth_date: date, birth_time: Tuple[int, int], 
                                    direction: DaewoonDirection) -> int:
        """대운 시작 나이 계산 (24절기 기준)"""
        
        birth_month = birth_date.month
        birth_year = birth_date.year
        
        # 해당 월의 절기 경계 찾기
        month_term = solar_terms_adapter.find_month_boundary(birth_year, birth_month)
        
        if not month_term:
            logger.warning(f"  절기 정보 없음, 기본값 사용: 3세")
            return 3
        
        # 절기 날짜와 출생일 비교
        term_date = month_term['date']
        
        if direction == DaewoonDirection.FORWARD:
            # 순행: 다음 절기까지의 일수
            if birth_date >= term_date:
                # 이번 달 절기 이후 출생 → 다음 달 절기까지
                next_month = birth_month + 1 if birth_month < 12 else 1
                next_year = birth_year if birth_month < 12 else birth_year + 1
                next_term = solar_terms_adapter.find_month_boundary(next_year, next_month)
                
                if next_term:
                    days_to_next_term = (next_term['date'] - birth_date).days
                else:
                    days_to_next_term = 30  # 기본값
            else:
                # 이번 달 절기 이전 출생 → 이번 달 절기까지
                days_to_next_term = (term_date - birth_date).days
        else:
            # 역행: 이전 절기까지의 일수
            if birth_date <= term_date:
                # 이번 달 절기 이전 출생 → 이전 달 절기까지
                prev_month = birth_month - 1 if birth_month > 1 else 12
                prev_year = birth_year if birth_month > 1 else birth_year - 1
                prev_term = solar_terms_adapter.find_month_boundary(prev_year, prev_month)
                
                if prev_term:
                    days_to_prev_term = (birth_date - prev_term['date']).days
                else:
                    days_to_prev_term = 30  # 기본값
            else:
                # 이번 달 절기 이후 출생 → 이번 달 절기까지  
                days_to_prev_term = (birth_date - term_date).days
            
            days_to_next_term = days_to_prev_term
        
        # 일수를 나이로 변환 (3일 = 1년)
        start_age = max(1, round(days_to_next_term / 3))
        
        logger.info(f"  절기 기준일: {term_date}, 간격: {days_to_next_term}일 → {start_age}세")
        
        return start_age
    
    def _calculate_daewoon_periods(self, month_pillar: str, direction: DaewoonDirection, 
                                  start_age: int) -> List[Dict[str, Any]]:
        """10년 주기 대운 계산"""
        
        if len(month_pillar) != 2:
            logger.error(f"월주 형식 오류: {month_pillar}")
            return []
        
        month_cheongan = month_pillar[0]
        month_jiji = month_pillar[1]
        
        # 천간/지지 인덱스 찾기 (한자→한글 변환 후)
        try:
            month_cheongan_hangul = normalize_to_hangul(month_cheongan)
            month_jiji_hangul = normalize_to_hangul(month_jiji)
            
            # 한글로 변환된 것을 다시 한자 리스트에서 찾기
            cheongan_mapping = ["갑", "을", "병", "정", "무", "기", "경", "신", "임", "계"]
            jiji_mapping = ["자", "축", "인", "묘", "진", "사", "오", "미", "신", "유", "술", "해"]
            
            cheongan_idx = cheongan_mapping.index(month_cheongan_hangul)
            jiji_idx = jiji_mapping.index(month_jiji_hangul)
            
        except ValueError as e:
            logger.error(f"월주 인덱스 오류: {e} - {month_cheongan}({month_cheongan_hangul}), {month_jiji}({month_jiji_hangul})")
            return []
        
        periods = []
        
        for i in range(8):  # 8개 대운 (80년)
            period_start_age = start_age + (i * 10)
            period_end_age = period_start_age + 9
            
            if direction == DaewoonDirection.FORWARD:
                # 순행: 다음 간지로
                new_cheongan_idx = (cheongan_idx + i + 1) % 10
                new_jiji_idx = (jiji_idx + i + 1) % 12
            else:
                # 역행: 이전 간지로
                new_cheongan_idx = (cheongan_idx - i - 1) % 10
                new_jiji_idx = (jiji_idx - i - 1) % 12
            
            daewoon_cheongan = CHEONGAN[new_cheongan_idx]
            daewoon_jiji = JIJI[new_jiji_idx]
            daewoon_ganji = daewoon_cheongan + daewoon_jiji
            
            # 대운의 오행/십신 분석
            cheongan_wuxing = get_cheongan_wuxing(daewoon_cheongan)
            jiji_wuxing = get_jiji_wuxing(daewoon_jiji)
            
            # 십신 관계는 일간 기준으로 계산해야 하므로 일단 None으로
            # (상위 함수에서 일간 정보와 함께 계산)
            
            period_info = {
                "period": i + 1,
                "start_age": period_start_age,
                "end_age": period_end_age,
                "age_range": f"{period_start_age}-{period_end_age}세",
                "ganji": daewoon_ganji,
                "cheongan": daewoon_cheongan,
                "jiji": daewoon_jiji,
                "cheongan_wuxing": cheongan_wuxing.value if cheongan_wuxing else None,
                "jiji_wuxing": jiji_wuxing.value if jiji_wuxing else None,
                "dominant_wuxing": None,  # 상위에서 계산
                "sipsin_relation": None,  # 상위에서 계산
                "fortune_level": None,    # 상위에서 계산
                "characteristics": []     # 상위에서 계산
            }
            
            periods.append(period_info)
        
        return periods
    
    def _get_current_daewoon(self, periods: List[Dict], current_age: int) -> Optional[Dict]:
        """현재 나이의 대운 찾기"""
        
        for period in periods:
            if period['start_age'] <= current_age <= period['end_age']:
                return period.copy()
        
        return None
    
    def _generate_analysis_summary(self, periods: List[Dict], current_daewoon: Optional[Dict]) -> Dict[str, Any]:
        """대운 분석 요약 생성"""
        
        summary = {
            "total_periods": len(periods),
            "current_period": None,
            "upcoming_periods": [],
            "key_transition_ages": [],
            "overall_pattern": "미분석"
        }
        
        if current_daewoon:
            summary["current_period"] = {
                "period": current_daewoon['period'],
                "age_range": current_daewoon['age_range'],
                "ganji": current_daewoon['ganji'],
                "dominant_wuxing": current_daewoon.get('dominant_wuxing', '미분류')
            }
        
        # 다가오는 주요 대운 (다음 3개)
        current_period_num = current_daewoon['period'] if current_daewoon else 0
        
        for period in periods:
            if period['period'] > current_period_num and len(summary["upcoming_periods"]) < 3:
                summary["upcoming_periods"].append({
                    "period": period['period'],
                    "age_range": period['age_range'], 
                    "ganji": period['ganji']
                })
        
        # 주요 전환점 (10년 단위)
        for period in periods[:5]:  # 앞의 5개 대운만
            summary["key_transition_ages"].append(period['start_age'])
        
        return summary


def analyze_saju_daewoon(pillars: Dict[str, Any], ilgan: str, birth_date: date,
                        birth_time: Tuple[int, int], gender: str, is_lunar: bool = False) -> Dict[str, Any]:
    """사주 대운 분석 메인 함수 (외부 호출용)"""
    
    analyzer = DaewoonAnalyzer()
    
    # 성별 변환
    try:
        gender_enum = Gender.MALE if gender.lower() == "male" else Gender.FEMALE
    except:
        gender_enum = Gender.MALE  # 기본값
    
    # 월주 추출
    month_pillar = pillars.get('month', {}).get('ganji', '戊寅')
    
    # 기본 대운 계산
    daewoon_result = analyzer.calculate_daewoon(
        birth_date, birth_time, gender_enum, month_pillar, is_lunar
    )
    
    if 'error' in daewoon_result:
        return daewoon_result
    
    # 일간 기준으로 십신 관계 추가 분석
    periods = daewoon_result['periods']
    
    for period in periods:
        cheongan = period['cheongan']
        jiji = period['jiji']
        
        # 십신 관계 계산
        cheongan_sipsin = get_sipsin_relation(ilgan, cheongan)
        
        if cheongan_sipsin:
            period['sipsin_relation'] = cheongan_sipsin.value
            period['sipsin_meaning'] = _get_sipsin_meaning(cheongan_sipsin)
        
        # 우세 오행 결정
        cheongan_wuxing = period['cheongan_wuxing']
        jiji_wuxing = period['jiji_wuxing']
        
        if cheongan_wuxing == jiji_wuxing:
            period['dominant_wuxing'] = cheongan_wuxing
        else:
            period['dominant_wuxing'] = cheongan_wuxing  # 천간이 우세
        
        # 운세 레벨 추정 (십신 기준)
        period['fortune_level'] = _estimate_fortune_level(cheongan_sipsin)
        
        # 특징 키워드
        period['characteristics'] = _generate_period_characteristics(
            cheongan_sipsin, period['dominant_wuxing']
        )
    
    return daewoon_result


def _get_sipsin_meaning(sipsin: SipSin) -> str:
    """십신 의미 설명"""
    meanings = {
        SipSin.BI_JIAN: "동반자, 경쟁, 자립",
        SipSin.GYEOP_JAE: "변화, 도전, 모험",
        SipSin.SIK_SIN: "표현, 재능, 창조",
        SipSin.SANG_GWAN: "혁신, 개혁, 변화",
        SipSin.PYEON_JAE: "기회, 유연성, 적응",
        SipSin.JEONG_JAE: "안정, 축적, 관리",
        SipSin.PYEON_GWAN: "권력, 추진력, 변화",
        SipSin.JEONG_GWAN: "명예, 책임, 질서",
        SipSin.PYEON_IN: "학습, 지혜, 변화",
        SipSin.JEONG_IN: "후원, 보호, 안정"
    }
    return meanings.get(sipsin, "미분류")


def _estimate_fortune_level(sipsin: Optional[SipSin]) -> str:
    """십신 기준 운세 레벨 추정"""
    if not sipsin:
        return "보통"
    
    positive_sipsins = [SipSin.JEONG_GWAN, SipSin.JEONG_JAE, SipSin.JEONG_IN, SipSin.SIK_SIN]
    challenging_sipsins = [SipSin.GYEOP_JAE, SipSin.SANG_GWAN, SipSin.PYEON_GWAN]
    
    if sipsin in positive_sipsins:
        return "길운"
    elif sipsin in challenging_sipsins:
        return "변화운"
    else:
        return "보통"


def _generate_period_characteristics(sipsin: Optional[SipSin], dominant_wuxing: Optional[str]) -> List[str]:
    """대운 기간 특징 키워드 생성"""
    characteristics = []
    
    # 십신 기준 특징
    if sipsin:
        sipsin_chars = {
            SipSin.BI_JIAN: ["협력운", "경쟁"],
            SipSin.GYEOP_JAE: ["변화운", "도전"],
            SipSin.SIK_SIN: ["재능운", "표현"],
            SipSin.SANG_GWAN: ["혁신운", "개혁"],
            SipSin.PYEON_JAE: ["기회운", "유연성"],
            SipSin.JEONG_JAE: ["재물운", "안정"],
            SipSin.PYEON_GWAN: ["권력운", "추진"],
            SipSin.JEONG_GWAN: ["명예운", "책임"],
            SipSin.PYEON_IN: ["학습운", "변화"],
            SipSin.JEONG_IN: ["후원운", "보호"]
        }
        characteristics.extend(sipsin_chars.get(sipsin, []))
    
    # 오행 기준 특징
    if dominant_wuxing:
        wuxing_chars = {
            "목": ["성장", "발전"],
            "화": ["활동", "열정"],
            "토": ["안정", "중심"],
            "금": ["수확", "완성"],
            "수": ["지혜", "유동성"]
        }
        characteristics.extend(wuxing_chars.get(dominant_wuxing, []))
    
    return characteristics[:3]  # 최대 3개만


# Production-ready module - test code removed