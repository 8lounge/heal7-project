"""
원자 모듈: 사주 핵심 상수
======================
입력: 없음
출력: 사주 계산에 필요한 모든 기본 상수
로직: 전통 명리학 기준 상수 정의

기존 saju_core_constants.py와 호환성 유지
"""

from enum import Enum
from typing import Dict, List, Tuple, Optional

# === 기본 상수 ===

# 60갑자 순환 (전체 목록)
GANJI_60 = [
    "갑자", "을축", "병인", "정묘", "무진", "기사", "경오", "신미", "임신", "계유",
    "갑술", "을해", "병자", "정축", "무인", "기묘", "경진", "신사", "임오", "계미",
    "갑신", "을유", "병술", "정해", "무자", "기축", "경인", "신묘", "임진", "계사",
    "갑오", "을미", "병신", "정유", "무술", "기해", "경자", "신축", "임인", "계묘",
    "갑진", "을사", "병오", "정미", "무신", "기유", "경술", "신해", "임자", "계축",
    "갑인", "을묘", "병진", "정사", "무오", "기미", "경신", "신유", "임술", "계해"
]

# 천간 (10개)
CHEONGAN = ["갑", "을", "병", "정", "무", "기", "경", "신", "임", "계"]

# 지지 (12개)  
JIJI = ["자", "축", "인", "묘", "진", "사", "오", "미", "신", "유", "술", "해"]

# 오행 (5개)
WUXING = ["목", "화", "토", "금", "수"]

# 음양
YIN_YANG = ["양", "음"]

# 12지 동물
ZODIAC_ANIMALS = ["쥐", "소", "호랑이", "토끼", "용", "뱀", "말", "양", "원숭이", "닭", "개", "돼지"]

# === 매핑 테이블 ===

# 천간 → 오행 매핑
CHEONGAN_WUXING = {
    "갑": "목", "을": "목",
    "병": "화", "정": "화", 
    "무": "토", "기": "토",
    "경": "금", "신": "금",
    "임": "수", "계": "수"
}

# 지지 → 오행 매핑
JIJI_WUXING = {
    "인": "목", "묘": "목",
    "사": "화", "오": "화",
    "진": "토", "술": "토", "축": "토", "미": "토",
    "신": "금", "유": "금", 
    "자": "수", "해": "수"
}

# 천간 → 음양 매핑
CHEONGAN_YIN_YANG = {
    "갑": "양", "을": "음",
    "병": "양", "정": "음",
    "무": "양", "기": "음", 
    "경": "양", "신": "음",
    "임": "양", "계": "음"
}

# 지지 → 음양 매핑
JIJI_YIN_YANG = {
    "자": "양", "축": "음", "인": "양", "묘": "음",
    "진": "양", "사": "음", "오": "양", "미": "음",
    "신": "양", "유": "음", "술": "양", "해": "음"
}

# 지지 → 동물 매핑
JIJI_ZODIAC = {
    "자": "쥐", "축": "소", "인": "호랑이", "묘": "토끼",
    "진": "용", "사": "뱀", "오": "말", "미": "양",
    "신": "원숭이", "유": "닭", "술": "개", "해": "돼지"
}

# 지장간 매핑 (지지 안에 숨어있는 천간들)
JIJANGGAN = {
    "자": [("임", 100)],
    "축": [("계", 30), ("신", 10), ("기", 60)],
    "인": [("무", 23), ("병", 23), ("갑", 54)],
    "묘": [("을", 100)],
    "진": [("을", 30), ("계", 10), ("무", 60)],
    "사": [("무", 23), ("경", 23), ("병", 54)],
    "오": [("정", 100)],
    "미": [("정", 30), ("을", 10), ("기", 60)],
    "신": [("경", 100)],
    "유": [("신", 100)],
    "술": [("신", 30), ("정", 10), ("무", 60)],
    "해": [("무", 23), ("갑", 23), ("임", 54)]
}

# === 기준점 상수 ===

# 갑자 계산 기준점 (1900년 1월 31일 = 갑진일)
GAPJA_REFERENCE_DATE = "1900-01-31"
GAPJA_REFERENCE_INDEX = 40  # 갑진의 인덱스

# 년주 계산 기준 (입춘)
YEAR_PILLAR_CUTOFF = {"month": 2, "day": 4}  # 2월 4일 입춘

# === 유틸리티 함수 ===

def split_ganji(ganji: str) -> Tuple[str, str]:
    """
    갑자를 천간과 지지로 분리
    
    Args:
        ganji: 갑자 문자열 (예: "갑자")
        
    Returns:
        Tuple[천간, 지지] (예: ("갑", "자"))
    """
    if len(ganji) != 2:
        raise ValueError("갑자는 2글자여야 합니다")
    return ganji[0], ganji[1]

def get_cheongan_wuxing(cheongan: str) -> str:
    """천간의 오행 반환"""
    return CHEONGAN_WUXING.get(cheongan, "미지")

def get_jiji_wuxing(jiji: str) -> str:
    """지지의 오행 반환"""
    return JIJI_WUXING.get(jiji, "미지")

def get_cheongan_yin_yang(cheongan: str) -> str:
    """천간의 음양 반환"""
    return CHEONGAN_YIN_YANG.get(cheongan, "미지")

def get_jiji_yin_yang(jiji: str) -> str:
    """지지의 음양 반환"""
    return JIJI_YIN_YANG.get(jiji, "미지")

def get_jiji_zodiac(jiji: str) -> str:
    """지지의 동물 반환"""
    return JIJI_ZODIAC.get(jiji, "미지")

def get_jijanggan(jiji: str) -> List[Tuple[str, int]]:
    """지지의 지장간 반환"""
    return JIJANGGAN.get(jiji, [])

def is_valid_ganji(ganji: str) -> bool:
    """유효한 갑자인지 확인"""
    return ganji in GANJI_60

def is_valid_cheongan(cheongan: str) -> bool:
    """유효한 천간인지 확인"""
    return cheongan in CHEONGAN

def is_valid_jiji(jiji: str) -> bool:
    """유효한 지지인지 확인"""
    return jiji in JIJI

# === 기존 호환성을 위한 Enum 클래스들 ===

class Cheongan(Enum):
    """천간 Enum (기존 코드 호환성)"""
    GAB = "갑"
    EUL = "을" 
    BYEONG = "병"
    JEONG = "정"
    MU = "무"
    GI = "기"
    GYEONG = "경"
    SIN = "신"
    IM = "임"
    GYE = "계"

class Jiji(Enum):
    """지지 Enum (기존 코드 호환성)"""
    JA = "자"
    CHUK = "축"
    IN = "인"
    MYO = "묘"
    JIN = "진"
    SA = "사"
    O = "오"
    MI = "미"
    SIN = "신"
    YU = "유"
    SUL = "술"
    HAE = "해"

class WuXing(Enum):
    """오행 Enum (기존 코드 호환성)"""
    MOK = "목"
    HWA = "화"
    TO = "토"
    GEUM = "금"
    SU = "수"