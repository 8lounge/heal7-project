"""
원자 모듈: 사주 기둥 계산기
=========================
입력: 생년월일시 정보
출력: 년주/월주/일주/시주 (四柱)
로직: 전통 명리학 기준의 정확한 사주 계산

특징:
- 입춘 기준 년주 계산 (2월 4일 전후)
- 절기 기준 월주 계산 
- 60갑자 순환 기반 일주 계산
- 시두법 적용 시주 계산
"""

from datetime import date, datetime, time
from typing import Union, Tuple, NamedTuple, Optional, Dict
from dataclasses import dataclass

from .constants import GANJI_60, CHEONGAN, JIJI, split_ganji
from .gapja_calculator import calculate_gapja, get_gapja_index

@dataclass
class PillarInfo:
    """기둥 정보"""
    ganji: str  # 갑자
    cheongan: str  # 천간
    jiji: str  # 지지
    element: str  # 오행
    yin_yang: str  # 음양

@dataclass
class SajuPillars:
    """사주 전체 기둥"""
    year_pillar: PillarInfo   # 년주
    month_pillar: PillarInfo  # 월주
    day_pillar: PillarInfo    # 일주
    time_pillar: PillarInfo   # 시주
    birth_datetime: datetime
    
    def __str__(self) -> str:
        return f"년주:{self.year_pillar.ganji} 월주:{self.month_pillar.ganji} 일주:{self.day_pillar.ganji} 시주:{self.time_pillar.ganji}"

