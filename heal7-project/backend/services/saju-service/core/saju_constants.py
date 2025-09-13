"""
🌟 사주 시스템 전역 상수 (GLOBAL CONSTANTS)
==============================================

이 파일은 모든 사주 계산의 상수 정의를 담고 있습니다.
다른 곳에서 상수를 중복 정의하지 마세요!

📍 중요 원칙:
- 이 파일의 상수들은 절대 변경하면 안 됩니다
- 특히 REFERENCE_DATE와 REFERENCE_GAPJA_INDEX는 시스템 전체의 기준점
- 새로운 상수 추가는 가능하지만 기존 상수 수정은 금지

📍 사용법:
from core.saju_constants import GAPJA_60, REFERENCE_DATE
gapja = GAPJA_60[index]
"""

from datetime import date
import os

# ==========================================
# 📍 핵심 기준점 (절대 변경 금지!)
# ==========================================

# 60갑자 계산의 절대 기준점
REFERENCE_DATE = date(1900, 1, 31)  # 1900년 1월 31일 = 갑진일
REFERENCE_GAPJA_INDEX = 40           # 갑진의 인덱스 (0-based)

# KASI API 설정
KASI_API_KEY = os.getenv('KASI_API_KEY', 'AR2zMFQPIPBFak%2BMdXzznzVmtsICp7dwd3eo9XCUP62kXpr4GrX3eqi28erzZhXfIemuo6C5AK58eLMKBw8VGQ%3D%3D')
KASI_BASE_URL = "http://apis.data.go.kr/B090041/openapi/service/LrsrCldInfoService"

# ==========================================
# 📍 60갑자 순환표 (인덱스 순서 중요)
# ==========================================

GAPJA_60 = [
    "갑자", "을축", "병인", "정묘", "무진", "기사", "경오", "신미", "임신", "계유",  # 0-9
    "갑술", "을해", "병자", "정축", "무인", "기묘", "경진", "신사", "임오", "계미",  # 10-19
    "갑신", "을유", "병술", "정해", "무자", "기축", "경인", "신묘", "임진", "계사",  # 20-29
    "갑오", "을미", "병신", "정유", "무술", "기해", "경자", "신축", "임인", "계묘",  # 30-39
    "갑진", "을사", "병오", "정미", "무신", "기유", "경술", "신해", "임자", "계축",  # 40-49 (갑진=40)
    "갑인", "을묘", "병진", "정사", "무오", "기미", "경신", "신유", "임술", "계해"   # 50-59
]

# ==========================================
# 📍 천간 (10개)
# ==========================================

CHEONGAN_10 = ["갑", "을", "병", "정", "무", "기", "경", "신", "임", "계"]

CHEONGAN_PROPERTIES = {
    "갑": {"element": "목", "yin_yang": "양", "chinese": "甲"},
    "을": {"element": "목", "yin_yang": "음", "chinese": "乙"},
    "병": {"element": "화", "yin_yang": "양", "chinese": "丙"},
    "정": {"element": "화", "yin_yang": "음", "chinese": "丁"},
    "무": {"element": "토", "yin_yang": "양", "chinese": "戊"},
    "기": {"element": "토", "yin_yang": "음", "chinese": "己"},
    "경": {"element": "금", "yin_yang": "양", "chinese": "庚"},
    "신": {"element": "금", "yin_yang": "음", "chinese": "辛"},
    "임": {"element": "수", "yin_yang": "양", "chinese": "壬"},
    "계": {"element": "수", "yin_yang": "음", "chinese": "癸"}
}

# ==========================================
# 📍 지지 (12개)
# ==========================================

JIJI_12 = ["자", "축", "인", "묘", "진", "사", "오", "미", "신", "유", "술", "해"]

