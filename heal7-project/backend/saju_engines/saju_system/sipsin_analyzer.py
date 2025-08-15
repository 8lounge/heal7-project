#!/usr/bin/env python3
"""
십신(十神) 분석 시스템
- 십신 패턴 분석
- 성격 특성 도출
- 직업 적성 분석
- 지장간 십신 분석
"""

from typing import Dict, List, Tuple, Any
from collections import Counter
from .myeongrihak_constants import (
    SipSin,
    SIPSIN_RELATIONS,
    SIPSIN_CHARACTERISTICS,
    SIPSIN_APTITUDES,
    JIJANGGAN,
    get_sipsin_relation,
    get_jijanggan
)

class SipSinPattern:
    """십신 패턴 분류"""
    
    # 십신 패턴별 특성
    PATTERN_CHARACTERISTICS = {
        "비견왕": {
            "description": "비견/겁재가 강한 독립적 성향", 
            "traits": ["독립심", "주관", "고집", "리더십"],
            "careers": ["경영", "독립사업", "프리랜서"]
        },
        "식상격": {
            "description": "식신/상관이 강한 표현력 중시",
            "traits": ["창의력", "표현력", "예술성", "자유분방"],
            "careers": ["예술", "창작", "방송", "교육"]
        },
        "재성격": {
            "description": "정재/편재가 강한 현실적 성향",
            "traits": ["현실감", "경제력", "사업수완", "물질중시"],
            "careers": ["사업", "금융", "부동산", "유통"]
        },
        "관성격": {
            "description": "정관/편관이 강한 권위 지향",
            "traits": ["책임감", "질서", "권위", "사회성"],
            "careers": ["공직", "대기업", "법조", "의료"]
        },
        "인성격": {
            "description": "정인/편인이 강한 학문 지향",
            "traits": ["학구열", "지혜", "보호본능", "종교성"],
            "careers": ["교육", "연구", "의료", "종교"]
        },
        "혼잡격": {
            "description": "여러 십신이 혼재하는 복합 성향",
            "traits": ["다재다능", "변화무쌍", "적응력", "복잡성"],
            "careers": ["멀티플레이어", "컨설팅", "기획"]
        }
    }

