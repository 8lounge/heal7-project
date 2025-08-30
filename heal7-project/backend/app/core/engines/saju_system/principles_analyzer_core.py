"""
실패 원리 분석기 - 핵심 진단 모듈
기본 원리 검증과 빠른 진단 기능
"""

import logging
from datetime import datetime, date, timedelta
from typing import Dict, List, Any, Optional

from .shared.principles_analyzer_models import (
    DeepAnalysisResult, QuickDiagnosticResult, PrincipleConstants, AnalysisStatus
)
from .kasi_precision_saju_calculator import KasiPrecisionSajuCalculator
from .myeongrihak_constants import CHEONGAN, JIJI

logger = logging.getLogger(__name__)

class PrinciplesAnalyzerCore:
    """실패 원리 분석기 - 핵심 진단 기능 (자주 사용되는 기본 검증)"""
    
    def __init__(self):
        self.kasi_calculator = KasiPrecisionSajuCalculator()
    
    async def quick_diagnostic(self, target_principle: str = None) -> List[QuickDiagnosticResult]:
        """빠른 원리 진단 - 가장 자주 사용됨"""
        
        results = []
        
        principles_to_check = [target_principle] if target_principle else PrincipleConstants.FAILED_PRINCIPLES
        
        for principle in principles_to_check:
            if principle == "년주_60갑자_순환":
                result = await self._quick_check_year_gapja_cycle()
            elif principle == "월주_24절기_기준":
                result = await self._quick_check_month_solar_terms()
            elif principle == "시주_시두법":
                result = await self._quick_check_sidubeop()
            elif principle == "월두법":
                result = await self._quick_check_woldoobeop()
            else:
                result = QuickDiagnosticResult(
                    principle_name=principle,
                    status=AnalysisStatus.UNKNOWN,
                    error_count=0,
                    accuracy_rate=0.0,
                    critical_issues=[f"알 수 없는 원리: {principle}"]
                )
            
            results.append(result)
        
        return results
    
    async def _quick_check_year_gapja_cycle(self) -> QuickDiagnosticResult:
        """연주 60갑자 순환 빠른 검증"""
        
        errors = []
        test_count = 0
        success_count = 0
        
        # 10개 연도 간단 테스트 (과거, 현재, 미래)
        test_years = [1924, 1950, 1984, 2000, 2020, 2024, 2044, 2060, 2084, 2100]
        
        for year in test_years:
            try:
                test_count += 1
                
                # 갑자 계산
                base_year = 1924  # 갑자년
                cycle_position = (year - base_year) % 60
                expected_cheongan_index = cycle_position % 10
                expected_jiji_index = cycle_position % 12
                
                # KASI 계산기로 검증
                result = self.kasi_calculator.calculate_saju(year, 6, 15, 12, 0)  # 여름 중간
                if result:
                    actual_year_pillar = result['pillars']['year']
                    actual_cheongan_index = actual_year_pillar['cheongan_index']
                    actual_jiji_index = actual_year_pillar['jiji_index']
                    
                    # 정확도 검증
                    if (expected_cheongan_index == actual_cheongan_index and 
                        expected_jiji_index == actual_jiji_index):
                        success_count += 1
                    else:
                        errors.append(f"{year}년: 예상 {expected_cheongan_index},{expected_jiji_index} vs 실제 {actual_cheongan_index},{actual_jiji_index}")
                else:
                    errors.append(f"{year}년: 계산 실패")
            
            except Exception as e:
                errors.append(f"{year}년: 오류 {str(e)}")
        
        accuracy_rate = success_count / test_count if test_count > 0 else 0.0
        
        # 상태 결정
        if accuracy_rate >= PrincipleConstants.MIN_ACCURACY_THRESHOLD:
            status = AnalysisStatus.PASS
        elif accuracy_rate >= 0.7:
            status = AnalysisStatus.WARNING
        else:
            status = AnalysisStatus.FAIL
        
        return QuickDiagnosticResult(
            principle_name="년주_60갑자_순환",
            status=status,
            error_count=len(errors),
            accuracy_rate=accuracy_rate,
            critical_issues=errors[:3]  # 상위 3개 오류만
        )
    
    async def _quick_check_month_solar_terms(self) -> QuickDiagnosticResult:
        """월주 절기 기준 빠른 검증"""
        
        errors = []
        test_count = 0
        success_count = 0
        
        # 절기 경계 근처 날짜들 테스트
        test_cases = [
            (2024, 2, 3),   # 입춘 전날
            (2024, 2, 4),   # 입춘 당일
            (2024, 2, 5),   # 입춘 다음날
            (2024, 3, 5),   # 경칩 근처
            (2024, 5, 5),   # 입하 근처
        ]
        
        for year, month, day in test_cases:
            try:
                test_count += 1
                
                # 월주 계산
                result = self.kasi_calculator.calculate_saju(year, month, day, 12, 0)
                if result:
                    month_pillar = result['pillars']['month']
                    month_jiji = month_pillar['jiji']
                    
                    # 기본 절기 기준 검증 (간단한 매핑)
                    expected_month_jiji_map = {
                        1: '丑', 2: '寅', 3: '卯', 4: '辰', 5: '巳', 6: '午',
                        7: '未', 8: '申', 9: '酉', 10: '戌', 11: '亥', 12: '子'
                    }
                    
                    # 절기 보정 적용 (입춘 이전은 전년도 12월로)
                    if month <= 2 and day < 4:  # 대략적 입춘 기준
                        expected_jiji = expected_month_jiji_map[12]
                    else:
                        expected_jiji = expected_month_jiji_map.get(month, '寅')
                    
                    if month_jiji == expected_jiji:
                        success_count += 1
                    else:
                        errors.append(f"{year}-{month:02d}-{day:02d}: 예상 {expected_jiji} vs 실제 {month_jiji}")
                else:
                    errors.append(f"{year}-{month:02d}-{day:02d}: 계산 실패")
            
            except Exception as e:
                errors.append(f"{year}-{month:02d}-{day:02d}: 오류 {str(e)}")
        
        accuracy_rate = success_count / test_count if test_count > 0 else 0.0
        
        # 상태 결정
        if accuracy_rate >= PrincipleConstants.MIN_ACCURACY_THRESHOLD:
            status = AnalysisStatus.PASS
        elif accuracy_rate >= 0.7:
            status = AnalysisStatus.WARNING
        else:
            status = AnalysisStatus.FAIL
        
        return QuickDiagnosticResult(
            principle_name="월주_24절기_기준",
            status=status,
            error_count=len(errors),
            accuracy_rate=accuracy_rate,
            critical_issues=errors[:3]
        )
    
    async def _quick_check_sidubeop(self) -> QuickDiagnosticResult:
        """시두법 빠른 검증"""
        
        errors = []
        test_count = 0
        success_count = 0
        
        # 다양한 시간대 테스트
        test_cases = [
            (2024, 6, 15, 0, 0),    # 자시 (23-01시)
            (2024, 6, 15, 6, 30),   # 묘시 (05-07시)
            (2024, 6, 15, 12, 0),   # 오시 (11-13시)
            (2024, 6, 15, 18, 45),  # 유시 (17-19시)
            (2024, 6, 15, 23, 30),  # 해시 (21-23시)
        ]
        
        for year, month, day, hour, minute in test_cases:
            try:
                test_count += 1
                
                result = self.kasi_calculator.calculate_saju(year, month, day, hour, minute)
                if result:
                    day_cheongan = result['pillars']['day']['cheongan']
                    hour_pillar = result['pillars']['hour']
                    hour_cheongan = hour_pillar['cheongan']
                    hour_jiji = hour_pillar['jiji']
                    
                    # 시지지 검증
                    expected_jiji = PrincipleConstants.HOUR_JIJI_MAPPING.get(hour)
                    if expected_jiji and hour_jiji == expected_jiji:
                        success_count += 1
                    else:
                        errors.append(f"{hour:02d}:{minute:02d} - 시지지 불일치: 예상 {expected_jiji} vs 실제 {hour_jiji}")
                else:
                    errors.append(f"{hour:02d}:{minute:02d}: 계산 실패")
            
            except Exception as e:
                errors.append(f"{hour:02d}:{minute:02d}: 오류 {str(e)}")
        
        accuracy_rate = success_count / test_count if test_count > 0 else 0.0
        
        # 상태 결정
        if accuracy_rate >= PrincipleConstants.MIN_ACCURACY_THRESHOLD:
            status = AnalysisStatus.PASS
        elif accuracy_rate >= 0.7:
            status = AnalysisStatus.WARNING
        else:
            status = AnalysisStatus.FAIL
        
        return QuickDiagnosticResult(
            principle_name="시주_시두법",
            status=status,
            error_count=len(errors),
            accuracy_rate=accuracy_rate,
            critical_issues=errors[:3]
        )
    
    async def _quick_check_woldoobeop(self) -> QuickDiagnosticResult:
        """월두법 빠른 검증"""
        
        errors = []
        test_count = 0
        success_count = 0
        
        # 다양한 연간별 월천간 테스트
        test_cases = [
            ('甲', 1), ('甲', 6), ('甲', 12),  # 갑년 테스트
            ('乙', 3), ('乙', 8),             # 을년 테스트
            ('丙', 2), ('丙', 7),             # 병년 테스트
        ]
        
        for year_cheongan, month in test_cases:
            try:
                test_count += 1
                
                # 갑년을 기준으로 연도 계산 (임시)
                base_year = 2024 if year_cheongan == '甲' else 2025  # 임시 매핑
                
                result = self.kasi_calculator.calculate_saju(base_year, month, 15, 12, 0)
                if result:
                    actual_year_cheongan = result['pillars']['year']['cheongan']
                    actual_month_cheongan = result['pillars']['month']['cheongan']
                    
                    # 월두법 검증
                    expected_month_cheongan_list = PrincipleConstants.MONTH_CHEONGAN_MAPPING.get(actual_year_cheongan)
                    if expected_month_cheongan_list:
                        expected_month_cheongan = expected_month_cheongan_list[month - 1]
                        
                        if actual_month_cheongan == expected_month_cheongan:
                            success_count += 1
                        else:
                            errors.append(f"{actual_year_cheongan}년 {month}월: 예상 {expected_month_cheongan} vs 실제 {actual_month_cheongan}")
                    else:
                        errors.append(f"{actual_year_cheongan}년: 월두법 매핑 없음")
                else:
                    errors.append(f"{year_cheongan}년 {month}월: 계산 실패")
            
            except Exception as e:
                errors.append(f"{year_cheongan}년 {month}월: 오류 {str(e)}")
        
        accuracy_rate = success_count / test_count if test_count > 0 else 0.0
        
        # 상태 결정
        if accuracy_rate >= PrincipleConstants.MIN_ACCURACY_THRESHOLD:
            status = AnalysisStatus.PASS
        elif accuracy_rate >= 0.7:
            status = AnalysisStatus.WARNING
        else:
            status = AnalysisStatus.FAIL
        
        return QuickDiagnosticResult(
            principle_name="월두법",
            status=status,
            error_count=len(errors),
            accuracy_rate=accuracy_rate,
            critical_issues=errors[:3]
        )
    
    async def get_diagnostic_summary(self) -> Dict[str, Any]:
        """진단 결과 요약"""
        
        all_results = await self.quick_diagnostic()
        
        total_principles = len(all_results)
        passed_count = sum(1 for r in all_results if r.status == AnalysisStatus.PASS)
        warning_count = sum(1 for r in all_results if r.status == AnalysisStatus.WARNING)
        failed_count = sum(1 for r in all_results if r.status == AnalysisStatus.FAIL)
        
        overall_health = "HEALTHY" if failed_count == 0 else "ISSUES_DETECTED"
        
        return {
            "diagnostic_timestamp": datetime.now().isoformat(),
            "overall_health": overall_health,
            "total_principles": total_principles,
            "passed": passed_count,
            "warnings": warning_count,  
            "failed": failed_count,
            "critical_issues": [
                issue for result in all_results 
                for issue in result.critical_issues
            ],
            "principle_details": [
                {
                    "name": result.principle_name,
                    "status": result.status,
                    "accuracy_rate": result.accuracy_rate,
                    "error_count": result.error_count
                }
                for result in all_results
            ]
        }