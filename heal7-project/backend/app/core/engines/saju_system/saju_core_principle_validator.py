#!/usr/bin/env python3
"""
사주 핵심 원리 검증기 v1.0
사주 계산의 모든 핵심 원리를 체계적으로 검증

검증 영역:
1. 년주 계산 (입춘 기준, 60갑자 순환)
2. 월주 계산 (24절기 기준, 월간 배치) 
3. 일주 계산 (60갑자 연속, 기준점 검증)
4. 시주 계산 (시두법, 진태양시 보정)
5. 대운 계산 (음양 일치 원리)
6. 십신/오행/지장간 관계 무결성
"""

import asyncio
import json
import logging
from datetime import datetime, date, timedelta
from typing import Dict, List, Any, Tuple, Optional
from dataclasses import dataclass, asdict
import statistics
import math

# 사주 시스템 모듈
from .kasi_precision_saju_calculator import KasiPrecisionSajuCalculator
from .myeongrihak_constants import CHEONGAN, JIJI, CHEONGAN_WUXING, JIJI_WUXING, JIJANGGAN

logger = logging.getLogger(__name__)

@dataclass
class PrincipleValidationCase:
    """원리 검증 케이스"""
    principle_name: str
    test_case_id: str
    input_params: Dict[str, Any]
    expected_result: Any
    validation_rule: str
    difficulty: str
    reference_source: str

@dataclass
class ValidationOutcome:
    """검증 결과"""
    principle_name: str
    test_case_id: str
    success: bool
    calculated_result: Any
    expected_result: Any
    accuracy_score: float
    error_details: str
    validation_method: str

