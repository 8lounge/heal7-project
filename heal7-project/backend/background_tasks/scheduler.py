
import requests
import json
import sqlite3
import psycopg2
import xml.etree.ElementTree as ET
import time
import os
import re
import subprocess
from datetime import datetime, date, timedelta
from typing import Dict, List, Tuple, Optional, Any

# --- Constants from various collectors ---
# KASI API 24절기 수집기 (kasi_api_collector.py)
KASI_SOLAR_BASE_URL = "https://apis.data.go.kr/B090041/openapi/service/SpcdeInfoService"
KASI_DECODED_KEY = "AR2zMFQPIPBFak+MdXzznzVmtsICp7dwd3eo9XCUP62kXpr4GrX3eqi28erzZhXfIemuo6C5AK58eLMKBw8VGQ=="
SOLAR_TERMS_NAMES = {
    "입춘", "우수", "경칩", "춘분", "청명", "곡우",
    "입하", "소만", "망종", "하지", "소서", "대서", 
    "입추", "처서", "백로", "추분", "한로", "상강",
    "입동", "소설", "대설", "동지", "소한", "대한"
}

# KASI 음양력 정보 API 수집기 (kasi_lunar_calendar_collector.py)
KASI_LUNAR_BASE_URL = "http://apis.data.go.kr/B090041/openapi/service/LrsrCldInfoService"
KASI_LUNAR_ENDPOINT = "getLunCalInfo"
KASI_LUNAR_SERVICE_KEY = "AR2zMFQPIPBFak+MdXzznzVmtsICp7dwd3eo9XCUP62kXpr4GrX3eqi28erzZhXfIemuo6C5AK58eLMKBw8VGQ=="

# 24절기 데이터 로더 (solar_terms_data_loader.py)
POSTGRES_DB_CONFIG = {
    'host': 'localhost',
    'database': 'livedb',
    'user': 'liveuser',
    'password': 'livepass2024'
}
SOLAR_TERMS_TEMPLATE = [
    ("소한", "小寒", "Minor Cold", 1, 5),
    ("대한", "大寒", "Major Cold", 1, 20),
    ("입춘", "立春", "Beginning of Spring", 2, 4),
    ("우수", "雨水", "Rain Water", 2, 19),
    ("경칩", "驚蟄", "Awakening of Insects", 3, 6),
    ("춘분", "春分", "Spring Equinox", 3, 21),
    ("청명", "淸明", "Clear and Bright", 4, 5),
    ("곡우", "穀雨", "Grain Rain", 4, 20),
    ("입하", "立夏", "Beginning of Summer", 5, 6),
    ("소만", "小滿", "Grain Full", 5, 21),
    ("망종", "芒種", "Grain in Ear", 6, 6),
    ("하지", "夏至", "Summer Solstice", 6, 21),
    ("소서", "小暑", "Minor Heat", 7, 7),
    ("대서", "大暑", "Major Heat", 7, 23),
    ("입추", "立秋", "Beginning of Autumn", 8, 8),
    ("처서", "處暑", "End of Heat", 8, 23),
    ("백로", "白露", "White Dew", 9, 8),
    ("추분", "秋分", "Autumn Equinox", 9, 23),
    ("한로", "寒露", "Cold Dew", 10, 8),
    ("상강", "霜降", "Frost Descent", 10, 23),
    ("입동", "立冬", "Beginning of Winter", 11, 7),
    ("소설", "小雪", "Minor Snow", 11, 22),
    ("대설", "大雪", "Major Snow", 12, 7),
    ("동지", "冬至", "Winter Solstice", 12, 22)
]
EXACT_DATES_2024_2026 = {
    2024: [
        ("소한", 1, 6), ("대한", 1, 20), ("입춘", 2, 4), ("우수", 2, 19),
        ("경칩", 3, 5), ("춘분", 3, 20), ("청명", 4, 4), ("곡우", 4, 19),
        ("입하", 5, 5), ("소만", 5, 20), ("망종", 6, 5), ("하지", 6, 21),
        ("소서", 7, 6), ("대서", 7, 22), ("입추", 8, 7), ("처서", 8, 22),
        ("백로", 9, 7), ("추분", 9, 22), ("한로", 10, 8), ("상강", 10, 23),
        ("입동", 11, 7), ("소설", 11, 22), ("대설", 12, 6), ("동지", 12, 21)
    ],
    2025: [
        ("소한", 1, 5), ("대한", 1, 20), ("입춘", 2, 3), ("우수", 2, 18),
        ("경칩", 3, 5), ("춘분", 3, 20), ("청명", 4, 4), ("곡우", 4, 20),
        ("입하", 5, 5), ("소만", 5, 20), ("망종", 6, 5), ("하지", 6, 21),
        ("소서", 7, 7), ("대서", 7, 22), ("입추", 8, 7), ("처서", 8, 23),
        ("백로", 9, 7), ("추분", 9, 23), ("한로", 10, 8), ("상강", 10, 23),
        ("입동", 11, 7), ("소설", 11, 22), ("대설", 12, 7), ("동지", 12, 21)
    ],
    2026: [
        ("소한", 1, 5), ("대한", 1, 20), ("입춘", 2, 4), ("우수", 2, 18),
        ("경칩", 3, 5), ("춘분", 3, 20), ("청명", 4, 4), ("곡우", 4, 20),
        ("입하", 5, 5), ("소만", 5, 21), ("망종", 6, 5), ("하지", 6, 21),
        ("소서", 7, 7), ("대서", 7, 22), ("입추", 8, 7), ("처서", 8, 23),
        ("백로", 9, 7), ("추분", 9, 23), ("한로", 10, 8), ("상강", 10, 23),
        ("입동", 11, 7), ("소설", 11, 22), ("대설", 12, 7), ("동지", 12, 21)
    ]
}

