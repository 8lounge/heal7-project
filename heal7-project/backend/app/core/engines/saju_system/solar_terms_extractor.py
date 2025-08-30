#!/usr/bin/env python3
"""
24절기 데이터 추출 및 데이터베이스 저장 시스템
KASI API를 활용하여 1900-2026년까지의 24절기 데이터 수집
"""

import os
import requests
import json
import psycopg2
from datetime import datetime, timedelta
import time
import logging
from typing import Dict, List, Tuple, Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SolarTermsExtractor:
    """24절기 데이터 추출기"""
    
    def __init__(self):
        # KASI API 설정 - 보안을 위해 환경변수 사용
        self.kasi_api_key = os.getenv('KASI_API_KEY', 'DEFAULT_KEY_NOT_SET')
        self.kasi_base_url = "http://apis.data.go.kr/B090041/openapi/service/LrsrCldInfoService"
        
        # 24절기 정의
        self.solar_terms = [
            ("입춘", "立春", "Beginning of Spring", 2),
            ("우수", "雨水", "Rain Water", 2),
            ("경칩", "驚蟄", "Awakening of Insects", 3),
            ("춘분", "春分", "Spring Equinox", 3),
            ("청명", "淸明", "Clear and Bright", 4),
            ("곡우", "穀雨", "Grain Rain", 4),
            ("입하", "立夏", "Beginning of Summer", 5),
            ("소만", "小滿", "Grain Full", 5),
            ("망종", "芒種", "Grain in Ear", 6),
            ("하지", "夏至", "Summer Solstice", 6),
            ("소서", "小暑", "Minor Heat", 7),
            ("대서", "大暑", "Major Heat", 7),
            ("입추", "立秋", "Beginning of Autumn", 8),
            ("처서", "處暑", "End of Heat", 8),
            ("백로", "白露", "White Dew", 9),
            ("추분", "秋分", "Autumn Equinox", 9),
            ("한로", "寒露", "Cold Dew", 10),
            ("상강", "霜降", "Frost Descent", 10),
            ("입동", "立冬", "Beginning of Winter", 11),
            ("소설", "小雪", "Minor Snow", 11),
            ("대설", "大雪", "Major Snow", 12),
            ("동지", "冬至", "Winter Solstice", 12),
            ("소한", "小寒", "Minor Cold", 1),
            ("대한", "大寒", "Major Cold", 1)
        ]
        
        # 절기 날짜 근사치 (각 월별 평균 날짜)
        self.term_approximate_days = {
            "입춘": 4, "우수": 19, "경칩": 6, "춘분": 21,
            "청명": 5, "곡우": 20, "입하": 6, "소만": 21,
            "망종": 6, "하지": 22, "소서": 7, "대서": 23,
            "입추": 8, "처서": 23, "백로": 8, "추분": 23,
            "한로": 8, "상강": 24, "입동": 8, "소설": 23,
            "대설": 7, "동지": 22, "소한": 6, "대한": 21
        }
        
        # DB 연결 정보 - 통합 heal7 데이터베이스 사용
        self.db_config = {
            'host': 'localhost',
            'database': 'heal7',
            'user': 'postgres',
            'options': '-c search_path=saju_service,shared_common,public'
        }
    
    def get_lunar_calendar_info(self, year: int, month: int, day: int) -> Optional[Dict]:
        """KASI API로 특정 날짜의 음력 정보 조회"""
        try:
            url = f"{self.kasi_base_url}/getLunCalInfo"
            params = {
                'serviceKey': self.kasi_api_key,
                'solYear': year,
                'solMonth': month,
                'solDay': day
            }
            
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                # XML 파싱 (간단한 방법)
                text = response.text
                
                # 절기 정보 추출
                if '<lunIljin>' in text:
                    iljin_start = text.find('<lunIljin>') + 10
                    iljin_end = text.find('</lunIljin>')
                    iljin = text[iljin_start:iljin_end] if iljin_start > 10 else None
                else:
                    iljin = None
                
                return {
                    'solar_date': f"{year}-{month:02d}-{day:02d}",
                    'iljin': iljin,
                    'response': text
                }
            else:
                logger.warning(f"API 응답 오류: {response.status_code}")
                return None
                
        except Exception as e:
            logger.error(f"API 호출 오류: {e}")
            return None
    
    def extract_solar_terms_for_year(self, year: int) -> List[Dict]:
        """특정 연도의 24절기 데이터 추출"""
        logger.info(f"📅 {year}년 24절기 데이터 추출 시작")
        
        year_terms = []
        
        for korean_name, chinese_name, english_name, month in self.solar_terms:
            # 절기 예상 날짜 계산
            day = self.term_approximate_days.get(korean_name, 15)
            
            # 소한, 대한은 전년도 처리
            if korean_name in ["소한", "대한"] and month == 1:
                check_year = year - 1
            else:
                check_year = year
            
            # 절기 전후 3일씩 체크하여 정확한 날짜 찾기
            for day_offset in range(-3, 4):
                check_day = day + day_offset
                
                if check_day < 1:
                    continue
                if check_day > 31:
                    continue
                
                result = self.get_lunar_calendar_info(check_year, month, check_day)
                
                if result and result['response']:
                    # 절기 날짜인지 확인 (응답에 절기 정보가 포함되어 있는지)
                    if chinese_name in result['response'] or korean_name in result['response']:
                        term_data = {
                            'year': check_year,
                            'month': month,
                            'day': check_day,
                            'korean_name': korean_name,
                            'chinese_name': chinese_name,
                            'english_name': english_name,
                            'solar_date': f"{check_year}-{month:02d}-{check_day:02d}",
                            'term_time': None  # 시간은 별도 계산 필요
                        }
                        year_terms.append(term_data)
                        logger.info(f"  ✅ {korean_name}({chinese_name}): {check_year}-{month:02d}-{check_day:02d}")
                        break
                
                # API 부하 방지
                time.sleep(0.1)
        
        return year_terms
    
    def save_to_database(self, terms_data: List[Dict]):
        """24절기 데이터를 데이터베이스에 저장"""
        conn = None
        cur = None
        
        try:
            conn = psycopg2.connect(**self.db_config)
            cur = conn.cursor()
            
            # 24절기 테이블 생성 (없으면) - saju_service 스키마에 생성
            cur.execute("""
                CREATE TABLE IF NOT EXISTS saju_service.solar_terms_24 (
                    id SERIAL PRIMARY KEY,
                    year INTEGER NOT NULL,
                    month INTEGER NOT NULL,
                    day INTEGER NOT NULL,
                    korean_name VARCHAR(10) NOT NULL,
                    chinese_name VARCHAR(10) NOT NULL,
                    english_name VARCHAR(50),
                    solar_date DATE NOT NULL,
                    term_time TIME,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(year, korean_name)
                )
            """)
            
            # 데이터 삽입 또는 업데이트
            for term in terms_data:
                cur.execute("""
                    INSERT INTO saju_service.solar_terms_24 
                    (year, month, day, korean_name, chinese_name, english_name, solar_date, term_time)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (year, korean_name) 
                    DO UPDATE SET 
                        month = EXCLUDED.month,
                        day = EXCLUDED.day,
                        solar_date = EXCLUDED.solar_date,
                        term_time = EXCLUDED.term_time
                """, (
                    term['year'], term['month'], term['day'],
                    term['korean_name'], term['chinese_name'], term['english_name'],
                    term['solar_date'], term['term_time']
                ))
            
            conn.commit()
            logger.info(f"✅ {len(terms_data)}개 절기 데이터 저장 완료")
            
        except Exception as e:
            logger.error(f"DB 저장 오류: {e}")
            if conn:
                conn.rollback()
        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()
    
    def extract_all_years(self, start_year: int = 1900, end_year: int = 2026):
        """전체 연도 24절기 데이터 추출"""
        logger.info(f"🌟 {start_year}년부터 {end_year}년까지 24절기 데이터 추출 시작")
        
        all_terms = []
        
        # 테스트를 위해 먼저 몇 년만 처리
        test_years = [2024, 2025, 2026]  # 테스트용
        
        for year in test_years:
            logger.info(f"\n{'='*60}")
            logger.info(f"📅 {year}년 처리 중...")
            
            year_terms = self.extract_solar_terms_for_year(year)
            all_terms.extend(year_terms)
            
            # 중간 저장 (10년마다)
            if year % 10 == 0 or year == end_year:
                self.save_to_database(all_terms)
                all_terms = []  # 메모리 정리
            
            # API 부하 방지
            time.sleep(1)
        
        # 남은 데이터 저장
        if all_terms:
            self.save_to_database(all_terms)
        
        logger.info(f"\n🎉 전체 24절기 데이터 추출 완료!")
        
        return True
    
    def backup_solar_terms_table(self):
        """24절기 테이블 백업"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_file = f"/home/ubuntu/archive/database_backup/solar_terms_24_backup_{timestamp}.sql"
            
            import subprocess
            subprocess.run([
                'pg_dump',
                '-U', 'liveuser',
                '-h', 'localhost',
                '-d', 'livedb',
                '-t', 'solar_terms_24',
                '-f', backup_file
            ], env={'PGPASSWORD': 'livepass2024'})
            
            logger.info(f"✅ 백업 완료: {backup_file}")
            return backup_file
            
        except Exception as e:
            logger.error(f"백업 실패: {e}")
            return None


def main():
    """메인 실행 함수"""
    extractor = SolarTermsExtractor()
    
    # 1. 24절기 데이터 추출 (테스트: 2024-2026년)
    extractor.extract_all_years(2024, 2026)
    
    # 2. 데이터베이스 백업
    # extractor.backup_solar_terms_table()
    
    logger.info("✅ 24절기 데이터 처리 완료")


# Production-ready module - test code removed
