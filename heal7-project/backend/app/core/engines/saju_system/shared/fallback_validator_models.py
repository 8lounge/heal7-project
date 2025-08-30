#!/usr/bin/env python3
"""
폴백시스템 검증 공통 모델 및 데이터 클래스
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List, Any, Optional

@dataclass
class SolarTermData:
    """24절기 데이터 클래스"""
    year: int
    term_name: str
    term_index: int  # 0-23 (입춘=0, 우수=1, ...)
    solar_date: datetime
    korean_name: str
    source: str  # "KASI" or "MANSERYEOK" or "CALCULATED"
    verified: bool = False

@dataclass
class ValidationResult:
    """검증 결과 데이터 클래스"""
    test_category: str
    test_name: str
    success: bool
    accuracy_score: float
    reference_value: Any
    calculated_value: Any
    error_message: Optional[str] = None
    execution_time_ms: float = 0.0

@dataclass
class QuickValidationSummary:
    """빠른 검증 요약 클래스"""
    total_tests: int
    success_count: int
    accuracy_rate: float
    critical_errors: List[str]
    status: str  # "PASS", "WARNING", "FAIL"

class ValidationConstants:
    """검증 상수 정의"""
    
    # 24절기 명칭 매핑
    SOLAR_TERMS = {
        0: "입춘", 1: "우수", 2: "경칩", 3: "춘분", 4: "청명", 5: "곡우",
        6: "입하", 7: "소만", 8: "망종", 9: "하지", 10: "소서", 11: "대서",
        12: "입추", 13: "처서", 14: "백로", 15: "추분", 16: "한로", 17: "상강",
        18: "입동", 19: "소설", 20: "대설", 21: "동지", 22: "소한", 23: "대한"
    }
    
    # 검증 기준값
    MIN_ACCURACY_THRESHOLD = 0.85  # 85% 정확도 기준
    CRITICAL_ACCURACY_THRESHOLD = 0.95  # 95% 임계 정확도
    
    # 테스트 카테고리
    TEST_CATEGORIES = [
        "solar_terms",
        "true_solar_time", 
        "leap_year_calculation",
        "sexagenary_cycle",
        "monthly_pillar",
        "great_fortune"
    ]