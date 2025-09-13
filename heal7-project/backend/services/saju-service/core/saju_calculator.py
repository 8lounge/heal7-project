"""
HEAL7 사주 계산 핵심 모듈
년주, 월주, 일주, 시주 계산 로직
"""

from typing import Optional, Dict, Tuple
from datetime import datetime, date

class SajuCalculator:
    """사주 계산 클래스"""
    
    천간 = ['갑', '을', '병', '정', '무', '기', '경', '신', '임', '계']
    지지 = ['자', '축', '인', '묘', '진', '사', '오', '미', '신', '유', '술', '해']
    
    갑자60순환 = [
        '갑자', '을축', '병인', '정묘', '무진', '기사', '경오', '신미', '임신', '계유',
        '갑술', '을해', '병자', '정축', '무인', '기묘', '경진', '신사', '임오', '계미',
        '갑신', '을유', '병술', '정해', '무자', '기축', '경인', '신묘', '임진', '계사',
        '갑오', '을미', '병신', '정유', '무술', '기해', '경자', '신축', '임인', '계묘',
        '갑진', '을사', '병오', '정미', '무신', '기유', '경술', '신해', '임자', '계축',
        '갑인', '을묘', '병진', '정사', '무오', '기미', '경신', '신유', '임술', '계해'
    ]
    
    # 절기별 월지지 매핑
    절기_월지지 = {
        '소한': '축', '대한': '축',
        '입춘': '인', '우수': '인',
        '경칩': '묘', '춘분': '묘',
        '청명': '진', '곡우': '진',
        '입하': '사', '소만': '사',
        '망종': '오', '하지': '오',
        '소서': '미', '대서': '미',
        '입추': '신', '처서': '신',
        '백로': '유', '추분': '유',
        '한로': '술', '상강': '술',
        '입동': '해', '소설': '해',
        '대설': '자', '동지': '자'
    }
    
    @classmethod
    def calculate_year_pillar(cls, year: int, month: int, day: int) -> str:
        """
        년주 계산 (입춘 기준)
        입춘(2월 4일경) 이전은 전년도로 계산
        """
        saju_year = year
        if month < 2 or (month == 2 and day < 4):
            saju_year = year - 1
        
        # 1900년 = 경자년(36번째) 기준
        base_year = 1900
        base_index = 36
        
        year_index = (base_index + (saju_year - base_year)) % 60
        if year_index < 0:
            year_index += 60
        
        return cls.갑자60순환[year_index]
    
    @classmethod
    def calculate_month_pillar(cls, year_gapja: str, month: int, day: int, 
                               solar_term: Optional[str] = None) -> str:
        """
        월주 계산 (절기 기준, 오호둔 적용)
        
        오호둔(五虎遁) 원리:
        - 갑기년: 병인월부터 시작
        - 을경년: 무인월부터 시작
        - 병신년: 경인월부터 시작
        - 정임년: 임인월부터 시작
        - 무계년: 갑인월부터 시작
        """
        if not year_gapja or len(year_gapja) < 2:
            return "계산불가"
        
        year_cheongan = year_gapja[0]
        
        # 오호둔 시작 천간 인덱스
        오호둔_시작 = {
            '갑': 2, '기': 2,  # 병(2)부터
            '을': 4, '경': 4,  # 무(4)부터
            '병': 6, '신': 6,  # 경(6)부터
            '정': 8, '임': 8,  # 임(8)부터
            '무': 0, '계': 0   # 갑(0)부터
        }
        
        if year_cheongan not in 오호둔_시작:
            return "계산불가"
        
        # 월지지 결정
        if solar_term and solar_term in cls.절기_월지지:
            월지지 = cls.절기_월지지[solar_term]
        else:
            # 절기 정보가 없으면 양력 월과 일로 추정
            월지지_추정 = {
                1: ('자', 6),   # 1월 6일 소한
                2: ('인', 4),   # 2월 4일 입춘
                3: ('묘', 6),   # 3월 6일 경칩
                4: ('진', 5),   # 4월 5일 청명
                5: ('사', 6),   # 5월 6일 입하
                6: ('오', 6),   # 6월 6일 망종
                7: ('미', 7),   # 7월 7일 소서
                8: ('신', 8),   # 8월 8일 입추
                9: ('유', 8),   # 9월 8일 백로
                10: ('술', 8),  # 10월 8일 한로
                11: ('해', 8),  # 11월 8일 입동
                12: ('자', 7)   # 12월 7일 대설
            }
            
            if month in 월지지_추정:
                지지, 절기일 = 월지지_추정[month]
                if month == 1:
                    월지지 = '자' if day < 절기일 else '축'
                elif month == 12:
                    월지지 = '해' if day < 절기일 else '자'
                else:
                    prev_month = month - 1
                    prev_지지, _ = 월지지_추정.get(prev_month, ('자', 1))
                    월지지 = prev_지지 if day < 절기일 else 지지
            else:
                월지지 = '자'
        
        # 월천간 계산
        try:
            월지지_idx = cls.지지.index(월지지)
            시작천간_idx = 오호둔_시작[year_cheongan]
            
            # 인월(지지 인덱스 2)부터의 간격 계산
            인월_idx = 2
            간격 = (월지지_idx - 인월_idx + 12) % 12
            
            월천간_idx = (시작천간_idx + 간격) % 10
            월천간 = cls.천간[월천간_idx]
            
            return 월천간 + 월지지
        except (ValueError, IndexError):
            return "계산불가"
    
    @classmethod
    def calculate_day_pillar(cls, year: int, month: int, day: int) -> str:
        """
        일주 계산 (60갑자 순환)
        1900년 1월 31일 = 갑진일 기준
        """
        기준일 = date(1900, 1, 31)
        target_date = date(year, month, day)
        
        날짜차이 = (target_date - 기준일).days
        갑자인덱스 = (40 + 날짜차이) % 60  # 갑진 = 40번째
        
        if 갑자인덱스 < 0:
            갑자인덱스 += 60
        
        return cls.갑자60순환[갑자인덱스]
    
    @classmethod
    def calculate_hour_pillar(cls, day_gapja: str, hour: int) -> str:
        """
        시주 계산 (일천간 기준)
        23-01시: 자시, 01-03시: 축시, ...
        """
        if not day_gapja or len(day_gapja) < 2:
            return "계산불가"
        
        day_cheongan = day_gapja[0]
        
        # 시지지 결정
        시지지_map = {
            (23, 0, 1): '자',
            (1, 2, 3): '축',
            (3, 4, 5): '인',
            (5, 6, 7): '묘',
            (7, 8, 9): '진',
            (9, 10, 11): '사',
            (11, 12, 13): '오',
            (13, 14, 15): '미',
            (15, 16, 17): '신',
            (17, 18, 19): '유',
            (19, 20, 21): '술',
            (21, 22, 23): '해'
        }
        
        시지지 = '자'
        for hours, 지지 in 시지지_map.items():
            if hour in hours:
                시지지 = 지지
                break
        
        # 일천간별 시천간 시작 (오자둔)
        오자둔_시작 = {
            '갑': 0, '기': 0,  # 갑자시부터
            '을': 2, '경': 2,  # 병자시부터
            '병': 4, '신': 4,  # 무자시부터
            '정': 6, '임': 6,  # 경자시부터
            '무': 8, '계': 8   # 임자시부터
        }
        
        if day_cheongan not in 오자둔_시작:
            return "계산불가"
        
        try:
            시지지_idx = cls.지지.index(시지지)
            시작천간_idx = 오자둔_시작[day_cheongan]
            
            시천간_idx = (시작천간_idx + 시지지_idx) % 10
            시천간 = cls.천간[시천간_idx]
            
            return 시천간 + 시지지
        except (ValueError, IndexError):
            return "계산불가"
    
    @classmethod
    def get_full_saju(cls, year: int, month: int, day: int, hour: int,
                      solar_term: Optional[str] = None) -> Dict[str, str]:
        """
        완전한 사주팔자 계산
        """
        year_pillar = cls.calculate_year_pillar(year, month, day)
        month_pillar = cls.calculate_month_pillar(year_pillar, month, day, solar_term)
        day_pillar = cls.calculate_day_pillar(year, month, day)
        hour_pillar = cls.calculate_hour_pillar(day_pillar, hour)
        
        return {
            "year_pillar": year_pillar,
            "month_pillar": month_pillar,
            "day_pillar": day_pillar,
            "hour_pillar": hour_pillar
        }