class SipSinAnalyzer:
    """십신 분석 엔진"""
    
    def __init__(self):
        self.sipsin_scores = {}
        self.sipsin_positions = {}
        
    def analyze_sipsin_pattern(self, pillars: Dict[str, Any], ilgan: str) -> Dict[str, Any]:
        """사주의 십신 패턴 종합 분석"""
        
        # 1. 기본 십신 분석
        basic_sipsin = self._calculate_basic_sipsin(pillars, ilgan)
        
        # 2. 지장간 십신 분석
        jijanggan_sipsin = self._calculate_jijanggan_sipsin(pillars, ilgan)
        
        # 3. 십신 점수 종합
        total_sipsin_scores = self._combine_sipsin_scores(basic_sipsin, jijanggan_sipsin)
        
        # 4. 패턴 분석
        pattern_analysis = self._analyze_sipsin_pattern(total_sipsin_scores)
        
        # 5. 성격 특성 도출
        personality_traits = self._derive_personality_traits(total_sipsin_scores, pattern_analysis)
        
        # 6. 직업 적성 분석
        career_aptitude = self._analyze_career_aptitude(total_sipsin_scores, pattern_analysis)
        
        return {
            "basic_sipsin": basic_sipsin,
            "jijanggan_sipsin": jijanggan_sipsin,
            "total_scores": total_sipsin_scores,
            "pattern_analysis": pattern_analysis,
            "personality_traits": personality_traits,
            "career_aptitude": career_aptitude,
            "ilgan": ilgan
        }
    
    def _calculate_basic_sipsin(self, pillars: Dict[str, Any], ilgan: str) -> Dict[str, Any]:
        """기본 십신 계산 (천간+지지)"""
        
        basic_sipsin = {}
        sipsin_counts = Counter()
        
        for pillar_name, pillar_data in pillars.items():
            cheongan = pillar_data['cheongan']
            jiji = pillar_data['jiji']
            
            # 천간 십신
            cheongan_sipsin = get_sipsin_relation(ilgan, cheongan)
            if cheongan_sipsin:
                basic_sipsin[f"{pillar_name}_cheongan"] = {
                    "gan": cheongan,
                    "sipsin": cheongan_sipsin.value,
                    "position": pillar_name
                }
                sipsin_counts[cheongan_sipsin.value] += 1.0
            
            # 지지 본기 십신 (지지의 정기 천간)
            jijanggan_list = get_jijanggan(jiji)
            if jijanggan_list:
                # 정기(마지막 지장간)만 사용
                main_jjg_gan = jijanggan_list[-1][0]
                jiji_sipsin = get_sipsin_relation(ilgan, main_jjg_gan)
                if jiji_sipsin:
                    basic_sipsin[f"{pillar_name}_jiji"] = {
                        "gan": main_jjg_gan,
                        "jiji": jiji,
                        "sipsin": jiji_sipsin.value,
                        "position": pillar_name
                    }
                    sipsin_counts[jiji_sipsin.value] += 0.8  # 지지는 천간보다 약간 약하게
        
        return {
            "details": basic_sipsin,
            "counts": dict(sipsin_counts)
        }
    
    def _calculate_jijanggan_sipsin(self, pillars: Dict[str, Any], ilgan: str) -> Dict[str, Any]:
        """지장간 십신 상세 분석"""
        
        jijanggan_sipsin = {}
        sipsin_scores = Counter()
        
        for pillar_name, pillar_data in pillars.items():
            jiji = pillar_data['jiji']
            jijanggan_list = get_jijanggan(jiji)
            
            if jijanggan_list:
                jiji_analysis = []
                
                for i, (jjg_gan, jjg_ratio) in enumerate(jijanggan_list):
                    jjg_sipsin = get_sipsin_relation(ilgan, jjg_gan)
                    
                    if jjg_sipsin:
                        # 지장간 위치 분류 (여기/중기/정기)
                        if len(jijanggan_list) == 1:
                            jjg_type = "정기"
                        elif i == 0:
                            jjg_type = "여기"
                        elif i == len(jijanggan_list) - 1:
                            jjg_type = "정기"
                        else:
                            jjg_type = "중기"
                        
                        jiji_analysis.append({
                            "gan": jjg_gan,
                            "ratio": jjg_ratio,
                            "type": jjg_type,
                            "sipsin": jjg_sipsin.value
                        })
                        
                        # 비율에 따른 점수 계산
                        score = (jjg_ratio / 100) * 0.6  # 지장간은 천간의 60% 비중
                        sipsin_scores[jjg_sipsin.value] += score
                
                jijanggan_sipsin[pillar_name] = {
                    "jiji": jiji,
                    "jijanggan": jiji_analysis
                }
        
        return {
            "details": jijanggan_sipsin,
            "scores": dict(sipsin_scores)
        }
    
    def _combine_sipsin_scores(self, basic_sipsin: Dict[str, Any], 
                              jijanggan_sipsin: Dict[str, Any]) -> Dict[str, float]:
        """십신 점수 종합"""
        
        total_scores = Counter()
        
        # 기본 십신 점수
        for sipsin, count in basic_sipsin.get("counts", {}).items():
            total_scores[sipsin] += count
        
        # 지장간 십신 점수
        for sipsin, score in jijanggan_sipsin.get("scores", {}).items():
            total_scores[sipsin] += score
        
        return dict(total_scores)
    
    def _analyze_sipsin_pattern(self, total_scores: Dict[str, float]) -> Dict[str, Any]:
        """십신 패턴 분석"""
        
        if not total_scores:
            return {"pattern_type": "미분류", "dominant_sipsin": None}
        
        # 가장 강한 십신
        dominant_sipsin = max(total_scores.items(), key=lambda x: x[1])[0]
        max_score = total_scores[dominant_sipsin]
        
        # 십신 그룹별 점수 계산
        groups = {
            "비견겁재": total_scores.get("비견", 0) + total_scores.get("겁재", 0),
            "식상": total_scores.get("식신", 0) + total_scores.get("상관", 0),
            "재성": total_scores.get("정재", 0) + total_scores.get("편재", 0),
            "관성": total_scores.get("정관", 0) + total_scores.get("편관", 0),
            "인성": total_scores.get("정인", 0) + total_scores.get("편인", 0)
        }
        
        # 가장 강한 그룹
        dominant_group = max(groups.items(), key=lambda x: x[1])[0]
        dominant_group_score = groups[dominant_group]
        
        # 패턴 분류
        total_sum = sum(total_scores.values())
        
        if total_sum == 0:
            pattern_type = "미분류"
        elif dominant_group_score / total_sum >= 0.4:  # 40% 이상
            pattern_type = f"비견왕" if dominant_group == "비견겁재" else f"{dominant_group}격"
        elif len([score for score in groups.values() if score > 0]) >= 4:  # 4개 이상 그룹
            pattern_type = "혼잡격"
        else:
            pattern_type = "균형격"
        
        # 패턴 강도 계산
        if dominant_group_score > 0:
            pattern_strength = min(100, (dominant_group_score / total_sum * 100))
        else:
            pattern_strength = 0
        
        return {
            "pattern_type": pattern_type,
            "dominant_sipsin": dominant_sipsin,
            "dominant_group": dominant_group,
            "pattern_strength": round(pattern_strength, 1),
            "group_scores": groups,
            "total_balance": self._calculate_sipsin_balance(groups)
        }
    
    def _calculate_sipsin_balance(self, groups: Dict[str, float]) -> Dict[str, Any]:
        """십신 균형도 계산"""
        
        total = sum(groups.values())
        if total == 0:
            return {"balance_ratio": 0, "status": "불완전"}
        
        # 각 그룹의 비율
        ratios = [score / total for score in groups.values()]
        
        # 표준편차 계산
        average = 1 / len(groups)  # 이상적 비율 (20%)
        variance = sum((ratio - average) ** 2 for ratio in ratios) / len(groups)
        balance_ratio = max(0, 100 - (variance ** 0.5 / average * 100))
        
        # 균형 상태 판정
        if balance_ratio >= 80:
            status = "매우 균형적"
        elif balance_ratio >= 60:
            status = "균형적"
        elif balance_ratio >= 40:
            status = "다소 불균형"
        else:
            status = "불균형"
        
        return {
            "balance_ratio": round(balance_ratio, 1),
            "status": status,
            "ratios": {group: round(score / total * 100, 1) for group, score in groups.items()}
        }
    
    def _derive_personality_traits(self, total_scores: Dict[str, float], 
                                  pattern_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """성격 특성 도출"""
        
        traits = {
            "core_traits": [],
            "strengths": [],
            "weaknesses": [],
            "behavioral_patterns": []
        }
        
        pattern_type = pattern_analysis.get("pattern_type", "")
        
        # 패턴별 기본 특성
        if pattern_type in SipSinPattern.PATTERN_CHARACTERISTICS:
            pattern_info = SipSinPattern.PATTERN_CHARACTERISTICS[pattern_type]
            traits["core_traits"] = pattern_info["traits"]
        
        # 우세 십신별 세부 특성
        for sipsin, score in sorted(total_scores.items(), key=lambda x: x[1], reverse=True)[:3]:
            if score > 0:
                for sipsin_enum in SipSin:
                    if sipsin_enum.value == sipsin:
                        char_info = SIPSIN_CHARACTERISTICS.get(sipsin_enum, {})
                        
                        if char_info.get("장점"):
                            traits["strengths"].extend(char_info["장점"][:2])  # 상위 2개
                        if char_info.get("단점"):
                            traits["weaknesses"].extend(char_info["단점"][:1])  # 상위 1개
                        if char_info.get("성격"):
                            traits["behavioral_patterns"].extend(char_info["성격"][:2])  # 상위 2개
        
        # 중복 제거
        traits["strengths"] = list(set(traits["strengths"]))[:5]
        traits["weaknesses"] = list(set(traits["weaknesses"]))[:3]
        traits["behavioral_patterns"] = list(set(traits["behavioral_patterns"]))[:5]
        
        return traits
    
    def _analyze_career_aptitude(self, total_scores: Dict[str, float], 
                                pattern_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """직업 적성 분석"""
        
        aptitude = {
            "primary_fields": [],
            "secondary_fields": [],
            "work_style": "",
            "leadership_potential": 0,
            "creativity_index": 0
        }
        
        pattern_type = pattern_analysis.get("pattern_type", "")
        
        # 패턴별 주요 적성 분야
        if pattern_type in SipSinPattern.PATTERN_CHARACTERISTICS:
            pattern_info = SipSinPattern.PATTERN_CHARACTERISTICS[pattern_type]
            aptitude["primary_fields"] = pattern_info["careers"]
        
        # 십신별 세부 적성
        for sipsin, score in sorted(total_scores.items(), key=lambda x: x[1], reverse=True)[:3]:
            if score > 0.5:  # 일정 점수 이상만
                for sipsin_enum in SipSin:
                    if sipsin_enum.value == sipsin:
                        sipsin_aptitudes = SIPSIN_APTITUDES.get(sipsin_enum, [])
                        aptitude["secondary_fields"].extend(sipsin_aptitudes[:2])
        
        # 리더십 지수 계산
        leadership_score = (
            total_scores.get("비견", 0) * 2 +
            total_scores.get("정관", 0) * 1.5 +
            total_scores.get("편관", 0) * 1.8
        )
        aptitude["leadership_potential"] = min(100, leadership_score * 20)
        
        # 창의성 지수 계산
        creativity_score = (
            total_scores.get("식신", 0) * 2 +
            total_scores.get("상관", 0) * 2.2 +
            total_scores.get("편인", 0) * 1.5
        )
        aptitude["creativity_index"] = min(100, creativity_score * 20)
        
        # 업무 스타일 결정
        groups = pattern_analysis.get("group_scores", {})
        dominant_group = max(groups.items(), key=lambda x: x[1])[0] if groups else ""
        
        work_styles = {
            "비견겁재": "독립적이고 주도적인 업무 스타일",
            "식상": "창의적이고 표현력이 풍부한 업무 스타일",
            "재성": "현실적이고 결과 지향적인 업무 스타일",
            "관성": "체계적이고 책임감 있는 업무 스타일",
            "인성": "연구적이고 학습 지향적인 업무 스타일"
        }
        aptitude["work_style"] = work_styles.get(dominant_group, "균형적인 업무 스타일")
        
        # 중복 제거
        aptitude["secondary_fields"] = list(set(aptitude["secondary_fields"]))[:8]
        
        return aptitude


def analyze_saju_sipsin(pillars: Dict[str, Any], ilgan: str) -> Dict[str, Any]:
    """사주 십신 분석 메인 함수"""
    analyzer = SipSinAnalyzer()
    return analyzer.analyze_sipsin_pattern(pillars, ilgan)


# Production-ready module - test code removed
