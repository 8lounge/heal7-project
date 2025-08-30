#!/usr/bin/env python3
"""
실패 원리 심층 분석기 v1.0
검증에서 실패한 핵심 원리들을 깊이 있게 연구하고 개선

실패 원리들:
1. 년주_60갑자_순환: 60년 주기 순환 검증 실패
2. 월주_24절기_기준: 절기 경계 월주 변경 검증 실패  
3. 월주_년간_월간_관계: 년간별 월간 배치 규칙 실패
4. 시주_시두법: 시두법 규칙 적용 실패

추가 연구:
5. 월두법: 월주 천간 결정의 핵심 법칙
"""

import asyncio
import json
import logging
from datetime import datetime, date, timedelta
from typing import Dict, List, Any, Tuple, Optional
from dataclasses import dataclass
import statistics
import math

# 사주 시스템 모듈
from .kasi_precision_saju_calculator import KasiPrecisionSajuCalculator
from .myeongrihak_constants import CHEONGAN, JIJI

logger = logging.getLogger(__name__)

@dataclass
class DeepAnalysisResult:
    """심층 분석 결과"""
    principle_name: str
    problem_description: str
    root_cause: str
    current_logic: str
    corrected_logic: str
    test_cases: List[Dict[str, Any]]
    improvement_score: float
    validation_results: List[Dict[str, Any]]

