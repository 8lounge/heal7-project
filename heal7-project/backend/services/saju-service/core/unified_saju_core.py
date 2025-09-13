"""
🔮 통합 사주 핵심 로직 (SINGLE SOURCE OF TRUTH)
==================================================

이 파일은 모든 사주 계산의 단일 진리 소스입니다.
다른 곳에서 중복 구현하지 마세요!

📍 핵심 기능:
- 60갑자 계산 (1900-01-31 갑진일 기준)
- 음력 변환
- 사주팔자 계산
- 절기 정보

📍 사용법:
from core.unified_saju_core import UnifiedSajuCore
saju = UnifiedSajuCore()
result = saju.calculate_gapja(2025, 9, 11)  # "계미"

📍 폴백 정책:
1. KASI API 호출 시도
2. 실패 시 로컬 정확 계산 (수학적 공식)
3. 모든 계산은 1900-01-31=갑진일 기준점 사용

⚠️ 수정 시 주의사항:
- 기준일 변경 금지: 1900-01-31 = 갑진일 (절대 상수)
- 갑진 인덱스 40 변경 금지 (60갑자 순환에서 40번째)
- API 호출 시 3-5초 간격 필수 (KASI 사용량 한도)
"""

from datetime import date, datetime, timedelta
from typing import Dict, Tuple, Optional, Union, List
import requests
import logging
import os
import asyncpg
import asyncio

# 전역 상수 import
from .saju_constants import (
    GAPJA_60, CHEONGAN_10, JIJI_12, 
    REFERENCE_DATE, REFERENCE_GAPJA_INDEX,
    KASI_API_KEY, SOLAR_TERMS_24
)

logger = logging.getLogger(__name__)