class BackgroundTaskScheduler:
    """다양한 백그라운드 작업 및 자동 수집을 관리하는 스케줄러"""

    def __init__(self):
        self.kasi_lunar_db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "database", "kasi", "kasi_lunar_calendar_official.db")
        self.kasi_solar_db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "database", "kasi", "accurate_kasi_solar_terms.db")

    # --- KASI Solar Terms Collection (from kasi_api_collector.py and solar_terms_extractor.py) ---
    def _get_sqlite_connection(self, db_path):
        return sqlite3.connect(db_path)

    def _get_postgres_connection(self):
        return psycopg2.connect(**POSTGRES_DB_CONFIG)

    def _get_xml_text(self, item, tag_name):
        element = item.find(tag_name)
        return element.text if element is not None else None

    def run_kasi_solar_terms_collection(self, start_year: int = 1901, end_year: int = 2026):
        print(f"🚀 KASI API로부터 {start_year}-{end_year}년 24절기 데이터 수집 시작")
        db_path = self.create_accurate_solar_terms_database()
        total_collected = 0
        for year in range(start_year, end_year + 1):
            year_data = self._collect_solar_terms_for_year(year)
            if year_data:
                saved = self._save_solar_terms_batch_data(year_data, db_path)
                total_collected += saved
                print(f"✅ {year}년: {saved}개 절기 저장 완료")
        print(f"🎉 전체 수집 완료! 총 {total_collected}개 절기.")

    def _collect_solar_terms_for_year(self, year: int) -> List[Dict]:
        year_data = []
        for month in range(1, 13):
            url = f"{KASI_SOLAR_BASE_URL}/getRestDeInfo"
            params = {
                'serviceKey': KASI_DECODED_KEY,
                'solYear': str(year),
                'solMonth': f'{month:02d}',
                'numOfRows': '100',
                '_type': 'xml'
            }
            try:
                response = requests.get(url, params=params, timeout=30)
                if response.status_code == 200:
                    root = ET.fromstring(response.text)
                    items = root.findall('.//item')
                    for item in items:
                        date_name = self._get_xml_text(item, 'dateName')
                        if date_name in SOLAR_TERMS_NAMES:
                            year_data.append({
                                'year': year, 'month': month, 'date_name': date_name,
                                'locdate': self._get_xml_text(item, 'locdate'),
                                'remarks': self._get_xml_text(item, 'remarks'),
                                'seq': self._get_xml_text(item, 'seq'),
                                'collected_at': datetime.now().isoformat(),
                                'source': 'KASI_API'
                            })
            except Exception as e:
                print(f"  ❌ {month}월 오류: {e}")
            time.sleep(2.5) # API 부하 방지
        return year_data

    def create_accurate_solar_terms_database(self):
        os.makedirs(os.path.dirname(self.kasi_solar_db_path), exist_ok=True)
        conn = self._get_sqlite_connection(self.kasi_solar_db_path)
        cursor = conn.cursor()
        cursor.execute('DROP TABLE IF EXISTS solar_terms')
        cursor.execute('''
        CREATE TABLE solar_terms (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            year INTEGER NOT NULL,
            month INTEGER NOT NULL,
            date_name TEXT NOT NULL,
            locdate TEXT NOT NULL,
            remarks TEXT,
            seq TEXT,
            collected_at TEXT NOT NULL,
            source TEXT NOT NULL,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(year, date_name)
        )
        ''')
        conn.commit()
        conn.close()
        print(f"✅ 새로운 정확한 절기 데이터베이스 생성: {self.kasi_solar_db_path}")
        return self.kasi_solar_db_path

    def _save_solar_terms_batch_data(self, data_batch: List[Dict], db_path: str) -> int:
        conn = self._get_sqlite_connection(db_path)
        cursor = conn.cursor()
        saved_count = 0
        for item in data_batch:
            try:
                cursor.execute('''
                INSERT OR REPLACE INTO solar_terms 
                (year, month, date_name, locdate, remarks, seq, collected_at, source)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    item['year'], item['month'], item['date_name'],
                    item['locdate'], item['remarks'], item['seq'],
                    item['collected_at'], item['source']
                ))
                saved_count += 1
            except Exception as e:
                print(f"❌ 저장 오류: {e}")
        conn.commit()
        conn.close()
        return saved_count

    def verify_solar_terms_database(self, db_path: str):
        print(f"\n🔍 절기 데이터베이스 검증 중...")
        conn = self._get_sqlite_connection(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM solar_terms")
        total_records = cursor.fetchone()[0]
        print(f"✅ 검증 결과: 총 레코드: {total_records:,}개")
        conn.close()

    # --- KASI Lunar Calendar Collection (from kasi_lunar_calendar_collector.py) ---
    def run_kasi_lunar_collection(self, start_year: int, end_year: int):
        print(f"🌙 KASI 음력 데이터 수집 시작: {start_year}-{end_year}")
        self.setup_lunar_calendar_database()
        for year in range(start_year, end_year + 1):
            self._collect_lunar_data_for_year(year)
        print("🎉 음력 데이터 수집 완료!")

    def setup_lunar_calendar_database(self):
        os.makedirs(os.path.dirname(self.kasi_lunar_db_path), exist_ok=True)
        conn = self._get_sqlite_connection(self.kasi_lunar_db_path)
        cursor = conn.cursor()
        cursor.execute('DROP TABLE IF EXISTS kasi_lunar_calendar')
        cursor.execute('''
        CREATE TABLE kasi_lunar_calendar (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            solar_date TEXT NOT NULL UNIQUE,
            solar_year INTEGER NOT NULL,
            solar_month INTEGER NOT NULL,
            solar_day INTEGER NOT NULL,
            lunar_year INTEGER,
            lunar_month INTEGER,
            lunar_day INTEGER,
            solar_leapyear TEXT,
            lunar_leapmonth TEXT,
            solar_week TEXT,
            lunar_wolgeon TEXT,
            lunar_nday INTEGER,
            raw_response TEXT,
            collected_at TEXT NOT NULL,
            UNIQUE(solar_date)
        )
        ''')
        conn.commit()
        conn.close()
        print(f"✅ 음력 데이터베이스 생성: {self.kasi_lunar_db_path}")

    def _collect_lunar_data_for_year(self, year: int):
        print(f"📅 {year}년 KASI 음력 데이터 수집")
        start_date = date(year, 1, 1)
        end_date = date(year, 12, 31)
        current_date = start_date
        while current_date <= end_date:
            lunar_info = self._collect_lunar_info_for_date_api(current_date)
            if lunar_info:
                self._save_lunar_info_to_db(lunar_info)
            current_date += timedelta(days=1)
            time.sleep(0.5) # API 부하 방지

    def _collect_lunar_info_for_date_api(self, target_date: date) -> Optional[Dict]:
        url = f"{KASI_LUNAR_BASE_URL}/{KASI_LUNAR_ENDPOINT}"
        params = {
            'serviceKey': KASI_LUNAR_SERVICE_KEY,
            'solYear': f'{target_date.year:04d}',
            'solMonth': f'{target_date.month:02d}',
            'solDay': f'{target_date.day:02d}',
            '_type': 'xml'
        }
        try:
            response = requests.get(url, params=params, timeout=15)
            if response.status_code == 200:
                root = ET.fromstring(response.text)
                item = root.find('.//item')
                if item:
                    return {
                        'solar_date': target_date.strftime('%Y-%m-%d'),
                        'solar_year': target_date.year,
                        'solar_month': target_date.month,
                        'solar_day': target_date.day,
                        'lunar_year': self._get_xml_text(item, 'lunYear'),
                        'lunar_month': self._get_xml_text(item, 'lunMonth'),
                        'lunar_day': self._get_xml_text(item, 'lunDay'),
                        'solar_leapyear': self._get_xml_text(item, 'solLeapyear'),
                        'lunar_leapmonth': self._get_xml_text(item, 'lunLeapmonth'),
                        'solar_week': self._get_xml_text(item, 'solWeek'),
                        'lunar_wolgeon': self._get_xml_text(item, 'lunWolgeon'),
                        'lunar_nday': self._get_xml_text(item, 'lunNday'),
                        'raw_response': response.text,
                        'collected_at': datetime.now().isoformat()
                    }
        except Exception as e:
            print(f"❌ {target_date}: 수집 오류 - {e}")
        return None

    def _save_lunar_info_to_db(self, lunar_info: Dict) -> bool:
        if not lunar_info: return False
        conn = self._get_sqlite_connection(self.kasi_lunar_db_path)
        cursor = conn.cursor()
        try:
            cursor.execute('''
            INSERT OR REPLACE INTO kasi_lunar_calendar
            (solar_date, solar_year, solar_month, solar_day,
             lunar_year, lunar_month, lunar_day, 
             solar_leapyear, lunar_leapmonth, solar_week, 
             lunar_wolgeon, lunar_nday, raw_response, collected_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                lunar_info['solar_date'], lunar_info['solar_year'], 
                lunar_info['solar_month'], lunar_info['solar_day'],
                lunar_info['lunar_year'], lunar_info['lunar_month'], 
                lunar_info['lunar_day'], lunar_info['solar_leapyear'],
                lunar_info['lunar_leapmonth'], lunar_info['solar_week'],
                lunar_info['lunar_wolgeon'], lunar_info['lunar_nday'],
                lunar_info['raw_response'], lunar_info['collected_at']
            ))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"❌ 저장 오류: {e}")
            return False

    # --- Solar Terms Data Loading (from solar_terms_data_loader.py) ---
    def run_solar_terms_data_load(self, start_year: int = 1900, end_year: int = 2026):
        print(f"📥 {start_year}-{end_year}년 24절기 데이터 로드 시작")
        self.create_solar_terms_postgres_table()
        total_count = 0
        for year in range(start_year, end_year + 1):
            if year in EXACT_DATES_2024_2026:
                solar_terms = EXACT_DATES_2024_2026[year]
            else:
                solar_terms = SOLAR_TERMS_TEMPLATE # Approximate data
            
            for idx, (korean_name, chinese_name, english_name, month, day) in enumerate(solar_terms, 1):
                if korean_name in ["소한", "대한"] and month == 1 and year not in EXACT_DATES_2024_2026: # Adjust for previous year for these terms
                    check_year = year - 1
                else:
                    check_year = year
                
                # 윤년 처리 (for approximate data)
                if month == 2 and day == 29 and not self._is_leap_year(check_year):
                    day = 28
                
                solar_date = f"{check_year}-{month:02d}-{day:02d}"
                
                conn = self._get_postgres_connection()
                cursor = conn.cursor()
                try:
                    cursor.execute("""
                        INSERT INTO solar_terms_24 
                        (year, month, day, korean_name, chinese_name, english_name, 
                         solar_date, term_order, season)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                        ON CONFLICT (year, korean_name) 
                        DO UPDATE SET 
                            month = EXCLUDED.month,
                            day = EXCLUDED.day,
                            solar_date = EXCLUDED.solar_date,
                            term_order = EXCLUDED.term_order,
                            season = EXCLUDED.season
                    """, (
                        check_year, month, day, korean_name, chinese_name, english_name,
                        solar_date, idx, self._get_season_from_month(month)
                    ))
                    total_count += 1
                    conn.commit()
                except Exception as e:
                    print(f"❌ 데이터 로드 오류: {e}")
                finally:
                    cursor.close()
                    conn.close()
        print(f"✅ 총 {total_count}개 24절기 데이터 로드 완료.")

    def create_solar_terms_postgres_table(self):
        conn = self._get_postgres_connection()
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS solar_terms_24 (
                id SERIAL PRIMARY KEY,
                year INTEGER NOT NULL,
                month INTEGER NOT NULL,
                day INTEGER NOT NULL,
                korean_name VARCHAR(10) NOT NULL,
                chinese_name VARCHAR(10) NOT NULL,
                english_name VARCHAR(50),
                solar_date DATE NOT NULL,
                lunar_month INTEGER,
                lunar_day INTEGER,
                term_time TIME,
                term_order INTEGER,
                season VARCHAR(10),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(year, korean_name)
            )
        """)
        conn.commit()
        conn.close()
        print("✅ 24절기 PostgreSQL 테이블 생성 완료")

    def _is_leap_year(self, year: int) -> bool:
        return (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)

    def _get_season_from_month(self, month: int) -> str:
        if month in [3, 4, 5]: return "봄"
        elif month in [6, 7, 8]: return "여름"
        elif month in [9, 10, 11]: return "가을"
        else: return "겨울"

    def backup_solar_terms_postgres_table(self):
        print("\n💾 PostgreSQL 24절기 테이블 백업...")
        backup_dir = "/home/ubuntu/archive/database_backup"
        os.makedirs(backup_dir, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = f"{backup_dir}/solar_terms_24_{timestamp}.sql"
        try:
            subprocess.run([
                'pg_dump',
                '-U', POSTGRES_DB_CONFIG['user'],
                '-h', POSTGRES_DB_CONFIG['host'],
                '-d', POSTGRES_DB_CONFIG['database'],
                '-t', 'solar_terms_24',
                '--data-only',
                '-f', backup_file
            ], env={'PGPASSWORD': POSTGRES_DB_CONFIG['password']}, check=True)
            print(f"✅ 백업 성공: {backup_file}")
        except subprocess.CalledProcessError as e:
            print(f"❌ 백업 실패: {e.stderr.decode()}")
        except Exception as e:
            print(f"❌ 백업 오류: {e}")

    # --- Solar Terms Extractor (from solar_terms_extractor.py) ---
    def run_solar_terms_extraction(self, start_year: int = 1900, end_year: int = 2026):
        print(f"🌟 {start_year}년부터 {end_year}년까지 24절기 데이터 추출 시작")
        all_terms = []
        for year in range(start_year, end_year + 1):
            year_terms = self._extract_solar_terms_for_year_api(year)
            all_terms.extend(year_terms)
            if year % 10 == 0 or year == end_year:
                self._save_extracted_solar_terms_to_db(all_terms)
                all_terms = []
            time.sleep(1) # API 부하 방지
        if all_terms:
            self._save_extracted_solar_terms_to_db(all_terms)
        print(f"\n🎉 전체 24절기 데이터 추출 완료!")

    def _extract_solar_terms_for_year_api(self, year: int) -> List[Dict]:
        year_terms = []
        for korean_name, chinese_name, english_name, month in SOLAR_TERMS_TEMPLATE:
            day = SOLAR_TERMS_TEMPLATE[SOLAR_TERMS_TEMPLATE.index((korean_name, chinese_name, english_name, month))][4] # Get approximate day
            for day_offset in range(-3, 4):
                check_day = day + day_offset
                if check_day < 1 or check_day > 31: continue
                result = self._get_lunar_calendar_info_api(year, month, check_day)
                if result and result['response']:
                    if chinese_name in result['response'] or korean_name in result['response']:
                        year_terms.append({
                            'year': year, 'month': month, 'day': check_day,
                            'korean_name': korean_name, 'chinese_name': chinese_name, 'english_name': english_name,
                            'solar_date': f"{year}-{month:02d}-{check_day:02d}",
                            'term_time': None
                        })
                        break
                time.sleep(0.1) # API 부하 방지
        return year_terms

    def _get_lunar_calendar_info_api(self, year: int, month: int, day: int) -> Optional[Dict]:
        url = f"{KASI_LUNAR_BASE_URL}/{KASI_LUNAR_ENDPOINT}"
        params = {
            'serviceKey': KASI_LUNAR_SERVICE_KEY,
            'solYear': year,
            'solMonth': month,
            'solDay': day
        }
        try:
            response = requests.get(url, params=params, timeout=10)
            if response.status_code == 200: return {'response': response.text}
        except Exception as e: print(f"API 호출 오류: {e}")
        return None

    def _save_extracted_solar_terms_to_db(self, terms_data: List[Dict]):
        conn = self._get_postgres_connection()
        cursor = conn.cursor()
        for term in terms_data:
            try:
                cursor.execute("""
                    INSERT INTO solar_terms_24 
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
            except Exception as e: print(f"DB 저장 오류: {e}")
        conn.commit()
        conn.close()


# --- Main execution example (for testing purposes) ---
# if __name__ == "__main__":
#     scheduler = BackgroundTaskScheduler()
#     # Example: Run KASI Solar Terms Collection
#     # scheduler.run_kasi_solar_terms_collection(2024, 2024)
#     # Example: Run KASI Lunar Calendar Collection
#     # scheduler.run_kasi_lunar_collection(2024, 2024)
#     # Example: Run Solar Terms Data Load (PostgreSQL)
#     # scheduler.run_solar_terms_data_load(2024, 2024)
#     # Example: Run Solar Terms Extraction (PostgreSQL)
#     # scheduler.run_solar_terms_extraction(2024, 2024)
#     # Example: Backup PostgreSQL Solar Terms Table
#     # scheduler.backup_solar_terms_postgres_table()
