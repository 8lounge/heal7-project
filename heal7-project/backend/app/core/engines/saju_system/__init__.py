"""
HEAL7 사주 시스템 v5.0 - 완전한 명리학 분석 엔진

구성 요소:
- myeongrihak_constants.py: 명리학 기초 상수
- kasi_precision_saju_calculator.py: KASI API 기반 정밀 사주 계산
- wuxing_analyzer.py: 오행 균형 분석
- sipsin_analyzer.py: 십신 패턴 분석  
- gyeokguk_analyzer.py: 격국 분석
- comprehensive_myeongrihak_analyzer.py: 통합 명리학 엔진
"""

from .comprehensive_myeongrihak_analyzer import (
    ComprehensiveMyeongRiHakAnalyzer,
    analyze_complete_saju,
    quick_saju_analysis,
    validate_v5_system
)

from .kasi_precision_saju_calculator import KasiPrecisionSajuCalculator
from .wuxing_analyzer import analyze_saju_wuxing
from .sipsin_analyzer import analyze_saju_sipsin
from .gyeokguk_analyzer import analyze_saju_gyeokguk

__version__ = "5.0.0"
__author__ = "HEAL7 Team"
__description__ = "완전한 명리학 분석 시스템 - KASI API 기반"

# 주요 기능들
__all__ = [
    "ComprehensiveMyeongRiHakAnalyzer",
    "analyze_complete_saju",
    "quick_saju_analysis", 
    "validate_v5_system",
    "KasiPrecisionSajuCalculator",
    "analyze_saju_wuxing",
    "analyze_saju_sipsin", 
    "analyze_saju_gyeokguk",
]