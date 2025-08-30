"""
KASI API 통합 정밀 만세력 계산 시스템 v2.0 - 리팩터링된 버전
2025-08-27 리팩터링 완성 - 모듈화 및 성능 최적화

구조:
- Core: 핵심 사주 계산, 달력 변환 (일반 사용자용)
- Advanced: 검증, 벤치마크, 최적화 (전문가용)

리팩터링 효과:
- 기존: 850줄 단일 파일
- 개선: 기능별 분리 + 공통 모델 모듈화  
- 성능: 사용 빈도에 따른 로드 최적화

과학적 정확도 기준:
- 서머타임 제외 (순수 천문학적 시간)
- 경도차 보정만 적용 (-32분)
- KASI API 완전 통합
- 전통 명리학 원리 준수

@author HEAL7 Team
@version 2.0.0
"""

from typing import Dict, Optional
from datetime import datetime

from .kasi_calculator_core import KasiCalculatorCore
from .kasi_calculator_advanced import KasiCalculatorAdvanced
from .shared.kasi_calculator_models import SajuResult, KasiApiConfig, CalculationMode

class KasiPrecisionSajuCalculator:
    """KASI API 정밀 사주 계산기 - 메인 코디네이터 (레거시 호환)"""
    
    def __init__(self):
        self.core_calculator = KasiCalculatorCore()
        self.advanced_calculator = None  # 필요시에만 로드
        self._calculation_mode = CalculationMode.KASI_PRIMARY
    
    def calculate_saju(self, year: int, month: int, day: int, 
                      hour: int = 12, minute: int = 0, 
                      is_lunar: bool = False, is_leap: bool = False) -> Optional[Dict]:
        """
        메인 사주 계산 인터페이스 - 가장 자주 사용됨
        레거시 호환성을 위해 원래 인터페이스 유지
        """
        return self.core_calculator.calculate_saju(
            year, month, day, hour, minute, is_lunar, is_leap
        )
    
    def set_calculation_mode(self, mode: str):
        """계산 모드 설정"""
        if mode in [CalculationMode.KASI_PRIMARY, CalculationMode.FALLBACK_ONLY, CalculationMode.HYBRID]:
            self._calculation_mode = mode
    
    def get_usage_stats(self) -> Dict:
        """사용 통계 조회"""
        return {
            "api_usage_count": self.core_calculator.usage_count,
            "usage_limit": KasiApiConfig.USAGE_LIMIT,
            "remaining_calls": max(0, KasiApiConfig.USAGE_LIMIT - self.core_calculator.usage_count),
            "calculation_mode": self._calculation_mode
        }
    
    # 고급 기능들 (전문가용 - 필요시에만 로드)
    def validate_extreme_cases(self) -> bool:
        """극한 상황 검증 - 전문가용"""
        if self.advanced_calculator is None:
            self.advanced_calculator = KasiCalculatorAdvanced()
        return self.advanced_calculator.validate_extreme_cases()
    
    def run_accuracy_test(self, test_count: int = 100) -> Dict:
        """정확도 테스트 - 전문가용"""
        if self.advanced_calculator is None:
            self.advanced_calculator = KasiCalculatorAdvanced()
        return self.advanced_calculator.comprehensive_accuracy_test(test_count)
    
    def run_performance_benchmark(self, iterations: int = 50) -> Dict:
        """성능 벤치마크 - 전문가용"""
        if self.advanced_calculator is None:
            self.advanced_calculator = KasiCalculatorAdvanced()
        return self.advanced_calculator.performance_benchmark(iterations)
    
    def generate_validation_report(self) -> str:
        """종합 검증 보고서 생성 - 전문가용"""
        if self.advanced_calculator is None:
            self.advanced_calculator = KasiCalculatorAdvanced()
        return self.advanced_calculator.generate_validation_report()
    
    # 레거시 호환성을 위한 기존 메소드들 (단순화)
    def is_leap_year(self, year: int) -> bool:
        """윤년 판정 (레거시 호환)"""
        return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)
    
    def apply_true_solar_time_correction(self, birth_datetime: datetime, longitude: float = 126.9780) -> datetime:
        """진태양시 보정 (레거시 호환)"""
        return self.core_calculator._calculate_pure_solar_time(birth_datetime)
    
    def apply_dst_correction(self, corrected_time: datetime, latitude: float, longitude: float) -> datetime:
        """서머타임 보정 (레거시 호환) - 현재 미적용"""
        return corrected_time
    
    def get_sexagenary_cycle(self, target_date) -> Dict:
        """60갑자 순환 조회 (레거시 호환)"""
        if hasattr(target_date, 'year'):
            year, month, day = target_date.year, target_date.month, target_date.day
        else:
            year, month, day = target_date[:3]
        
        result = self.calculate_saju(year, month, day, 12, 0)
        if result and 'pillars' in result:
            day_pillar = result['pillars']['day']
            return {
                "day_cheongan_index": day_pillar.get('cheongan_index', 0),
                "day_jiji_index": day_pillar.get('jiji_index', 0),
                "day_gapja": day_pillar.get('gapja', '甲子')
            }
        
        return {"day_cheongan_index": 0, "day_jiji_index": 0, "day_gapja": "甲子"}
    
    def calculate_monthly_pillar(self, target_date) -> Dict:
        """월주 계산 (레거시 호환)"""
        if hasattr(target_date, 'year'):
            year, month, day = target_date.year, target_date.month, target_date.day
        else:
            year, month, day = target_date[:3]
        
        result = self.calculate_saju(year, month, day, 12, 0)
        if result and 'pillars' in result:
            month_pillar = result['pillars']['month']
            return {
                "month_index": month_pillar.get('jiji_index', 0) + 1,
                "month_gapja": month_pillar.get('gapja', '甲寅')
            }
        
        return {"month_index": 1, "month_gapja": "甲寅"}


# CLI 실행용 및 테스트
if __name__ == "__main__":
    import sys
    
    calculator = KasiPrecisionSajuCalculator()
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "--test":
            # 기본 테스트 실행
            test_result = calculator.calculate_saju(1990, 5, 15, 14, 30)
            print(f"테스트 결과: {test_result}")
            
        elif sys.argv[1] == "--validate":
            # 검증 실행
            validation_result = calculator.validate_extreme_cases()
            print(f"검증 결과: {'통과' if validation_result else '실패'}")
            
        elif sys.argv[1] == "--benchmark":
            # 성능 벤치마크
            benchmark_result = calculator.run_performance_benchmark(20)
            print(f"평균 계산 시간: {benchmark_result.get('average_time_per_calculation', 0):.1f}ms")
            
        elif sys.argv[1] == "--report":
            # 종합 보고서 생성
            report_path = calculator.generate_validation_report()
            print(f"보고서 생성: {report_path}")
            
    else:
        # 기본 사용 예시
        result = calculator.calculate_saju(2024, 8, 27, 15, 30)
        if result:
            pillars = result['pillars']
            saju = f"{pillars['year']['gapja']} {pillars['month']['gapja']} {pillars['day']['gapja']} {pillars['hour']['gapja']}"
            print(f"사주: {saju}")
            print(f"일간: {result['ilgan']}")
            
            # 사용 통계
            stats = calculator.get_usage_stats()
            print(f"API 사용량: {stats['api_usage_count']}/{stats['usage_limit']}")
        else:
            print("사주 계산 실패")