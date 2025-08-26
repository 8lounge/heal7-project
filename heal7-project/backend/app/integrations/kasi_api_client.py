
import os
import requests
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
from typing import Dict, Tuple, Optional
import logging
import re

logger = logging.getLogger(__name__)

# KASI API 응답 파싱을 위한 한글-한자 매핑
KOREAN_TO_CHINESE_GANJEE = {
    # 천간
    '갑': '甲', '을': '乙', '병': '丙', '정': '丁', '무': '戊',
    '기': '己', '경': '庚', '신': '辛', '임': '壬', '계': '癸',
    # 지지
    '자': '子', '축': '丑', '인': '寅', '묘': '卯', '진': '辰', '사': '巳',
    '오': '午', '미': '未', '신': '申', '유': '酉', '술': '戌', '해': '亥'
}

class KasiApiClient:
    """KASI API 연동 클라이언트"""
    
    def __init__(self):
        self.kasi_service_key = os.getenv('KASI_SERVICE_KEY',
            'AR2zMFQPIPBFak+MdXzznzVmtsICp7dwd3eo9XCUP62kXpr4GrX3eqi28erzZhXfIemuo6C5AK58eLMKBw8VGQ==')
        self.kasi_lunar_api = "http://apis.data.go.kr/B090041/openapi/service/LrsrCldInfoService"
        
        self.daily_usage_limit = 300  # 일일 한계
        self.monthly_usage_limit = 9500  # 월 한계 (여유분 500건)
        self.current_usage = 0
        self.usage_reset_date = datetime.now().date()
        
    def _check_usage_limit(self) -> bool:
        current_date = datetime.now().date()
        if current_date != self.usage_reset_date:
            self.current_usage = 0
            self.usage_reset_date = current_date
        
        days_in_month = current_date.day
        estimated_monthly_usage = self.current_usage * (30 / days_in_month) if days_in_month > 0 else 0
        
        if estimated_monthly_usage > self.monthly_usage_limit:
            logger.warning(f"⚠️ 월간 KASI API 사용량 한계 예상: {estimated_monthly_usage:.0f}/{self.monthly_usage_limit}")
            return False
            
        if self.current_usage >= self.daily_usage_limit:
            logger.warning(f"⚠️ 일일 KASI API 사용량 한계: {self.current_usage}/{self.daily_usage_limit}")
            return False
            
        return True

    def lunar_to_solar(self, lun_year: int, lun_month: int, lun_day: int, is_leap: bool) -> Optional[Dict]:
        if not self._check_usage_limit():
            logger.warning("KASI API 사용량 한계 도달 - 음력->양력 변환 불가")
            return None
        self.current_usage += 1
        
        try:
            url = f"{self.kasi_lunar_api}/getSolCalInfo"
            params = {
                'ServiceKey': self.kasi_service_key,
                'lunYear': str(lun_year),
                'lunMonth': f"{lun_month:02d}",
                'lunDay': f"{lun_day:02d}",
                'leapMonth': '윤' if is_leap else '평',
                'numOfRows': '1',
                'pageNo': '1'
            }
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            root = ET.fromstring(response.content)
            
            result_code = root.find('.//resultCode')
            if result_code is not None and result_code.text == '00':
                item = root.find('.//item')
                if item is not None:
                    sol_year = item.find('solYear')
                    sol_month = item.find('solMonth')
                    sol_day = item.find('solDay')
                    if all([sol_year is not None, sol_month is not None, sol_day is not None]):
                        return {
                            'year': int(sol_year.text),
                            'month': int(sol_month.text),
                            'day': int(sol_day.text)
                        }
        except Exception as e:
            logger.error(f"KASI 음력->양력 변환 API 오류: {e}")
        return None
        
    def solar_to_lunar(self, sol_year: int, sol_month: int, sol_day: int) -> Optional[Dict]:
        if not self._check_usage_limit():
            logger.warning("KASI API 사용량 한계 도달 - 양력->음력 변환 불가")
            return None
        self.current_usage += 1
        
        try:
            url = f"{self.kasi_lunar_api}/getLunCalInfo"
            params = {
                'ServiceKey': self.kasi_service_key,
                'solYear': str(sol_year),
                'solMonth': f"{sol_month:02d}",
                'solDay': f"{sol_day:02d}",
                'numOfRows': '1',
                'pageNo': '1'
            }
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            root = ET.fromstring(response.content)
            
            result_code = root.find('.//resultCode')
            if result_code is not None and result_code.text == '00':
                item = root.find('.//item')
                if item is not None:
                    lun_year = item.find('lunYear')
                    lun_month = item.find('lunMonth')
                    lun_day = item.find('lunDay')
                    leap_month = item.find('leapMonth')
                    if all([lun_year is not None, lun_month is not None, lun_day is not None]):
                        return {
                            'year': int(lun_year.text),
                            'month': int(lun_month.text),
                            'day': int(lun_day.text),
                            'is_leap': leap_month is not None and leap_month.text == '윤'
                        }
        except Exception as e:
            logger.error(f"KASI 양력->음력 변환 API 오류: {e}")
        return None
        
    def get_day_pillar(self, date: datetime) -> Optional[str]:
        if not self._check_usage_limit():
            logger.warning("KASI API 사용량 한계 도달 - 일진 조회 불가")
            return None
        self.current_usage += 1
        
        try:
            url = f"{self.kasi_lunar_api}/getLunCalInfo"
            params = {
                'ServiceKey': self.kasi_service_key,
                'solYear': str(date.year),
                'solMonth': f"{date.month:02d}",
                'solDay': f"{date.day:02d}",
                'numOfRows': '1',
                'pageNo': '1'
            }
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            root = ET.fromstring(response.content)
            
            result_code = root.find('.//resultCode')
            if result_code is not None and result_code.text == '00':
                item = root.find('.//item')
                if item is not None:
                    lun_iljin = item.find('lunIljin')
                    if lun_iljin is not None and lun_iljin.text:
                        return self._parse_kasi_ganjee(lun_iljin.text)
        except Exception as e:
            logger.warning(f"KASI 일진 조회 실패: {e}")
        return None
        
    def _parse_kasi_ganjee(self, kasi_text: str) -> str:
        if not kasi_text:
            return ""
        chinese_match = re.search(r'\(([^)]+)\)', kasi_text)
        if chinese_match:
            chinese_part = chinese_match.group(1)
            if all(c in '甲乙丙丁戊己庚辛壬癸子丑寅卯辰巳午未申酉戌亥' for c in chinese_part):
                return chinese_part
        result = ""
        for char in re.sub(r'\([^)]*\)', '', kasi_text).strip():
            result += KOREAN_TO_CHINESE_GANJEE.get(char, char)
        return result if len(result) == 2 else ""
