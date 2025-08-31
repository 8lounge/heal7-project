"""
실패 원리 분석기 공통 모델 및 데이터 클래스
"""

from dataclasses import dataclass
from typing import Dict, List, Any
from datetime import datetime

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

@dataclass
class QuickDiagnosticResult:
    """빠른 진단 결과"""
    principle_name: str
    status: str  # "PASS", "WARNING", "FAIL"
    error_count: int
    accuracy_rate: float
    critical_issues: List[str]

class PrincipleConstants:
    """원리 분석 상수"""
    
    # 분석 대상 원리들
    FAILED_PRINCIPLES = [
        "년주_60갑자_순환",
        "월주_24절기_기준", 
        "월주_년간_월간_관계",
        "시주_시두법",
        "월두법"
    ]
    
    # 검증 기준값
    MIN_ACCURACY_THRESHOLD = 0.85  # 85% 정확도 기준
    CRITICAL_ERROR_THRESHOLD = 5   # 5개 이상 오류시 FAIL
    
    # 시두법 검증을 위한 시간 매핑
    HOUR_JIJI_MAPPING = {
        0: '子', 1: '子', 2: '丑', 3: '丑', 4: '寅', 5: '寅',
        6: '卯', 7: '卯', 8: '辰', 9: '辰', 10: '巳', 11: '巳',
        12: '午', 13: '午', 14: '未', 15: '未', 16: '申', 17: '申',
        18: '酉', 19: '酉', 20: '戌', 21: '戌', 22: '亥', 23: '亥'
    }
    
    # 월두법 검증을 위한 연간별 월간 매핑
    MONTH_CHEONGAN_MAPPING = {
        '甲': ['丙', '丁', '戊', '己', '庚', '辛', '壬', '癸', '甲', '乙', '丙', '丁'],
        '己': ['丙', '丁', '戊', '己', '庚', '辛', '壬', '癸', '甲', '乙', '丙', '丁'],
        '乙': ['戊', '己', '庚', '辛', '壬', '癸', '甲', '乙', '丙', '丁', '戊', '己'],
        '庚': ['戊', '己', '庚', '辛', '壬', '癸', '甲', '乙', '丙', '丁', '戊', '己'],
        '丙': ['庚', '辛', '壬', '癸', '甲', '乙', '丙', '丁', '戊', '己', '庚', '辛'],
        '辛': ['庚', '辛', '壬', '癸', '甲', '乙', '丙', '丁', '戊', '己', '庚', '辛'],
        '丁': ['壬', '癸', '甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸'],
        '壬': ['壬', '癸', '甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸'],
        '戊': ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸', '甲', '乙'],
        '癸': ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸', '甲', '乙']
    }

class AnalysisStatus:
    """분석 상태 상수"""
    PASS = "PASS"
    WARNING = "WARNING" 
    FAIL = "FAIL"
    UNKNOWN = "UNKNOWN"