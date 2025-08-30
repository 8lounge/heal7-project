#!/usr/bin/env python3
"""
폴백시스템 종합 검증 도구 v2.0 - 리팩터링된 버전

구조:
- Core: 기본 검증, 빠른 체크 (일반 사용자용)
- Advanced: 상세 분석, 종합 보고서 (전문가용)

리팩터링 효과:
- 기존: 965줄 단일 파일
- 개선: 기능별 분리 + 공통 모델 모듈화
- 성능: 사용 빈도에 따른 로드 최적화

@author HEAL7 Team
@version 2.0.0
"""

import asyncio
from typing import Dict, List, Any, Optional

from .fallback_validator_core import FallbackValidatorCore
from .fallback_validator_advanced import FallbackValidatorAdvanced
from .shared.fallback_validator_models import (
    ValidationResult, QuickValidationSummary, ValidationConstants
)

class FallbackSystemValidator:
    """폴백시스템 종합 검증 도구 - 메인 코디네이터"""
    
    def __init__(self):
        self.core_validator = FallbackValidatorCore()
        self.advanced_validator = None  # 필요시에만 로드
    
    async def quick_check(self, target_year: int = None) -> QuickValidationSummary:
        """빠른 기본 검증 - 가장 자주 사용됨"""
        return await self.core_validator.quick_validation(target_year)
    
    async def comprehensive_check(self, start_year: int = 1950, end_year: int = 2025) -> List[ValidationResult]:
        """종합 검증 - 전문가용 상세 분석"""
        if self.advanced_validator is None:
            self.advanced_validator = FallbackValidatorAdvanced()
        
        await self.advanced_validator.run_comprehensive_validation(start_year, end_year)
        return self.advanced_validator.validation_results
    
    async def get_validation_summary(self) -> Dict[str, Any]:
        """검증 결과 요약 정보"""
        quick_result = await self.quick_check()
        
        return {
            "quick_validation": {
                "status": quick_result.status,
                "accuracy_rate": quick_result.accuracy_rate,
                "total_tests": quick_result.total_tests,
                "success_count": quick_result.success_count,
                "critical_errors": quick_result.critical_errors
            },
            "system_info": {
                "validator_version": "2.0.0",
                "test_categories": ValidationConstants.TEST_CATEGORIES,
                "min_accuracy_threshold": ValidationConstants.MIN_ACCURACY_THRESHOLD,
                "critical_accuracy_threshold": ValidationConstants.CRITICAL_ACCURACY_THRESHOLD
            }
        }


# 레거시 호환성을 위한 메인 실행 함수들
async def run_fallback_validation(start_year: int = 1950, end_year: int = 2025) -> List[ValidationResult]:
    """폴백시스템 종합 검증 실행 (레거시 호환)"""
    validator = FallbackSystemValidator()
    return await validator.comprehensive_check(start_year, end_year)

async def run_quick_validation(target_year: int = None) -> QuickValidationSummary:
    """빠른 검증 실행"""
    validator = FallbackSystemValidator()
    return await validator.quick_check(target_year)

# CLI 실행용
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--quick":
        # 빠른 검증
        result = asyncio.run(run_quick_validation())
        print(f"검증 상태: {result.status}")
        print(f"정확도: {result.accuracy_rate:.1%}")
        print(f"테스트: {result.success_count}/{result.total_tests}")
        
        if result.critical_errors:
            print("치명적 오류:")
            for error in result.critical_errors:
                print(f"  - {error}")
    else:
        # 종합 검증
        start = int(sys.argv[1]) if len(sys.argv) > 1 else 1950
        end = int(sys.argv[2]) if len(sys.argv) > 2 else 2025
        
        results = asyncio.run(run_fallback_validation(start, end))
        print(f"종합 검증 완료: {len(results)}개 테스트 실행")