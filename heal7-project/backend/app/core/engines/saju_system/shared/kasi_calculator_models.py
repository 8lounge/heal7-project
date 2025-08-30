"""
KASI 정밀 사주 계산기 공통 모델 및 상수
"""

from typing import Dict, List, Optional
from datetime import datetime

# KASI API 응답 파싱을 위한 한글-한자 매핑
KOREAN_TO_CHINESE_GANJEE = {
    # 천간
    '갑': '甲', '을': '乙', '병': '丙', '정': '丁', '무': '戊',
    '기': '己', '경': '庚', '신': '辛', '임': '壬', '계': '癸',
    # 지지
    '자': '子', '축': '丑', '인': '寅', '묘': '卯', '진': '辰', '사': '巳',
    '오': '午', '미': '未', '신': '申', '유': '酉', '술': '戌', '해': '亥'
}

# 천간/지지 상수
CHEONGAN = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸']
JIJI = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥']

# 시두법 - 일간에 따른 시천간 계산 (KASI 기준)
SIDUBEOP = {
    '甲': ['乙', '丁', '己', '辛', '癸', '乙', '丁', '己', '辛', '癸', '乙', '丁'],
    '己': ['乙', '丁', '己', '辛', '癸', '乙', '丁', '己', '辛', '癸', '乙', '丁'],
    '乙': ['丁', '己', '辛', '癸', '乙', '丁', '己', '辛', '癸', '乙', '丁', '己'],
    '庚': ['丁', '己', '辛', '癸', '乙', '丁', '己', '辛', '癸', '乙', '丁', '己'],
    '丙': ['己', '辛', '癸', '乙', '丁', '己', '辛', '癸', '乙', '丁', '己', '辛'],
    '辛': ['己', '辛', '癸', '乙', '丁', '己', '辛', '癸', '乙', '丁', '己', '辛'],
    '丁': ['辛', '癸', '乙', '丁', '己', '辛', '癸', '乙', '丁', '己', '辛', '癸'],
    '壬': ['辛', '癸', '乙', '丁', '己', '辛', '癸', '乙', '丁', '己', '辛', '癸'],
    '戊': ['癸', '乙', '丁', '己', '辛', '癸', '乙', '丁', '己', '辛', '癸', '乙'],
    '癸': ['癸', '乙', '丁', '己', '辛', '癸', '乙', '丁', '己', '辛', '癸', '乙']
}

# 갑자일수 기준 테이블 (고정값)
GAPJA_REFERENCE_TABLE = {
    (1900, 1, 31): 0,
    (1901, 1, 19): 0,
    (1950, 1, 1): 0,
    (2000, 1, 1): 34,
    (2025, 1, 1): 40
}

class SajuResult:
    """사주 계산 결과 표준 모델"""
    
    def __init__(self, pillars: Dict, ilgan: str, calendar_info: Dict = None):
        self.pillars = pillars
        self.ilgan = ilgan
        self.calendar_info = calendar_info or {}
    
    def to_dict(self) -> Dict:
        return {
            'pillars': self.pillars,
            'ilgan': self.ilgan,
            'calendar_info': self.calendar_info
        }
    
    @property
    def formatted_saju(self) -> str:
        """사주 4주 포맷 문자열"""
        return f"{self.pillars['year']['gapja']} {self.pillars['month']['gapja']} {self.pillars['day']['gapja']} {self.pillars['hour']['gapja']}"

class KasiApiConfig:
    """KASI API 설정 상수"""
    
    BASE_URL = "http://apis.data.go.kr/B090041/openapi/service/LrsrCldInfoService"
    USAGE_LIMIT = 900  # 하루 사용량 제한
    TIMEOUT_SECONDS = 10  # API 타임아웃
    
    # API 엔드포인트
    ENDPOINTS = {
        'solar_to_lunar': '/getSolCalInfo',
        'lunar_to_solar': '/getLunCalInfo', 
        'solar_terms': '/get24DivisionsInfo',
        'sexagenary_cycle': '/getSpcifyDayInfo'
    }

class CalculationMode:
    """계산 모드 상수"""
    KASI_PRIMARY = "kasi_primary"  # KASI API 우선
    FALLBACK_ONLY = "fallback_only"  # 폴백 계산만
    HYBRID = "hybrid"  # 하이브리드 (KASI + 폴백)