"""
KASI API 정밀 사주 계산기 - 핵심 계산 모듈
자주 사용되는 핵심 사주 계산 기능들
"""

import os
import requests
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
from typing import Dict, Tuple, Optional
import logging
import re

from .shared.kasi_calculator_models import (
    KOREAN_TO_CHINESE_GANJEE, CHEONGAN, JIJI, SIDUBEOP,
    GAPJA_REFERENCE_TABLE, SajuResult, KasiApiConfig, CalculationMode
)

logger = logging.getLogger(__name__)

class KasiCalculatorCore:
    """KASI API 기반 핵심 사주 계산기 - 자주 사용되는 기본 기능"""
    
    def __init__(self):
        self.api_key = os.getenv('KASI_API_KEY', '')
        self.usage_count = 0
        self.gapja_cache = self._build_basic_gapja_cache()
    
    def calculate_saju(self, year: int, month: int, day: int, 
                      hour: int = 12, minute: int = 0, 
                      is_lunar: bool = False, is_leap: bool = False) -> Optional[Dict]:
        """
        메인 사주 계산 함수 - 가장 자주 사용됨
        KASI API 우선, 실패시 폴백 계산
        """
        try:
            # 입력 검증
            if not self._validate_input_date(year, month, day, hour, minute):
                return None
            
            birth_datetime = datetime(year, month, day, hour, minute)
            
            # 달력 변환 (음력→양력 or 양력→음력)
            calendar_info = {}
            if is_lunar:
                solar_data = self._lunar_to_solar_kasi(year, month, day, is_leap)
                if solar_data:
                    calendar_info = {
                        'input_type': '음력',
                        'lunar': {
                            'year': year, 'month': month, 'day': day,
                            'is_leap': is_leap,
                            'date_string': f"{year}년 {month}월 {day}일" + (" (윤달)" if is_leap else "")
                        },
                        'solar': solar_data
                    }
                    # 양력 날짜로 변경
                    birth_datetime = datetime(
                        solar_data['year'], solar_data['month'], solar_data['day'],
                        hour, minute
                    )
            else:
                lunar_data = self._solar_to_lunar_kasi(year, month, day)
                if lunar_data:
                    calendar_info = {
                        'input_type': '양력',
                        'solar': {
                            'year': year, 'month': month, 'day': day,
                            'date_string': f"{year}년 {month}월 {day}일"
                        },
                        'lunar': lunar_data
                    }
            
            # 진태양시 계산
            true_solar_time = self._calculate_pure_solar_time(birth_datetime)
            
            # 사주 4주 계산
            pillars = {
                'year': self._calculate_year_pillar(true_solar_time.year, true_solar_time),
                'month': self._calculate_month_pillar(true_solar_time.year, true_solar_time.month, true_solar_time),
                'day': self._calculate_day_pillar(true_solar_time.year, true_solar_time.month, true_solar_time.day, true_solar_time),
                'hour': self._calculate_hour_pillar(true_solar_time)
            }
            
            # 일간 추출
            ilgan = pillars['day']['gapja'][0] if pillars['day']['gapja'] else '甲'
            
            return SajuResult(pillars, ilgan, calendar_info).to_dict()
            
        except Exception as e:
            logger.error(f"사주 계산 오류: {e}")
            return self._fallback_calculation(year, month, day, hour, minute, is_lunar)
    
    def _lunar_to_solar_kasi(self, lun_year: int, lun_month: int, lun_day: int, is_leap: bool) -> Optional[Dict]:
        """음력 → 양력 변환 (KASI API)"""
        if not self.api_key or not self._check_basic_usage_limit():
            return self._approximate_lunar_to_solar(lun_year, lun_month, lun_day)
        
        try:
            url = f"{KasiApiConfig.BASE_URL}{KasiApiConfig.ENDPOINTS['lunar_to_solar']}"
            params = {
                'serviceKey': self.api_key,
                'lunYear': lun_year,
                'lunMonth': str(lun_month).zfill(2),
                'lunDay': str(lun_day).zfill(2),
                'lunLeapmonth': 'Y' if is_leap else 'N'
            }
            
            response = requests.get(url, params=params, timeout=KasiApiConfig.TIMEOUT_SECONDS)
            response.raise_for_status()
            
            root = ET.fromstring(response.content)
            sol_year = root.find('.//solYear')
            sol_month = root.find('.//solMonth')
            sol_day = root.find('.//solDay')
            
            if sol_year is not None and sol_month is not None and sol_day is not None:
                self.usage_count += 1
                return {
                    'year': int(sol_year.text),
                    'month': int(sol_month.text),
                    'day': int(sol_day.text),
                    'date_string': f"{sol_year.text}년 {sol_month.text}월 {sol_day.text}일"
                }
            
        except Exception as e:
            logger.warning(f"KASI 음력→양력 변환 실패: {e}")
        
        return self._approximate_lunar_to_solar(lun_year, lun_month, lun_day)
    
    def _solar_to_lunar_kasi(self, sol_year: int, sol_month: int, sol_day: int) -> Optional[Dict]:
        """양력 → 음력 변환 (KASI API)"""
        if not self.api_key or not self._check_basic_usage_limit():
            return self._approximate_solar_to_lunar(sol_year, sol_month, sol_day)
        
        try:
            url = f"{KasiApiConfig.BASE_URL}{KasiApiConfig.ENDPOINTS['solar_to_lunar']}"
            params = {
                'serviceKey': self.api_key,
                'solYear': sol_year,
                'solMonth': str(sol_month).zfill(2),
                'solDay': str(sol_day).zfill(2)
            }
            
            response = requests.get(url, params=params, timeout=KasiApiConfig.TIMEOUT_SECONDS)
            response.raise_for_status()
            
            root = ET.fromstring(response.content)
            lun_year = root.find('.//lunYear')
            lun_month = root.find('.//lunMonth') 
            lun_day = root.find('.//lunDay')
            leap_month = root.find('.//lunLeapmonth')
            
            if lun_year is not None and lun_month is not None and lun_day is not None:
                self.usage_count += 1
                is_leap = leap_month is not None and leap_month.text == 'Y'
                
                return {
                    'year': int(lun_year.text),
                    'month': int(lun_month.text), 
                    'day': int(lun_day.text),
                    'is_leap': is_leap,
                    'date_string': f"{lun_year.text}년 {lun_month.text}월 {lun_day.text}일" + (" (윤달)" if is_leap else "")
                }
            
        except Exception as e:
            logger.warning(f"KASI 양력→음력 변환 실패: {e}")
        
        return self._approximate_solar_to_lunar(sol_year, sol_month, sol_day)
    
    def _calculate_pure_solar_time(self, birth_datetime: datetime) -> datetime:
        """진태양시 계산 (서울 기준 -32분 보정)"""
        # 서울 표준시 기준 경도차 보정 (동경 127.5도 - 135도 = -7.5도 = -30분)
        # 추가 보정 -2분 (전통적 보정)
        longitude_correction = timedelta(minutes=-32)
        return birth_datetime + longitude_correction
    
    def _calculate_year_pillar(self, year: int, true_solar_time: datetime) -> Dict:
        """연주 계산"""
        # 입춘 기준 연주 계산 (2월 4일 전후)
        if true_solar_time.month == 1 or (true_solar_time.month == 2 and true_solar_time.day < 4):
            year = year - 1
        
        # 갑자 순환 계산 (60갑자)
        base_year = 1924  # 갑자년 기준
        cycle_position = (year - base_year) % 60
        
        cheongan_index = cycle_position % 10
        jiji_index = cycle_position % 12
        
        gapja = CHEONGAN[cheongan_index] + JIJI[jiji_index]
        
        return {
            'gapja': gapja,
            'cheongan': CHEONGAN[cheongan_index],
            'jiji': JIJI[jiji_index],
            'cheongan_index': cheongan_index,
            'jiji_index': jiji_index
        }
    
    def _calculate_month_pillar(self, year: int, month: int, true_solar_time: datetime) -> Dict:
        """월주 계산 (절기 기준)"""
        # 기본 월지지 매핑 (입춘 기준)
        month_jiji_map = {
            1: '寅', 2: '卯', 3: '辰', 4: '巳', 5: '午', 6: '未',
            7: '申', 8: '酉', 9: '戌', 10: '亥', 11: '子', 12: '丑'
        }
        
        # 절기 기준 월지지 결정
        month_jiji = month_jiji_map.get(true_solar_time.month, '寅')
        
        # 월천간 계산 (연간에 따른 월천간 매핑)
        year_cheongan = self._calculate_year_pillar(year, true_solar_time)['cheongan']
        
        # 월천간 매핑 테이블 (전통 명리학)
        month_cheongan_map = {
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
        
        month_index = true_solar_time.month - 1
        month_cheongan_list = month_cheongan_map.get(year_cheongan, month_cheongan_map['甲'])
        month_cheongan = month_cheongan_list[month_index]
        
        gapja = month_cheongan + month_jiji
        
        return {
            'gapja': gapja,
            'cheongan': month_cheongan,
            'jiji': month_jiji,
            'cheongan_index': CHEONGAN.index(month_cheongan),
            'jiji_index': JIJI.index(month_jiji)
        }
    
    def _calculate_day_pillar(self, year: int, month: int, day: int, true_solar_time: datetime) -> Dict:
        """일주 계산"""
        # KASI API 우선 시도
        kasi_result = self._get_day_pillar_from_kasi(true_solar_time)
        if kasi_result:
            return self._parse_day_pillar_result(kasi_result)
        
        # 폴백 계산
        return self._calculate_day_pillar_fallback(true_solar_time)
    
    def _calculate_hour_pillar(self, true_solar_time: datetime) -> Dict:
        """시주 계산"""
        hour = true_solar_time.hour
        
        # 시지지 계산 (2시간 단위)
        hour_jiji_index = ((hour + 1) // 2) % 12
        hour_jiji = JIJI[hour_jiji_index]
        
        # 일간 구하기 (일주에서)
        day_pillar = self._calculate_day_pillar(
            true_solar_time.year, true_solar_time.month, true_solar_time.day, true_solar_time
        )
        day_cheongan = day_pillar['cheongan']
        
        # 시두법으로 시천간 계산
        hour_cheongan_list = SIDUBEOP.get(day_cheongan, SIDUBEOP['甲'])
        hour_cheongan = hour_cheongan_list[hour_jiji_index]
        
        gapja = hour_cheongan + hour_jiji
        
        return {
            'gapja': gapja,
            'cheongan': hour_cheongan,
            'jiji': hour_jiji,
            'cheongan_index': CHEONGAN.index(hour_cheongan),
            'jiji_index': hour_jiji_index
        }
    
    # 헬퍼 메소드들
    def _validate_input_date(self, year: int, month: int, day: int, hour: int, minute: int) -> bool:
        """입력 날짜 유효성 검증"""
        try:
            if not (1900 <= year <= 2100):
                return False
            if not (1 <= month <= 12):
                return False
            if not (1 <= day <= 31):
                return False
            if not (0 <= hour <= 23):
                return False
            if not (0 <= minute <= 59):
                return False
            return True
        except:
            return False
    
    def _check_basic_usage_limit(self) -> bool:
        """기본 사용량 제한 체크"""
        return self.usage_count < (KasiApiConfig.USAGE_LIMIT * 0.8)  # 80% 제한
    
    def _build_basic_gapja_cache(self) -> Dict:
        """기본 갑자 캐시 구축"""
        cache = {}
        for key, base_value in GAPJA_REFERENCE_TABLE.items():
            cache[key] = base_value
        return cache
    
    # 폴백 및 근사 계산 메소드들 (간소화)
    def _fallback_calculation(self, year: int, month: int, day: int, 
                            hour: int, minute: int, is_lunar: bool) -> Optional[Dict]:
        """폴백 사주 계산"""
        try:
            birth_datetime = datetime(year, month, day, hour, minute)
            true_solar_time = self._calculate_pure_solar_time(birth_datetime)
            
            pillars = {
                'year': self._calculate_year_pillar(year, true_solar_time),
                'month': self._calculate_month_pillar(year, month, true_solar_time),
                'day': self._calculate_day_pillar_fallback(true_solar_time),
                'hour': self._calculate_hour_pillar(true_solar_time)
            }
            
            ilgan = pillars['day']['cheongan']
            
            return SajuResult(pillars, ilgan, {'input_type': '폴백계산'}).to_dict()
            
        except Exception as e:
            logger.error(f"폴백 계산 실패: {e}")
            return None