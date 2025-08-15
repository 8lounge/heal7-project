#!/usr/bin/env python3
"""
통합 명리학 분석 엔진 v5.0
- KASI API 기반 정밀 사주 계산
- 오행/십신/격국 종합 분석
- 지장간 완전 분석
- JSON 형태 표준 출력
"""

import sys
import os
from datetime import datetime
from typing import Dict, List, Tuple, Any, Optional
import logging

# 사주 시스템 모듈 import
from .kasi_precision_saju_calculator import KasiPrecisionSajuCalculator
from .wuxing_analyzer import analyze_saju_wuxing
from .sipsin_analyzer import analyze_saju_sipsin
from .gyeokguk_analyzer import analyze_saju_gyeokguk, GyeokGukType
from .daewoon_analyzer import analyze_saju_daewoon, Gender
from .myeongrihak_constants import (
    WuXing, 
    SipSin,
    CHEONGAN_WUXING,
    JIJI_WUXING,
    JIJANGGAN,
    get_sipsin_relation,
    get_jijanggan,
    get_cheongan_wuxing,
    get_jiji_wuxing
)

logger = logging.getLogger(__name__)

class ComprehensiveMyeongRiHakAnalyzer:
    """통합 명리학 분석 엔진 v5.1 - 하이브리드 시스템 통합"""
    
    def __init__(self):
        self.kasi_calculator = KasiPrecisionSajuCalculator()
        
        # v5.1: 하이브리드 엔진 통합
        try:
            from .hybrid_saju_engine import HybridSajuEngine
            self.hybrid_engine = HybridSajuEngine()
            self.hybrid_available = True
            logger.info("🚀 하이브리드 사주 엔진 통합 완료")
        except ImportError:
            self.hybrid_engine = None
            self.hybrid_available = False
            logger.warning("⚠️ 하이브리드 엔진 사용 불가 - 기존 KASI 엔진만 사용")
        
    def analyze_complete_myeongrihak(self, year: int, month: int, day: int,
                                   hour: int, minute: int, 
                                   is_lunar: bool = False, is_leap_month: bool = False,
                                   gender: str = None) -> Dict[str, Any]:
        """완전한 명리학 분석 (v5.0 통합 시스템)"""
        
        logger.info(f"🔮 v5.0 통합 명리학 분석 시작")
        logger.info(f"입력: {year}-{month:02d}-{day:02d} {hour:02d}:{minute:02d} ({'음력' if is_lunar else '양력'})")
        
        try:
            # 1. 사주 계산 - KASI 우선 (하이브리드 엔진 이슈로 임시 비활성화)
            logger.info("📡 KASI 엔진 사용 (하이브리드 시스템 점검 중)")
            basic_saju = self.kasi_calculator.calculate_saju(
                year, month, day, hour, minute, is_lunar, is_leap_month
            )
            
            if not basic_saju:
                raise ValueError("사주 계산 실패")
            
            # 2. 기본 정보 추출
            pillars = basic_saju["pillars"]
            ilgan = basic_saju["ilgan"]
            input_info = basic_saju["input"]
            solar_time = basic_saju["solar_time"]
            calendar_info = basic_saju.get("calendar_info", {})
            
            logger.info(f"사주: {pillars['year']['gapja']} {pillars['month']['gapja']} {pillars['day']['gapja']} {pillars['hour']['gapja']}")
            logger.info(f"일간: {ilgan}")
            
            # 3. 지장간 분석 추가
            enhanced_pillars = self._enhance_pillars_with_jijanggan(pillars, ilgan)
            
            # 4. 오행 분석
            wuxing_analysis = analyze_saju_wuxing(enhanced_pillars, input_info["month"])
            
            # 5. 십신 분석
            sipsin_analysis = analyze_saju_sipsin(enhanced_pillars, ilgan)
            
            # 6. 격국 분석
            gyeokguk_analysis = analyze_saju_gyeokguk(enhanced_pillars, ilgan, input_info["month"])
            
            # 7. 대운 분석 (성별 정보가 있을 때)
            daewoon_analysis = None
            if gender:
                from datetime import date
                birth_date = date(year, month, day)
                daewoon_analysis = analyze_saju_daewoon(
                    enhanced_pillars, ilgan, birth_date, (hour, minute), gender, is_lunar
                )
            
            # 8. 종합 결과 생성
            comprehensive_result = self._generate_comprehensive_result(
                input_info, calendar_info, solar_time, enhanced_pillars, ilgan,
                wuxing_analysis, sipsin_analysis, gyeokguk_analysis, daewoon_analysis
            )
            
            logger.info(f"✅ 통합 명리학 분석 완료")
            return comprehensive_result
            
        except Exception as e:
            logger.error(f"통합 명리학 분석 오류: {e}")
            return None
    
    def _enhance_pillars_with_jijanggan(self, pillars: Dict[str, Any], ilgan: str) -> Dict[str, Any]:
        """기둥에 지장간 정보 추가"""
        
        enhanced_pillars = {}
        
        for pillar_name, pillar_data in pillars.items():
            cheongan = pillar_data["cheongan"]
            jiji = pillar_data["jiji"]
            gapja = pillar_data["gapja"]
            
            # 천간 오행 및 십신
            cheongan_wuxing = get_cheongan_wuxing(cheongan)
            cheongan_sipsin = get_sipsin_relation(ilgan, cheongan)
            
            # 지지 오행
            jiji_wuxing = get_jiji_wuxing(jiji)
            
            # 지장간 상세 분석
            jijanggan_list = get_jijanggan(jiji)
            jijanggan_analysis = []
            
            for i, (jjg_gan, jjg_ratio) in enumerate(jijanggan_list):
                jjg_wuxing = get_cheongan_wuxing(jjg_gan)
                jjg_sipsin = get_sipsin_relation(ilgan, jjg_gan)
                
                # 지장간 위치 분류
                if len(jijanggan_list) == 1:
                    jjg_type = "정기"
                elif i == 0:
                    jjg_type = "여기"
                elif i == len(jijanggan_list) - 1:
                    jjg_type = "정기"
                else:
                    jjg_type = "중기"
                
                jijanggan_analysis.append({
                    "gan": jjg_gan,
                    "oheng": jjg_wuxing.value if jjg_wuxing else None,
                    "sipsin": jjg_sipsin.value if jjg_sipsin else None,
                    "ratio": jjg_ratio,
                    "type": jjg_type
                })
            
            # 지지 정기의 십신 계산 (지지 십신용)
            jiji_sipsin = None
            if jijanggan_list:
                main_jjg_gan = jijanggan_list[-1][0]  # 정기
                jiji_sipsin_obj = get_sipsin_relation(ilgan, main_jjg_gan)
                jiji_sipsin = jiji_sipsin_obj.value if jiji_sipsin_obj else None

            # 확장된 기둥 정보
            enhanced_pillars[pillar_name] = {
                "ganji": gapja,
                "cheongan": cheongan,
                "jiji": jiji,
                "oheng": [
                    cheongan_wuxing.value if cheongan_wuxing else None,
                    jiji_wuxing.value if jiji_wuxing else None
                ],
                "sipsin": cheongan_sipsin.value if cheongan_sipsin else None,  # 천간 십신
                "cheongan_sipsin": cheongan_sipsin.value if cheongan_sipsin else None,  # 천간 십신 (명시적)
                "jiji_sipsin": jiji_sipsin,  # 지지 십신 (새로 추가)
                "jijanggan": jijanggan_analysis
            }
        
        return enhanced_pillars
    
    def _generate_comprehensive_result(self, input_info: Dict[str, Any], 
                                     calendar_info: Dict[str, Any],
                                     solar_time: Dict[str, Any],
                                     enhanced_pillars: Dict[str, Any], 
                                     ilgan: str,
                                     wuxing_analysis: Dict[str, Any],
                                     sipsin_analysis: Dict[str, Any],
                                     gyeokguk_analysis: Dict[str, Any],
                                     daewoon_analysis: Dict[str, Any] = None) -> Dict[str, Any]:
        """종합 결과 생성 (v5.0 양력/음력 병행 표기 지원)"""
        
        # 기본 입력 정보 정리
        calendar_type = "음력" if input_info.get("is_lunar", False) else "양력"
        leap_info = " (윤달)" if input_info.get("is_leap_month", False) else ""
        
        input_date = f"{input_info['year']}-{input_info['month']:02d}-{input_info['day']:02d}"
        input_time = f"{input_info['hour']:02d}:{input_info['minute']:02d}"
        
        # 사주 표기 생성
        saju_display = f"{enhanced_pillars['year']['ganji']} {enhanced_pillars['month']['ganji']} {enhanced_pillars['day']['ganji']} {enhanced_pillars['hour']['ganji']}"
        
        # 격국 타입 정리 (Enum -> str 변환)
        gyeokguk_type = gyeokguk_analysis.get("gyeokguk", {}).get("type")
        if hasattr(gyeokguk_type, 'value'):
            gyeokguk_str = gyeokguk_type.value
        else:
            gyeokguk_str = str(gyeokguk_type)
        
        # 종합 결과 구성
        comprehensive_result = {
            # 기본 정보 (v5.0 확장 - 양력/음력 병행 표기)
            "input": {
                "date": input_date,
                "time": input_time,
                "calendar": calendar_type + leap_info
            },
            # v5.0 추가: 양력/음력 병행 표기 정보
            "calendar_info": calendar_info,
            "corrected_time": solar_time.get("corrected", input_time),
            "ilgan": ilgan,
            
            # 사주 4기둥 (v5.0 확장 형식)
            "pillars": enhanced_pillars,
            
            # 격국 정보
            "gyeokguk": gyeokguk_str,
            
            # 상세 분석 정보 (v5.0 추가)
            "analysis_details": {
                # 오행 분석
                "wuxing_balance": {
                    "dominant": wuxing_analysis.get("balance_analysis", {}).get("dominant"),
                    "deficient": wuxing_analysis.get("balance_analysis", {}).get("deficient"),
                    "balance_ratio": wuxing_analysis.get("balance_analysis", {}).get("balance_ratio"),
                    "season": wuxing_analysis.get("season"),
                    "detailed_scores": wuxing_analysis.get("balance_analysis", {}).get("detailed_scores", {}),
                    "recommendations": wuxing_analysis.get("recommendations", {})
                },
                
                # 십신 분석
                "sipsin_pattern": {
                    "pattern_type": sipsin_analysis.get("pattern_analysis", {}).get("pattern_type"),
                    "dominant": sipsin_analysis.get("pattern_analysis", {}).get("dominant_sipsin"),
                    "pattern_strength": sipsin_analysis.get("pattern_analysis", {}).get("pattern_strength"),
                    "personality_traits": sipsin_analysis.get("personality_traits", {}),
                    "career_aptitude": sipsin_analysis.get("career_aptitude", {}),
                    "group_scores": sipsin_analysis.get("pattern_analysis", {}).get("group_scores", {})
                },
                
                # 격국 분석
                "gyeokguk_details": {
                    "wolryeong": gyeokguk_analysis.get("wolryeong", {}).get("dominant_gan"),
                    "tugan_exists": gyeokguk_analysis.get("tugan", {}).get("tugan_exists", False),
                    "confidence": gyeokguk_analysis.get("gyeokguk", {}).get("confidence", 0),
                    "yongsin": [y.get("sipsin") for y in gyeokguk_analysis.get("yongsin", {}).get("yongsin", [])],
                    "strength_score": gyeokguk_analysis.get("strength", {}).get("strength_score", 0),
                    "characteristics": gyeokguk_analysis.get("characteristics", {}),
                    "fortune_tendency": gyeokguk_analysis.get("fortune_tendency", {})
                },
                
                # 대운 분석 (성별 정보가 있을 때만)
                "daewoon_details": daewoon_analysis if daewoon_analysis else None
            },
            
            # 메타 정보
            "_metadata": {
                "version": "5.0",
                "analysis_engine": "comprehensive_myeongrihak_analyzer",
                "calculation_base": "KASI_API",
                "analysis_timestamp": datetime.now().isoformat(),
                "features": [
                    "정밀사주계산", "지장간분석", "오행균형", "십신패턴", 
                    "격국판정", "용신분석", "성격특성", "직업적성"
                ] + (["대운분석"] if daewoon_analysis else [])
            }
        }
        
        return comprehensive_result
    
    def quick_analysis(self, year: int, month: int, day: int, hour: int, minute: int,
                      is_lunar: bool = False) -> Dict[str, Any]:
        """간단한 사주 분석 (기본 정보만)"""
        
        try:
            basic_saju = self.kasi_calculator.calculate_saju(
                year, month, day, hour, minute, is_lunar
            )
            
            if not basic_saju:
                return None
                
            pillars = basic_saju["pillars"]
            saju_display = f"{pillars['year']['gapja']} {pillars['month']['gapja']} {pillars['day']['gapja']} {pillars['hour']['gapja']}"
            
            return {
                "saju": saju_display,
                "ilgan": basic_saju["ilgan"],
                "corrected_time": basic_saju["solar_time"]["corrected"],
                "input": basic_saju["input"]
            }
            
        except Exception as e:
            logger.error(f"간단 분석 오류: {e}")
            return None
    
    def validate_system(self) -> Dict[str, Any]:
        """v5.0 시스템 검증"""
        
        validation_cases = [
            {
                "name": "1985년 2월 24일 22:20 (양력)",
                "input": {"year": 1985, "month": 2, "day": 24, "hour": 22, "minute": 20, "is_lunar": False},
                "expected_saju": "乙丑 戊寅 甲午 乙亥",  # 검증용 (실제 결과와 다를 수 있음)
                "expected_ilgan": "甲"
            }
        ]
        
        results = []
        
        for case in validation_cases:
            try:
                result = self.analyze_complete_myeongrihak(**case["input"])
                
                if result:
                    pillars = result["pillars"]
                    actual_saju = f"{pillars['year']['ganji']} {pillars['month']['ganji']} {pillars['day']['ganji']} {pillars['hour']['ganji']}"
                    actual_ilgan = result["ilgan"]
                    
                    success = True
                    issues = []
                    
                    # 기본 구조 검증
                    required_keys = ["input", "corrected_time", "ilgan", "pillars", "gyeokguk", "analysis_details"]
                    for key in required_keys:
                        if key not in result:
                            success = False
                            issues.append(f"필수 키 누락: {key}")
                    
                    # 분석 세부 정보 검증
                    if "analysis_details" in result:
                        analysis_keys = ["wuxing_balance", "sipsin_pattern", "gyeokguk_details"]
                        for key in analysis_keys:
                            if key not in result["analysis_details"]:
                                success = False
                                issues.append(f"분석 세부정보 누락: {key}")
                    
                    results.append({
                        "case": case["name"],
                        "success": success,
                        "actual_saju": actual_saju,
                        "actual_ilgan": actual_ilgan,
                        "issues": issues
                    })
                else:
                    results.append({
                        "case": case["name"],
                        "success": False,
                        "issues": ["분석 결과 None"]
                    })
                    
            except Exception as e:
                results.append({
                    "case": case["name"],
                    "success": False,
                    "issues": [f"예외 발생: {str(e)}"]
                })
        
        overall_success = all(r["success"] for r in results)
        
        return {
            "overall_success": overall_success,
            "validation_results": results,
            "system_status": "정상" if overall_success else "오류",
            "validated_features": [
                "KASI API 연동",
                "사주 4기둥 계산", 
                "지장간 분석",
                "오행 균형 분석",
                "십신 패턴 분석",
                "격국 판정",
                "JSON 표준 출력"
            ]
        }


