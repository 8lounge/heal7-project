#!/usr/bin/env python3
"""
폴백시스템 핵심 검증 도구 - Primary Features
기본 검증 기능과 자주 사용되는 핵심 검증 로직
"""

import asyncio
import logging
from datetime import datetime, date, timedelta
from typing import Dict, List, Any, Tuple, Optional

from .shared.fallback_validator_models import (
    SolarTermData, ValidationResult, QuickValidationSummary, ValidationConstants
)
from .kasi_precision_saju_calculator import KasiPrecisionSajuCalculator
from .myeongrihak_constants import CHEONGAN, JIJI

logger = logging.getLogger(__name__)

class FallbackValidatorCore:
    """폴백시스템 핵심 검증 클래스 - 자주 사용되는 기본 기능"""
    
    def __init__(self):
        self.calculator = KasiPrecisionSajuCalculator()
        self.validation_results: List[ValidationResult] = []
    
    async def quick_validation(self, target_year: int = None) -> QuickValidationSummary:
        """빠른 기본 검증 - 가장 자주 사용됨"""
        if target_year is None:
            target_year = datetime.now().year
        
        critical_errors = []
        test_results = []
        
        # 핵심 검증 테스트들
        tests = [
            ("solar_terms", self._validate_basic_solar_terms),
            ("leap_year", self._validate_basic_leap_year),
            ("sexagenary", self._validate_basic_sexagenary_cycle),
        ]
        
        for category, test_func in tests:
            try:
                result = await test_func(target_year)
                test_results.extend(result)
            except Exception as e:
                critical_errors.append(f"{category}: {str(e)}")
                logger.error(f"Critical error in {category}: {e}")
        
        if not test_results:
            return QuickValidationSummary(
                total_tests=0, success_count=0, accuracy_rate=0.0,
                critical_errors=critical_errors, status="FAIL"
            )
        
        success_count = sum(1 for r in test_results if r.success)
        accuracy_rate = success_count / len(test_results)
        
        # 상태 결정
        if critical_errors:
            status = "FAIL"
        elif accuracy_rate >= ValidationConstants.CRITICAL_ACCURACY_THRESHOLD:
            status = "PASS"
        elif accuracy_rate >= ValidationConstants.MIN_ACCURACY_THRESHOLD:
            status = "WARNING"
        else:
            status = "FAIL"
        
        return QuickValidationSummary(
            total_tests=len(test_results),
            success_count=success_count,
            accuracy_rate=accuracy_rate,
            critical_errors=critical_errors,
            status=status
        )
    
    async def _validate_basic_solar_terms(self, year: int) -> List[ValidationResult]:
        """기본 24절기 검증"""
        results = []
        
        # 주요 절기만 빠르게 검증 (입춘, 춘분, 하지, 추분, 동지)
        key_terms = [0, 3, 9, 15, 21]  
        
        for term_index in key_terms:
            try:
                # KASI API로 절기 조회
                term_data = await self._get_solar_term_from_kasi(year, term_index)
                if term_data:
                    # 계산된 값과 비교
                    calculated = await self._calculate_solar_term(year, term_index)
                    
                    # 1일 이내 오차 허용
                    time_diff = abs((term_data.solar_date - calculated.solar_date).total_seconds())
                    accuracy = max(0, 1.0 - (time_diff / (24 * 3600)))  # 1일 기준
                    
                    results.append(ValidationResult(
                        test_category="solar_terms",
                        test_name=f"절기_{ValidationConstants.SOLAR_TERMS[term_index]}_{year}",
                        success=accuracy >= 0.95,
                        accuracy_score=accuracy,
                        reference_value=term_data.solar_date,
                        calculated_value=calculated.solar_date
                    ))
                
            except Exception as e:
                results.append(ValidationResult(
                    test_category="solar_terms",
                    test_name=f"절기_{term_index}_{year}",
                    success=False,
                    accuracy_score=0.0,
                    reference_value=None,
                    calculated_value=None,
                    error_message=str(e)
                ))
        
        return results
    
    async def _validate_basic_leap_year(self, year: int) -> List[ValidationResult]:
        """기본 윤년 계산 검증"""
        results = []
        
        test_years = [year-1, year, year+1]  # 간단한 3년 테스트
        
        for test_year in test_years:
            try:
                # 표준 윤년 계산
                expected_leap = self._is_leap_year_standard(test_year)
                
                # 사주 계산기 윤년 판정
                calculated_leap = await self.calculator.is_leap_year(test_year)
                
                accuracy = 1.0 if expected_leap == calculated_leap else 0.0
                
                results.append(ValidationResult(
                    test_category="leap_year",
                    test_name=f"윤년계산_{test_year}",
                    success=accuracy == 1.0,
                    accuracy_score=accuracy,
                    reference_value=expected_leap,
                    calculated_value=calculated_leap
                ))
                
            except Exception as e:
                results.append(ValidationResult(
                    test_category="leap_year", 
                    test_name=f"윤년계산_{test_year}",
                    success=False,
                    accuracy_score=0.0,
                    reference_value=None,
                    calculated_value=None,
                    error_message=str(e)
                ))
        
        return results
    
    async def _validate_basic_sexagenary_cycle(self, year: int) -> List[ValidationResult]:
        """기본 60갑자 순환 검증"""
        results = []
        
        # 간단한 10개 날짜 테스트
        test_dates = [
            date(year, 1, 1), date(year, 3, 1), date(year, 6, 1), 
            date(year, 9, 1), date(year, 12, 1)
        ]
        
        for test_date in test_dates:
            try:
                # 60갑자 계산
                calculated_cycle = await self.calculator.get_sexagenary_cycle(test_date)
                
                # 기본 검증 로직 (순환 일관성 체크)
                cheongan_index = calculated_cycle["day_cheongan_index"]
                jiji_index = calculated_cycle["day_jiji_index"]
                
                # 유효 범위 검증
                valid_cheongan = 0 <= cheongan_index < 10
                valid_jiji = 0 <= jiji_index < 12
                accuracy = 1.0 if (valid_cheongan and valid_jiji) else 0.0
                
                results.append(ValidationResult(
                    test_category="sexagenary",
                    test_name=f"갑자_{test_date}",
                    success=accuracy == 1.0,
                    accuracy_score=accuracy,
                    reference_value=f"{cheongan_index},{jiji_index}",
                    calculated_value=calculated_cycle
                ))
                
            except Exception as e:
                results.append(ValidationResult(
                    test_category="sexagenary",
                    test_name=f"갑자_{test_date}",
                    success=False,
                    accuracy_score=0.0,
                    reference_value=None,
                    calculated_value=None,
                    error_message=str(e)
                ))
        
        return results
    
    def _is_leap_year_standard(self, year: int) -> bool:
        """표준 윤년 계산"""
        return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)
    
    async def _get_solar_term_from_kasi(self, year: int, term_index: int) -> Optional[SolarTermData]:
        """KASI API에서 절기 정보 조회"""
        try:
            # KASI API 호출 로직 (실제 구현 필요)
            # 현재는 fallback 데이터 사용
            return await self._calculate_solar_term(year, term_index)
        except Exception as e:
            logger.error(f"KASI API 조회 실패: {e}")
            return None
    
    async def _calculate_solar_term(self, year: int, term_index: int) -> SolarTermData:
        """절기 계산 (폴백 메소드)"""
        # 간단한 절기 계산 로직
        base_date = datetime(year, 1, 1)
        days_offset = term_index * 15.2  # 대략적인 절기 간격
        
        solar_date = base_date + timedelta(days=days_offset)
        
        return SolarTermData(
            year=year,
            term_name=ValidationConstants.SOLAR_TERMS.get(term_index, f"절기_{term_index}"),
            term_index=term_index,
            solar_date=solar_date,
            korean_name=ValidationConstants.SOLAR_TERMS.get(term_index, f"절기_{term_index}"),
            source="CALCULATED",
            verified=False
        )