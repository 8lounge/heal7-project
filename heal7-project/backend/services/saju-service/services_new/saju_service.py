"""
🔮 간소화된 통합 사주 서비스 (Simple Unified Saju Service)
=================================================================

심플 통합 원칙:
- 하나의 핵심 엔진만 사용 (unified_saju_core)
- 복잡한 의존성 제거
- 직관적인 인터페이스 제공
- 레거시 코드 완전 분리

작성: 2025-09-12
목적: 분산된 사주 로직을 하나로 통합
"""

from datetime import datetime
from typing import Dict, Any, Optional
from enum import Enum

# 로컬 통합 엔진 import
from core.unified_saju_core import UnifiedSajuCore

class Gender(Enum):
    """성별 열거형"""
    MALE = "male"
    FEMALE = "female"

class BirthInfo:
    """출생 정보 클래스 (간소화)"""
    def __init__(self, year: int, month: int, day: int, hour: int, minute: int, 
                 gender: str, name: str = None, is_lunar: bool = False):
        self.year = year
        self.month = month  
        self.day = day
        self.hour = hour
        self.minute = minute
        self.gender = gender
        self.name = name or "Unknown"
        self.is_lunar = is_lunar
    
    def __str__(self):
        return f"{self.year}-{self.month:02d}-{self.day:02d} {self.hour:02d}:{self.minute:02d} ({self.gender})"

class SajuResult:
    """사주 결과 클래스 (간소화)"""
    def __init__(self, data: Dict[str, Any]):
        # 필수 필드
        self.birth_info = data.get('birth_info')
        self.year_pillar = data.get('year_pillar', '갑자')
        self.month_pillar = data.get('month_pillar', '을축') 
        self.day_pillar = data.get('day_pillar', '병인')
        self.time_pillar = data.get('time_pillar', '정묘')
        self.day_master = data.get('day_master', '병')
        
        # 추가 분석 데이터
        self.element_balance = data.get('element_balance', {})
        self.sipsin_analysis = data.get('sipsin_analysis', {})
        self.sinsal = data.get('sinsal', [])
        self.palcha = data.get('palcha', '기본 팔자')
        self.is_strong_day_master = data.get('is_strong_day_master', True)
        
        # 메타데이터
        self.created_at = data.get('created_at', datetime.now())
        self.calculation_method = data.get('calculation_method', 'unified_simple')

class SajuService:
    """
    🌟 심플 통합 사주 서비스
    
    단일 책임: 사주 계산 및 해석
    의존성: unified_saju_core만 사용
    """
    
    def __init__(self):
        """서비스 초기화"""
        self.core = None
        self._initialized = False
    
    async def initialize(self):
        """비동기 초기화"""
        if not self._initialized:
            try:
                self.core = UnifiedSajuCore()
                self._initialized = True
                print("✅ Simple Saju Service initialized successfully")
            except Exception as e:
                print(f"❌ Failed to initialize Saju Service: {e}")
                raise
    
    async def calculate_saju(self, birth_info: BirthInfo) -> SajuResult:
        """
        메인 사주 계산 함수
        
        Args:
            birth_info: 출생 정보
            
        Returns:
            SajuResult: 사주 계산 결과
        """
        if not self._initialized:
            await self.initialize()
        
        try:
            print(f"🔮 Computing saju for: {birth_info}")
            
            # 핵심 계산 수행
            result_data = self.core.calculate_comprehensive_saju({
                'year': birth_info.year,
                'month': birth_info.month,
                'day': birth_info.day,
                'hour': birth_info.hour,
                'minute': birth_info.minute,
                'gender': birth_info.gender,
                'name': birth_info.name,
                'is_lunar': birth_info.is_lunar
            })
            
            # 결과 구조화
            result_data['birth_info'] = birth_info
            result_data['calculation_method'] = 'unified_simple'
            result_data['created_at'] = datetime.now()
            
            return SajuResult(result_data)
            
        except Exception as e:
            print(f"❌ Saju calculation error: {e}")
            # 기본 결과 반환 (서비스 중단 방지)
            return SajuResult({
                'birth_info': birth_info,
                'year_pillar': '갑자', 'month_pillar': '을축',
                'day_pillar': '병인', 'time_pillar': '정묘',
                'day_master': '병',
                'element_balance': {},
                'sipsin_analysis': {},
                'sinsal': [],
                'palcha': f'계산 오류로 기본값 반환 ({str(e)})',
                'is_strong_day_master': True,
                'calculation_method': 'error_fallback',
                'created_at': datetime.now()
            })

# 호환성을 위한 별칭
SajuServiceResult = SajuResult

# 심플 통합 완료
print("🌟 Simple Unified Saju Service Module Loaded")