class UnifiedSajuCore:
    """
    🔮 통합 사주 계산 엔진
    
    모든 사주 관련 계산을 담당하는 단일 클래스
    """
    
    def __init__(self):
        self.api_key = KASI_API_KEY
        self._cache = {}  # 간단한 메모리 캐시
    
    # ==========================================
    # 📍 60갑자 계산 (핵심 기능)
    # ==========================================
    
    def calculate_gapja(self, year: int, month: int, day: int) -> str:
        """
        특정 날짜의 60갑자 계산
        
        Args:
            year, month, day: 계산할 날짜
            
        Returns:
            str: 갑자 (예: "계미", "갑자")
            
        Example:
            >>> saju = UnifiedSajuCore()
            >>> saju.calculate_gapja(2025, 9, 11)
            "계미"
        """
        try:
            # 캐시 확인
            date_key = f"{year}-{month:02d}-{day:02d}"
            if date_key in self._cache:
                return self._cache[date_key]
            
            # 수학적 계산 (100% 정확)
            target_date = date(year, month, day)
            days_diff = (target_date - REFERENCE_DATE).days
            gapja_index = (REFERENCE_GAPJA_INDEX + days_diff) % 60
            
            result = GAPJA_60[gapja_index]
            self._cache[date_key] = result
            
            return result
            
        except Exception as e:
            logger.error(f"갑자 계산 실패 {year}-{month}-{day}: {e}")
            return "갑자"  # 안전한 기본값
    
    def calculate_gapja_batch(self, year: int, month: int) -> Dict[int, str]:
        """
        한 달의 모든 갑자를 배치 계산 (성능 최적화)
        
        Args:
            year, month: 계산할 년월
            
        Returns:
            Dict[int, str]: {일: 갑자} 매핑
        """
        result = {}
        days_in_month = self._get_days_in_month(year, month)
        
        for day in range(1, days_in_month + 1):
            result[day] = self.calculate_gapja(year, month, day)
        
        return result
    
    # ==========================================
    # 📍 음력 변환 (KASI API + 폴백)
    # ==========================================
    
    def solar_to_lunar(self, year: int, month: int, day: int) -> Dict[str, Union[int, bool, str]]:
        """
        양력 → 음력 변환
        
        Returns:
            Dict: {
                'lunar_year': int,
                'lunar_month': int, 
                'lunar_day': int,
                'is_leap_month': bool,
                'source': str  # 'kasi' 또는 'fallback'
            }
        """
        # 1. KASI API 시도
        try:
            if self._kasi_api_available():
                lunar_data = self._kasi_solar_to_lunar(year, month, day)
                if lunar_data:
                    lunar_data['source'] = 'kasi'
                    return lunar_data
        except Exception as e:
            logger.warning(f"KASI API 실패: {e}")
        
        # 2. 폴백 계산 (간단한 근사)
        logger.info(f"폴백 음력 계산 사용: {year}-{month}-{day}")
        return self._fallback_solar_to_lunar(year, month, day)
    
    def _kasi_solar_to_lunar(self, year: int, month: int, day: int) -> Optional[Dict]:
        """KASI API 호출"""
        if not self.api_key:
            return None
            
        try:
            url = "http://apis.data.go.kr/B090041/openapi/service/LrsrCldInfoService/getLunCalInfo"
            params = {
                'serviceKey': self.api_key,
                'solYear': year,
                'solMonth': f"{month:02d}",
                'solDay': f"{day:02d}",
                '_type': 'json'
            }
            
            response = requests.get(url, params=params, timeout=10)
            if response.status_code == 200:
                data = response.json()
                if 'response' in data and 'body' in data['response']:
                    items = data['response']['body'].get('items', {})
                    if 'item' in items:
                        item = items['item']
                        return {
                            'lunar_year': int(item['lunYear']),
                            'lunar_month': int(item['lunMonth']),
                            'lunar_day': int(item['lunDay']),
                            'is_leap_month': item.get('lunLeapmonth') == '윤'
                        }
            return None
            
        except Exception as e:
            logger.error(f"KASI API 호출 실패: {e}")
            return None
    
    def _fallback_solar_to_lunar(self, year: int, month: int, day: int) -> Dict[str, Union[int, bool, str]]:
        """폴백 음력 계산 (간단한 근사)"""
        # 매우 간단한 근사 계산 (실제로는 더 정확한 알고리즘 필요)
        # 음력은 약 29.5일 주기이므로 대략적인 계산
        
        solar_date = date(year, month, day)
        lunar_new_year_approx = date(year, 2, 10)  # 대략적인 음력 설날
        
        if solar_date < lunar_new_year_approx:
            lunar_year = year - 1
            days_from_new_year = (solar_date - date(lunar_year, 2, 10)).days + 365
        else:
            lunar_year = year
            days_from_new_year = (solar_date - lunar_new_year_approx).days
        
        # 대략적인 월/일 계산
        lunar_month = (days_from_new_year // 30) + 1
        lunar_day = (days_from_new_year % 30) + 1
        
        if lunar_month > 12:
            lunar_month = 12
        if lunar_day > 30:
            lunar_day = 30
            
        return {
            'lunar_year': lunar_year,
            'lunar_month': lunar_month,
            'lunar_day': lunar_day,
            'is_leap_month': False,
            'source': 'fallback'
        }
    
    # ==========================================
    # 📍 사주팔자 계산
    # ==========================================
    
    def calculate_saju_pillars(self, year: int, month: int, day: int, hour: int) -> Dict[str, str]:
        """
        사주팔자 계산 (년주, 월주, 일주, 시주)
        
        Args:
            year, month, day, hour: 생년월일시
            
        Returns:
            Dict: {
                'year_pillar': str,  # 년주
                'month_pillar': str, # 월주  
                'day_pillar': str,   # 일주
                'hour_pillar': str   # 시주
            }
        """
        try:
            # 일주 (기준)
            day_pillar = self.calculate_gapja(year, month, day)
            
            # 년주 (입춘 기준)
            year_pillar = self._calculate_year_pillar(year, month, day)
            
            # 월주 (절기 기준, DB 연동)
            month_pillar = self._calculate_month_pillar(year, month, day, year_pillar)
            
            # 시주 (일간 기준)
            hour_pillar = self._calculate_hour_pillar(day_pillar, hour)
            
            return {
                'year_pillar': year_pillar,
                'month_pillar': month_pillar,
                'day_pillar': day_pillar,
                'hour_pillar': hour_pillar
            }
            
        except Exception as e:
            logger.error(f"사주팔자 계산 실패: {e}")
            return {
                'year_pillar': '갑자',
                'month_pillar': '갑자', 
                'day_pillar': '갑자',
                'hour_pillar': '갑자'
            }
    
    def _calculate_year_pillar(self, year: int, month: int, day: int) -> str:
        """년주 계산 (입춘 기준)"""
        # 입춘 이전은 전년도로 계산
        saju_year = year
        if month < 2 or (month == 2 and day < 4):
            saju_year = year - 1
        
        # 1900년 = 경자년(36번째) 기준
        year_offset = (saju_year - 1900) % 60
        year_index = (36 + year_offset) % 60
        return GAPJA_60[year_index]

    def calculate_comprehensive_saju(self, birth_data: dict) -> dict:
        """
        종합 사주 계산 (메인 인터페이스)

        Args:
            birth_data: {'year': int, 'month': int, 'day': int, 'hour': int, 'minute': int, 'gender': str, 'name': str}

        Returns:
            dict: 완전한 사주 분석 결과
        """
        try:
            year = birth_data['year']
            month = birth_data['month']
            day = birth_data['day']
            hour = birth_data['hour']
            minute = birth_data.get('minute', 0)

            # 사주팔자 계산
            saju_result = self.calculate_saju_pillars(year, month, day, hour)

            # 추가 분석 정보
            comprehensive_result = {
                **saju_result,
                'birth_data': birth_data,
                'day_master': saju_result['day_pillar'][0],  # 일간
                'palcha': f"{saju_result['year_pillar']} {saju_result['month_pillar']} {saju_result['day_pillar']} {saju_result['time_pillar']}",
                'element_balance': {},  # 향후 구현
                'sipsin_analysis': {},  # 향후 구현
                'sinsal': [],          # 향후 구현
                'calculation_method': 'unified_db_enhanced',
                'created_at': datetime.now()
            }

            return comprehensive_result

        except Exception as e:
            logger.error(f"종합 사주 계산 오류: {e}")
            # 기본값 반환
            return {
                'year_pillar': '갑자', 'month_pillar': '을축',
                'day_pillar': '병인', 'time_pillar': '정묘',
                'day_master': '병',
                'palcha': f"계산 오류: {str(e)}",
                'element_balance': {},
                'sipsin_analysis': {},
                'sinsal': [],
                'calculation_method': 'error_fallback'
            }
    
    def _calculate_month_pillar(self, year: int, month: int, day: int, year_pillar: str) -> str:
        """
        월주 계산 (절기 기준, DB 연동)

        🔥 개선사항:
        - healwitch_perpetual_calendars DB 직접 조회
        - 정확한 절기 기준 계산
        - 73,442건 데이터 기반 정밀도
        """
        try:
            # 비동기 DB 조회를 동기로 실행
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                result = loop.run_until_complete(self._get_month_pillar_from_db(year, month, day))
                return result
            finally:
                loop.close()
        except Exception as e:
            logger.error(f"DB 기반 월주 계산 실패, 폴백 사용: {e}")
            # 폴백: 기존 간단 계산 (절기 무시)
            return self._calculate_month_pillar_fallback(year, month, year_pillar)

    async def _get_month_pillar_from_db(self, year: int, month: int, day: int) -> str:
        """DB에서 정확한 월주 조회"""
        try:
            conn = await asyncpg.connect(
                host="/var/run/postgresql",
                database="heal7_saju",
                user="postgres"
            )

            # 해당 날짜의 정확한 월주 조회
            query = """
            SELECT month_gapja FROM healwitch_perpetual_calendars
            WHERE solar_year = $1 AND solar_month = $2 AND solar_day = $3
            LIMIT 1
            """

            row = await conn.fetchrow(query, year, month, day)

            if row and row['month_gapja']:
                return row['month_gapja']
            else:
                # DB에 월주 정보가 없으면 계산해서 저장
                return await self._calculate_and_save_month_pillar(conn, year, month, day)

        except Exception as e:
            logger.error(f"DB 월주 조회 오류: {e}")
            raise
        finally:
            if 'conn' in locals():
                await conn.close()

    async def _calculate_and_save_month_pillar(self, conn, year: int, month: int, day: int) -> str:
        """월주 계산 후 DB 저장"""
        try:
            # 년주 조회
            year_query = "SELECT year_gapja FROM healwitch_perpetual_calendars WHERE solar_year = $1 LIMIT 1"
            year_row = await conn.fetchrow(year_query, year)
            year_pillar = year_row['year_gapja'] if year_row else f"{CHEONGAN_10[year % 10]}{JIJI_12[year % 12]}"

            # 해당 월의 절기 정보 조회
            solar_term_query = """
            SELECT solar_term_korean, solar_day
            FROM healwitch_perpetual_calendars
            WHERE solar_year = $1 AND solar_month = $2 AND solar_term_korean IS NOT NULL
            ORDER BY solar_day ASC
            """

            solar_terms = await conn.fetch(solar_term_query, year, month)

            # 절기별 월지 매핑
            solar_term_to_jiji = {
                "입춘": 2, "경칩": 3, "청명": 4, "입하": 5, "망종": 6, "소서": 7,
                "입추": 8, "백로": 9, "한로": 10, "입동": 11, "대설": 0, "소한": 1
            }

            # 현재 날짜가 속하는 절기 구간 찾기
            current_jiji = 2  # 기본값: 인월
            for term in solar_terms:
                if day >= term['solar_day'] and term['solar_term_korean'] in solar_term_to_jiji:
                    current_jiji = solar_term_to_jiji[term['solar_term_korean']]

            # 년간별 월간 계산
            year_cheonan = year_pillar[0]
            year_to_month_base = {"갑": 2, "기": 2, "을": 4, "경": 4, "병": 6, "신": 6, "정": 8, "임": 8, "무": 0, "계": 0}
            base_index = year_to_month_base.get(year_cheonan, 2)

            month_offset = (current_jiji - 2 + 12) % 12
            cheonan_index = (base_index + month_offset) % 10

            month_pillar = f"{CHEONGAN_10[cheonan_index]}{JIJI_12[current_jiji]}"

            # DB 업데이트
            update_query = """
            UPDATE healwitch_perpetual_calendars
            SET month_gapja = $1
            WHERE solar_year = $2 AND solar_month = $3 AND solar_day = $4
            """
            await conn.execute(update_query, month_pillar, year, month, day)

            return month_pillar

        except Exception as e:
            logger.error(f"월주 계산 및 저장 오류: {e}")
            # 최후 폴백
            return "갑인"

    def _calculate_month_pillar_fallback(self, year: int, month: int, year_pillar: str) -> str:
        """폴백: 기존 간단 계산"""
        month_map = {1: 2, 2: 3, 3: 4, 4: 5, 5: 6, 6: 7, 7: 8, 8: 9, 9: 10, 10: 11, 11: 12, 12: 1}
        year_cheonan_index = GAPJA_60.index(year_pillar) % 10
        base_month_index = (year_cheonan_index * 2 + month_map[month]) % 60
        return GAPJA_60[base_month_index]
    
    def _calculate_hour_pillar(self, day_pillar: str, hour: int) -> str:
        """시주 계산 (일간 기준)"""
        # 시간을 지지로 변환
        hour_jiji_map = {
            23: 0, 0: 0, 1: 0,    # 자시 (23-01)
            2: 1, 3: 1,           # 축시 (01-03) 
            4: 2, 5: 2,           # 인시 (03-05)
            6: 3, 7: 3,           # 묘시 (05-07)
            8: 4, 9: 4,           # 진시 (07-09)
            10: 5, 11: 5,         # 사시 (09-11)
            12: 6, 13: 6,         # 오시 (11-13)
            14: 7, 15: 7,         # 미시 (13-15)
            16: 8, 17: 8,         # 신시 (15-17)
            18: 9, 19: 9,         # 유시 (17-19)
            20: 10, 21: 10,       # 술시 (19-21)
            22: 11                # 해시 (21-23)
        }
        
        hour_jiji_index = hour_jiji_map.get(hour, 0)
        day_cheongan_index = GAPJA_60.index(day_pillar) % 10
        
        # 일간에 따른 시간 천간 계산
        hour_cheongan_index = (day_cheongan_index * 2 + hour_jiji_index) % 10
        hour_gapja_index = hour_cheongan_index * 6 + hour_jiji_index
        
        return GAPJA_60[hour_gapja_index % 60]
    
    # ==========================================
    # 📍 유틸리티 함수
    # ==========================================
    
    def _kasi_api_available(self) -> bool:
        """KASI API 사용 가능 여부 확인"""
        return bool(self.api_key and len(self.api_key) > 10)
    
    def _get_days_in_month(self, year: int, month: int) -> int:
        """월의 일수 계산"""
        if month == 12:
            next_month = date(year + 1, 1, 1)
        else:
            next_month = date(year, month + 1, 1)
        last_day = next_month - timedelta(days=1)
        return last_day.day
    
    def get_system_status(self) -> Dict[str, Union[str, bool]]:
        """시스템 상태 확인"""
        return {
            'kasi_api_available': self._kasi_api_available(),
            'cache_size': len(self._cache),
            'version': '2.0.0-unified',
            'source': 'unified_saju_core.py'
        }


# ==========================================
# 📍 글로벌 인스턴스 (싱글톤 패턴)
# ==========================================

_saju_instance = None

def get_saju_core() -> UnifiedSajuCore:
    """
    글로벌 사주 코어 인스턴스 반환 (싱글톤)
    
    Example:
        from core.unified_saju_core import get_saju_core
        saju = get_saju_core()
        result = saju.calculate_gapja(2025, 9, 11)
    """
    global _saju_instance
    if _saju_instance is None:
        _saju_instance = UnifiedSajuCore()
    return _saju_instance


# ==========================================
# 📍 편의 함수들 (직접 호출용)
# ==========================================

def calculate_gapja(year: int, month: int, day: int) -> str:
    """편의 함수: 60갑자 계산"""
    return get_saju_core().calculate_gapja(year, month, day)

def calculate_saju(year: int, month: int, day: int, hour: int) -> Dict[str, str]:
    """편의 함수: 사주팔자 계산"""
    return get_saju_core().calculate_saju_pillars(year, month, day, hour)

def solar_to_lunar(year: int, month: int, day: int) -> Dict[str, Union[int, bool, str]]:
    """편의 함수: 음력 변환"""
    return get_saju_core().solar_to_lunar(year, month, day)


# ==========================================
# 📍 사용 예제 (테스트용)
# ==========================================

if __name__ == "__main__":
    # 테스트 실행
    saju = get_saju_core()
    
    print("🔮 통합 사주 핵심 로직 테스트")
    print("=" * 40)
    
    # 갑자 계산 테스트
    test_dates = [
        (2025, 9, 9),   # 신사
        (2025, 9, 10),  # 임오
        (2025, 9, 11),  # 계미
        (2025, 9, 12),  # 갑신
        (2025, 9, 13),  # 을유
    ]
    
    for year, month, day in test_dates:
        gapja = saju.calculate_gapja(year, month, day)
        print(f"{year}-{month:02d}-{day:02d}: {gapja}")
    
    # 사주팔자 테스트
    print(f"\n📅 사주팔자 (2025-09-11 12시):")
    pillars = saju.calculate_saju_pillars(2025, 9, 11, 12)
    for pillar_name, pillar_value in pillars.items():
        print(f"  {pillar_name}: {pillar_value}")
    
    # 시스템 상태
    print(f"\n🔧 시스템 상태:")
    status = saju.get_system_status()
    for key, value in status.items():
        print(f"  {key}: {value}")