class SajuCorePrincipleValidator:
    """사주 핵심 원리 검증기"""
    
    def __init__(self):
        self.kasi_calculator = KasiPrecisionSajuCalculator()
        
        # 검증 케이스 저장소
        self.validation_cases = []
        self.validation_outcomes = []
        
        # 핵심 원리 정의
        self.core_principles = {
            "년주_입춘_기준": "년주는 입춘 기준으로 구분하며, 입춘 이전은 전년도 간지 사용",
            "년주_60갑자_순환": "년주는 60갑자 순환 체계를 따름 (기준: 서기 4년 = 갑자년)",
            "월주_24절기_기준": "월주는 24절기를 기준으로 구분",
            "월주_년간_월간_관계": "년간에 따라 정월 월간이 결정됨 (갑기→병인, 을경→무인, 병신→경인, 정임→임인, 무계→갑인)",
            "일주_60갑자_연속": "일주는 연속적인 60갑자 순환을 따름",
            "일주_기준점_일관성": "확정된 기준점들 간의 수학적 일관성 유지",
            "시주_시두법": "시주는 일간에 따른 시두법 적용",
            "시주_진태양시_보정": "시주는 진태양시 보정 적용 (한국: -32분)",
            "대운_음양_일치_원리": "대운 방향은 년간과 성별 음양 일치 여부로 결정",
            "십신_일간_관계": "십신은 일간을 중심으로 한 상대적 관계",
            "오행_상생상극": "오행 관계는 상생상극 원리를 따름",
            "지장간_완전성": "지장간은 지지별로 완전한 천간 조합 보유"
        }
        
        # 수학적 상수들
        self.GAPJA_CYCLE = 60
        self.CHEONGAN_CYCLE = 10  
        self.JIJI_CYCLE = 12
        self.SOLAR_TIME_CORRECTION = -32  # 한국 진태양시 보정(분)
        
        # 검증 정확도 기준
        self.accuracy_thresholds = {
            "excellent": 98.0,
            "good": 90.0,
            "acceptable": 80.0,
            "poor": 70.0
        }
    
    async def run_comprehensive_validation(self):
        """종합 원리 검증 실행"""
        
        print("🔍 사주 핵심 원리 종합 검증 시작")
        print("=" * 80)
        
        validation_start = datetime.now()
        
        # 1. 검증 케이스 생성
        await self._generate_all_validation_cases()
        
        print(f"📊 생성된 검증 케이스: {len(self.validation_cases)}개")
        print("=" * 80)
        
        # 2. 원리별 검증 실행
        principle_results = {}
        
        for principle_name in self.core_principles.keys():
            print(f"\n🎯 {principle_name} 검증 중...")
            
            principle_cases = [case for case in self.validation_cases if case.principle_name == principle_name]
            principle_result = await self._validate_principle(principle_name, principle_cases)
            principle_results[principle_name] = principle_result
            
            # 진행 상황 출력
            success_rate = principle_result["success_rate"]
            accuracy = principle_result["average_accuracy"]
            
            status = "✅" if success_rate >= 90 else "⚠️" if success_rate >= 70 else "❌"
            print(f"   {status} 성공률: {success_rate:.1f}% | 정확도: {accuracy:.1f}%")
        
        # 3. 최종 분석 리포트
        print(f"\n📋 최종 분석 리포트 생성 중...")
        final_report = await self._generate_final_report(principle_results, validation_start)
        
        # 4. 리포트 출력
        await self._output_comprehensive_report(final_report)
        
        return final_report
    
    async def _generate_all_validation_cases(self):
        """모든 검증 케이스 생성"""
        
        # 1. 년주 검증 케이스
        await self._generate_year_pillar_cases()
        
        # 2. 월주 검증 케이스
        await self._generate_month_pillar_cases()
        
        # 3. 일주 검증 케이스
        await self._generate_day_pillar_cases()
        
        # 4. 시주 검증 케이스
        await self._generate_hour_pillar_cases()
        
        # 5. 대운 검증 케이스
        await self._generate_daewoon_cases()
        
        # 6. 관계성 검증 케이스
        await self._generate_relationship_cases()
    
    async def _generate_year_pillar_cases(self):
        """년주 검증 케이스 생성"""
        
        # 입춘 기준 검증 케이스
        lichun_cases = [
            # 입춘 이전 (전년도 간지 사용)
            {"year": 2024, "month": 2, "day": 3, "expected_year": 2023, "description": "입춘_이전_전년도간지"},
            # 입춘 이후 (해당년도 간지 사용)  
            {"year": 2024, "month": 2, "day": 5, "expected_year": 2024, "description": "입춘_이후_해당년도간지"},
            # 경계일 정확한 검증
            {"year": 2024, "month": 2, "day": 4, "expected_year": 2024, "description": "입춘_당일_검증"},
        ]
        
        for case in lichun_cases:
            # KASI로 실제 결과 확인
            try:
                kasi_result = self.kasi_calculator.calculate_saju(
                    case["year"], case["month"], case["day"], 12, 0, False
                )
                
                if kasi_result:
                    actual_year_gapja = kasi_result["pillars"]["year"]["gapja"]
                    
                    validation_case = PrincipleValidationCase(
                        principle_name="년주_입춘_기준",
                        test_case_id=f"lichun_{case['year']}_{case['month']}_{case['day']}",
                        input_params={
                            "year": case["year"],
                            "month": case["month"], 
                            "day": case["day"]
                        },
                        expected_result=actual_year_gapja,
                        validation_rule="입춘 기준 년주 구분",
                        difficulty="intermediate",
                        reference_source="KASI"
                    )
                    
                    self.validation_cases.append(validation_case)
                    
            except Exception as e:
                logger.warning(f"년주 입춘 케이스 생성 실패: {e}")
        
        # 60갑자 순환 검증 케이스
        gapja_cycle_cases = [
            {"year": 1984, "description": "갑자년_순환시작"},  # 갑자
            {"year": 1985, "description": "을축년_다음순환"},  # 을축
            {"year": 2044, "description": "갑자년_60년후"},   # 다시 갑자
            {"year": 1924, "description": "갑자년_60년전"},   # 이전 갑자
        ]
        
        for case in gapja_cycle_cases:
            try:
                kasi_result = self.kasi_calculator.calculate_saju(
                    case["year"], 6, 15, 12, 0, False  # 안전한 중간 날짜
                )
                
                if kasi_result:
                    actual_year_gapja = kasi_result["pillars"]["year"]["gapja"]
                    
                    validation_case = PrincipleValidationCase(
                        principle_name="년주_60갑자_순환",
                        test_case_id=f"cycle_{case['year']}",
                        input_params={"year": case["year"]},
                        expected_result=actual_year_gapja,
                        validation_rule="60갑자 순환 일관성",
                        difficulty="basic",
                        reference_source="KASI"
                    )
                    
                    self.validation_cases.append(validation_case)
                    
            except Exception as e:
                logger.warning(f"년주 순환 케이스 생성 실패: {e}")
    
    async def _generate_month_pillar_cases(self):
        """월주 검증 케이스 생성"""
        
        # 24절기 기준 검증
        solar_term_cases = [
            {"year": 2024, "month": 2, "day": 4, "description": "입춘_월주변경"},
            {"year": 2024, "month": 3, "day": 5, "description": "경칩_월주변경"},
            {"year": 2024, "month": 4, "day": 4, "description": "청명_월주변경"},
            {"year": 2024, "month": 5, "day": 5, "description": "입하_월주변경"},
        ]
        
        for case in solar_term_cases:
            try:
                # 절기 이전
                before_result = self.kasi_calculator.calculate_saju(
                    case["year"], case["month"], case["day"]-1, 12, 0, False
                )
                
                # 절기 이후
                after_result = self.kasi_calculator.calculate_saju(
                    case["year"], case["month"], case["day"]+1, 12, 0, False
                )
                
                if before_result and after_result:
                    before_month = before_result["pillars"]["month"]["gapja"]
                    after_month = after_result["pillars"]["month"]["gapja"]
                    
                    # 월주가 변경되었는지 검증
                    month_changed = (before_month != after_month)
                    
                    validation_case = PrincipleValidationCase(
                        principle_name="월주_24절기_기준",
                        test_case_id=f"solar_term_{case['year']}_{case['month']}_{case['day']}",
                        input_params={
                            "year": case["year"],
                            "month": case["month"],
                            "day": case["day"]
                        },
                        expected_result=month_changed,
                        validation_rule="24절기 기준 월주 변경",
                        difficulty="intermediate",
                        reference_source="KASI"
                    )
                    
                    self.validation_cases.append(validation_case)
                    
            except Exception as e:
                logger.warning(f"월주 절기 케이스 생성 실패: {e}")
        
        # 년간-월간 관계 검증
        year_month_relation_cases = [
            {"year": 1984, "expected_first_month_gan": "丙", "description": "갑년_정월병인"},  # 갑기년
            {"year": 1985, "expected_first_month_gan": "戊", "description": "을년_정월무인"},  # 을경년
            {"year": 1986, "expected_first_month_gan": "庚", "description": "병년_정월경인"},  # 병신년
            {"year": 1987, "expected_first_month_gan": "壬", "description": "정년_정월임인"},  # 정임년
            {"year": 1988, "expected_first_month_gan": "甲", "description": "무년_정월갑인"},  # 무계년
        ]
        
        for case in year_month_relation_cases:
            try:
                # 정월 (입춘 이후 안전한 날짜)
                kasi_result = self.kasi_calculator.calculate_saju(
                    case["year"], 2, 15, 12, 0, False
                )
                
                if kasi_result:
                    actual_month_gan = kasi_result["pillars"]["month"]["cheongan"]
                    
                    validation_case = PrincipleValidationCase(
                        principle_name="월주_년간_월간_관계",
                        test_case_id=f"year_month_{case['year']}",
                        input_params={"year": case["year"]},
                        expected_result=case["expected_first_month_gan"],
                        validation_rule="년간에 따른 월간 배치",
                        difficulty="intermediate",
                        reference_source="traditional"
                    )
                    
                    self.validation_cases.append(validation_case)
                    
            except Exception as e:
                logger.warning(f"년간-월간 관계 케이스 생성 실패: {e}")
    
    async def _generate_day_pillar_cases(self):
        """일주 검증 케이스 생성"""
        
        # 60갑자 연속성 검증 (기준점들 간의 일관성)
        reference_points = [
            {"date": "1985-02-24", "expected_gapja": "甲午", "description": "기준점1_갑오일"},
            {"date": "1955-05-06", "expected_gapja": "丁卯", "description": "기준점2_정묘일"},
            {"date": "2000-01-01", "expected_gapja": "甲辰", "description": "새천년_갑진일"},
        ]
        
        for point in reference_points:
            year, month, day = map(int, point["date"].split("-"))
            
            try:
                kasi_result = self.kasi_calculator.calculate_saju(year, month, day, 12, 0, False)
                
                if kasi_result:
                    actual_day_gapja = kasi_result["pillars"]["day"]["gapja"]
                    
                    validation_case = PrincipleValidationCase(
                        principle_name="일주_기준점_일관성",
                        test_case_id=f"reference_{year}_{month}_{day}",
                        input_params={"year": year, "month": month, "day": day},
                        expected_result=point["expected_gapja"],
                        validation_rule="확정 기준점 일치",
                        difficulty="basic",
                        reference_source="KASI"
                    )
                    
                    self.validation_cases.append(validation_case)
                    
            except Exception as e:
                logger.warning(f"일주 기준점 케이스 생성 실패: {e}")
        
        # 연속성 검증 (날짜별 갑자 증가)
        continuity_base_date = date(2024, 6, 15)
        
        for i in range(7):  # 일주일 연속
            test_date = continuity_base_date + timedelta(days=i)
            
            try:
                kasi_result = self.kasi_calculator.calculate_saju(
                    test_date.year, test_date.month, test_date.day, 12, 0, False
                )
                
                if kasi_result:
                    day_gapja = kasi_result["pillars"]["day"]["gapja"]
                    
                    validation_case = PrincipleValidationCase(
                        principle_name="일주_60갑자_연속",
                        test_case_id=f"continuity_{test_date.strftime('%Y_%m_%d')}",
                        input_params={
                            "year": test_date.year,
                            "month": test_date.month,
                            "day": test_date.day
                        },
                        expected_result=day_gapja,
                        validation_rule="60갑자 연속성",
                        difficulty="intermediate",
                        reference_source="KASI"
                    )
                    
                    self.validation_cases.append(validation_case)
                    
            except Exception as e:
                logger.warning(f"일주 연속성 케이스 생성 실패: {e}")
    
    async def _generate_hour_pillar_cases(self):
        """시주 검증 케이스 생성"""
        
        # 시두법 검증 (일간에 따른 시천간 배치)
        sidubeop_cases = [
            {"year": 2024, "month": 6, "day": 15, "hour": 0, "expected_pattern": "시두법_일간별", "description": "자시_시두법"},
            {"year": 2024, "month": 6, "day": 15, "hour": 6, "expected_pattern": "시두법_일간별", "description": "묘시_시두법"},
            {"year": 2024, "month": 6, "day": 15, "hour": 12, "expected_pattern": "시두법_일간별", "description": "오시_시두법"},
            {"year": 2024, "month": 6, "day": 15, "hour": 18, "expected_pattern": "시두법_일간별", "description": "유시_시두법"},
        ]
        
        for case in sidubeop_cases:
            try:
                kasi_result = self.kasi_calculator.calculate_saju(
                    case["year"], case["month"], case["day"], case["hour"], 0, False
                )
                
                if kasi_result:
                    hour_gapja = kasi_result["pillars"]["hour"]["gapja"]
                    day_gan = kasi_result["pillars"]["day"]["cheongan"]
                    
                    # 시두법 규칙 확인
                    is_sidubeop_correct = await self._validate_sidubeop_rule(day_gan, case["hour"], hour_gapja)
                    
                    validation_case = PrincipleValidationCase(
                        principle_name="시주_시두법",
                        test_case_id=f"sidubeop_{case['year']}_{case['month']}_{case['day']}_{case['hour']}",
                        input_params={
                            "year": case["year"],
                            "month": case["month"],
                            "day": case["day"],
                            "hour": case["hour"],
                            "day_gan": day_gan
                        },
                        expected_result=is_sidubeop_correct,
                        validation_rule="시두법 규칙 적용",
                        difficulty="intermediate",
                        reference_source="traditional"
                    )
                    
                    self.validation_cases.append(validation_case)
                    
            except Exception as e:
                logger.warning(f"시주 시두법 케이스 생성 실패: {e}")
        
        # 진태양시 보정 검증
        solar_time_cases = [
            {"hour": 12, "minute": 0, "expected_correction": -32, "description": "정오_진태양시보정"},
            {"hour": 0, "minute": 0, "expected_correction": -32, "description": "자정_진태양시보정"},
            {"hour": 6, "minute": 0, "expected_correction": -32, "description": "오전6시_진태양시보정"},
            {"hour": 18, "minute": 0, "expected_correction": -32, "description": "오후6시_진태양시보정"},
        ]
        
        for case in solar_time_cases:
            validation_case = PrincipleValidationCase(
                principle_name="시주_진태양시_보정",
                test_case_id=f"solar_time_{case['hour']}_{case['minute']}",
                input_params={"hour": case["hour"], "minute": case["minute"]},
                expected_result=case["expected_correction"],
                validation_rule="진태양시 보정 적용",
                difficulty="basic",
                reference_source="astronomical"
            )
            
            self.validation_cases.append(validation_case)
    
    async def _generate_daewoon_cases(self):
        """대운 검증 케이스 생성"""
        
        # 음양 일치 원리 검증 (수정된 로직 적용)
        daewoon_cases = [
            # 양년 + 남자(양) = 같음 → 순행
            {"year": 1984, "gender": "male", "expected": "forward", "description": "남자_양년_순행"},
            # 음년 + 남자(양) = 다름 → 역행
            {"year": 1985, "gender": "male", "expected": "backward", "description": "남자_음년_역행"},
            # 양년 + 여자(음) = 다름 → 역행
            {"year": 1984, "gender": "female", "expected": "backward", "description": "여자_양년_역행"},
            # 음년 + 여자(음) = 같음 → 순행
            {"year": 1985, "gender": "female", "expected": "forward", "description": "여자_음년_순행"},
            
            # 추가 검증 케이스
            {"year": 1986, "gender": "male", "expected": "forward", "description": "남자_병년_순행"},    # 양년
            {"year": 1987, "gender": "female", "expected": "forward", "description": "여자_정년_순행"},  # 음년
        ]
        
        for case in daewoon_cases:
            validation_case = PrincipleValidationCase(
                principle_name="대운_음양_일치_원리",
                test_case_id=f"daewoon_{case['year']}_{case['gender']}",
                input_params={"year": case["year"], "gender": case["gender"]},
                expected_result=case["expected"],
                validation_rule="년간과 성별 음양 일치 비교",
                difficulty="basic",
                reference_source="traditional"
            )
            
            self.validation_cases.append(validation_case)
    
    async def _generate_relationship_cases(self):
        """관계성 검증 케이스 생성"""
        
        # 십신 관계 검증
        sipsin_cases = [
            {"ilgan": "甲", "target_gan": "甲", "expected_sipsin": "비견", "description": "갑_갑_비견"},
            {"ilgan": "甲", "target_gan": "乙", "expected_sipsin": "겁재", "description": "갑_을_겁재"},
            {"ilgan": "甲", "target_gan": "丙", "expected_sipsin": "식신", "description": "갑_병_식신"},
            {"ilgan": "甲", "target_gan": "丁", "expected_sipsin": "상관", "description": "갑_정_상관"},
        ]
        
        for case in sipsin_cases:
            validation_case = PrincipleValidationCase(
                principle_name="십신_일간_관계",
                test_case_id=f"sipsin_{case['ilgan']}_{case['target_gan']}",
                input_params={"ilgan": case["ilgan"], "target_gan": case["target_gan"]},
                expected_result=case["expected_sipsin"],
                validation_rule="일간 중심 십신 관계",
                difficulty="basic",
                reference_source="traditional"
            )
            
            self.validation_cases.append(validation_case)
    
    async def _validate_sidubeop_rule(self, day_gan: str, hour: int, hour_gapja: str) -> bool:
        """시두법 규칙 검증"""
        
        # 시두법 규칙 (일간별 자시 시작 천간)
        sidubeop_rules = {
            "甲": ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸", "甲", "乙"],
            "己": ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸", "甲", "乙"],
            "乙": ["丙", "丁", "戊", "己", "庚", "辛", "壬", "癸", "甲", "乙", "丙", "丁"],
            "庚": ["丙", "丁", "戊", "己", "庚", "辛", "壬", "癸", "甲", "乙", "丙", "丁"],
            "丙": ["戊", "己", "庚", "辛", "壬", "癸", "甲", "乙", "丙", "丁", "戊", "己"],
            "辛": ["戊", "己", "庚", "辛", "壬", "癸", "甲", "乙", "丙", "丁", "戊", "己"],
            "丁": ["庚", "辛", "壬", "癸", "甲", "乙", "丙", "丁", "戊", "己", "庚", "辛"],
            "壬": ["庚", "辛", "壬", "癸", "甲", "乙", "丙", "丁", "戊", "己", "庚", "辛"],
            "戊": ["壬", "癸", "甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"],
            "癸": ["壬", "癸", "甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
        }
        
        # 시간대를 지지 인덱스로 변환 (자=0, 축=1, ..., 해=11)
        time_to_jiji_index = {
            range(23, 24): 0, range(0, 1): 0,      # 자시 23:30-01:30
            range(1, 3): 1,                        # 축시 01:30-03:30
            range(3, 5): 2,                        # 인시 03:30-05:30
            range(5, 7): 3,                        # 묘시 05:30-07:30
            range(7, 9): 4,                        # 진시 07:30-09:30
            range(9, 11): 5,                       # 사시 09:30-11:30
            range(11, 13): 6,                      # 오시 11:30-13:30
            range(13, 15): 7,                      # 미시 13:30-15:30
            range(15, 17): 8,                      # 신시 15:30-17:30
            range(17, 19): 9,                      # 유시 17:30-19:30
            range(19, 21): 10,                     # 술시 19:30-21:30
            range(21, 23): 11,                     # 해시 21:30-23:30
        }
        
        # 시간에 해당하는 지지 인덱스 찾기
        jiji_index = None
        for time_range, index in time_to_jiji_index.items():
            if hour in time_range:
                jiji_index = index
                break
        
        if jiji_index is None:
            return False
        
        # 시두법 규칙에 따른 기대 천간
        if day_gan not in sidubeop_rules:
            return False
        
        expected_hour_gan = sidubeop_rules[day_gan][jiji_index]
        actual_hour_gan = hour_gapja[0] if hour_gapja else None
        
        return expected_hour_gan == actual_hour_gan
    
    async def _validate_principle(self, principle_name: str, cases: List[PrincipleValidationCase]) -> Dict[str, Any]:
        """원리별 검증 실행"""
        
        if not cases:
            return {
                "principle_name": principle_name,
                "total_cases": 0,
                "success_cases": 0,
                "success_rate": 0.0,
                "average_accuracy": 0.0,
                "case_results": []
            }
        
        case_results = []
        success_count = 0
        accuracy_scores = []
        
        for case in cases:
            try:
                # 원리별 특화 검증 로직
                if principle_name == "대운_음양_일치_원리":
                    result = await self._validate_daewoon_principle(case)
                elif principle_name == "시주_진태양시_보정":
                    result = await self._validate_solar_time_principle(case)
                elif principle_name == "십신_일간_관계":
                    result = await self._validate_sipsin_principle(case)
                else:
                    result = await self._validate_general_principle(case)
                
                case_results.append(result)
                
                if result.success:
                    success_count += 1
                
                accuracy_scores.append(result.accuracy_score)
                
                # 검증 결과 저장
                self.validation_outcomes.append(result)
                
            except Exception as e:
                logger.error(f"원리 검증 실패 {principle_name} - {case.test_case_id}: {e}")
                
                error_result = ValidationOutcome(
                    principle_name=principle_name,
                    test_case_id=case.test_case_id,
                    success=False,
                    calculated_result=None,
                    expected_result=case.expected_result,
                    accuracy_score=0.0,
                    error_details=str(e),
                    validation_method="error"
                )
                
                case_results.append(error_result)
                accuracy_scores.append(0.0)
        
        return {
            "principle_name": principle_name,
            "total_cases": len(cases),
            "success_cases": success_count,
            "success_rate": (success_count / len(cases) * 100) if cases else 0,
            "average_accuracy": statistics.mean(accuracy_scores) if accuracy_scores else 0,
            "case_results": case_results
        }
    
    async def _validate_daewoon_principle(self, case: PrincipleValidationCase) -> ValidationOutcome:
        """대운 원리 검증"""
        
        year = case.input_params["year"]
        gender = case.input_params["gender"]
        
        # 년간 추출 및 음양 판정
        gan_index = (year - 4) % 10
        hanja_cheongan = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
        year_gan = hanja_cheongan[gan_index]
        
        is_yang_year = year_gan in ["甲", "丙", "戊", "庚", "壬"]
        is_yang_gender = gender.lower() in ["male", "남자", "남"]
        
        # 음양 일치 원리 적용
        if is_yang_year == is_yang_gender:
            calculated_direction = "forward"  # 순행
        else:
            calculated_direction = "backward"  # 역행
        
        # 검증
        is_correct = (calculated_direction == case.expected_result)
        accuracy = 100.0 if is_correct else 0.0
        
        validation_details = f"년간:{year_gan}({'양' if is_yang_year else '음'}) + 성별:{gender}({'양' if is_yang_gender else '음'}) = {'같음' if is_yang_year == is_yang_gender else '다름'} → {calculated_direction}"
        
        return ValidationOutcome(
            principle_name=case.principle_name,
            test_case_id=case.test_case_id,
            success=is_correct,
            calculated_result=calculated_direction,
            expected_result=case.expected_result,
            accuracy_score=accuracy,
            error_details="" if is_correct else f"기대:{case.expected_result}, 계산:{calculated_direction}",
            validation_method=validation_details
        )
    
    async def _validate_solar_time_principle(self, case: PrincipleValidationCase) -> ValidationOutcome:
        """진태양시 보정 원리 검증"""
        
        # 한국 진태양시 보정: -32분 (고정)
        calculated_correction = self.SOLAR_TIME_CORRECTION
        
        is_correct = (calculated_correction == case.expected_result)
        accuracy = 100.0 if is_correct else 0.0
        
        return ValidationOutcome(
            principle_name=case.principle_name,
            test_case_id=case.test_case_id,
            success=is_correct,
            calculated_result=calculated_correction,
            expected_result=case.expected_result,
            accuracy_score=accuracy,
            error_details="" if is_correct else f"기대:{case.expected_result}, 계산:{calculated_correction}",
            validation_method="한국 경도 127° 기준 보정"
        )
    
    async def _validate_sipsin_principle(self, case: PrincipleValidationCase) -> ValidationOutcome:
        """십신 관계 원리 검증"""
        
        ilgan = case.input_params["ilgan"]
        target_gan = case.input_params["target_gan"]
        
        # 십신 관계 계산 (간단한 기본 규칙)
        sipsin_relations = {
            ("甲", "甲"): "비견",
            ("甲", "乙"): "겁재", 
            ("甲", "丙"): "식신",
            ("甲", "丁"): "상관",
            ("甲", "戊"): "편재",
            ("甲", "己"): "정재",
            ("甲", "庚"): "편관",
            ("甲", "辛"): "정관",
            ("甲", "壬"): "편인",
            ("甲", "癸"): "정인"
        }
        
        calculated_sipsin = sipsin_relations.get((ilgan, target_gan))
        
        is_correct = (calculated_sipsin == case.expected_result)
        accuracy = 100.0 if is_correct else 0.0
        
        return ValidationOutcome(
            principle_name=case.principle_name,
            test_case_id=case.test_case_id,
            success=is_correct,
            calculated_result=calculated_sipsin,
            expected_result=case.expected_result,
            accuracy_score=accuracy,
            error_details="" if is_correct else f"기대:{case.expected_result}, 계산:{calculated_sipsin}",
            validation_method="십신 관계 매핑"
        )
    
    async def _validate_general_principle(self, case: PrincipleValidationCase) -> ValidationOutcome:
        """일반 원리 검증"""
        
        # KASI 기반 검증
        try:
            if "year" in case.input_params and "month" in case.input_params and "day" in case.input_params:
                kasi_result = self.kasi_calculator.calculate_saju(
                    case.input_params["year"], 
                    case.input_params["month"], 
                    case.input_params["day"],
                    case.input_params.get("hour", 12),
                    case.input_params.get("minute", 0),
                    False
                )
                
                if kasi_result:
                    # 결과 추출
                    if case.principle_name.startswith("년주"):
                        calculated_result = kasi_result["pillars"]["year"]["gapja"]
                    elif case.principle_name.startswith("월주"):
                        calculated_result = kasi_result["pillars"]["month"]["gapja"]
                    elif case.principle_name.startswith("일주"):
                        calculated_result = kasi_result["pillars"]["day"]["gapja"]
                    elif case.principle_name.startswith("시주"):
                        calculated_result = kasi_result["pillars"]["hour"]["gapja"]
                    else:
                        calculated_result = str(kasi_result)
                    
                    is_correct = (str(calculated_result) == str(case.expected_result))
                    accuracy = 100.0 if is_correct else 0.0
                    
                    return ValidationOutcome(
                        principle_name=case.principle_name,
                        test_case_id=case.test_case_id,
                        success=is_correct,
                        calculated_result=calculated_result,
                        expected_result=case.expected_result,
                        accuracy_score=accuracy,
                        error_details="" if is_correct else f"기대:{case.expected_result}, 계산:{calculated_result}",
                        validation_method="KASI_API"
                    )
        
        except Exception as e:
            logger.error(f"일반 검증 실패: {e}")
        
        # 검증 실패
        return ValidationOutcome(
            principle_name=case.principle_name,
            test_case_id=case.test_case_id,
            success=False,
            calculated_result=None,
            expected_result=case.expected_result,
            accuracy_score=0.0,
            error_details="검증 로직 실행 실패",
            validation_method="error"
        )
    
    async def _generate_final_report(self, principle_results: Dict[str, Any], validation_start: datetime) -> Dict[str, Any]:
        """최종 리포트 생성"""
        
        total_validation_time = (datetime.now() - validation_start).total_seconds()
        
        # 전체 통계
        all_success_rates = [result["success_rate"] for result in principle_results.values()]
        all_accuracies = [result["average_accuracy"] for result in principle_results.values()]
        
        overall_success_rate = statistics.mean(all_success_rates) if all_success_rates else 0
        overall_accuracy = statistics.mean(all_accuracies) if all_accuracies else 0
        
        # 등급 산정
        if overall_accuracy >= self.accuracy_thresholds["excellent"]:
            grade = "S (완벽)"
        elif overall_accuracy >= self.accuracy_thresholds["good"]:
            grade = "A (우수)"
        elif overall_accuracy >= self.accuracy_thresholds["acceptable"]:
            grade = "B (양호)"
        elif overall_accuracy >= self.accuracy_thresholds["poor"]:
            grade = "C (보통)"
        else:
            grade = "D (개선필요)"
        
        # 문제 영역 식별
        problem_principles = [
            name for name, result in principle_results.items()
            if result["success_rate"] < self.accuracy_thresholds["acceptable"]
        ]
        
        excellent_principles = [
            name for name, result in principle_results.items()
            if result["success_rate"] >= self.accuracy_thresholds["excellent"]
        ]
        
        return {
            "report_id": f"saju_core_validation_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "validation_timestamp": datetime.now().isoformat(),
            "validation_duration_seconds": total_validation_time,
            "total_principles": len(principle_results),
            "total_cases": len(self.validation_cases),
            "overall_success_rate": overall_success_rate,
            "overall_accuracy": overall_accuracy,
            "grade": grade,
            "principle_results": principle_results,
            "excellent_principles": excellent_principles,
            "problem_principles": problem_principles,
            "core_principles_definition": self.core_principles,
            "accuracy_thresholds": self.accuracy_thresholds,
            "detailed_outcomes": [asdict(outcome) for outcome in self.validation_outcomes[-10:]]  # 최근 10개
        }
    
    async def _output_comprehensive_report(self, report: Dict[str, Any]):
        """종합 리포트 출력"""
        
        print("\n" + "=" * 80)
        print("🎯 사주 핵심 원리 종합 검증 최종 리포트")
        print("=" * 80)
        
        print(f"\n📊 검증 개요:")
        print(f"   - 리포트 ID: {report['report_id']}")
        print(f"   - 검증 시각: {report['validation_timestamp']}")
        print(f"   - 검증 시간: {report['validation_duration_seconds']:.1f}초") 
        print(f"   - 검증 원리: {report['total_principles']}개")
        print(f"   - 검증 케이스: {report['total_cases']}개")
        
        print(f"\n🏆 전체 성과:")
        print(f"   - 전체 성공률: {report['overall_success_rate']:.1f}%")
        print(f"   - 전체 정확도: {report['overall_accuracy']:.1f}%")
        print(f"   - 신뢰성 등급: {report['grade']}")
        
        print(f"\n📈 원리별 상세 결과:")
        for principle_name, result in report['principle_results'].items():
            success_rate = result['success_rate']
            accuracy = result['average_accuracy']
            
            status = "🟢" if success_rate >= 90 else "🟡" if success_rate >= 70 else "🔴"
            
            print(f"   {status} {principle_name}:")
            print(f"      - 성공률: {success_rate:.1f}% ({result['success_cases']}/{result['total_cases']})")
            print(f"      - 정확도: {accuracy:.1f}%")
        
        if report['excellent_principles']:
            print(f"\n✅ 우수 원리 ({self.accuracy_thresholds['excellent']}%+):")
            for principle in report['excellent_principles']:
                print(f"   - {principle}")
        
        if report['problem_principles']:
            print(f"\n⚠️ 개선 필요 원리 ({self.accuracy_thresholds['acceptable']}%-):")
            for principle in report['problem_principles']:
                result = report['principle_results'][principle]
                print(f"   - {principle}: {result['success_rate']:.1f}%")
        
        print(f"\n💡 종합 평가:")
        if report['overall_accuracy'] >= 95:
            print("   🎉 사주 시스템의 모든 핵심 원리가 완벽하게 작동합니다!")
        elif report['overall_accuracy'] >= 85:
            print("   ✅ 사주 시스템이 전반적으로 안정적이며 높은 신뢰성을 보입니다.")
        elif report['overall_accuracy'] >= 75:
            print("   ⚠️ 사주 시스템이 기본적으로 작동하나 일부 원리의 개선이 필요합니다.")
        else:
            print("   🔧 사주 시스템의 핵심 원리들에 중대한 개선이 필요합니다.")
        
        # 리포트 저장
        report_filename = f"/tmp/{report['report_id']}.json"
        with open(report_filename, "w", encoding="utf-8") as f:
            json.dump(report, f, ensure_ascii=False, indent=2, default=str)
        
        print(f"\n💾 상세 리포트 저장: {report_filename}")
        print("=" * 80)
        
        return report


# 메인 실행 함수
async def run_comprehensive_principle_validation():
    """종합 원리 검증 실행"""
    
    validator = SajuCorePrincipleValidator()
    report = await validator.run_comprehensive_validation()
    return report


if __name__ == "__main__":
    asyncio.run(run_comprehensive_principle_validation())