#!/usr/bin/env python3
"""
격국(格局) 분석 시스템
- 월령 기준 격국 판정
- 투간 성공 여부 분석
- 용신/희신 분석
- 격국별 특성 및 운세 분석
"""

from typing import Dict, List, Tuple, Any, Optional
from enum import Enum
from .myeongrihak_constants import (
    WuXing,
    SipSin,
    CHEONGAN_WUXING,
    JIJI_WUXING,
    JIJANGGAN,
    MONTH_TO_JIJI,
    SIPSIN_RELATIONS,
    get_sipsin_relation,
    get_jijanggan
)

class GyeokGukType(Enum):
    """격국 유형"""
    # 정격 (正格)
    JEONG_GWAN_GYEOK = "정관격"      # 正官格
    PYEON_GWAN_GYEOK = "편관격"      # 偏官格 (七殺格)
    JEONG_JAE_GYEOK = "정재격"       # 正財格
    PYEON_JAE_GYEOK = "편재격"       # 偏財格
    SIK_SIN_GYEOK = "식신격"         # 食神格
    SANG_GWAN_GYEOK = "상관격"       # 傷官格
    JEONG_IN_GYEOK = "정인격"        # 正印格
    PYEON_IN_GYEOK = "편인격"        # 偏印格
    
    # 변격 (變格)
    GONG_WANG_GYEOK = "건왕격"       # 建旺格 (비견/겁재 강함)
    JONG_WANG_GYEOK = "종왕격"       # 從旺格 (일간이 극도로 강함)
    JONG_JAE_GYEOK = "종재격"        # 從財格 (재성에 종함)
    JONG_SAL_GYEOK = "종살격"        # 從殺格 (편관에 종함)
    HWA_QI_GYEOK = "화기격"          # 化氣格 (합화)
    
    # 특수격
    MI_BOON_GYEOK = "미분류격"       # 분류 불가능한 격국

