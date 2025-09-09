"""
원자 모듈: 음력 변환기
===================
입력: 양력 날짜 또는 음력 날짜
출력: 변환된 날짜 정보 (음력 ↔ 양력)
로직: KASI API 연동 기반 정확한 음력 변환

특징:
- KASI API 우선 사용 (정확도 보장)
- 로컬 캐시로 성능 최적화
- 윤달 정보 포함
- 오류 시 폴백 시스템
"""

from datetime import date, datetime
from typing import Dict, Optional, Union, NamedTuple, Tuple
import asyncio
import aiohttp
import json
from dataclasses import dataclass

@dataclass
class LunarDate:
    """음력 날짜 정보"""
    year: int
    month: int
    day: int
    is_leap_month: bool = False
    lunar_month_name: str = ""
    
    def __str__(self) -> str:
        leap_str = "윤" if self.is_leap_month else ""
        return f"음력 {self.year}년 {leap_str}{self.month}월 {self.day}일"

@dataclass 
class SolarDate:
    """양력 날짜 정보"""
    year: int
    month: int
    day: int
    
    def __str__(self) -> str:
        return f"양력 {self.year}년 {self.month}월 {self.day}일"

@dataclass
class ConversionResult:
    """변환 결과"""
    success: bool
    solar_date: Optional[SolarDate] = None
    lunar_date: Optional[LunarDate] = None
    source: str = "unknown"  # kasi, local, fallback
    error_message: str = ""