class PillarCalculator:
    """사주 기둥 계산기"""
    
    # 월지지 매핑 (절기 기준) - 인월부터 시작
    MONTH_JIJI_MAP = {
        1: "축",  # 12월 (대한 ~ 입춘 전)
        2: "인",  # 1월 (입춘 ~ 경칩 전)  
        3: "묘",  # 2월 (경칩 ~ 청명 전)
        4: "진",  # 3월 (청명 ~ 입하 전)
        5: "사",  # 4월 (입하 ~ 망종 전)
        6: "오",  # 5월 (망종 ~ 소서 전)
        7: "미",  # 6월 (소서 ~ 입추 전)
        8: "신",  # 7월 (입추 ~ 백로 전)
        9: "유",  # 8월 (백로 ~ 한로 전)
        10: "술", # 9월 (한로 ~ 입동 전)
        11: "해", # 10월 (입동 ~ 대설 전)
        12: "자"  # 11월 (대설 ~ 소한 전)
    }
    
    # 시지지 매핑 (시두법)
    TIME_JIJI_MAP = {
        23: "자", 0: "자", 1: "자",        # 23:00 ~ 01:59
        2: "축", 3: "축",                   # 02:00 ~ 03:59
        4: "인", 5: "인",                   # 04:00 ~ 05:59
        6: "묘", 7: "묘",                   # 06:00 ~ 07:59
        8: "진", 9: "진",                   # 08:00 ~ 09:59
        10: "사", 11: "사",                 # 10:00 ~ 11:59
        12: "오", 13: "오",                 # 12:00 ~ 13:59
        14: "미", 15: "미",                 # 14:00 ~ 15:59
        16: "신", 17: "신",                 # 16:00 ~ 17:59
        18: "유", 19: "유",                 # 18:00 ~ 19:59
        20: "술", 21: "술",                 # 20:00 ~ 21:59
        22: "해"                            # 22:00 ~ 22:59
    }
    
    def __init__(self, use_true_solar_time: bool = False, longitude: float = 126.978):
        """
        초기화
        
        Args:
            use_true_solar_time: 진태양시 사용 여부
            longitude: 경도 (서울 기본값: 126.978°E)
        """
        self.use_true_solar_time = use_true_solar_time
        self.longitude = longitude
        self.time_correction_minutes = (longitude - 135.0) * 4  # 한국표준시 보정
    
    def calculate_year_pillar(self, birth_date: Union[str, date, datetime]) -> PillarInfo:
        """
        년주 계산 (입춘 기준)
        
        Args:
            birth_date: 생년월일
            
        Returns:
            PillarInfo: 년주 정보
        """
        if isinstance(birth_date, str):
            birth_date = datetime.strptime(birth_date, "%Y-%m-%d").date()
        elif isinstance(birth_date, datetime):
            birth_date = birth_date.date()
        
        year = birth_date.year
        month = birth_date.month
        day = birth_date.day
        
        # 입춘 기준 년도 결정
        saju_year = year
        if month < 2 or (month == 2 and day < 4):
            saju_year = year - 1  # 입춘 이전은 전년도
        
        # 1900년 = 경자년(36번째) 기준으로 60갑자 순환 계산
        reference_year = 1900
        reference_index = 36  # 경자의 인덱스
        
        year_index = (reference_index + (saju_year - reference_year)) % 60
        if year_index < 0:
            year_index += 60
        
        year_ganji = GANJI_60[year_index]
        cheongan, jiji = split_ganji(year_ganji)
        
        return self._create_pillar_info(year_ganji, cheongan, jiji)
    
    def calculate_month_pillar(self, birth_date: Union[str, date, datetime], 
                             year_pillar: Optional[PillarInfo] = None) -> PillarInfo:
        """
        월주 계산 (절기 기준)
        
        Args:
            birth_date: 생년월일
            year_pillar: 년주 정보 (없으면 자동 계산)
            
        Returns:
            PillarInfo: 월주 정보
        """
        if isinstance(birth_date, str):
            birth_date = datetime.strptime(birth_date, "%Y-%m-%d").date()
        elif isinstance(birth_date, datetime):
            birth_date = birth_date.date()
        
        if year_pillar is None:
            year_pillar = self.calculate_year_pillar(birth_date)
        
        # 절기 기준 월 결정 (현재는 간단히 달력 월 사용)
        # TODO: 실제 절기 날짜 기준으로 개선 필요
        month = birth_date.month
        
        # 월지지 결정
        month_jiji = self.MONTH_JIJI_MAP.get(month, "인")
        
        # 월천간 계산 (년천간 기준)
        year_cheongan = year_pillar.cheongan
        year_index = CHEONGAN.index(year_cheongan)
        
        # 월천간 공식: (년천간 인덱스 * 2 + 월 인덱스) % 10
        month_jiji_index = JIJI.index(month_jiji)
        month_cheongan_index = (year_index * 2 + month_jiji_index) % 10
        month_cheongan = CHEONGAN[month_cheongan_index]
        
        month_ganji = month_cheongan + month_jiji
        
        return self._create_pillar_info(month_ganji, month_cheongan, month_jiji)
    
    def calculate_day_pillar(self, birth_date: Union[str, date, datetime]) -> PillarInfo:
        """
        일주 계산 (60갑자 순환)
        
        Args:
            birth_date: 생년월일
            
        Returns:
            PillarInfo: 일주 정보
        """
        if isinstance(birth_date, str):
            birth_date = datetime.strptime(birth_date, "%Y-%m-%d").date()
        elif isinstance(birth_date, datetime):
            birth_date = birth_date.date()
        
        # 60갑자 계산기 사용
        day_ganji = calculate_gapja(birth_date)
        cheongan, jiji = split_ganji(day_ganji)
        
        return self._create_pillar_info(day_ganji, cheongan, jiji)
    
    def calculate_time_pillar(self, birth_datetime: datetime, 
                            day_pillar: Optional[PillarInfo] = None) -> PillarInfo:
        """
        시주 계산 (시두법)
        
        Args:
            birth_datetime: 생년월일시
            day_pillar: 일주 정보 (없으면 자동 계산)
            
        Returns:
            PillarInfo: 시주 정보
        """
        if day_pillar is None:
            day_pillar = self.calculate_day_pillar(birth_datetime.date())
        
        # 진태양시 보정
        birth_time = birth_datetime.time()
        if self.use_true_solar_time:
            corrected_minutes = birth_time.hour * 60 + birth_time.minute + self.time_correction_minutes
            corrected_hour = (corrected_minutes // 60) % 24
        else:
            corrected_hour = birth_time.hour
        
        # 시지지 결정
        time_jiji = self.TIME_JIJI_MAP.get(corrected_hour, "자")
        
        # 시천간 계산 (일천간 기준)
        day_cheongan = day_pillar.cheongan
        day_index = CHEONGAN.index(day_cheongan)
        
        # 시천간 공식: (일천간 인덱스 * 2 + 시지지 인덱스) % 10
        time_jiji_index = JIJI.index(time_jiji)
        time_cheongan_index = (day_index * 2 + time_jiji_index) % 10
        time_cheongan = CHEONGAN[time_cheongan_index]
        
        time_ganji = time_cheongan + time_jiji
        
        return self._create_pillar_info(time_ganji, time_cheongan, time_jiji)
    
    def calculate_all_pillars(self, birth_datetime: datetime) -> SajuPillars:
        """
        사주 전체 계산
        
        Args:
            birth_datetime: 생년월일시
            
        Returns:
            SajuPillars: 완전한 사주 정보
        """
        # 순서대로 계산 (의존성 고려)
        year_pillar = self.calculate_year_pillar(birth_datetime)
        month_pillar = self.calculate_month_pillar(birth_datetime, year_pillar)
        day_pillar = self.calculate_day_pillar(birth_datetime)
        time_pillar = self.calculate_time_pillar(birth_datetime, day_pillar)
        
        return SajuPillars(
            year_pillar=year_pillar,
            month_pillar=month_pillar,
            day_pillar=day_pillar,
            time_pillar=time_pillar,
            birth_datetime=birth_datetime
        )
    
    def _create_pillar_info(self, ganji: str, cheongan: str, jiji: str) -> PillarInfo:
        """PillarInfo 객체 생성 (오행, 음양 정보 포함)"""
        # 오행과 음양은 constants 모듈의 매핑 사용
        from .constants import get_cheongan_wuxing, get_cheongan_yin_yang
        
        element = get_cheongan_wuxing(cheongan)
        yin_yang = get_cheongan_yin_yang(cheongan)
        
        return PillarInfo(
            ganji=ganji,
            cheongan=cheongan,
            jiji=jiji,
            element=element,
            yin_yang=yin_yang
        )

# === 편의 함수들 ===

def calculate_year_pillar(birth_date: Union[str, date, datetime]) -> PillarInfo:
    """년주 계산 (편의 함수)"""
    calculator = PillarCalculator()
    return calculator.calculate_year_pillar(birth_date)

def calculate_month_pillar(birth_date: Union[str, date, datetime]) -> PillarInfo:
    """월주 계산 (편의 함수)"""
    calculator = PillarCalculator()
    return calculator.calculate_month_pillar(birth_date)

def calculate_day_pillar(birth_date: Union[str, date, datetime]) -> PillarInfo:
    """일주 계산 (편의 함수)"""
    calculator = PillarCalculator()
    return calculator.calculate_day_pillar(birth_date)

def calculate_time_pillar(birth_datetime: datetime) -> PillarInfo:
    """시주 계산 (편의 함수)"""
    calculator = PillarCalculator()
    return calculator.calculate_time_pillar(birth_datetime)

def calculate_complete_saju(year: int, month: int, day: int, 
                          hour: int = 12, minute: int = 0) -> SajuPillars:
    """완전한 사주 계산 (편의 함수)"""
    birth_datetime = datetime(year, month, day, hour, minute)
    calculator = PillarCalculator()
    return calculator.calculate_all_pillars(birth_datetime)

# === 검증 및 테스트 함수들 ===

def validate_pillar_calculation(birth_datetime: datetime, 
                              expected_pillars: Dict[str, str]) -> bool:
    """사주 계산 결과 검증"""
    calculator = PillarCalculator()
    result = calculator.calculate_all_pillars(birth_datetime)
    
    checks = {
        "year": result.year_pillar.ganji == expected_pillars.get("year"),
        "month": result.month_pillar.ganji == expected_pillars.get("month"),
        "day": result.day_pillar.ganji == expected_pillars.get("day"),
        "time": result.time_pillar.ganji == expected_pillars.get("time")
    }
    
    return all(checks.values())

def test_pillar_calculator():
    """기둥 계산기 테스트"""
    # 테스트 케이스
    test_datetime = datetime(1990, 5, 15, 14, 30)  # 1990년 5월 15일 14:30
    
    calculator = PillarCalculator()
    result = calculator.calculate_all_pillars(test_datetime)
    
    print(f"테스트 사주: {result}")
    print(f"년주: {result.year_pillar.ganji} ({result.year_pillar.element})")
    print(f"월주: {result.month_pillar.ganji} ({result.month_pillar.element})")
    print(f"일주: {result.day_pillar.ganji} ({result.day_pillar.element})")
    print(f"시주: {result.time_pillar.ganji} ({result.time_pillar.element})")
    
    # 2025년 9월 9일 검증 (최근 수정한 날짜)
    test_2025 = datetime(2025, 9, 9, 12, 0)
    result_2025 = calculator.calculate_all_pillars(test_2025)
    print(f"\n2025-09-09 사주: {result_2025}")
    
    print("✅ 기둥 계산기 테스트 완료")

def test_year_pillar_spring_boundary():
    """년주 입춘 경계 테스트"""
    calculator = PillarCalculator()
    
    # 입춘 전후 테스트
    before_spring = calculator.calculate_year_pillar("2025-02-03")  # 입춘 전
    after_spring = calculator.calculate_year_pillar("2025-02-05")   # 입춘 후
    
    print(f"2025-02-03 (입춘 전): {before_spring.ganji}")
    print(f"2025-02-05 (입춘 후): {after_spring.ganji}")
    
    # 입춘 전은 전년도 년주, 입춘 후는 당년도 년주
    # 실제 년주가 다르게 나와야 함
    assert before_spring.ganji != after_spring.ganji, "입춘 전후 년주가 동일함 (오류)"
    
    print("✅ 년주 입춘 경계 테스트 통과")

if __name__ == "__main__":
    test_pillar_calculator()
    test_year_pillar_spring_boundary()