class FailedPrinciplesDeepAnalyzer:
    """실패 원리 심층 분석기"""
    
    def __init__(self):
        self.kasi_calculator = KasiPrecisionSajuCalculator()
        
        # 분석 결과 저장
        self.analysis_results = []
        
        # 명리학 핵심 상수들
        self.CHEONGAN_HANJA = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
        self.JIJI_HANJA = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
        
        # 60갑자 완전 매핑
        self.GAPJA_60 = []
        for i in range(60):
            cheongan = self.CHEONGAN_HANJA[i % 10] 
            jiji = self.JIJI_HANJA[i % 12]
            self.GAPJA_60.append(cheongan + jiji)
        
        # 24절기 한자명 (정확한 순서)
        self.SOLAR_TERMS_24 = [
            "立春", "雨水", "驚蟄", "春分", "清明", "穀雨",      # 봄 (1-6월)
            "立夏", "小滿", "芒種", "夏至", "小暑", "大暑",      # 여름 (7-12월) 
            "立秋", "處暑", "白露", "秋分", "寒露", "霜降",      # 가을 (13-18월)
            "立冬", "小雪", "大雪", "冬至", "小寒", "大寒"       # 겨울 (19-24월)
        ]
        
        # 월두법 핵심 규칙 (년간별 정월 월간)
        self.WOLDOOBEOP_RULES = {
            # 갑기년: 정월부터 병인
            "甲": "丙", "己": "丙",
            # 을경년: 정월부터 무인  
            "乙": "戊", "庚": "戊",
            # 병신년: 정월부터 경인
            "丙": "庚", "辛": "庚", 
            # 정임년: 정월부터 임인
            "丁": "壬", "壬": "壬",
            # 무계년: 정월부터 갑인
            "戊": "甲", "癸": "甲"
        }
        
        # 시두법 핵심 규칙 (일간별 자시 천간)
        self.SIDUBEOP_RULES = {
            # 갑기일: 자시부터 갑자
            "甲": "甲", "己": "甲",
            # 을경일: 자시부터 병자
            "乙": "丙", "庚": "丙",
            # 병신일: 자시부터 무자
            "丙": "戊", "辛": "戊",
            # 정임일: 자시부터 경자
            "丁": "庚", "壬": "庚",
            # 무계일: 자시부터 임자
            "戊": "壬", "癸": "壬"
        }
    
    async def run_deep_analysis(self):
        """실패 원리들 심층 분석 실행"""
        
        print("🔍 실패 원리 심층 분석 시작")
        print("=" * 80)
        print("년주 60갑자 순환 | 월주 24절기 | 월두법 | 시두법 심층 연구")
        print("=" * 80)
        
        analysis_start = datetime.now()
        
        # 1. 년주 60갑자 순환 분석
        print("\n🎯 1. 년주 60갑자 순환 로직 심층 분석")
        print("-" * 50)
        year_analysis = await self._analyze_year_gapja_cycle()
        self.analysis_results.append(year_analysis)
        
        # 2. 월주 24절기 경계 분석  
        print("\n🎯 2. 월주 24절기 경계 로직 심층 분석")
        print("-" * 50)
        month_solar_analysis = await self._analyze_month_solar_terms()
        self.analysis_results.append(month_solar_analysis)
        
        # 3. 월두법 (년간-월간 관계) 분석
        print("\n🎯 3. 월두법 (년간-월간 관계) 심층 분석")
        print("-" * 50)
        woldoobeop_analysis = await self._analyze_woldoobeop_logic()
        self.analysis_results.append(woldoobeop_analysis)
        
        # 4. 시두법 분석
        print("\n🎯 4. 시두법 매핑 로직 심층 분석")
        print("-" * 50) 
        sidubeop_analysis = await self._analyze_sidubeop_logic()
        self.analysis_results.append(sidubeop_analysis)
        
        # 5. 통합 개선 방안
        print("\n🎯 5. 통합 개선 방안 및 최종 검증")
        print("-" * 50)
        integrated_improvements = await self._generate_integrated_improvements()
        
        # 6. 최종 리포트
        total_time = (datetime.now() - analysis_start).total_seconds()
        await self._output_comprehensive_analysis_report(total_time)
        
        return self.analysis_results
    
    async def _analyze_year_gapja_cycle(self) -> DeepAnalysisResult:
        """년주 60갑자 순환 심층 분석"""
        
        print("   📊 60갑자 순환 수학적 일관성 분석 중...")
        
        # 기준점들로 수학적 일관성 검증
        reference_years = [
            {"year": 1984, "expected": "甲子", "description": "갑자년_기준"},
            {"year": 1985, "expected": "乙丑", "description": "을축년_다음"},
            {"year": 2044, "expected": "甲子", "description": "60년후_갑자"},  # 1984 + 60
            {"year": 1924, "expected": "甲子", "description": "60년전_갑자"},  # 1984 - 60
        ]
        
        test_results = []
        correct_count = 0
        
        for ref_year in reference_years:
            try:
                # KASI로 실제 년주 확인
                kasi_result = self.kasi_calculator.calculate_saju(
                    ref_year["year"], 6, 15, 12, 0, False  # 중간 안전 날짜
                )
                
                if kasi_result:
                    actual_year_gapja = kasi_result["pillars"]["year"]["gapja"]
                    
                    # 수학적 계산 검증
                    calculated_index = (ref_year["year"] - 4) % 60  # 서기 4년 = 갑자년
                    calculated_gapja = self.GAPJA_60[calculated_index]
                    
                    # 비교
                    kasi_match = (actual_year_gapja == ref_year["expected"])
                    math_match = (calculated_gapja == ref_year["expected"])
                    kasi_math_match = (actual_year_gapja == calculated_gapja)
                    
                    if kasi_match and math_match and kasi_math_match:
                        correct_count += 1
                        status = "✅"
                    else:
                        status = "❌"
                    
                    test_result = {
                        "year": ref_year["year"],
                        "description": ref_year["description"],
                        "expected": ref_year["expected"],
                        "kasi_actual": actual_year_gapja,
                        "math_calculated": calculated_gapja,
                        "kasi_match": kasi_match,
                        "math_match": math_match,
                        "kasi_math_match": kasi_math_match,
                        "status": status
                    }
                    
                    test_results.append(test_result)
                    
                    print(f"      {status} {ref_year['year']}년: 기대={ref_year['expected']}, KASI={actual_year_gapja}, 계산={calculated_gapja}")
                    
            except Exception as e:
                logger.error(f"년주 분석 실패 {ref_year['year']}: {e}")
        
        # 근본 원인 분석
        if correct_count < len(reference_years):
            root_cause = "60갑자 순환 기준점 또는 수학적 공식에 오류"
            problem = "KASI 결과와 수학적 계산 간 불일치 발견"
            
            # 실제 패턴 분석
            if test_results:
                kasi_years = [r["kasi_actual"] for r in test_results if r["kasi_actual"]]
                calc_years = [r["math_calculated"] for r in test_results if r["math_calculated"]]
                
                corrected_logic = f"""
                수정된 60갑자 순환 로직:
                1. KASI 기준 년주: {', '.join(kasi_years[:3])}...
                2. 수학 계산 년주: {', '.join(calc_years[:3])}...
                3. 기준점 재검토 필요: 서기 4년 = 갑자년 검증
                4. 입춘 경계 처리 강화
                """
        else:
            root_cause = "검증 로직 자체의 오류"
            problem = "실제로는 정상 작동하나 검증 방식 부정확"
            corrected_logic = "검증 케이스 및 기대값 재검토 필요"
        
        improvement_score = (correct_count / len(reference_years)) * 100
        
        print(f"   📊 60갑자 순환 분석 완료: {improvement_score:.1f}% 일치율")
        
        return DeepAnalysisResult(
            principle_name="년주_60갑자_순환",
            problem_description=problem,
            root_cause=root_cause,
            current_logic="(년도 - 4) % 60으로 갑자 인덱스 계산",
            corrected_logic=corrected_logic,
            test_cases=reference_years,
            improvement_score=improvement_score,
            validation_results=test_results
        )
    
    async def _analyze_month_solar_terms(self) -> DeepAnalysisResult:
        """월주 24절기 경계 심층 분석"""
        
        print("   📅 24절기 경계 월주 변경 로직 분석 중...")
        
        # 절기 경계 테스트 케이스들
        solar_term_boundaries = [
            {"date": "2024-02-04", "term": "立春", "description": "입춘_월주변경"},
            {"date": "2024-03-05", "term": "驚蟄", "description": "경칩_월주변경"},
            {"date": "2024-04-04", "term": "清明", "description": "청명_월주변경"},
            {"date": "2024-05-05", "term": "立夏", "description": "입하_월주변경"},
        ]
        
        test_results = []
        boundary_changes = 0
        
        for boundary in solar_term_boundaries:
            try:
                year, month, day = map(int, boundary["date"].split("-"))
                
                # 절기 이전일 (하루 전)
                before_result = self.kasi_calculator.calculate_saju(year, month, day-1, 12, 0, False)
                
                # 절기 이후일 (하루 후)
                after_result = self.kasi_calculator.calculate_saju(year, month, day+1, 12, 0, False)
                
                if before_result and after_result:
                    before_month = before_result["pillars"]["month"]["gapja"]
                    after_month = after_result["pillars"]["month"]["gapja"]
                    
                    # 월주 변경 여부
                    month_changed = (before_month != after_month)
                    
                    if month_changed:
                        boundary_changes += 1
                        status = "✅"
                    else:
                        status = "❌"
                    
                    test_result = {
                        "date": boundary["date"],
                        "term": boundary["term"],
                        "description": boundary["description"],
                        "before_month": before_month,
                        "after_month": after_month,
                        "month_changed": month_changed,
                        "status": status
                    }
                    
                    test_results.append(test_result)
                    
                    print(f"      {status} {boundary['term']} ({boundary['date']}): {before_month} → {after_month}")
                    
            except Exception as e:
                logger.error(f"절기 경계 분석 실패 {boundary['date']}: {e}")
        
        # 월두법과 연계 분석
        print("   🔄 월두법과 절기 경계 연관성 분석...")
        
        # 2024년 전체 월주 패턴 분석
        year_2024_months = []
        for month in range(1, 13):
            try:
                mid_month_result = self.kasi_calculator.calculate_saju(2024, month, 15, 12, 0, False)
                if mid_month_result:
                    month_gapja = mid_month_result["pillars"]["month"]["gapja"]
                    year_gapja = mid_month_result["pillars"]["year"]["gapja"]
                    year_2024_months.append({
                        "month": month,
                        "year_gapja": year_gapja,
                        "month_gapja": month_gapja,
                        "month_gan": month_gapja[0] if month_gapja else None
                    })
            except Exception as e:
                logger.warning(f"2024년 {month}월 분석 실패: {e}")
        
        # 월두법 규칙 검증
        woldoobeop_match = 0
        if year_2024_months:
            year_gan = year_2024_months[0]["year_gapja"][0]  # 2024년 천간 (甲)
            expected_first_month_gan = self.WOLDOOBEOP_RULES.get(year_gan)
            
            # 정월(인월) 월간 확인 (보통 2-3월경)
            for month_data in year_2024_months:
                if month_data["month"] in [2, 3]:  # 정월 후보
                    if month_data["month_gan"] == expected_first_month_gan:
                        woldoobeop_match += 1
        
        improvement_score = (boundary_changes / len(solar_term_boundaries)) * 100
        
        # 근본 원인 분석
        if improvement_score < 80:
            root_cause = "절기 경계 판정 로직 또는 기준일 설정 오류"
            corrected_logic = f"""
            개선된 24절기 경계 로직:
            1. 정확한 절기일 계산 (KASI API 기준)
            2. 절기 이전/이후 명확한 구분
            3. 월두법과 절기의 연관성 강화
            4. 2024년 월간 패턴: {[m['month_gan'] for m in year_2024_months[:6]]}
            """
        else:
            root_cause = "검증 방식의 오류 - 실제 로직은 정상"
            corrected_logic = "절기 경계 검증 방법론 개선 필요"
        
        print(f"   📊 24절기 경계 분석 완료: {improvement_score:.1f}% 경계 변경률")
        print(f"   🔄 월두법 연관성: {woldoobeop_match}개월 일치")
        
        return DeepAnalysisResult(
            principle_name="월주_24절기_기준",
            problem_description="절기 경계에서 월주 변경 검증 실패",
            root_cause=root_cause,
            current_logic="절기 이전/이후 월주 비교로 변경 여부 판정",
            corrected_logic=corrected_logic,
            test_cases=solar_term_boundaries,
            improvement_score=improvement_score,
            validation_results=test_results
        )
    
    async def _analyze_woldoobeop_logic(self) -> DeepAnalysisResult:
        """월두법 (년간-월간 관계) 심층 분석"""
        
        print("   🌙 월두법 규칙 정확성 분석 중...")
        
        # 월두법 규칙별 검증
        woldoobeop_test_cases = [
            {"year": 1984, "year_gan": "甲", "expected_jan_gan": "丙", "description": "갑년_정월병인"},
            {"year": 1985, "year_gan": "乙", "expected_jan_gan": "戊", "description": "을년_정월무인"},  
            {"year": 1986, "year_gan": "丙", "expected_jan_gan": "庚", "description": "병년_정월경인"},
            {"year": 1987, "year_gan": "丁", "expected_jan_gan": "壬", "description": "정년_정월임인"},
            {"year": 1988, "year_gan": "戊", "expected_jan_gan": "甲", "description": "무년_정월갑인"},
        ]
        
        test_results = []
        correct_matches = 0
        
        for test_case in woldoobeop_test_cases:
            try:
                # 입춘 이후 안전한 정월 날짜로 검증
                kasi_result = self.kasi_calculator.calculate_saju(
                    test_case["year"], 2, 15, 12, 0, False
                )
                
                if kasi_result:
                    actual_year_gan = kasi_result["pillars"]["year"]["cheongan"]
                    actual_month_gan = kasi_result["pillars"]["month"]["cheongan"] 
                    
                    # 년간 일치 확인
                    year_gan_match = (actual_year_gan == test_case["year_gan"])
                    
                    # 월간 일치 확인
                    month_gan_match = (actual_month_gan == test_case["expected_jan_gan"])
                    
                    if year_gan_match and month_gan_match:
                        correct_matches += 1
                        status = "✅"
                    else:
                        status = "❌"
                    
                    test_result = {
                        "year": test_case["year"],
                        "description": test_case["description"],
                        "expected_year_gan": test_case["year_gan"],
                        "expected_month_gan": test_case["expected_jan_gan"],
                        "actual_year_gan": actual_year_gan,
                        "actual_month_gan": actual_month_gan,
                        "year_gan_match": year_gan_match,
                        "month_gan_match": month_gan_match,
                        "status": status
                    }
                    
                    test_results.append(test_result)
                    
                    print(f"      {status} {test_case['year']}년: 년간={actual_year_gan}(기대:{test_case['year_gan']}) 월간={actual_month_gan}(기대:{test_case['expected_jan_gan']})")
                    
            except Exception as e:
                logger.error(f"월두법 분석 실패 {test_case['year']}: {e}")
        
        # 월두법 핵심 규칙 패턴 분석
        print("   🔍 월두법 핵심 규칙 패턴 검증...")
        
        # 실제 KASI 데이터로 월두법 규칙 역산
        discovered_rules = {}
        
        for result in test_results:
            if result["year_gan_match"]:
                year_gan = result["actual_year_gan"]
                month_gan = result["actual_month_gan"]
                
                if year_gan not in discovered_rules:
                    discovered_rules[year_gan] = []
                discovered_rules[year_gan].append(month_gan)
        
        # 규칙 일관성 검증
        consistent_rules = {}
        for year_gan, month_gans in discovered_rules.items():
            if len(set(month_gans)) == 1:  # 일관된 규칙
                consistent_rules[year_gan] = month_gans[0]
        
        improvement_score = (correct_matches / len(woldoobeop_test_cases)) * 100
        
        # 근본 원인 분석
        if improvement_score < 80:
            root_cause = "월두법 규칙 테이블 또는 적용 로직 오류"
            
            corrected_logic = f"""
            수정된 월두법 규칙:
            기존 규칙: {self.WOLDOOBEOP_RULES}
            실제 발견: {consistent_rules}
            
            개선 방안:
            1. KASI 기준 월두법 규칙 재구성
            2. 절기와 월간 관계 정밀 매핑
            3. 정월 기준일 정확한 설정
            """
        else:
            root_cause = "검증 시점 또는 방법론 오류"
            corrected_logic = "월두법 검증 시기 및 절기 고려 개선"
        
        print(f"   📊 월두법 분석 완료: {improvement_score:.1f}% 정확도")
        print(f"   🎯 발견된 규칙: {len(consistent_rules)}개 일관성 확인")
        
        return DeepAnalysisResult(
            principle_name="월주_년간_월간_관계_월두법",
            problem_description="년간에 따른 월간 배치 규칙 검증 실패",
            root_cause=root_cause,
            current_logic=f"월두법 규칙: {self.WOLDOOBEOP_RULES}",
            corrected_logic=corrected_logic,
            test_cases=woldoobeop_test_cases,
            improvement_score=improvement_score,
            validation_results=test_results
        )
    
    async def _analyze_sidubeop_logic(self) -> DeepAnalysisResult:
        """시두법 매핑 로직 심층 분석"""
        
        print("   ⏰ 시두법 규칙 정확성 분석 중...")
        
        # 시두법 핵심 테스트 케이스들
        sidubeop_test_cases = [
            {"date": "2024-06-15", "hour": 0, "description": "갑일_자시_갑자", "expected_pattern": "甲일+자시→甲"},
            {"date": "2024-06-16", "hour": 0, "description": "을일_자시_병자", "expected_pattern": "乙일+자시→丙"},
            {"date": "2024-06-17", "hour": 0, "description": "병일_자시_무자", "expected_pattern": "丙일+자시→戊"},
            {"date": "2024-06-18", "hour": 6, "description": "일간별_묘시", "expected_pattern": "묘시_시두법"},
        ]
        
        test_results = []
        correct_applications = 0
        
        for test_case in sidubeop_test_cases:
            try:
                year, month, day = map(int, test_case["date"].split("-"))
                
                # KASI로 실제 시주 계산
                kasi_result = self.kasi_calculator.calculate_saju(
                    year, month, day, test_case["hour"], 0, False
                )
                
                if kasi_result:
                    day_gan = kasi_result["pillars"]["day"]["cheongan"]
                    hour_gapja = kasi_result["pillars"]["hour"]["gapja"]
                    hour_gan = hour_gapja[0] if hour_gapja else None
                    hour_jiji = hour_gapja[1] if len(hour_gapja) > 1 else None
                    
                    # 시두법 규칙 적용
                    expected_hour_gan = self.SIDUBEOP_RULES.get(day_gan)
                    
                    if expected_hour_gan:
                        # 시간에 따른 천간 계산
                        hour_index = self._get_hour_jiji_index(test_case["hour"])
                        
                        if hour_index is not None:
                            # 천간 순환 계산
                            base_gan_index = self.CHEONGAN_HANJA.index(expected_hour_gan)
                            calculated_gan_index = (base_gan_index + hour_index) % 10
                            calculated_hour_gan = self.CHEONGAN_HANJA[calculated_gan_index]
                            
                            # 검증
                            sidubeop_match = (hour_gan == calculated_hour_gan)
                            
                            if sidubeop_match:
                                correct_applications += 1
                                status = "✅"
                            else:
                                status = "❌"
                        else:
                            status = "❓"
                            sidubeop_match = False
                            calculated_hour_gan = "시간_인덱스_오류"
                    else:
                        status = "❓"
                        sidubeop_match = False
                        calculated_hour_gan = "규칙_없음"
                    
                    test_result = {
                        "date": test_case["date"],
                        "hour": test_case["hour"],
                        "description": test_case["description"],
                        "day_gan": day_gan,
                        "hour_gapja": hour_gapja,
                        "hour_gan": hour_gan,
                        "expected_base_gan": expected_hour_gan,
                        "calculated_gan": calculated_hour_gan,
                        "sidubeop_match": sidubeop_match,
                        "status": status
                    }
                    
                    test_results.append(test_result)
                    
                    print(f"      {status} {test_case['description']}: 일간={day_gan}, 시주={hour_gapja}, 기대={calculated_hour_gan}")
                    
            except Exception as e:
                logger.error(f"시두법 분석 실패 {test_case['date']}: {e}")
        
        # 시두법 전체 매핑 테이블 검증
        print("   🕐 시두법 12시진 전체 매핑 검증...")
        
        # 특정일(갑일)로 12시진 전체 검증
        full_day_test = await self._verify_full_day_sidubeop("2024-06-15")  # 갑일 추정
        
        improvement_score = (correct_applications / len(sidubeop_test_cases)) * 100
        
        # 근본 원인 분석
        if improvement_score < 80:
            root_cause = "시두법 규칙 테이블 또는 시간 인덱스 계산 오류"
            
            corrected_logic = f"""
            수정된 시두법 로직:
            1. 현재 규칙: {self.SIDUBEOP_RULES}
            2. 시간 인덱스 재검토 필요
            3. 12시진 매핑: {self._get_12_hour_mapping()}
            4. 천간 순환 계산 검증
            5. 전체 테스트: {full_day_test}
            """
        else:
            root_cause = "검증 방법론 또는 기준 설정 오류"
            corrected_logic = "시두법 검증 로직 및 시간 경계 처리 개선"
        
        print(f"   📊 시두법 분석 완료: {improvement_score:.1f}% 정확도")
        
        return DeepAnalysisResult(
            principle_name="시주_시두법",
            problem_description="일간에 따른 시천간 배치 규칙 검증 실패",
            root_cause=root_cause,
            current_logic=f"시두법 규칙: {self.SIDUBEOP_RULES}",
            corrected_logic=corrected_logic,
            test_cases=sidubeop_test_cases,
            improvement_score=improvement_score,
            validation_results=test_results
        )
    
    def _get_hour_jiji_index(self, hour: int) -> Optional[int]:
        """시간을 12지지 인덱스로 변환"""
        
        # 12시진 매핑 (자=0, 축=1, ..., 해=11)
        hour_mapping = {
            23: 0, 0: 0,           # 자시 (23:00-01:00) 
            1: 1, 2: 1,            # 축시 (01:00-03:00)
            3: 2, 4: 2,            # 인시 (03:00-05:00)
            5: 3, 6: 3,            # 묘시 (05:00-07:00)
            7: 4, 8: 4,            # 진시 (07:00-09:00)
            9: 5, 10: 5,           # 사시 (09:00-11:00)
            11: 6, 12: 6,          # 오시 (11:00-13:00)
            13: 7, 14: 7,          # 미시 (13:00-15:00)
            15: 8, 16: 8,          # 신시 (15:00-17:00)
            17: 9, 18: 9,          # 유시 (17:00-19:00)
            19: 10, 20: 10,        # 술시 (19:00-21:00)
            21: 11, 22: 11,        # 해시 (21:00-23:00)
        }
        
        return hour_mapping.get(hour)
    
    def _get_12_hour_mapping(self) -> Dict[str, str]:
        """12시진 한자 매핑"""
        
        return {
            "子": "자시 (23-01)",
            "丑": "축시 (01-03)",
            "寅": "인시 (03-05)", 
            "卯": "묘시 (05-07)",
            "辰": "진시 (07-09)",
            "巳": "사시 (09-11)",
            "午": "오시 (11-13)",
            "未": "미시 (13-15)",
            "申": "신시 (15-17)",
            "酉": "유시 (17-19)",
            "戌": "술시 (19-21)",
            "亥": "해시 (21-23)"
        }
    
    async def _verify_full_day_sidubeop(self, test_date: str) -> Dict[str, Any]:
        """특정일 12시진 전체 시두법 검증"""
        
        year, month, day = map(int, test_date.split("-"))
        hour_tests = []
        
        # 12시진 대표 시간으로 테스트
        test_hours = [0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22]
        
        for hour in test_hours:
            try:
                result = self.kasi_calculator.calculate_saju(year, month, day, hour, 0, False)
                if result:
                    hour_tests.append({
                        "hour": hour,
                        "hour_gapja": result["pillars"]["hour"]["gapja"],
                        "day_gan": result["pillars"]["day"]["cheongan"]
                    })
            except:
                pass
        
        return {
            "test_date": test_date,
            "tested_hours": len(hour_tests),
            "pattern": [test["hour_gapja"] for test in hour_tests[:6]]  # 처음 6개만
        }
    
    async def _generate_integrated_improvements(self) -> Dict[str, Any]:
        """통합 개선 방안 생성"""
        
        print("   🔧 통합 개선 방안 수립 중...")
        
        # 모든 분석 결과 종합
        total_principles = len(self.analysis_results)
        high_score_principles = [r for r in self.analysis_results if r.improvement_score >= 80]
        low_score_principles = [r for r in self.analysis_results if r.improvement_score < 80]
        
        # 우선순위 개선 영역
        priority_improvements = []
        
        for result in low_score_principles:
            priority_improvements.append({
                "principle": result.principle_name,
                "priority": "HIGH" if result.improvement_score < 50 else "MEDIUM",
                "root_cause": result.root_cause,
                "improvement_action": result.corrected_logic
            })
        
        # 전체 개선 전략
        improvement_strategy = {
            "total_principles_analyzed": total_principles,
            "high_performance_count": len(high_score_principles),
            "needs_improvement_count": len(low_score_principles),
            "priority_improvements": priority_improvements,
            "integrated_approach": """
            통합 개선 접근법:
            1. KASI API 기준 검증 강화
            2. 명리학 핵심 규칙 재검토
            3. 검증 로직 vs 실제 로직 분리
            4. 시간 경계 처리 정밀화
            5. 절기-월주 연관성 강화
            """
        }
        
        print(f"   📊 분석 완료: {len(high_score_principles)}/{total_principles}개 원리 양호")
        print(f"   🎯 우선 개선: {len(priority_improvements)}개 영역")
        
        return improvement_strategy
    
    async def _output_comprehensive_analysis_report(self, total_time: float):
        """종합 분석 리포트 출력"""
        
        print("\n" + "=" * 80)
        print("🎯 실패 원리 심층 분석 최종 리포트")
        print("=" * 80)
        
        print(f"\n📊 분석 개요:")
        print(f"   - 분석 대상: {len(self.analysis_results)}개 실패 원리")
        print(f"   - 분석 시간: {total_time:.1f}초")
        print(f"   - 분석 방법: KASI API 기준 + 명리학 원리 검증")
        
        print(f"\n🎯 원리별 상세 분석:")
        
        for result in self.analysis_results:
            score = result.improvement_score
            grade = "🟢" if score >= 80 else "🟡" if score >= 50 else "🔴"
            
            print(f"\n   {grade} {result.principle_name}")
            print(f"      📊 개선 점수: {score:.1f}%")
            print(f"      🔍 문제점: {result.problem_description}")
            print(f"      🎯 근본원인: {result.root_cause}")
            print(f"      🛠️ 현재로직: {result.current_logic}")
            
            if result.validation_results:
                success_count = sum(1 for v in result.validation_results if v.get("status") == "✅")
                total_count = len(result.validation_results)
                print(f"      ✅ 검증결과: {success_count}/{total_count} 성공")
        
        # 핵심 발견사항
        print(f"\n💡 핵심 발견사항:")
        
        avg_score = sum(r.improvement_score for r in self.analysis_results) / len(self.analysis_results)
        
        if avg_score >= 80:
            print("   🎉 대부분의 원리가 정상 작동 - 검증 방법론 개선 필요")
        elif avg_score >= 50:
            print("   ⚠️ 일부 원리에 실제 오류 존재 - 선별적 개선 필요")
        else:
            print("   🚨 다수 원리에 중대한 오류 - 전면적 재검토 필요")
        
        # 구체적 개선 권장사항
        print(f"\n🔧 구체적 개선 권장사항:")
        
        critical_principles = [r for r in self.analysis_results if r.improvement_score < 50]
        
        if critical_principles:
            print("   🚨 즉시 개선 필요:")
            for p in critical_principles:
                print(f"      - {p.principle_name}: {p.root_cause}")
        
        moderate_principles = [r for r in self.analysis_results if 50 <= r.improvement_score < 80]
        
        if moderate_principles:
            print("   ⚠️ 단기 개선 권장:")
            for p in moderate_principles:
                print(f"      - {p.principle_name}: {p.problem_description}")
        
        good_principles = [r for r in self.analysis_results if r.improvement_score >= 80]
        
        if good_principles:
            print("   ✅ 검증 로직 개선:")
            for p in good_principles:
                print(f"      - {p.principle_name}: 실제 로직 정상, 검증 방식 개선")
        
        # 최종 결론
        print(f"\n📋 최종 결론:")
        
        if avg_score >= 80:
            print("   🎯 실패 원리들의 실제 로직은 대부분 정상입니다.")
            print("   🔧 주요 문제는 검증 방법론과 기준 설정에 있습니다.")
            print("   💡 검증 시점, 비교 기준, 경계 처리를 정밀화하면 해결됩니다.")
        else:
            print("   🚨 일부 원리에 실제 로직 오류가 존재합니다.")
            print("   🛠️ 명리학 핵심 규칙과 KASI 기준의 재정렬이 필요합니다.")
            print("   📚 전통 명리학 서적과의 교차 검증을 권장합니다.")
        
        # 리포트 저장
        report_data = {
            "analysis_timestamp": datetime.now().isoformat(),
            "total_analysis_time": total_time,
            "analysis_results": [
                {
                    "principle_name": r.principle_name,
                    "improvement_score": r.improvement_score,
                    "problem_description": r.problem_description,
                    "root_cause": r.root_cause,
                    "current_logic": r.current_logic,
                    "corrected_logic": r.corrected_logic,
                    "test_cases_count": len(r.test_cases),
                    "validation_results_count": len(r.validation_results)
                }
                for r in self.analysis_results
            ],
            "overall_score": avg_score,
            "critical_count": len(critical_principles),
            "moderate_count": len(moderate_principles),
            "good_count": len(good_principles)
        }
        
        report_filename = f"/tmp/failed_principles_deep_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_filename, "w", encoding="utf-8") as f:
            json.dump(report_data, f, ensure_ascii=False, indent=2, default=str)
        
        print(f"\n💾 상세 분석 리포트 저장: {report_filename}")
        print("=" * 80)


# 메인 실행 함수
async def run_failed_principles_analysis():
    """실패 원리 심층 분석 실행"""
    
    analyzer = FailedPrinciplesDeepAnalyzer()
    results = await analyzer.run_deep_analysis()
    return results


if __name__ == "__main__":
    asyncio.run(run_failed_principles_analysis())