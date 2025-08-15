#!/usr/bin/env python3
"""
24절기 레거시 데이터 어댑터
기존 manse_calendar_data 테이블의 절기 데이터를 활용하는 유틸리티
"""

import psycopg2
from datetime import datetime, date
from typing import Dict, List, Optional, Tuple
import logging

logger = logging.getLogger(__name__)

class SolarTermsLegacyAdapter:
    """레거시 24절기 데이터 어댑터"""
    
    def __init__(self):
        self.db_config = {
            'host': 'localhost',
            'database': 'livedb',
            'user': 'liveuser',
            'password': 'livepass2024'
        }
        
        # 24절기 순서 (입춘부터 시작)
        self.solar_terms_order = [
            "立春", "雨水", "驚蟄", "春分", "淸明", "穀雨",    # 봄
            "立夏", "小滿", "芒種", "夏至", "小暑", "大暑",    # 여름  
            "立秋", "處暑", "白露", "秋分", "寒露", "霜降",    # 가을
            "立冬", "小雪", "大雪", "冬至", "小寒", "大寒"     # 겨울
        ]
        
        # 절기 한자 → 한글 매핑
        self.hanja_to_hangul = {
            "立春": "입춘", "雨水": "우수", "驚蟄": "경칩", "春分": "춘분",
            "淸明": "청명", "穀雨": "곡우", "立夏": "입하", "小滿": "소만",
            "芒種": "망종", "夏至": "하지", "小暑": "소서", "大暑": "대서",
            "立秋": "입추", "處暑": "처서", "白露": "백로", "秋分": "추분",
            "寒露": "한로", "霜降": "상강", "立冬": "입동", "小雪": "소설",
            "大雪": "대설", "冬至": "동지", "小寒": "소한", "大寒": "대한"
        }
    
    def get_solar_term_for_date(self, target_date: date) -> Optional[Dict]:
        """특정 날짜의 절기 정보 조회"""
        conn = None
        cur = None
        
        try:
            conn = psycopg2.connect(**self.db_config)
            cur = conn.cursor()
            
            # 해당 날짜의 절기 조회 (text 타입 컬럼 처리)
            cur.execute("""
                SELECT cd_sy, cd_sm, cd_sd, cd_hterms, cd_kterms, cd_terms_time
                FROM manse_calendar_data 
                WHERE cd_sy = %s AND cd_sm = %s AND cd_sd = %s 
                AND cd_hterms IS NOT NULL 
                AND cd_hterms != 'NULL'
                AND cd_hterms != ''
            """, (target_date.year, str(target_date.month), str(target_date.day)))
            
            result = cur.fetchone()
            
            if result:
                year, month, day, hanja_name, hangul_name, term_time = result
                
                # 시간 파싱 (YYYYMMDDHHMM 형식)
                if term_time and len(str(term_time)) >= 12:
                    time_str = str(term_time)
                    hour = int(time_str[8:10])
                    minute = int(time_str[10:12])
                else:
                    hour, minute = 12, 0  # 기본값
                
                return {
                    'date': target_date,
                    'hanja_name': hanja_name,
                    'hangul_name': hangul_name,
                    'hour': hour,
                    'minute': minute,
                    'datetime': datetime(year, int(month), int(day), hour, minute),
                    'term_order': self.get_term_order(hanja_name)
                }
            
            return None
            
        except Exception as e:
            logger.error(f"절기 조회 오류: {e}")
            return None
        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()
    
    def get_year_solar_terms(self, year: int) -> List[Dict]:
        """특정 연도의 모든 절기 조회"""
        conn = None
        cur = None
        
        try:
            conn = psycopg2.connect(**self.db_config)
            cur = conn.cursor()
            
            # 해당 연도의 모든 절기 조회 (text 타입 처리)
            cur.execute("""
                SELECT cd_sy, cd_sm, cd_sd, cd_hterms, cd_kterms, cd_terms_time
                FROM manse_calendar_data 
                WHERE cd_sy = %s 
                AND cd_hterms IS NOT NULL 
                AND cd_hterms != 'NULL'
                AND cd_hterms != ''
                ORDER BY CAST(cd_sm AS INTEGER), CAST(cd_sd AS INTEGER)
            """, (year,))
            
            results = cur.fetchall()
            year_terms = []
            
            for result in results:
                year, month, day, hanja_name, hangul_name, term_time = result
                
                # 시간 파싱
                if term_time and len(str(term_time)) >= 12:
                    time_str = str(term_time)
                    hour = int(time_str[8:10])
                    minute = int(time_str[10:12])
                else:
                    hour, minute = 12, 0
                
                year_terms.append({
                    'date': date(year, int(month), int(day)),
                    'hanja_name': hanja_name,
                    'hangul_name': hangul_name,
                    'hour': hour,
                    'minute': minute,
                    'datetime': datetime(year, int(month), int(day), hour, minute),
                    'term_order': self.get_term_order(hanja_name),
                    'season': self.get_season(hanja_name)
                })
            
            # 절기 순서로 정렬 (입춘부터)
            year_terms.sort(key=lambda x: (x['term_order'], x['date']))
            
            return year_terms
            
        except Exception as e:
            logger.error(f"연도별 절기 조회 오류: {e}")
            return []
        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()
    
    def get_term_order(self, hanja_name: str) -> int:
        """절기 순서 반환 (입춘=1, 우수=2, ...)"""
        try:
            return self.solar_terms_order.index(hanja_name) + 1
        except ValueError:
            return 99  # 알 수 없는 절기
    
    def get_season(self, hanja_name: str) -> str:
        """절기의 계절 반환"""
        if hanja_name in ["立春", "雨水", "驚蟄", "春分", "淸明", "穀雨"]:
            return "봄"
        elif hanja_name in ["立夏", "小滿", "芒種", "夏至", "小暑", "大暑"]:
            return "여름"
        elif hanja_name in ["立秋", "處暑", "白露", "秋分", "寒露", "霜降"]:
            return "가을"
        elif hanja_name in ["立冬", "小雪", "大雪", "冬至", "小寒", "大寒"]:
            return "겨울"
        else:
            return "미분류"
    
    def find_month_boundary(self, year: int, month: int) -> Optional[Dict]:
        """월의 절기 경계 찾기 (월주 결정용)"""
        conn = None
        cur = None
        
        try:
            conn = psycopg2.connect(**self.db_config)
            cur = conn.cursor()
            
            # 해당 월과 이전/다음 월의 절기 찾기 (text 타입 처리)
            cur.execute("""
                SELECT cd_sy, cd_sm, cd_sd, cd_hterms, cd_kterms, cd_terms_time
                FROM manse_calendar_data 
                WHERE cd_sy = %s 
                AND CAST(cd_sm AS INTEGER) BETWEEN %s AND %s
                AND cd_hterms IS NOT NULL 
                AND cd_hterms != 'NULL'
                AND cd_hterms != ''
                ORDER BY CAST(cd_sm AS INTEGER), CAST(cd_sd AS INTEGER)
            """, (year, max(1, month-1), min(12, month+1)))
            
            results = cur.fetchall()
            
            # 해당 월의 주요 절기 찾기
            month_terms = []
            for result in results:
                year, m, day, hanja_name, hangul_name, term_time = result
                
                if int(m) == month:
                    month_terms.append({
                        'date': date(year, int(m), int(day)),
                        'hanja_name': hanja_name,
                        'hangul_name': hangul_name,
                        'term_order': self.get_term_order(hanja_name)
                    })
            
            if month_terms:
                # 가장 빠른 절기 반환 (월주 결정의 기준)
                month_terms.sort(key=lambda x: x['date'])
                return month_terms[0]
            
            return None
            
        except Exception as e:
            logger.error(f"월 경계 절기 조회 오류: {e}")
            return None
        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()
    
    def is_lichun_passed(self, target_date: date) -> bool:
        """입춘이 지났는지 확인 (세운 계산용)"""
        year = target_date.year
        
        # 해당 연도 입춘 날짜 조회
        lichun_info = self.get_specific_term(year, "立春")
        
        if lichun_info:
            lichun_date = lichun_info['date']
            return target_date >= lichun_date
        
        return False  # 입춘 정보가 없으면 보수적으로 False
    
    def get_specific_term(self, year: int, hanja_name: str) -> Optional[Dict]:
        """특정 연도의 특정 절기 조회"""
        conn = None
        cur = None
        
        try:
            conn = psycopg2.connect(**self.db_config)
            cur = conn.cursor()
            
            cur.execute("""
                SELECT cd_sy, cd_sm, cd_sd, cd_hterms, cd_kterms, cd_terms_time
                FROM manse_calendar_data 
                WHERE cd_sy = %s 
                AND cd_hterms = %s
                LIMIT 1
            """, (year, hanja_name))
            
            result = cur.fetchone()
            
            if result:
                year, month, day, hanja_name, hangul_name, term_time = result
                
                # 시간 파싱
                if term_time and len(str(term_time)) >= 12:
                    time_str = str(term_time)
                    hour = int(time_str[8:10])
                    minute = int(time_str[10:12])
                else:
                    hour, minute = 12, 0
                
                return {
                    'date': date(year, int(month), int(day)),
                    'hanja_name': hanja_name,
                    'hangul_name': hangul_name,
                    'hour': hour,
                    'minute': minute,
                    'datetime': datetime(year, int(month), int(day), hour, minute)
                }
            
            return None
            
        except Exception as e:
            logger.error(f"특정 절기 조회 오류: {e}")
            return None
        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()
    
    def cleanup_duplicate_table(self):
        """중복으로 생성된 solar_terms_24 테이블 정리"""
        conn = None
        cur = None
        
        try:
            conn = psycopg2.connect(**self.db_config)
            cur = conn.cursor()
            
            # 중복 테이블 삭제
            cur.execute("DROP TABLE IF EXISTS solar_terms_24 CASCADE")
            conn.commit()
            
            logger.info("✅ 중복 solar_terms_24 테이블 삭제 완료")
            
        except Exception as e:
            logger.error(f"테이블 정리 오류: {e}")
            if conn:
                conn.rollback()
        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()


# 전역 인스턴스
solar_terms_adapter = SolarTermsLegacyAdapter()


def get_solar_term_for_date(target_date: date) -> Optional[Dict]:
    """날짜별 절기 조회 (외부 사용)"""
    return solar_terms_adapter.get_solar_term_for_date(target_date)


def get_year_solar_terms(year: int) -> List[Dict]:
    """연도별 절기 조회 (외부 사용)"""
    return solar_terms_adapter.get_year_solar_terms(year)


def is_lichun_passed(target_date: date) -> bool:
    """입춘 통과 확인 (외부 사용)"""
    return solar_terms_adapter.is_lichun_passed(target_date)


def get_month_primary_term(year: int, month: int) -> Optional[Dict]:
    """월주 결정을 위한 주요 절기 조회"""
    return solar_terms_adapter.find_month_boundary(year, month)


# Production-ready module - test code removed