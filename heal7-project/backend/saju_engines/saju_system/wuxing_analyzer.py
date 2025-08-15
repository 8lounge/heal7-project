#!/usr/bin/env python3
"""
오행(五行) 분석 시스템
- 오행 균형 분석
- 계절별 왕상휴수사 분석
- 상생상극 관계 분석
- 세력 점수 계산
"""

from typing import Dict, List, Tuple, Any
from enum import Enum
from .myeongrihak_constants import (
    WuXing, 
    CHEONGAN_WUXING, 
    JIJI_WUXING,
    JIJANGGAN,
    SEASONAL_WUXING_STRENGTH,
    WUXING_SAENGSAENG,
    WUXING_SANGGEUK,
    get_season_by_month,
    get_wuxing_strength_in_season,
    get_cheongan_wuxing,
    get_jiji_wuxing,
    get_jijanggan
)

class WuXingStrength(Enum):
    """오행 세력"""
    WANG = "왕"    # 旺
    SANG = "상"    # 相
    HYU = "휴"     # 休
    SU = "수"      # 囚
    SA = "사"      # 死

class WuXingAnalyzer:
    """오행 분석 엔진"""
    
    def __init__(self):
        # 오행별 기본 점수
        self.base_scores = {
            WuXing.WOOD: 0,
            WuXing.FIRE: 0,
            WuXing.EARTH: 0,
            WuXing.METAL: 0,
            WuXing.WATER: 0
        }
        
        # 세력 점수 배수
        self.strength_multipliers = {
            "왕": 3.0,   # 旺
            "상": 2.0,   # 相
            "휴": 1.0,   # 休
            "수": 0.5,   # 囚
            "사": 0.3    # 死
        }
        
    def analyze_wuxing_balance(self, pillars: Dict[str, Any], birth_month: int) -> Dict[str, Any]:
        """사주의 오행 균형 종합 분석"""
        
        # 1. 기본 오행 점수 계산
        basic_scores = self._calculate_basic_wuxing_scores(pillars)
        
        # 2. 계절별 세력 적용
        season = get_season_by_month(birth_month)
        season_adjusted_scores = self._apply_seasonal_strength(basic_scores, season)
        
        # 3. 상생상극 보정
        interaction_adjusted_scores = self._apply_wuxing_interactions(season_adjusted_scores)
        
        # 4. 균형 분석
        balance_analysis = self._analyze_balance(interaction_adjusted_scores)
        
        # 5. 종합 결과
        result = {
            "basic_scores": basic_scores,
            "season_adjusted_scores": season_adjusted_scores,
            "final_scores": interaction_adjusted_scores,
            "season": season,
            "balance_analysis": balance_analysis,
            "recommendations": self._generate_recommendations(balance_analysis)
        }
        
        return result
    
    def _calculate_basic_wuxing_scores(self, pillars: Dict[str, Any]) -> Dict[WuXing, float]:
        """기본 오행 점수 계산"""
        
        scores = self.base_scores.copy()
        
        for pillar_name, pillar_data in pillars.items():
            cheongan = pillar_data['cheongan']
            jiji = pillar_data['jiji']
            
            # 천간 오행 (100% 세력)
            cheongan_wuxing = get_cheongan_wuxing(cheongan)
            if cheongan_wuxing:
                scores[cheongan_wuxing] += 1.0
            
            # 지지 오행 (본기 100% + 지장간 비율별)
            jiji_wuxing = get_jiji_wuxing(jiji)
            if jiji_wuxing:
                scores[jiji_wuxing] += 1.0
            
            # 지장간 추가 점수
            jijanggan_list = get_jijanggan(jiji)
            for jjg_gan, jjg_ratio in jijanggan_list:
                jjg_wuxing = get_cheongan_wuxing(jjg_gan)
                if jjg_wuxing:
                    # 지장간 비율에 따른 점수 (예: 60% = 0.6점)
                    scores[jjg_wuxing] += (jjg_ratio / 100) * 0.5
        
        return scores
    
    def _apply_seasonal_strength(self, basic_scores: Dict[WuXing, float], 
                                season: str) -> Dict[WuXing, float]:
        """계절별 왕상휴수사 세력 적용"""
        
        seasonal_strength = SEASONAL_WUXING_STRENGTH.get(season, {})
        adjusted_scores = {}
        
        for wuxing, base_score in basic_scores.items():
            strength = seasonal_strength.get(wuxing, "휴")
            multiplier = self.strength_multipliers.get(strength, 1.0)
            adjusted_scores[wuxing] = base_score * multiplier
        
        return adjusted_scores
    
    def _apply_wuxing_interactions(self, season_scores: Dict[WuXing, float]) -> Dict[WuXing, float]:
        """상생상극 관계 보정 적용"""
        
        interaction_scores = season_scores.copy()
        
        # 상생 관계 보정 (생하는 오행이 강하면 생받는 오행도 강화)
        for generator, receiver in WUXING_SAENGSAENG.items():
            if season_scores[generator] > 2.0:  # 생하는 오행이 강할 때
                boost = season_scores[generator] * 0.2  # 20% 보정
                interaction_scores[receiver] += boost
        
        # 상극 관계 보정 (극하는 오행이 강하면 극받는 오행 약화)
        for attacker, victim in WUXING_SANGGEUK.items():
            if season_scores[attacker] > 2.0:  # 극하는 오행이 강할 때
                reduction = season_scores[attacker] * 0.15  # 15% 감소
                interaction_scores[victim] = max(0, interaction_scores[victim] - reduction)
        
        return interaction_scores
    
    def _analyze_balance(self, final_scores: Dict[WuXing, float]) -> Dict[str, Any]:
        """오행 균형 분석"""
        
        total_score = sum(final_scores.values())
        
        # 각 오행의 비율 계산
        ratios = {}
        for wuxing, score in final_scores.items():
            ratios[wuxing.value] = (score / total_score * 100) if total_score > 0 else 0
        
        # 최강/최약 오행 찾기
        sorted_wuxing = sorted(final_scores.items(), key=lambda x: x[1], reverse=True)
        dominant_wuxing = sorted_wuxing[0][0] if sorted_wuxing else None
        deficient_wuxing = sorted_wuxing[-1][0] if sorted_wuxing else None
        
        # 균형도 계산 (표준편차 기반)
        if total_score > 0:
            average = total_score / 5
            variance = sum((score - average) ** 2 for score in final_scores.values()) / 5
            balance_ratio = max(0, 100 - (variance ** 0.5 / average * 100))
        else:
            balance_ratio = 0
        
        # 균형 상태 판정
        if balance_ratio >= 80:
            balance_status = "매우 균형적"
        elif balance_ratio >= 60:
            balance_status = "균형적"
        elif balance_ratio >= 40:
            balance_status = "다소 불균형"
        else:
            balance_status = "불균형"
        
        return {
            "total_score": total_score,
            "ratios": ratios,
            "dominant": dominant_wuxing.value if dominant_wuxing else None,
            "deficient": deficient_wuxing.value if deficient_wuxing else None,
            "balance_ratio": round(balance_ratio, 1),
            "balance_status": balance_status,
            "detailed_scores": {wuxing.value: round(score, 2) for wuxing, score in final_scores.items()}
        }
    
    def _generate_recommendations(self, balance_analysis: Dict[str, Any]) -> Dict[str, List[str]]:
        """오행 균형 기반 개선 권장사항"""
        
        dominant = balance_analysis.get("dominant")
        deficient = balance_analysis.get("deficient")
        balance_ratio = balance_analysis.get("balance_ratio", 0)
        
        recommendations = {
            "strengths": [],
            "improvements": [],
            "lifestyle": [],
            "career": []
        }
        
        # 우세 오행 기반 강점
        if dominant:
            wuxing_strengths = {
                "목": ["창의력", "성장력", "유연성", "도전정신"],
                "화": ["열정", "표현력", "사교성", "리더십"],
                "토": ["안정성", "신뢰성", "포용력", "실용성"],
                "금": ["논리성", "정의감", "완벽주의", "결단력"],
                "수": ["지혜", "적응력", "직관력", "유연성"]
            }
            recommendations["strengths"] = wuxing_strengths.get(dominant, [])
        
        # 부족 오행 기반 개선사항
        if deficient and balance_ratio < 60:
            wuxing_improvements = {
                "목": ["창의적 활동 증가", "새로운 도전", "유연성 개발"],
                "화": ["사교 활동 확대", "표현력 개발", "열정적 추진"],
                "토": ["안정성 확보", "신뢰 관계 구축", "실용적 접근"],
                "금": ["논리적 사고 훈련", "원칙 준수", "정리정돈"],
                "수": ["학습과 연구", "직관력 개발", "유연한 사고"]
            }
            recommendations["improvements"] = wuxing_improvements.get(deficient, [])
        
        # 라이프스타일 권장사항
        if dominant == "목":
            recommendations["lifestyle"] = ["식물 기르기", "자연 접촉", "새로운 경험"]
        elif dominant == "화":
            recommendations["lifestyle"] = ["사교 모임", "예술 활동", "활발한 운동"]
        elif dominant == "토":
            recommendations["lifestyle"] = ["규칙적 생활", "건강한 식사", "안정적 환경"]
        elif dominant == "금":
            recommendations["lifestyle"] = ["정리정돈", "목표 설정", "운동 루틴"]
        elif dominant == "수":
            recommendations["lifestyle"] = ["독서와 학습", "조용한 환경", "명상"]
        
        # 직업 적성 권장사항
        career_suggestions = {
            "목": ["교육", "상담", "창작", "환경", "농업"],
            "화": ["예술", "방송", "영업", "서비스", "엔터테인먼트"],
            "토": ["부동산", "건설", "금융", "관리", "공무원"],
            "금": ["법조", "의료", "기술", "제조", "군경"],
            "수": ["연구", "IT", "학술", "물류", "통신"]
        }
        if dominant:
            recommendations["career"] = career_suggestions.get(dominant, [])
        
        return recommendations
    
    def get_wuxing_compatibility(self, person1_wuxing: WuXing, person2_wuxing: WuXing) -> Dict[str, Any]:
        """두 오행 간의 상성 분석"""
        
        compatibility_score = 50  # 기본 점수
        relationship = "중성"
        description = ""
        
        # 상생 관계 확인
        if WUXING_SAENGSAENG.get(person1_wuxing) == person2_wuxing:
            compatibility_score = 85
            relationship = "상생(생성)"
            description = f"{person1_wuxing.value}이 {person2_wuxing.value}을 생성하는 관계"
        elif WUXING_SAENGSAENG.get(person2_wuxing) == person1_wuxing:
            compatibility_score = 85
            relationship = "상생(수혜)"
            description = f"{person2_wuxing.value}이 {person1_wuxing.value}을 생성하는 관계"
        
        # 상극 관계 확인
        elif WUXING_SANGGEUK.get(person1_wuxing) == person2_wuxing:
            compatibility_score = 25
            relationship = "상극(공격)"
            description = f"{person1_wuxing.value}이 {person2_wuxing.value}을 극하는 관계"
        elif WUXING_SANGGEUK.get(person2_wuxing) == person1_wuxing:
            compatibility_score = 25
            relationship = "상극(피해)"
            description = f"{person2_wuxing.value}이 {person1_wuxing.value}을 극하는 관계"
        
        # 동일 오행
        elif person1_wuxing == person2_wuxing:
            compatibility_score = 70
            relationship = "동류"
            description = f"같은 {person1_wuxing.value} 오행으로 서로 이해가 높음"
        
        return {
            "compatibility_score": compatibility_score,
            "relationship": relationship,
            "description": description,
            "advice": self._get_compatibility_advice(relationship, compatibility_score)
        }
    
    def _get_compatibility_advice(self, relationship: str, score: int) -> str:
        """상성별 조언"""
        
        if relationship == "상생(생성)":
            return "서로를 발전시키는 최고의 조합입니다. 적극적인 협력을 추천합니다."
        elif relationship == "상생(수혜)":
            return "상대방으로부터 많은 도움을 받을 수 있는 관계입니다."
        elif relationship == "상극(공격)":
            return "갈등이 발생하기 쉬우니 상대방을 이해하려는 노력이 필요합니다."
        elif relationship == "상극(피해)":
            return "스트레스를 받기 쉬우니 적절한 거리를 유지하는 것이 좋습니다."
        elif relationship == "동류":
            return "서로 이해하기 쉽지만 발전을 위해서는 다른 요소가 필요할 수 있습니다."
        else:
            return "무난한 관계로 큰 갈등은 없으나 특별한 시너지도 기대하기 어렵습니다."


def analyze_saju_wuxing(pillars: Dict[str, Any], birth_month: int) -> Dict[str, Any]:
    """사주 오행 분석 메인 함수"""
    analyzer = WuXingAnalyzer()
    return analyzer.analyze_wuxing_balance(pillars, birth_month)


# Production-ready module - test code removed