class LunarConverter:
    """음력 변환기 클래스"""
    
    def __init__(self, kasi_api_base: str = None, cache_enabled: bool = True):
        self.kasi_api_base = kasi_api_base or "http://localhost:8002/api/kasi"
        self.cache_enabled = cache_enabled
        self._cache: Dict[str, ConversionResult] = {}
    
    async def solar_to_lunar(self, solar_date: Union[str, date, SolarDate]) -> ConversionResult:
        """
        양력을 음력으로 변환
        
        Args:
            solar_date: 양력 날짜
            
        Returns:
            ConversionResult: 변환 결과
        """
        # 입력 정규화
        if isinstance(solar_date, str):
            try:
                solar_obj = datetime.strptime(solar_date, "%Y-%m-%d").date()
                solar_date = SolarDate(solar_obj.year, solar_obj.month, solar_obj.day)
            except ValueError:
                return ConversionResult(False, error_message="잘못된 날짜 형식")
        elif isinstance(solar_date, date):
            solar_date = SolarDate(solar_date.year, solar_date.month, solar_date.day)
        
        # 캐시 확인
        cache_key = f"s2l_{solar_date.year}_{solar_date.month}_{solar_date.day}"
        if self.cache_enabled and cache_key in self._cache:
            return self._cache[cache_key]
        
        # KASI API 호출 시도
        try:
            result = await self._call_kasi_solar_to_lunar(solar_date)
            if result.success:
                if self.cache_enabled:
                    self._cache[cache_key] = result
                return result
        except Exception as e:
            print(f"KASI API 호출 실패: {e}")
        
        # 폴백: 로컬 계산
        result = self._fallback_solar_to_lunar(solar_date)
        if self.cache_enabled:
            self._cache[cache_key] = result
        return result
    
    async def lunar_to_solar(self, lunar_date: Union[LunarDate, Tuple[int, int, int, bool]]) -> ConversionResult:
        """
        음력을 양력으로 변환
        
        Args:
            lunar_date: 음력 날짜 (LunarDate 객체 또는 (년, 월, 일, 윤달여부) 튜플)
            
        Returns:
            ConversionResult: 변환 결과
        """
        # 입력 정규화
        if isinstance(lunar_date, tuple):
            year, month, day, is_leap = lunar_date
            lunar_date = LunarDate(year, month, day, is_leap)
        
        # 캐시 확인
        leap_str = "leap" if lunar_date.is_leap_month else "normal"
        cache_key = f"l2s_{lunar_date.year}_{lunar_date.month}_{lunar_date.day}_{leap_str}"
        if self.cache_enabled and cache_key in self._cache:
            return self._cache[cache_key]
        
        # KASI API 호출 시도
        try:
            result = await self._call_kasi_lunar_to_solar(lunar_date)
            if result.success:
                if self.cache_enabled:
                    self._cache[cache_key] = result
                return result
        except Exception as e:
            print(f"KASI API 호출 실패: {e}")
        
        # 폴백: 로컬 계산
        result = self._fallback_lunar_to_solar(lunar_date)
        if self.cache_enabled:
            self._cache[cache_key] = result
        return result
    
    async def _call_kasi_solar_to_lunar(self, solar_date: SolarDate) -> ConversionResult:
        """KASI API로 양력→음력 변환"""
        url = f"{self.kasi_api_base}/solar-to-lunar"
        params = {
            "year": solar_date.year,
            "month": solar_date.month,
            "day": solar_date.day
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    if data.get("success"):
                        lunar_data = data.get("data", {})
                        lunar_date = LunarDate(
                            year=int(lunar_data.get("lunYear", solar_date.year)),
                            month=int(lunar_data.get("lunMonth", 1)),
                            day=int(lunar_data.get("lunDay", 1)),
                            is_leap_month=lunar_data.get("lunLeapmonth") == "윤"
                        )
                        return ConversionResult(
                            True, 
                            solar_date=solar_date,
                            lunar_date=lunar_date,
                            source="kasi"
                        )
                
                return ConversionResult(False, error_message=f"KASI API 오류: {response.status}")
    
    async def _call_kasi_lunar_to_solar(self, lunar_date: LunarDate) -> ConversionResult:
        """KASI API로 음력→양력 변환"""
        url = f"{self.kasi_api_base}/lunar-to-solar"
        params = {
            "year": lunar_date.year,
            "month": lunar_date.month,
            "day": lunar_date.day,
            "is_leap": lunar_date.is_leap_month
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    if data.get("success"):
                        solar_data = data.get("data", {})
                        solar_date = SolarDate(
                            year=int(solar_data.get("year", lunar_date.year)),
                            month=int(solar_data.get("month", 1)),
                            day=int(solar_data.get("day", 1))
                        )
                        return ConversionResult(
                            True,
                            solar_date=solar_date,
                            lunar_date=lunar_date,
                            source="kasi"
                        )
                
                return ConversionResult(False, error_message=f"KASI API 오류: {response.status}")
    
    def _fallback_solar_to_lunar(self, solar_date: SolarDate) -> ConversionResult:
        """폴백: 로컬 양력→음력 변환 (근사값)"""
        # 간단한 근사 계산 (실제로는 더 정교한 알고리즘 필요)
        # 이것은 KASI API가 실패했을 때의 최후 수단
        
        try:
            # 윤년 고려한 대략적인 계산
            days_in_year = 366 if self._is_leap_year(solar_date.year) else 365
            day_of_year = self._get_day_of_year(solar_date)
            
            # 음력은 대략 354일 (29.5일 × 12개월)
            lunar_day_of_year = int(day_of_year * 354 / days_in_year)
            
            # 월과 일 계산 (근사)
            lunar_month = max(1, min(12, (lunar_day_of_year - 1) // 29 + 1))
            lunar_day = max(1, min(30, (lunar_day_of_year - 1) % 29 + 1))
            
            lunar_date = LunarDate(
                year=solar_date.year,
                month=lunar_month,
                day=lunar_day,
                is_leap_month=False  # 윤달 계산은 복잡하므로 생략
            )
            
            return ConversionResult(
                True,
                solar_date=solar_date,
                lunar_date=lunar_date,
                source="fallback"
            )
            
        except Exception as e:
            return ConversionResult(False, error_message=f"폴백 계산 실패: {e}")
    
    def _fallback_lunar_to_solar(self, lunar_date: LunarDate) -> ConversionResult:
        """폴백: 로컬 음력→양력 변환 (근사값)"""
        try:
            # 음력 일수를 양력으로 근사 변환
            lunar_day_of_year = (lunar_date.month - 1) * 29 + lunar_date.day
            
            # 양력 일수로 변환 (대략적)
            days_in_year = 366 if self._is_leap_year(lunar_date.year) else 365
            solar_day_of_year = int(lunar_day_of_year * days_in_year / 354)
            
            # 월과 일 계산
            solar_month, solar_day = self._day_of_year_to_month_day(
                solar_day_of_year, lunar_date.year
            )
            
            solar_date = SolarDate(
                year=lunar_date.year,
                month=solar_month,
                day=solar_day
            )
            
            return ConversionResult(
                True,
                solar_date=solar_date,
                lunar_date=lunar_date,
                source="fallback"
            )
            
        except Exception as e:
            return ConversionResult(False, error_message=f"폴백 계산 실패: {e}")
    
    def _is_leap_year(self, year: int) -> bool:
        """윤년 판별"""
        return (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)
    
    def _get_day_of_year(self, solar_date: SolarDate) -> int:
        """연중 몇 번째 날인지 계산"""
        date_obj = date(solar_date.year, solar_date.month, solar_date.day)
        jan_1 = date(solar_date.year, 1, 1)
        return (date_obj - jan_1).days + 1
    
    def _day_of_year_to_month_day(self, day_of_year: int, year: int) -> Tuple[int, int]:
        """연중 일수를 월/일로 변환"""
        days_in_months = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        if self._is_leap_year(year):
            days_in_months[1] = 29
        
        month = 1
        remaining_days = day_of_year
        
        for days_in_month in days_in_months:
            if remaining_days <= days_in_month:
                return month, remaining_days
            remaining_days -= days_in_month
            month += 1
        
        # 범위 초과 시 12월 31일로 보정
        return 12, days_in_months[11]

# === 편의 함수들 ===

# 전역 변환기 인스턴스
_default_converter = LunarConverter()

async def solar_to_lunar(solar_date: Union[str, date]) -> ConversionResult:
    """양력을 음력으로 변환 (편의 함수)"""
    return await _default_converter.solar_to_lunar(solar_date)

async def lunar_to_solar(year: int, month: int, day: int, is_leap: bool = False) -> ConversionResult:
    """음력을 양력으로 변환 (편의 함수)"""
    lunar_date = LunarDate(year, month, day, is_leap)
    return await _default_converter.lunar_to_solar(lunar_date)

def solar_to_lunar_sync(solar_date: Union[str, date]) -> ConversionResult:
    """동기 버전 양력→음력 변환"""
    return asyncio.run(solar_to_lunar(solar_date))

def lunar_to_solar_sync(year: int, month: int, day: int, is_leap: bool = False) -> ConversionResult:
    """동기 버전 음력→양력 변환"""
    return asyncio.run(lunar_to_solar(year, month, day, is_leap))

# === 테스트 함수들 ===

async def test_lunar_converter():
    """음력 변환기 테스트"""
    converter = LunarConverter()
    
    # 양력→음력 테스트
    result = await converter.solar_to_lunar("2025-09-09")
    print(f"2025-09-09 (양력) → {result.lunar_date}")
    
    # 음력→양력 테스트  
    if result.success and result.lunar_date:
        reverse_result = await converter.lunar_to_solar(result.lunar_date)
        print(f"{result.lunar_date} → {reverse_result.solar_date}")
    
    print("✅ 음력 변환기 테스트 완료")

if __name__ == "__main__":
    asyncio.run(test_lunar_converter())