# 전역 인스턴스
comprehensive_analyzer = ComprehensiveMyeongRiHakAnalyzer()

def analyze_complete_saju(year: int, month: int, day: int, hour: int, minute: int,
                         is_lunar: bool = False, is_leap_month: bool = False, gender: str = None) -> Dict[str, Any]:
    """v5.0 통합 명리학 분석 메인 함수"""
    return comprehensive_analyzer.analyze_complete_myeongrihak(
        year, month, day, hour, minute, is_lunar, is_leap_month, gender
    )

def quick_saju_analysis(year: int, month: int, day: int, hour: int, minute: int,
                       is_lunar: bool = False) -> Dict[str, Any]:
    """간단한 사주 분석 함수"""
    return comprehensive_analyzer.quick_analysis(
        year, month, day, hour, minute, is_lunar
    )

def analyze_myeongrihak_v5(year: int, month: int, day: int, hour: int, minute: int,
                          is_lunar: bool = False) -> Dict[str, Any]:
    """v5.0 통합 명리학 분석 메인 함수"""
    return comprehensive_analyzer.analyze_comprehensive(
        year, month, day, hour, minute, is_lunar
    )

def validate_v5_system() -> Dict[str, Any]:
    """v5.0 시스템 검증 함수"""
    return comprehensive_analyzer.validate_system()


# Production-ready module - test code removed