JIJI_PROPERTIES = {
    "자": {"zodiac": "쥐",      "element": "수", "season": "겨울", "chinese": "子"},
    "축": {"zodiac": "소",      "element": "토", "season": "겨울", "chinese": "丑"},
    "인": {"zodiac": "호랑이",  "element": "목", "season": "봄",   "chinese": "寅"},
    "묘": {"zodiac": "토끼",    "element": "목", "season": "봄",   "chinese": "卯"},
    "진": {"zodiac": "용",      "element": "토", "season": "봄",   "chinese": "辰"},
    "사": {"zodiac": "뱀",      "element": "화", "season": "여름", "chinese": "巳"},
    "오": {"zodiac": "말",      "element": "화", "season": "여름", "chinese": "午"},
    "미": {"zodiac": "양",      "element": "토", "season": "여름", "chinese": "未"},
    "신": {"zodiac": "원숭이",  "element": "금", "season": "가을", "chinese": "申"},
    "유": {"zodiac": "닭",      "element": "금", "season": "가을", "chinese": "酉"},
    "술": {"zodiac": "개",      "element": "토", "season": "가을", "chinese": "戌"},
    "해": {"zodiac": "돼지",    "element": "수", "season": "겨울", "chinese": "亥"}
}

# ==========================================
# 📍 24절기 정보
# ==========================================

SOLAR_TERMS_24 = [
    "입춘", "우수", "경칩", "춘분", "청명", "곡우",      # 봄 (1-6)
    "입하", "소만", "망종", "하지", "소서", "대서",      # 여름 (7-12)
    "입추", "처서", "백로", "추분", "한로", "상강",      # 가을 (13-18)
    "입동", "소설", "대설", "동지", "소한", "대한"       # 겨울 (19-24)
]

SOLAR_TERMS_CHINESE = {
    "입춘": "立春", "우수": "雨水", "경칩": "驚蟄", "춘분": "春分", "청명": "淸明", "곡우": "穀雨",
    "입하": "立夏", "소만": "小滿", "망종": "芒種", "하지": "夏至", "소서": "小暑", "대서": "大暑",
    "입추": "立秋", "처서": "處暑", "백로": "白露", "추분": "秋分", "한로": "寒露", "상강": "霜降",
    "입동": "立冬", "소설": "小雪", "대설": "大雪", "동지": "冬至", "소한": "小寒", "대한": "大寒"
}

# ==========================================
# 📍 오행 (五行) 관계
# ==========================================

WUXING_5 = ["목", "화", "토", "금", "수"]

WUXING_RELATIONS = {
    "상생": {  # 서로 생성하는 관계
        "목": "화",  # 목생화
        "화": "토",  # 화생토
        "토": "금",  # 토생금
        "금": "수",  # 금생수
        "수": "목"   # 수생목
    },
    "상극": {  # 서로 극하는 관계
        "목": "토",  # 목극토
        "화": "금",  # 화극금
        "토": "수",  # 토극수
        "금": "목",  # 금극목
        "수": "화"   # 수극화
    }
}

# ==========================================
# 📍 시간 관련 상수
# ==========================================

# 시간대별 지지 매핑 (24시간 → 12지지)
HOUR_TO_JIJI = {
    23: "자", 0: "자", 1: "자",      # 자시 (23-01)
    2: "축", 3: "축",                # 축시 (01-03)
    4: "인", 5: "인",                # 인시 (03-05)
    6: "묘", 7: "묘",                # 묘시 (05-07)
    8: "진", 9: "진",                # 진시 (07-09)
    10: "사", 11: "사",              # 사시 (09-11)
    12: "오", 13: "오",              # 오시 (11-13)
    14: "미", 15: "미",              # 미시 (13-15)
    16: "신", 17: "신",              # 신시 (15-17)
    18: "유", 19: "유",              # 유시 (17-19)
    20: "술", 21: "술",              # 술시 (19-21)
    22: "해"                         # 해시 (21-23)
}

# ==========================================
# 📍 API 응답 및 설정
# ==========================================

# API 응답 템플릿
API_SUCCESS_TEMPLATE = {
    "success": True,
    "data": None,
    "source": "unified_saju_core",
    "version": "2.0.0"
}

