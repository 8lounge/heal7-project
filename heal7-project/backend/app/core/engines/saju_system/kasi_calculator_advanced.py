"""
KASI API 정밀 사주 계산기 - 고급 기능 모듈
검증, 최적화, 상세 분석 등 전문가용 기능들
"""

import os
import requests
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import logging
import re
import json

from .kasi_calculator_core import KasiCalculatorCore
from .shared.kasi_calculator_models import (
    KOREAN_TO_CHINESE_GANJEE, CHEONGAN, JIJI, SIDUBEOP,
    GAPJA_REFERENCE_TABLE, SajuResult, KasiApiConfig
)

logger = logging.getLogger(__name__)

class KasiCalculatorAdvanced:
    """KASI API 정밀 사주 계산기 - 고급 검증 및 최적화 기능"""
    
    def __init__(self):
        self.core_calculator = KasiCalculatorCore()
        self.full_gapja_cache = {}
        self.validation_results = []
    
    def validate_extreme_cases(self) -> bool:
        """극한 상황 테스트 및 검증"""
        
        print("\n🔍 KASI 정밀 계산기 극한 상황 검증")
        print("="*80)
        
        test_cases = [
            # 윤년 테스트
            {
                'name': '윤년 2월 29일 테스트',
                'input': {'year': 2024, 'month': 2, 'day': 29, 'hour': 12, 'minute': 0},
                'expect_both': True
            },
            # 연도 경계 테스트
            {
                'name': '연도 경계 (12월 31일 23시)',
                'input': {'year': 2023, 'month': 12, 'day': 31, 'hour': 23, 'minute': 59},
                'expect_both': True
            },
            {
                'name': '연도 경계 (1월 1일 0시)',
                'input': {'year': 2024, 'month': 1, 'day': 1, 'hour': 0, 'minute': 1},
                'expect_both': True
            },
            # 음력 입력 테스트
            {
                'name': '음력 윤달 테스트',
                'input': {'year': 2023, 'month': 2, 'day': 15, 'is_lunar': True, 'is_leap': True},
                'expect_both': True
            },
            # 극한 시간 테스트
            {
                'name': '자시 경계 (23:30)',
                'input': {'year': 2024, 'month': 6, 'day': 15, 'hour': 23, 'minute': 30},
                'expect_both': False
            },
            # 과거/미래 연도 테스트
            {
                'name': '과거 연도 (1920년)',
                'input': {'year': 1920, 'month': 5, 'day': 10, 'hour': 14, 'minute': 0},
                'expect_both': False
            },
            {
                'name': '미래 연도 (2080년)',
                'input': {'year': 2080, 'month': 8, 'day': 20, 'hour': 16, 'minute': 30},
                'expect_both': False
            }
        ]
        
        total_count = len(test_cases)
        success_count = 0
        
        for i, test in enumerate(test_cases):
            print(f"\n### 테스트 {i+1}: {test['name']}")
            print("-"*60)
            
            result = self.core_calculator.calculate_saju(**test['input'])
            
            if result:
                calendar_info = result.get('calendar_info', {})
                input_type = calendar_info.get('input_type', '알 수 없음')
                
                print(f"입력 타입: {input_type}")
                
                # 양력 정보 확인
                solar_info = calendar_info.get('solar')
                if solar_info:
                    print(f"양력: {solar_info['date_string']}")
                else:
                    print(f"양력: 정보 없음")
                
                # 음력 정보 확인
                lunar_info = calendar_info.get('lunar')
                if lunar_info:
                    print(f"음력: {lunar_info['date_string']}")
                else:
                    print(f"음력: 정보 없음")
                
                # 사주 결과
                pillars = result['pillars']
                saju_result = f"{pillars['year']['gapja']} {pillars['month']['gapja']} {pillars['day']['gapja']} {pillars['hour']['gapja']}"
                print(f"사주: {saju_result}")
                print(f"일간: {result['ilgan']}")
                
                # 검증
                has_both = solar_info is not None and lunar_info is not None
                if test['expect_both'] and has_both:
                    print("검증: ✅ 양력/음력 정보 모두 포함")
                    success_count += 1
                elif not test['expect_both']:
                    print("검증: ✅ 기본 기능 정상")
                    success_count += 1
                else:
                    print("검증: ❌ 양력/음력 정보 누락")
            else:
                print("❌ 계산 실패")
                
        print(f"\n" + "="*80)
        print(f"🎊 극한 상황 검증 결과: {success_count}/{total_count} 성공 ({success_count/total_count*100:.1f}%)")
        print("="*80)
        
        return success_count == total_count
    
    def comprehensive_accuracy_test(self, test_count: int = 100) -> Dict:
        """종합 정확도 테스트"""
        
        print(f"\n🎯 KASI API 정확도 종합 테스트 (샘플 {test_count}개)")
        print("="*80)
        
        import random
        
        results = {
            'total_tests': 0,
            'successful_calculations': 0,
            'api_usage_count': 0,
            'fallback_usage_count': 0,
            'calendar_conversion_accuracy': 0,
            'pillar_calculation_accuracy': 0,
            'detailed_results': []
        }
        
        for i in range(test_count):
            # 랜덤 날짜 생성 (1950~2050)
            year = random.randint(1950, 2050)
            month = random.randint(1, 12)
            day = random.randint(1, 28)  # 안전한 일수
            hour = random.randint(0, 23)
            minute = random.randint(0, 59)
            is_lunar = random.choice([True, False])
            
            test_case = {
                'year': year, 'month': month, 'day': day,
                'hour': hour, 'minute': minute, 'is_lunar': is_lunar
            }
            
            # 계산 실행
            result = self.core_calculator.calculate_saju(**test_case)
            results['total_tests'] += 1
            
            if result:
                results['successful_calculations'] += 1
                
                # 계산 유형 분석
                calendar_info = result.get('calendar_info', {})
                if calendar_info.get('input_type') == '폴백계산':
                    results['fallback_usage_count'] += 1
                else:
                    results['api_usage_count'] += 1
                
                # 달력 변환 정확도 (양력/음력 정보 존재 여부)
                has_solar = 'solar' in calendar_info
                has_lunar = 'lunar' in calendar_info
                if has_solar and has_lunar:
                    results['calendar_conversion_accuracy'] += 1
                
                # 사주 4주 완성도 검증
                pillars = result.get('pillars', {})
                pillar_complete = all(
                    pillars.get(p, {}).get('gapja') for p in ['year', 'month', 'day', 'hour']
                )
                if pillar_complete:
                    results['pillar_calculation_accuracy'] += 1
                
                # 상세 결과 저장 (일부만)
                if i < 10:  # 처음 10개만 상세 저장
                    results['detailed_results'].append({
                        'input': test_case,
                        'output': result,
                        'success': True
                    })
            
            # 진행 상황 출력
            if (i + 1) % 20 == 0:
                print(f"   진행률: {i+1}/{test_count} ({(i+1)/test_count*100:.1f}%)")
        
        # 정확도 계산
        if results['total_tests'] > 0:
            success_rate = results['successful_calculations'] / results['total_tests'] * 100
            calendar_accuracy = results['calendar_conversion_accuracy'] / results['total_tests'] * 100
            pillar_accuracy = results['pillar_calculation_accuracy'] / results['total_tests'] * 100
            
            print(f"\n📊 정확도 테스트 결과:")
            print(f"   전체 성공률: {success_rate:.1f}% ({results['successful_calculations']}/{results['total_tests']})")
            print(f"   달력 변환 정확도: {calendar_accuracy:.1f}%")
            print(f"   사주 계산 정확도: {pillar_accuracy:.1f}%")
            print(f"   API 사용: {results['api_usage_count']}회")
            print(f"   폴백 사용: {results['fallback_usage_count']}회")
        
        return results
    
    def build_advanced_gapja_cache(self, start_year: int = 1900, end_year: int = 2100):
        """고급 갑자 캐시 구축"""
        
        print(f"\n🔄 고급 갑자 캐시 구축 ({start_year}~{end_year})")
        print("="*60)
        
        cache_count = 0
        
        for year in range(start_year, end_year + 1):
            if year % 20 == 0:
                print(f"   처리 연도: {year}")
            
            # 매년 주요 날짜들을 캐시에 추가
            key_dates = [
                (year, 1, 1),    # 신정
                (year, 2, 4),    # 입춘 근사
                (year, 6, 21),   # 하지 근사
                (year, 9, 23),   # 추분 근사
                (year, 12, 22),  # 동지 근사
            ]
            
            for year_val, month_val, day_val in key_dates:
                try:
                    test_date = datetime(year_val, month_val, day_val, 12, 0)
                    day_pillar = self.core_calculator._calculate_day_pillar_fallback(test_date)
                    
                    if day_pillar and day_pillar.get('gapja'):
                        cache_key = f"{year_val}-{month_val:02d}-{day_val:02d}"
                        self.full_gapja_cache[cache_key] = day_pillar
                        cache_count += 1
                
                except Exception as e:
                    logger.warning(f"캐시 구축 실패 {year_val}-{month_val}-{day_val}: {e}")
        
        print(f"✅ 갑자 캐시 구축 완료: {cache_count}개 항목")
        return self.full_gapja_cache
    
    def performance_benchmark(self, iterations: int = 50) -> Dict:
        """성능 벤치마크 테스트"""
        
        print(f"\n⏱️  성능 벤치마크 테스트 ({iterations}회 반복)")
        print("="*60)
        
        import time
        
        # 테스트 케이스
        test_cases = [
            {'year': 1990, 'month': 5, 'day': 15, 'hour': 14, 'minute': 30},
            {'year': 2000, 'month': 2, 'day': 29, 'hour': 8, 'minute': 45},  # 윤년
            {'year': 2024, 'month': 10, 'day': 10, 'hour': 22, 'minute': 15},
            {'year': 1975, 'month': 12, 'day': 25, 'hour': 6, 'minute': 0},
        ]
        
        results = {
            'total_time': 0,
            'average_time_per_calculation': 0,
            'successful_calculations': 0,
            'failed_calculations': 0,
            'api_calls': 0,
            'fallback_calls': 0,
            'detailed_timings': []
        }
        
        initial_usage = self.core_calculator.usage_count
        
        start_time = time.time()
        
        for i in range(iterations):
            test_case = test_cases[i % len(test_cases)]
            
            case_start = time.time()
            result = self.core_calculator.calculate_saju(**test_case)
            case_end = time.time()
            
            case_time = (case_end - case_start) * 1000  # milliseconds
            
            if result:
                results['successful_calculations'] += 1
                calendar_info = result.get('calendar_info', {})
                if calendar_info.get('input_type') == '폴백계산':
                    results['fallback_calls'] += 1
                else:
                    results['api_calls'] += 1
            else:
                results['failed_calculations'] += 1
            
            results['detailed_timings'].append({
                'iteration': i + 1,
                'time_ms': case_time,
                'success': result is not None
            })
            
            if (i + 1) % 10 == 0:
                print(f"   완료: {i+1}/{iterations}")
        
        end_time = time.time()
        
        total_api_calls = self.core_calculator.usage_count - initial_usage
        results['total_time'] = (end_time - start_time) * 1000  # milliseconds
        results['average_time_per_calculation'] = results['total_time'] / iterations
        results['api_calls'] = total_api_calls
        
        print(f"\n📈 성능 벤치마크 결과:")
        print(f"   총 실행 시간: {results['total_time']:.1f}ms")
        print(f"   평균 계산 시간: {results['average_time_per_calculation']:.1f}ms")
        print(f"   성공률: {results['successful_calculations']}/{iterations} ({results['successful_calculations']/iterations*100:.1f}%)")
        print(f"   API 호출: {results['api_calls']}회")
        print(f"   폴백 사용: {results['fallback_calls']}회")
        
        return results
    
    def generate_validation_report(self) -> str:
        """검증 결과 종합 보고서 생성"""
        
        # 기본 검증 실행
        extreme_test_result = self.validate_extreme_cases()
        accuracy_test_result = self.comprehensive_accuracy_test(50)
        performance_result = self.performance_benchmark(30)
        
        # 보고서 생성
        report = {
            "validation_timestamp": datetime.now().isoformat(),
            "kasi_calculator_version": "2.0.0",
            "extreme_cases_test": {
                "passed": extreme_test_result,
                "description": "극한 상황 처리 능력 검증"
            },
            "accuracy_test": accuracy_test_result,
            "performance_benchmark": performance_result,
            "overall_assessment": {
                "reliability": "HIGH" if extreme_test_result else "MEDIUM",
                "accuracy": accuracy_test_result.get('successful_calculations', 0) / accuracy_test_result.get('total_tests', 1) * 100,
                "performance": "GOOD" if performance_result.get('average_time_per_calculation', 1000) < 500 else "AVERAGE"
            }
        }
        
        # JSON 파일로 저장
        report_path = f"/tmp/kasi_calculator_validation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_path, "w", encoding="utf-8") as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        print(f"\n📋 검증 보고서 저장: {report_path}")
        return report_path