class GyeokGukAnalyzer:
    """격국 분석 엔진"""
    
    def __init__(self):
        # 격국별 특성 정의
        self.gyeokguk_characteristics = {
            GyeokGukType.JEONG_GWAN_GYEOK: {
                "description": "정관이 월령을 얻어 투간한 격국",
                "traits": ["품격", "명예", "책임감", "지도력"],
                "career": ["공직", "대기업", "교육", "의료"],
                "yongsin": ["인성", "비겁"],
                "kisin": ["상관", "상극오행"]
            },
            GyeokGukType.PYEON_GWAN_GYEOK: {
                "description": "편관(칠살)이 월령을 얻어 투간한 격국",
                "traits": ["강인함", "결단력", "추진력", "권위"],
                "career": ["군경", "법조", "경영", "스포츠"],
                "yongsin": ["식신", "인성"],
                "kisin": ["재성", "겁재"]
            },
            GyeokGukType.JEONG_JAE_GYEOK: {
                "description": "정재가 월령을 얻어 투간한 격국",
                "traits": ["신중함", "현실감", "안정", "관리능력"],
                "career": ["금융", "회계", "관리직", "부동산"],
                "yongsin": ["비겁", "관성"],
                "kisin": ["겁재", "편인"]
            },
            GyeokGukType.PYEON_JAE_GYEOK: {
                "description": "편재가 월령을 얻어 투간한 격국",
                "traits": ["사업수완", "기회포착", "활동성", "변화추구"],
                "career": ["사업", "투자", "무역", "영업"],
                "yongsin": ["비겁", "관성"],
                "kisin": ["겁재", "편인"]
            },
            GyeokGukType.SIK_SIN_GYEOK: {
                "description": "식신이 월령을 얻어 투간한 격국",
                "traits": ["온화함", "창의성", "표현력", "예술성"],
                "career": ["예술", "요리", "서비스", "교육"],
                "yongsin": ["재성", "비겁"],
                "kisin": ["편인", "겁재"]
            },
            GyeokGukType.SANG_GWAN_GYEOK: {
                "description": "상관이 월령을 얻어 투간한 격국",
                "traits": ["재능", "개성", "자유분방", "반항성"],
                "career": ["예술", "방송", "창작", "IT"],
                "yongsin": ["재성", "인성"],
                "kisin": ["정관", "겁재"]
            },
            GyeokGukType.JEONG_IN_GYEOK: {
                "description": "정인이 월령을 얻어 투간한 격국",
                "traits": ["학구열", "지혜", "인자함", "보호본능"],
                "career": ["교육", "학술", "의료", "종교"],
                "yongsin": ["관성", "재성"],
                "kisin": ["식상", "비겁"]
            },
            GyeokGukType.PYEON_IN_GYEOK: {
                "description": "편인이 월령을 얻어 투간한 격국",
                "traits": ["직관력", "독창성", "신비주의", "개성"],
                "career": ["연구", "예술", "종교", "상담"],
                "yongsin": ["관성", "재성"],
                "kisin": ["식상", "비겁"]
            },
            GyeokGukType.GONG_WANG_GYEOK: {
                "description": "일간이 월령을 얻어 매우 강한 격국",
                "traits": ["독립성", "주관", "고집", "리더십"],
                "career": ["경영", "독립사업", "자영업"],
                "yongsin": ["식상", "재성", "관성"],
                "kisin": ["비겫", "인성"]
            }
        }
    
    def analyze_gyeokguk(self, pillars: Dict[str, Any], ilgan: str, birth_month: int) -> Dict[str, Any]:
        """격국 종합 분석"""
        
        # 1. 월령 분석
        wolryeong_analysis = self._analyze_wolryeong(birth_month, pillars)
        
        # 2. 투간 분석
        tugan_analysis = self._analyze_tugan(pillars, ilgan, wolryeong_analysis)
        
        # 3. 격국 판정
        gyeokguk_determination = self._determine_gyeokguk(wolryeong_analysis, tugan_analysis, pillars, ilgan)
        
        # 4. 용신/희신 분석
        yongsin_analysis = self._analyze_yongsin_huisin(gyeokguk_determination, pillars, ilgan)
        
        # 5. 격국 강도 및 성취도 분석
        strength_analysis = self._analyze_gyeokguk_strength(gyeokguk_determination, tugan_analysis, pillars)
        
        return {
            "wolryeong": wolryeong_analysis,
            "tugan": tugan_analysis,
            "gyeokguk": gyeokguk_determination,
            "yongsin": yongsin_analysis,
            "strength": strength_analysis,
            "characteristics": self._get_gyeokguk_characteristics(gyeokguk_determination),
            "fortune_tendency": self._analyze_fortune_tendency(gyeokguk_determination, strength_analysis)
        }
    
    def _analyze_wolryeong(self, birth_month: int, pillars: Dict[str, Any]) -> Dict[str, Any]:
        """월령 분석 (월지의 주도권 분석)"""
        
        month_jiji = pillars['month']['jiji']
        month_jijanggan = get_jijanggan(month_jiji)
        
        # 월령의 주기(正氣) - 가장 강한 지장간
        if month_jijanggan:
            dominant_gan = month_jijanggan[-1][0]  # 정기
            dominant_ratio = month_jijanggan[-1][1]
            dominant_wuxing = CHEONGAN_WUXING.get(dominant_gan)
        else:
            dominant_gan = None
            dominant_ratio = 0
            dominant_wuxing = None
        
        # 월령의 세부 구성
        wolryeong_composition = []
        for gan, ratio in month_jijanggan:
            wuxing = CHEONGAN_WUXING.get(gan)
            wolryeong_composition.append({
                "gan": gan,
                "wuxing": wuxing.value if wuxing else None,
                "ratio": ratio,
                "type": "정기" if gan == dominant_gan else ("중기" if len(month_jijanggan) == 3 and ratio > 10 else "여기")
            })
        
        return {
            "month_jiji": month_jiji,
            "dominant_gan": dominant_gan,
            "dominant_wuxing": dominant_wuxing.value if dominant_wuxing else None,
            "dominant_ratio": dominant_ratio,
            "composition": wolryeong_composition,
            "season_strength": self._get_seasonal_strength(birth_month)
        }
    
    def _analyze_tugan(self, pillars: Dict[str, Any], ilgan: str, 
                      wolryeong_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """투간 분석 (천간에 월령의 기운이 나타나는지 확인)"""
        
        dominant_gan = wolryeong_analysis.get("dominant_gan")
        if not dominant_gan:
            return {"tugan_exists": False, "tugan_positions": [], "tugan_strength": 0}
        
        # 월령의 주기가 천간에 투출되었는지 확인
        tugan_positions = []
        tugan_strength = 0
        
        for pillar_name, pillar_data in pillars.items():
            cheongan = pillar_data['cheongan']
            
            # 직접 투간 (같은 천간)
            if cheongan == dominant_gan:
                tugan_positions.append({
                    "position": pillar_name,
                    "gan": cheongan,
                    "type": "직접투간",
                    "strength": 100
                })
                tugan_strength += 100
            
            # 동류 투간 (같은 오행)
            elif CHEONGAN_WUXING.get(cheongan) == CHEONGAN_WUXING.get(dominant_gan):
                tugan_positions.append({
                    "position": pillar_name,
                    "gan": cheongan,
                    "type": "동류투간",
                    "strength": 60
                })
                tugan_strength += 60
        
        # 투간 성공 여부 판정
        tugan_exists = len(tugan_positions) > 0
        
        # 투간 위치별 가중치 적용
        weighted_strength = 0
        position_weights = {"year": 0.8, "month": 1.5, "day": 1.0, "hour": 0.6}
        
        for tugan in tugan_positions:
            weight = position_weights.get(tugan["position"], 1.0)
            weighted_strength += tugan["strength"] * weight
        
        return {
            "tugan_exists": tugan_exists,
            "tugan_positions": tugan_positions,
            "tugan_strength": tugan_strength,
            "weighted_strength": weighted_strength,
            "tugan_quality": self._evaluate_tugan_quality(tugan_positions)
        }
    
    def _determine_gyeokguk(self, wolryeong_analysis: Dict[str, Any], 
                           tugan_analysis: Dict[str, Any],
                           pillars: Dict[str, Any], ilgan: str) -> Dict[str, Any]:
        """격국 판정"""
        
        dominant_gan = wolryeong_analysis.get("dominant_gan")
        tugan_exists = tugan_analysis.get("tugan_exists", False)
        
        if not dominant_gan:
            return {
                "type": GyeokGukType.MI_BOON_GYEOK,
                "confidence": 0,
                "reason": "월령 주기 불분명"
            }
        
        # 월령 주기와 일간의 십신 관계 확인
        ilgan_to_wolryeong_sipsin = get_sipsin_relation(ilgan, dominant_gan)
        
        if not ilgan_to_wolryeong_sipsin:
            return {
                "type": GyeokGukType.MI_BOON_GYEOK,
                "confidence": 0,
                "reason": "십신 관계 불분명"
            }
        
        # 십신에 따른 격국 분류
        sipsin_to_gyeokguk = {
            SipSin.JEONG_GWAN: GyeokGukType.JEONG_GWAN_GYEOK,
            SipSin.PYEON_GWAN: GyeokGukType.PYEON_GWAN_GYEOK,
            SipSin.JEONG_JAE: GyeokGukType.JEONG_JAE_GYEOK,
            SipSin.PYEON_JAE: GyeokGukType.PYEON_JAE_GYEOK,
            SipSin.SIK_SIN: GyeokGukType.SIK_SIN_GYEOK,
            SipSin.SANG_GWAN: GyeokGukType.SANG_GWAN_GYEOK,
            SipSin.JEONG_IN: GyeokGukType.JEONG_IN_GYEOK,
            SipSin.PYEON_IN: GyeokGukType.PYEON_IN_GYEOK
        }
        
        base_gyeokguk = sipsin_to_gyeokguk.get(ilgan_to_wolryeong_sipsin)
        
        # 특수 상황 검사
        if ilgan_to_wolryeong_sipsin in [SipSin.BI_JIAN, SipSin.GYEOP_JAE]:
            # 건왕격 가능성
            base_gyeokguk = GyeokGukType.GONG_WANG_GYEOK
        
        # 투간 성공 여부에 따른 격국 신뢰도
        if tugan_exists and base_gyeokguk:
            confidence = min(95, 60 + tugan_analysis.get("weighted_strength", 0) / 10)
            gyeokguk_type = base_gyeokguk
            reason = f"{ilgan_to_wolryeong_sipsin.value} 월령 득세, 투간 성공"
        elif base_gyeokguk:
            confidence = min(70, 40 + wolryeong_analysis.get("dominant_ratio", 0) / 2)
            gyeokguk_type = base_gyeokguk
            reason = f"{ilgan_to_wolryeong_sipsin.value} 월령 득세, 투간 미성공"
        else:
            confidence = 20
            gyeokguk_type = GyeokGukType.MI_BOON_GYEOK
            reason = "격국 조건 불충족"
        
        return {
            "type": gyeokguk_type,
            "confidence": round(confidence, 1),
            "reason": reason,
            "wolryeong_sipsin": ilgan_to_wolryeong_sipsin.value,
            "tugan_success": tugan_exists
        }
    
    def _analyze_yongsin_huisin(self, gyeokguk_determination: Dict[str, Any], 
                               pillars: Dict[str, Any], ilgan: str) -> Dict[str, Any]:
        """용신/희신 분석"""
        
        gyeokguk_type = gyeokguk_determination.get("type")
        
        if gyeokguk_type == GyeokGukType.MI_BOON_GYEOK:
            return {
                "yongsin": [],
                "huisin": [],
                "kisin": [],
                "analysis": "격국 미분류로 용신 분석 불가"
            }
        
        # 격국별 기본 용신/기신
        gyeokguk_char = self.gyeokguk_characteristics.get(gyeokguk_type, {})
        basic_yongsin = gyeokguk_char.get("yongsin", [])
        basic_kisin = gyeokguk_char.get("kisin", [])
        
        # 사주 내 용신/기신 존재 여부 확인
        present_yongsin = []
        present_kisin = []
        
        for pillar_name, pillar_data in pillars.items():
            cheongan = pillar_data['cheongan']
            ilgan_to_cheongan_sipsin = get_sipsin_relation(ilgan, cheongan)
            
            if ilgan_to_cheongan_sipsin:
                sipsin_name = ilgan_to_cheongan_sipsin.value
                
                # 용신 확인
                for yongsin_group in basic_yongsin:
                    if self._is_sipsin_in_group(sipsin_name, yongsin_group):
                        present_yongsin.append({
                            "position": pillar_name,
                            "gan": cheongan,
                            "sipsin": sipsin_name,
                            "role": "용신"
                        })
                
                # 기신 확인
                for kisin_group in basic_kisin:
                    if self._is_sipsin_in_group(sipsin_name, kisin_group):
                        present_kisin.append({
                            "position": pillar_name,
                            "gan": cheongan,
                            "sipsin": sipsin_name,
                            "role": "기신"
                        })
        
        # 희신 (용신을 도와주는 십신)
        huisin = self._find_huisin(present_yongsin, pillars, ilgan)
        
        return {
            "yongsin": present_yongsin,
            "huisin": huisin,
            "kisin": present_kisin,
            "yongsin_strength": len(present_yongsin),
            "kisin_strength": len(present_kisin),
            "balance_evaluation": self._evaluate_yongsin_kisin_balance(present_yongsin, present_kisin)
        }
    
    def _analyze_gyeokguk_strength(self, gyeokguk_determination: Dict[str, Any], 
                                  tugan_analysis: Dict[str, Any],
                                  pillars: Dict[str, Any]) -> Dict[str, Any]:
        """격국 강도 및 성취도 분석"""
        
        confidence = gyeokguk_determination.get("confidence", 0)
        tugan_strength = tugan_analysis.get("weighted_strength", 0)
        
        # 기본 강도 계산
        base_strength = confidence
        
        # 투간 강도 보정
        tugan_bonus = min(30, tugan_strength / 10)
        
        # 파격 요소 확인 (격국을 깨뜨리는 요소)
        disruption_penalty = self._check_gyeokguk_disruption(gyeokguk_determination, pillars)
        
        # 최종 강도 계산
        final_strength = max(0, base_strength + tugan_bonus - disruption_penalty)
        
        # 성취도 평가
        if final_strength >= 85:
            achievement_level = "매우 높음"
            potential = "탁월한 성취 잠재력"
        elif final_strength >= 70:
            achievement_level = "높음"
            potential = "뛰어난 성취 잠재력"
        elif final_strength >= 55:
            achievement_level = "보통"
            potential = "일반적 성취 잠재력"
        elif final_strength >= 40:
            achievement_level = "낮음"
            potential = "노력 필요"
        else:
            achievement_level = "매우 낮음"
            potential = "큰 노력과 보완 필요"
        
        return {
            "strength_score": round(final_strength, 1),
            "achievement_level": achievement_level,
            "potential": potential,
            "components": {
                "base_strength": confidence,
                "tugan_bonus": tugan_bonus,
                "disruption_penalty": disruption_penalty
            }
        }
    
    def _get_seasonal_strength(self, birth_month: int) -> str:
        """계절별 세력 평가"""
        if birth_month in [3, 4, 5]:
            return "목왕화상토사금수수휴"  # 봄
        elif birth_month in [6, 7, 8]:
            return "화왕토상금사수수목휴"  # 여름
        elif birth_month in [9, 10, 11]:
            return "금왕수상목사화수토휴"  # 가을
        else:
            return "수왕목상화사토수금휴"  # 겨울
    
    def _evaluate_tugan_quality(self, tugan_positions: List[Dict]) -> str:
        """투간 품질 평가"""
        if not tugan_positions:
            return "투간 없음"
        
        has_direct = any(t["type"] == "직접투간" for t in tugan_positions)
        month_position = any(t["position"] == "month" for t in tugan_positions)
        
        if has_direct and month_position:
            return "최상급 투간"
        elif has_direct:
            return "상급 투간"
        elif month_position:
            return "중급 투간"
        else:
            return "하급 투간"
    
    def _is_sipsin_in_group(self, sipsin_name: str, group_name: str) -> bool:
        """십신이 특정 그룹에 속하는지 확인"""
        groups = {
            "인성": ["정인", "편인"],
            "비겁": ["비견", "겁재"],
            "식상": ["식신", "상관"],
            "재성": ["정재", "편재"],
            "관성": ["정관", "편관"]
        }
        return sipsin_name in groups.get(group_name, [])
    
    def _find_huisin(self, present_yongsin: List[Dict], 
                    pillars: Dict[str, Any], ilgan: str) -> List[Dict]:
        """희신 찾기 (용신을 도와주는 십신)"""
        # 단순화된 희신 로직
        return []  # 복잡한 희신 로직은 추후 구현
    
    def _evaluate_yongsin_kisin_balance(self, yongsin: List[Dict], 
                                       kisin: List[Dict]) -> str:
        """용신/기신 균형 평가"""
        yongsin_count = len(yongsin)
        kisin_count = len(kisin)
        
        if yongsin_count > kisin_count * 2:
            return "용신 매우 강함"
        elif yongsin_count > kisin_count:
            return "용신 강함"
        elif yongsin_count == kisin_count:
            return "균형적"
        elif kisin_count > yongsin_count * 2:
            return "기신 매우 강함"
        else:
            return "기신 강함"
    
    def _check_gyeokguk_disruption(self, gyeokguk_determination: Dict[str, Any], 
                                  pillars: Dict[str, Any]) -> float:
        """격국 파괴 요소 확인"""
        # 단순화된 파격 체크
        return 0  # 복잡한 파격 로직은 추후 구현
    
    def _get_gyeokguk_characteristics(self, gyeokguk_determination: Dict[str, Any]) -> Dict[str, Any]:
        """격국별 특성 반환"""
        gyeokguk_type = gyeokguk_determination.get("type")
        return self.gyeokguk_characteristics.get(gyeokguk_type, {})
    
    def _analyze_fortune_tendency(self, gyeokguk_determination: Dict[str, Any], 
                                 strength_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """운세 경향 분석"""
        gyeokguk_type = gyeokguk_determination.get("type")
        strength = strength_analysis.get("strength_score", 0)
        
        # 격국별 기본 운세 경향
        fortune_patterns = {
            GyeokGukType.JEONG_GWAN_GYEOK: "점진적 상승, 안정적 발전",
            GyeokGukType.PYEON_GWAN_GYEOK: "굴곡이 크지만 강한 추진력",
            GyeokGukType.JEONG_JAE_GYEOK: "꾸준한 축적, 안정적 성장",
            GyeokGukType.PYEON_JAE_GYEOK: "기회 포착으로 급성장 가능",
            GyeokGukType.SIK_SIN_GYEOK: "재능 발휘로 점진적 성공",
            GyeokGukType.SANG_GWAN_GYEOK: "창의력으로 독특한 성공",
            GyeokGukType.JEONG_IN_GYEOK: "학문과 지혜로 늦은 성공",
            GyeokGukType.PYEON_IN_GYEOK: "직감과 통찰로 특별한 성취",
            GyeokGukType.GONG_WANG_GYEOK: "강한 추진력으로 자력 성공"
        }
        
        base_pattern = fortune_patterns.get(gyeokguk_type, "일반적 운세 경향")
        
        # 격국 강도에 따른 보정
        if strength >= 80:
            potential_modifier = " (매우 높은 성취 가능)"
        elif strength >= 60:
            potential_modifier = " (좋은 성취 가능)"
        elif strength >= 40:
            potential_modifier = " (보통 성취 가능)"
        else:
            potential_modifier = " (노력과 보완 필요)"
        
        return {
            "basic_tendency": base_pattern,
            "modified_tendency": base_pattern + potential_modifier,
            "peak_periods": self._predict_peak_periods(gyeokguk_type),
            "caution_periods": self._predict_caution_periods(gyeokguk_type)
        }
    
    def _predict_peak_periods(self, gyeokguk_type: GyeokGukType) -> List[str]:
        """격국별 대운 호황기 예측 (간략화)"""
        peak_periods = {
            GyeokGukType.JEONG_GWAN_GYEOK: ["인성운", "비겁운"],
            GyeokGukType.PYEON_GWAN_GYEOK: ["식상운", "인성운"],
            GyeokGukType.JEONG_JAE_GYEOK: ["비겁운", "관성운"],
            GyeokGukType.PYEON_JAE_GYEOK: ["비겁운", "관성운"],
            GyeokGukType.SIK_SIN_GYEOK: ["재성운", "비겁운"],
            GyeokGukType.SANG_GWAN_GYEOK: ["재성운", "인성운"],
            GyeokGukType.JEONG_IN_GYEOK: ["관성운", "재성운"],
            GyeokGukType.PYEON_IN_GYEOK: ["관성운", "재성운"],
            GyeokGukType.GONG_WANG_GYEOK: ["식상운", "재성운", "관성운"]
        }
        return peak_periods.get(gyeokguk_type, ["일반운"])
    
    def _predict_caution_periods(self, gyeokguk_type: GyeokGukType) -> List[str]:
        """격국별 대운 주의기 예측 (간략화)"""
        caution_periods = {
            GyeokGukType.JEONG_GWAN_GYEOK: ["상관운"],
            GyeokGukType.PYEON_GWAN_GYEOK: ["재성운", "겁재운"],
            GyeokGukType.JEONG_JAE_GYEOK: ["겁재운", "편인운"],
            GyeokGukType.PYEON_JAE_GYEOK: ["겁재운", "편인운"],
            GyeokGukType.SIK_SIN_GYEOK: ["편인운"],
            GyeokGukType.SANG_GWAN_GYEOK: ["정관운"],
            GyeokGukType.JEONG_IN_GYEOK: ["식상운"],
            GyeokGukType.PYEON_IN_GYEOK: ["식상운"],
            GyeokGukType.GONG_WANG_GYEOK: ["인성운"]
        }
        return caution_periods.get(gyeokguk_type, [])


def analyze_saju_gyeokguk(pillars: Dict[str, Any], ilgan: str, birth_month: int) -> Dict[str, Any]:
    """사주 격국 분석 메인 함수"""
    analyzer = GyeokGukAnalyzer()
    return analyzer.analyze_gyeokguk(pillars, ilgan, birth_month)


# Production-ready module - test code removed
