#!/usr/bin/env python3
"""
실패 원리 심층 분석기 v2.0 - 리팩터링된 버전

구조:
- Core: 기본 원리 검증, 빠른 진단 (일반 사용자용)
- Advanced: 상세 분석, 종합 보고서 (전문가용)

리팩터링 효과:
- 기존: 816줄 단일 파일
- 개선: 기능별 분리 + 공통 모델 모듈화
- 성능: 사용 빈도에 따른 로드 최적화

실패 원리들:
1. 년주_60갑자_순환: 60년 주기 순환 검증
2. 월주_24절기_기준: 절기 경계 월주 변경 검증
3. 월주_년간_월간_관계: 년간별 월간 배치 규칙
4. 시주_시두법: 시두법 규칙 적용
5. 월두법: 월주 천간 결정 핵심 법칙

@author HEAL7 Team
@version 2.0.0
"""

import asyncio
from typing import Dict, List, Any, Optional

from .principles_analyzer_core import PrinciplesAnalyzerCore
from .principles_analyzer_advanced import PrinciplesAnalyzerAdvanced
from .shared.principles_analyzer_models import (
    DeepAnalysisResult, QuickDiagnosticResult, PrincipleConstants
)

class FailedPrinciplesDeepAnalyzer:
    """실패 원리 심층 분석기 - 메인 코디네이터"""
    
    def __init__(self):
        self.core_analyzer = PrinciplesAnalyzerCore()
        self.advanced_analyzer = None  # 필요시에만 로드
    
    async def quick_diagnostic(self, target_principle: str = None) -> List[QuickDiagnosticResult]:
        """빠른 원리 진단 - 가장 자주 사용됨"""
        return await self.core_analyzer.quick_diagnostic(target_principle)
    
    async def run_deep_analysis(self) -> List[DeepAnalysisResult]:
        """종합 심층 분석 - 전문가용 상세 분석"""
        if self.advanced_analyzer is None:
            self.advanced_analyzer = PrinciplesAnalyzerAdvanced()
        
        return await self.advanced_analyzer.run_comprehensive_deep_analysis()
    
    async def get_system_health_summary(self) -> Dict[str, Any]:
        """시스템 건강도 요약"""
        return await self.core_analyzer.get_diagnostic_summary()
    
    async def analyze_specific_principle(self, principle_name: str) -> Dict[str, Any]:
        """특정 원리 집중 분석"""
        
        # 빠른 진단
        quick_results = await self.quick_diagnostic(principle_name)
        quick_result = quick_results[0] if quick_results else None
        
        # 상세 분석 (필요시)
        detailed_result = None
        if quick_result and quick_result.status != "PASS":
            if self.advanced_analyzer is None:
                self.advanced_analyzer = PrinciplesAnalyzerAdvanced()
            
            # 개별 원리 상세 분석 (간소화)
            detailed_result = {
                "principle": principle_name,
                "requires_detailed_analysis": True,
                "recommendation": "종합 심층 분석 실행 권장"
            }
        
        return {
            "principle_name": principle_name,
            "quick_diagnostic": quick_result.__dict__ if quick_result else None,
            "detailed_analysis": detailed_result,
            "analysis_timestamp": asyncio.get_event_loop().time()
        }


# 레거시 호환성을 위한 함수들
async def run_failed_principles_analysis() -> List[DeepAnalysisResult]:
    """실패 원리 분석 실행 (레거시 호환)"""
    analyzer = FailedPrinciplesDeepAnalyzer()
    return await analyzer.run_deep_analysis()

async def quick_principles_check() -> List[QuickDiagnosticResult]:
    """빠른 원리 체크"""
    analyzer = FailedPrinciplesDeepAnalyzer()
    return await analyzer.quick_diagnostic()

# CLI 실행용
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--quick":
        # 빠른 진단
        results = asyncio.run(quick_principles_check())
        for result in results:
            status_emoji = "✅" if result.status == "PASS" else "⚠️" if result.status == "WARNING" else "❌"
            print(f"{status_emoji} {result.principle_name}: {result.status} (정확도: {result.accuracy_rate:.1%})")
            
            if result.critical_issues:
                for issue in result.critical_issues[:2]:  # 상위 2개만
                    print(f"   - {issue}")
    
    elif len(sys.argv) > 1 and sys.argv[1].startswith("--principle="):
        # 특정 원리 분석
        principle = sys.argv[1].split("=")[1]
        analyzer = FailedPrinciplesDeepAnalyzer()
        result = asyncio.run(analyzer.analyze_specific_principle(principle))
        print(f"원리: {result['principle_name']}")
        
        if result['quick_diagnostic']:
            diag = result['quick_diagnostic']
            print(f"상태: {diag['status']}")
            print(f"정확도: {diag['accuracy_rate']:.1%}")
    
    else:
        # 종합 분석
        results = asyncio.run(run_failed_principles_analysis())
        print(f"실패 원리 종합 분석 완료: {len(results)}개 원리 분석")
        
        for result in results:
            print(f"- {result.principle_name}: 개선 점수 {result.improvement_score:.2f}")