API_ERROR_TEMPLATE = {
    "success": False,
    "error": None,
    "source": "unified_saju_core",
    "version": "2.0.0"
}

# 시스템 설정
SYSTEM_CONFIG = {
    "cache_enabled": True,
    "cache_max_size": 1000,
    "api_timeout": 10,
    "fallback_enabled": True,
    "debug_mode": False
}

# ==========================================
# 📍 유틸리티 함수
# ==========================================

def get_gapja_info(gapja: str) -> dict:
    """
    갑자 정보 반환
    
    Args:
        gapja: 갑자 문자열 (예: "갑자")
        
    Returns:
        dict: 갑자 상세 정보
    """
    if gapja not in GAPJA_60:
        return {"error": "Invalid gapja"}
    
    index = GAPJA_60.index(gapja)
    cheongan = gapja[0]
    jiji = gapja[1]
    
    return {
        "gapja": gapja,
        "index": index,
        "cheongan": cheongan,
        "jiji": jiji,
        "cheongan_info": CHEONGAN_PROPERTIES.get(cheongan, {}),
        "jiji_info": JIJI_PROPERTIES.get(jiji, {})
    }

def get_element_relation(element1: str, element2: str) -> str:
    """
    두 오행 간의 관계 반환
    
    Args:
        element1, element2: 오행 ("목", "화", "토", "금", "수")
        
    Returns:
        str: "상생", "상극", "비화", "비극" 중 하나
    """
    if element1 not in WUXING_5 or element2 not in WUXING_5:
        return "unknown"
    
    if WUXING_RELATIONS["상생"].get(element1) == element2:
        return "상생"
    elif WUXING_RELATIONS["상극"].get(element1) == element2:
        return "상극"
    elif element1 == element2:
        return "비화"  # 같은 오행
    else:
        return "비극"  # 특별한 관계 없음

def validate_date(year: int, month: int, day: int) -> bool:
    """
    날짜 유효성 검증
    
    Args:
        year, month, day: 검증할 날짜
        
    Returns:
        bool: 유효한 날짜인지 여부
    """
    try:
        date(year, month, day)
        return True
    except ValueError:
        return False

# ==========================================
# 📍 상수 무결성 검증
# ==========================================

def validate_constants() -> dict:
    """
    상수들의 무결성 검증
    
    Returns:
        dict: 검증 결과
    """
    results = {
        "gapja_60_count": len(GAPJA_60) == 60,
        "cheongan_10_count": len(CHEONGAN_10) == 10,
        "jiji_12_count": len(JIJI_12) == 12,
        "solar_terms_24_count": len(SOLAR_TERMS_24) == 24,
        "reference_gapja_valid": GAPJA_60[REFERENCE_GAPJA_INDEX] == "갑진",
        "all_valid": True
    }
    
    # 전체 유효성 확인
    results["all_valid"] = all(results.values())
    
    return results


# ==========================================
# 📍 상수 검증 실행 (임포트 시 자동 실행)
# ==========================================

if __name__ == "__main__":
    print("🌟 사주 시스템 전역 상수 검증")
    print("=" * 40)
    
    validation = validate_constants()
    for key, value in validation.items():
        status = "✅" if value else "❌"
        print(f"{status} {key}: {value}")
    
    print(f"\n📍 기준 정보:")
    print(f"  기준일: {REFERENCE_DATE}")
    print(f"  기준갑자: {GAPJA_60[REFERENCE_GAPJA_INDEX]} (인덱스 {REFERENCE_GAPJA_INDEX})")
    
    # 갑자 정보 테스트
    print(f"\n🔮 갑자 정보 테스트:")
    test_gapja = "계미"
    info = get_gapja_info(test_gapja)
    print(f"  {test_gapja}: {info}")
else:
    # 임포트 시 자동 검증
    validation = validate_constants()
    if not validation["all_valid"]:
        raise ValueError("❌ 사주 상수 무결성 검증 실패! 상수 파일을 확인하세요.")