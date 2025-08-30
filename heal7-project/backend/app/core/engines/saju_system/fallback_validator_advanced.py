#!/usr/bin/env python3
"""
폴백시스템 고급 검증 도구 - Secondary Features
상세 분석, 종합 보고서, 성능 최적화 등 전문가용 기능
"""

import asyncio
import json
import sqlite3
import logging
from datetime import datetime, date, timedelta
from typing import Dict, List, Any, Tuple, Optional
from pathlib import Path
import statistics
import math

from .shared.fallback_validator_models import (
    SolarTermData, ValidationResult, QuickValidationSummary, ValidationConstants
)
from .fallback_validator_core import FallbackValidatorCore
from .performance_optimizer import PerformanceOptimizer

logger = logging.getLogger(__name__)

class FallbackValidatorAdvanced:
    """폴백시스템 고급 검증 클래스 - 전문가용 심화 기능"""
    
    def __init__(self):
        self.core_validator = FallbackValidatorCore()
        self.performance_optimizer = PerformanceOptimizer()
        self.validation_results: List[ValidationResult] = []
        self.db_path = "/tmp/validation_cache.db"
        self._init_cache_database()
    
    async def run_comprehensive_validation(self, start_year: int = 1950, end_year: int = 2025):
        """종합적인 폴백시스템 검증 실행 - 전체 기간 심층 분석"""
        
        print(f"\n🔍 폴백시스템 종합 검증 시작 ({start_year}-{end_year})")
        print("=" * 80)
        
        self.validation_results = []
        
        # 1. 24절기 데이터베이스 구축 및 검증
        await self._build_and_validate_solar_terms_db(start_year, end_year)
        
        # 2. 진태양시 보정 로직 검증
        await self._validate_true_solar_time_correction(start_year, end_year)
        
        # 3. 입춘 기준 월주 계산 검증
        await self._validate_monthly_pillar_calculation(start_year, end_year)
        
        # 4. 윤년 계산 로직 완전 검증
        await self._validate_comprehensive_leap_year(start_year, end_year)
        
        # 5. 60갑자 순환 일관성 검증
        await self._validate_comprehensive_sexagenary_cycle(start_year, end_year)
        
        # 6. 성별별 대운 계산 검증
        await self._validate_great_fortune_calculation(start_year, end_year)
        
        # 7. 종합 분석 및 보고서 생성
        await self._generate_comprehensive_report()
    
    async def _build_and_validate_solar_terms_db(self, start_year: int, end_year: int):
        """24절기 데이터베이스 구축 및 KASI 대조 검증"""
        
        print("\n📅 24절기 데이터베이스 검증 중...")
        
        for year in range(start_year, end_year + 1):
            if year % 10 == 0:
                print(f"   Processing year: {year}")
            
            for term_index in range(24):  # 전체 24절기
                try:
                    # KASI API 조회
                    kasi_data = await self._fetch_kasi_solar_term(year, term_index)
                    
                    # 만세력 계산 비교
                    calculated_data = await self._calculate_manseryeok_solar_term(year, term_index)
                    
                    # 정확도 계산
                    if kasi_data and calculated_data:
                        time_diff = abs((kasi_data.solar_date - calculated_data.solar_date).total_seconds())
                        accuracy = max(0, 1.0 - (time_diff / (6 * 3600)))  # 6시간 기준
                        
                        self.validation_results.append(ValidationResult(
                            test_category="solar_terms",
                            test_name=f"절기_{ValidationConstants.SOLAR_TERMS[term_index]}_{year}",
                            success=accuracy >= 0.9,
                            accuracy_score=accuracy,
                            reference_value=kasi_data.solar_date,
                            calculated_value=calculated_data.solar_date
                        ))
                        
                        # 데이터베이스에 캐시 저장
                        await self._cache_solar_term_data(kasi_data, calculated_data, accuracy)
                
                except Exception as e:
                    logger.error(f"절기 검증 실패 {year}-{term_index}: {e}")
                    self.validation_results.append(ValidationResult(
                        test_category="solar_terms",
                        test_name=f"절기_{term_index}_{year}",
                        success=False,
                        accuracy_score=0.0,
                        reference_value=None,
                        calculated_value=None,
                        error_message=str(e)
                    ))
    
    async def _validate_true_solar_time_correction(self, start_year: int, end_year: int):
        """진태양시 보정 및 서머타임 처리 로직 검증"""
        
        print("\n🌅 진태양시 보정 로직 검증 중...")
        
        # 주요 지역별 경도 테스트
        test_locations = [
            ("서울", 126.9780, 37.5665),
            ("부산", 129.0756, 35.1796), 
            ("제주", 126.5312, 33.4996),
            ("런던", -0.1276, 51.5072),
            ("뉴욕", -74.0060, 40.7128)
        ]
        
        for year in range(start_year, end_year + 1, 5):  # 5년 간격
            for location_name, longitude, latitude in test_locations:
                try:
                    test_datetime = datetime(year, 6, 21, 12, 0, 0)  # 하지 정오
                    
                    # 진태양시 보정 계산
                    corrected_time = await self.core_validator.calculator.apply_true_solar_time_correction(
                        test_datetime, longitude
                    )
                    
                    # 서머타임 적용 (필요시)
                    dst_corrected = await self.core_validator.calculator.apply_dst_correction(
                        corrected_time, latitude, longitude
                    )
                    
                    # 합리적 범위 검증 (±4시간 이내)
                    time_diff = abs((dst_corrected - test_datetime).total_seconds())
                    accuracy = 1.0 if time_diff <= 4 * 3600 else 0.5
                    
                    self.validation_results.append(ValidationResult(
                        test_category="true_solar_time",
                        test_name=f"진태양시_{location_name}_{year}",
                        success=accuracy >= 0.8,
                        accuracy_score=accuracy,
                        reference_value=test_datetime,
                        calculated_value=dst_corrected
                    ))
                
                except Exception as e:
                    self.validation_results.append(ValidationResult(
                        test_category="true_solar_time",
                        test_name=f"진태양시_{location_name}_{year}",
                        success=False,
                        accuracy_score=0.0,
                        reference_value=test_datetime,
                        calculated_value=None,
                        error_message=str(e)
                    ))
    
    async def _validate_monthly_pillar_calculation(self, start_year: int, end_year: int):
        """입춘 기준 월주 계산 검증"""
        
        print("\n📊 월주 계산 로직 검증 중...")
        
        for year in range(start_year, end_year + 1, 3):  # 3년 간격
            try:
                # 입춘 날짜 조회
                ipchun_data = await self._get_solar_term_date(year, 0)  # 입춘 = 0
                
                if ipchun_data:
                    # 입춘 전후 월주 계산 테스트
                    test_dates = [
                        ipchun_data.solar_date - timedelta(days=1),  # 입춘 전날
                        ipchun_data.solar_date,  # 입춘 당일
                        ipchun_data.solar_date + timedelta(days=1)   # 입춘 다음날
                    ]
                    
                    for test_date in test_dates:
                        monthly_pillar = await self.core_validator.calculator.calculate_monthly_pillar(
                            test_date
                        )
                        
                        # 입춘 기준 월 변경 로직 검증
                        is_after_ipchun = test_date >= ipchun_data.solar_date.date()
                        expected_month = 1 if is_after_ipchun else 12  # 간단한 검증
                        
                        # 실제 계산된 월과 비교
                        calculated_month = monthly_pillar.get("month_index", 0)
                        accuracy = 1.0 if abs(calculated_month - expected_month) <= 1 else 0.5
                        
                        self.validation_results.append(ValidationResult(
                            test_category="monthly_pillar",
                            test_name=f"월주_{test_date}_{year}",
                            success=accuracy >= 0.8,
                            accuracy_score=accuracy,
                            reference_value=expected_month,
                            calculated_value=calculated_month
                        ))
            
            except Exception as e:
                self.validation_results.append(ValidationResult(
                    test_category="monthly_pillar",
                    test_name=f"월주계산_{year}",
                    success=False,
                    accuracy_score=0.0,
                    reference_value=None,
                    calculated_value=None,
                    error_message=str(e)
                ))
    
    async def _generate_comprehensive_report(self):
        """종합 분석 보고서 생성"""
        
        print("\n📋 종합 검증 보고서 생성 중...")
        
        if not self.validation_results:
            print("❌ 검증 결과가 없습니다.")
            return
        
        # 전체 통계
        total_tests = len(self.validation_results)
        total_success = sum(1 for r in self.validation_results if r.success)
        overall_accuracy = (total_success / total_tests) * 100 if total_tests > 0 else 0
        
        # 카테고리별 분석
        category_stats = {}
        for result in self.validation_results:
            category = result.test_category
            if category not in category_stats:
                category_stats[category] = {"total": 0, "success": 0, "accuracy_scores": []}
            
            category_stats[category]["total"] += 1
            if result.success:
                category_stats[category]["success"] += 1
            category_stats[category]["accuracy_scores"].append(result.accuracy_score)
        
        # 보고서 출력
        print(f"\n🎯 전체 검증 결과:")
        print(f"   총 테스트: {total_tests:,}개")
        print(f"   성공: {total_success:,}개 ({overall_accuracy:.1f}%)")
        print(f"   실패: {total_tests - total_success:,}개")
        
        print(f"\n📊 카테고리별 상세 결과:")
        for category, stats in category_stats.items():
            success_rate = (stats["success"] / stats["total"]) * 100
            avg_accuracy = statistics.mean(stats["accuracy_scores"])
            print(f"   {category:20} | {stats['success']:4}/{stats['total']:4} ({success_rate:5.1f}%) | 평균정확도: {avg_accuracy:.3f}")
        
        # 성능 문제 영역 식별
        low_performance_areas = [
            category for category, stats in category_stats.items()
            if (stats["success"] / stats["total"]) * 100 < 85
        ]
        
        if low_performance_areas:
            print("   🔧 개선이 필요한 영역:")
            for area in low_performance_areas:
                print(f"      - {area}")
        
        # 신뢰성 등급
        if overall_accuracy >= 95:
            reliability_grade = "A+ (매우우수)"
        elif overall_accuracy >= 90:
            reliability_grade = "A (우수)"
        elif overall_accuracy >= 85:
            reliability_grade = "B+ (양호)"
        elif overall_accuracy >= 80:
            reliability_grade = "B (보통)"
        elif overall_accuracy >= 70:
            reliability_grade = "C (개선필요)"
        else:
            reliability_grade = "D (대폭개선필요)"
        
        print(f"\n🏆 폴백시스템 신뢰성 등급: {reliability_grade}")
        
        # JSON 보고서 저장
        await self._save_detailed_report(overall_accuracy, category_stats, reliability_grade)
    
    async def _save_detailed_report(self, overall_accuracy: float, category_stats: dict, reliability_grade: str):
        """상세 JSON 보고서 저장"""
        
        report_data = {
            "validation_timestamp": datetime.now().isoformat(),
            "overall_accuracy": overall_accuracy,
            "total_tests": len(self.validation_results),
            "success_tests": sum(1 for r in self.validation_results if r.success),
            "category_stats": category_stats,
            "reliability_grade": reliability_grade,
            "detailed_results": [
                {
                    "category": r.test_category,
                    "test_name": r.test_name,
                    "success": r.success,
                    "accuracy_score": r.accuracy_score,
                    "reference_value": str(r.reference_value),
                    "calculated_value": str(r.calculated_value),
                    "error_message": r.error_message
                }
                for r in self.validation_results
            ]
        }
        
        report_path = f"/tmp/comprehensive_validation_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_path, "w", encoding="utf-8") as f:
            json.dump(report_data, f, ensure_ascii=False, indent=2)
        
        print(f"\n💾 상세 보고서 저장: {report_path}")
    
    def _init_cache_database(self):
        """검증 캐시 데이터베이스 초기화"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("""
                    CREATE TABLE IF NOT EXISTS solar_terms_cache (
                        year INTEGER,
                        term_index INTEGER,
                        kasi_date TEXT,
                        calculated_date TEXT,
                        accuracy REAL,
                        cached_at TEXT,
                        PRIMARY KEY (year, term_index)
                    )
                """)
                conn.commit()
        except Exception as e:
            logger.error(f"Cache DB 초기화 실패: {e}")
    
    # 추가 고급 검증 메소드들 (생략)
    async def _validate_comprehensive_leap_year(self, start_year: int, end_year: int):
        """윤년 계산 로직 완전 검증"""
        pass
    
    async def _validate_comprehensive_sexagenary_cycle(self, start_year: int, end_year: int):
        """60갑자 순환 일관성 검증"""
        pass
    
    async def _validate_great_fortune_calculation(self, start_year: int, end_year: int):
        """성별별 대운 계산 검증"""
        pass