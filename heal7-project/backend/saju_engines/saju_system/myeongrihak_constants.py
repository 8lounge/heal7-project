#!/usr/bin/env python3
"""
명리학 기초 상수 데이터
- 천간/지지/지장간 매핑
- 십신 관계 매핑
- 오행 속성 정의
"""

from typing import Dict, List, Tuple
from enum import Enum

class WuXing(Enum):
    """오행 (五行)"""
    WOOD = "목"      # 木
    FIRE = "화"      # 火
    EARTH = "토"     # 土
    METAL = "금"     # 金
    WATER = "수"     # 水

class SipSin(Enum):
    """십신 (十神)"""
    BI_JIAN = "비견"      # 比肩
    GYEOP_JAE = "겁재"    # 劫財
    SIK_SIN = "식신"      # 食神
    SANG_GWAN = "상관"    # 傷官
    PYEON_JAE = "편재"    # 偏財
    JEONG_JAE = "정재"    # 正財
    PYEON_GWAN = "편관"   # 偏官 (칠살)
    JEONG_GWAN = "정관"   # 正官
    PYEON_IN = "편인"     # 偏印
    JEONG_IN = "정인"     # 正印

# 천간 (天干) 10개 - 한글
CHEONGAN = [
    "갑", "을", "병", "정", "무", "기", "경", "신", "임", "계"
]

# 지지 (地支) 12개 - 한글
JIJI = [
    "자", "축", "인", "묘", "진", "사", "오", "미", "신", "유", "술", "해"
]

# 한자 ↔ 한글 변환 매핑 (KASI API 호환)
HANJA_TO_HANGUL = {
    # 천간 한자 → 한글
    "甲": "갑", "乙": "을", "丙": "병", "丁": "정", "戊": "무", 
    "己": "기", "庚": "경", "辛": "신", "壬": "임", "癸": "계",
    
    # 지지 한자 → 한글
    "子": "자", "丑": "축", "寅": "인", "卯": "묘", "辰": "진", "巳": "사",
    "午": "오", "未": "미", "申": "신", "酉": "유", "戌": "술", "亥": "해"
}

HANGUL_TO_HANJA = {v: k for k, v in HANJA_TO_HANGUL.items()}

# 60갑자 순환
GAPJA_60 = []
for cheon in CHEONGAN:
    for ji in JIJI:
        if (CHEONGAN.index(cheon) % 2) == (JIJI.index(ji) % 2):
            GAPJA_60.append(f"{cheon}{ji}")

# 천간의 오행
CHEONGAN_WUXING = {
    "갑": WuXing.WOOD,   "을": WuXing.WOOD,
    "병": WuXing.FIRE,   "정": WuXing.FIRE,
    "무": WuXing.EARTH,  "기": WuXing.EARTH,
    "경": WuXing.METAL,  "신": WuXing.METAL,
    "임": WuXing.WATER,  "계": WuXing.WATER
}

# 지지의 오행
JIJI_WUXING = {
    "자": WuXing.WATER,  "축": WuXing.EARTH,  "인": WuXing.WOOD,
    "묘": WuXing.WOOD,   "진": WuXing.EARTH,  "사": WuXing.FIRE,
    "오": WuXing.FIRE,   "미": WuXing.EARTH,  "신": WuXing.METAL,
    "유": WuXing.METAL,  "술": WuXing.EARTH,  "해": WuXing.WATER
}

# 지장간 (地藏干) - 지지 안에 숨어있는 천간들
JIJANGGAN = {
    "자": [("임", 100)],                    # 子: 壬100%
    "축": [("기", 60), ("계", 30), ("신", 10)],  # 丑: 己60% 癸30% 辛10%
    "인": [("갑", 60), ("병", 30), ("무", 10)],  # 寅: 甲60% 丙30% 戊10%
    "묘": [("을", 100)],                    # 卯: 乙100%
    "진": [("무", 60), ("을", 30), ("계", 10)],  # 辰: 戊60% 乙30% 癸10%
    "사": [("병", 60), ("무", 30), ("경", 10)],  # 巳: 丙60% 戊30% 庚10%
    "오": [("정", 70), ("기", 30)],          # 午: 丁70% 己30%
    "미": [("기", 60), ("정", 30), ("을", 10)],  # 未: 己60% 丁30% 乙10%
    "신": [("경", 60), ("무", 30), ("임", 10)],  # 申: 庚60% 戊30% 壬10%
    "유": [("신", 100)],                    # 酉: 辛100%
    "술": [("무", 60), ("신", 30), ("정", 10)],  # 戌: 戊60% 辛30% 丁10%
    "해": [("임", 70), ("갑", 30)],          # 亥: 壬70% 甲30%
}

# 십신 관계 계산 (일간 기준)
SIPSIN_RELATIONS = {
    # 일간이 갑목일 때
    "갑": {
        "갑": SipSin.BI_JIAN,   "을": SipSin.GYEOP_JAE,
        "병": SipSin.SIK_SIN,   "정": SipSin.SANG_GWAN,
        "무": SipSin.PYEON_JAE,  "기": SipSin.JEONG_JAE,
        "경": SipSin.PYEON_GWAN, "신": SipSin.JEONG_GWAN,
        "임": SipSin.PYEON_IN,   "계": SipSin.JEONG_IN
    },
    # 일간이 을목일 때
    "을": {
        "갑": SipSin.GYEOP_JAE,  "을": SipSin.BI_JIAN,
        "병": SipSin.SANG_GWAN,  "정": SipSin.SIK_SIN,
        "무": SipSin.JEONG_JAE,  "기": SipSin.PYEON_JAE,
        "경": SipSin.JEONG_GWAN,  "신": SipSin.PYEON_GWAN,
        "임": SipSin.JEONG_IN,   "계": SipSin.PYEON_IN
    },
    # 일간이 병화일 때
    "병": {
        "갑": SipSin.PYEON_IN,   "을": SipSin.JEONG_IN,
        "병": SipSin.BI_JIAN,   "정": SipSin.GYEOP_JAE,
        "무": SipSin.SIK_SIN,   "기": SipSin.SANG_GWAN,
        "경": SipSin.PYEON_JAE,  "신": SipSin.JEONG_JAE,
        "임": SipSin.PYEON_GWAN, "계": SipSin.JEONG_GWAN
    },
    # 일간이 정화일 때
    "정": {
        "갑": SipSin.JEONG_IN,   "을": SipSin.PYEON_IN,
        "병": SipSin.GYEOP_JAE,  "정": SipSin.BI_JIAN,
        "무": SipSin.SANG_GWAN,  "기": SipSin.SIK_SIN,
        "경": SipSin.JEONG_JAE,  "신": SipSin.PYEON_JAE,
        "임": SipSin.JEONG_GWAN,  "계": SipSin.PYEON_GWAN
    },
    # 일간이 무토일 때
    "무": {
        "갑": SipSin.PYEON_GWAN, "을": SipSin.JEONG_GWAN,
        "병": SipSin.PYEON_IN,   "정": SipSin.JEONG_IN,
        "무": SipSin.BI_JIAN,   "기": SipSin.GYEOP_JAE,
        "경": SipSin.SIK_SIN,   "신": SipSin.SANG_GWAN,
        "임": SipSin.PYEON_JAE,  "계": SipSin.JEONG_JAE
    },
    # 일간이 기토일 때
    "기": {
        "갑": SipSin.JEONG_GWAN,  "을": SipSin.PYEON_GWAN,
        "병": SipSin.JEONG_IN,   "정": SipSin.PYEON_IN,
        "무": SipSin.GYEOP_JAE,  "기": SipSin.BI_JIAN,
        "경": SipSin.SANG_GWAN,  "신": SipSin.SIK_SIN,
        "임": SipSin.JEONG_JAE,  "계": SipSin.PYEON_JAE
    },
    # 일간이 경금일 때
    "경": {
        "갑": SipSin.PYEON_JAE,  "을": SipSin.JEONG_JAE,
        "병": SipSin.PYEON_GWAN, "정": SipSin.JEONG_GWAN,
        "무": SipSin.PYEON_IN,   "기": SipSin.JEONG_IN,
        "경": SipSin.BI_JIAN,   "신": SipSin.GYEOP_JAE,
        "임": SipSin.SIK_SIN,   "계": SipSin.SANG_GWAN
    },
    # 일간이 신금일 때
    "신": {
        "갑": SipSin.JEONG_JAE,  "을": SipSin.PYEON_JAE,
        "병": SipSin.JEONG_GWAN,  "정": SipSin.PYEON_GWAN,
        "무": SipSin.JEONG_IN,   "기": SipSin.PYEON_IN,
        "경": SipSin.GYEOP_JAE,  "신": SipSin.BI_JIAN,
        "임": SipSin.SANG_GWAN,  "계": SipSin.SIK_SIN
    },
    # 일간이 임수일 때
    "임": {
        "갑": SipSin.SIK_SIN,   "을": SipSin.SANG_GWAN,
        "병": SipSin.PYEON_JAE,  "정": SipSin.JEONG_JAE,
        "무": SipSin.PYEON_GWAN, "기": SipSin.JEONG_GWAN,
        "경": SipSin.PYEON_IN,   "신": SipSin.JEONG_IN,
        "임": SipSin.BI_JIAN,   "계": SipSin.GYEOP_JAE
    },
    # 일간이 계수일 때
    "계": {
        "갑": SipSin.SANG_GWAN,  "을": SipSin.SIK_SIN,
        "병": SipSin.JEONG_JAE,  "정": SipSin.PYEON_JAE,
        "무": SipSin.JEONG_GWAN,  "기": SipSin.PYEON_GWAN,
        "경": SipSin.JEONG_IN,   "신": SipSin.PYEON_IN,
        "임": SipSin.GYEOP_JAE,  "계": SipSin.BI_JIAN
    }
}

# 오행 상생관계 (相生)
WUXING_SAENGSAENG = {
    WuXing.WOOD: WuXing.FIRE,    # 목생화
    WuXing.FIRE: WuXing.EARTH,   # 화생토
    WuXing.EARTH: WuXing.METAL,  # 토생금
    WuXing.METAL: WuXing.WATER,  # 금생수
    WuXing.WATER: WuXing.WOOD    # 수생목
}

# 오행 상극관계 (相剋)
WUXING_SANGGEUK = {
    WuXing.WOOD: WuXing.EARTH,   # 목극토
    WuXing.FIRE: WuXing.METAL,   # 화극금
    WuXing.EARTH: WuXing.WATER,  # 토극수
    WuXing.METAL: WuXing.WOOD,   # 금극목
    WuXing.WATER: WuXing.FIRE    # 수극화
}

# 계절별 왕상휴수사 (旺相休囚死)
SEASONAL_WUXING_STRENGTH = {
    "spring": {  # 봄 (인묘진월)
        WuXing.WOOD: "왕",     # 木旺
        WuXing.FIRE: "상",     # 火相
        WuXing.EARTH: "사",    # 土死
        WuXing.METAL: "수",    # 金囚
        WuXing.WATER: "휴"     # 水休
    },
    "summer": {  # 여름 (사오미월)
        WuXing.FIRE: "왕",     # 火旺
        WuXing.EARTH: "상",    # 土相
        WuXing.METAL: "사",    # 金死
        WuXing.WATER: "수",    # 水囚
        WuXing.WOOD: "휴"      # 木休
    },
    "autumn": {  # 가을 (신유술월)
        WuXing.METAL: "왕",    # 金旺
        WuXing.WATER: "상",    # 水相
        WuXing.WOOD: "사",     # 木死
        WuXing.FIRE: "수",     # 火囚
        WuXing.EARTH: "휴"     # 土休
    },
    "winter": {  # 겨울 (해자축월)
        WuXing.WATER: "왕",    # 水旺
        WuXing.WOOD: "상",     # 木相
        WuXing.FIRE: "사",     # 火死
        WuXing.EARTH: "수",    # 土囚
        WuXing.METAL: "휴"     # 金休
    }
}

# 계절별 월 매핑
SEASON_MONTHS = {
    "spring": [2, 3, 4],   # 인묘진월 (음력)
    "summer": [5, 6, 7],   # 사오미월
    "autumn": [8, 9, 10],  # 신유술월
    "winter": [11, 12, 1]  # 해자축월
}

# 격국 판정용 월령 매핑
MONTH_TO_JIJI = {
    1: "축",  2: "인",  3: "묘",  4: "진",
    5: "사",  6: "오",  7: "미",  8: "신",
    9: "유",  10: "술", 11: "해", 12: "자"
}

# 십신별 성격 특성
SIPSIN_CHARACTERISTICS = {
    SipSin.BI_JIAN: {
        "성격": ["독립적", "주관이 뚜렷", "자신감", "고집"],
        "장점": ["추진력", "리더십", "결단력"],
        "단점": ["고집", "독선", "타인 의견 무시"]
    },
    SipSin.GYEOP_JAE: {
        "성격": ["경쟁심", "활동적", "도전적", "변화 추구"],
        "장점": ["적응력", "추진력", "혁신성"],
        "단점": ["성급함", "변덕", "안정성 부족"]
    },
    SipSin.SIK_SIN: {
        "성격": ["온화함", "배려", "예술적", "창의적"],
        "장점": ["표현력", "창조성", "사교성"],
        "단점": ["현실감 부족", "우유부단", "감정적"]
    },
    SipSin.SANG_GWAN: {
        "성격": ["재능", "개성", "자유분방", "반항적"],
        "장점": ["창의력", "예술성", "독창성"],
        "단점": ["반항심", "규칙 무시", "극단적"]
    },
    SipSin.PYEON_JAE: {
        "성격": ["현실적", "합리적", "기회주의", "활동적"],
        "장점": ["사업 수완", "현실 감각", "적응력"],
        "단점": ["이기적", "변덕", "의리 부족"]
    },
    SipSin.JEONG_JAE: {
        "성격": ["신중함", "책임감", "보수적", "안정 추구"],
        "장점": ["신뢰성", "성실성", "관리 능력"],
        "단점": ["융통성 부족", "소극적", "변화 거부"]
    },
    SipSin.PYEON_GWAN: {
        "성격": ["강인함", "투쟁심", "불굴의 의지", "권위적"],
        "장점": ["추진력", "극복력", "리더십"],
        "단점": ["공격적", "독선적", "스트레스"]
    },
    SipSin.JEONG_GWAN: {
        "성격": ["품격", "예의", "질서", "명예 중시"],
        "장점": ["신뢰성", "도덕성", "리더십"],
        "단점": ["완고함", "형식주의", "경직성"]
    },
    SipSin.PYEON_IN: {
        "성격": ["독특함", "개성", "직관적", "신비주의"],
        "장점": ["통찰력", "창의성", "독창성"],
        "단점": ["편견", "극단적", "사회성 부족"]
    },
    SipSin.JEONG_IN: {
        "성격": ["지혜", "학구적", "인자함", "보호본능"],
        "장점": ["학습 능력", "포용력", "지도력"],
        "단점": ["우유부단", "수동적", "의존성"]
    }
}

# 십신별 적성 분야
SIPSIN_APTITUDES = {
    SipSin.BI_JIAN: ["경영", "독립사업", "스포츠", "군인"],
    SipSin.GYEOP_JAE: ["영업", "마케팅", "엔터테인먼트", "모험가"],
    SipSin.SIK_SIN: ["예술", "요리", "서비스업", "교육"],
    SipSin.SANG_GWAN: ["디자인", "방송", "연예", "창작"],
    SipSin.PYEON_JAE: ["무역", "유통", "투자", "부동산"],
    SipSin.JEONG_JAE: ["은행", "회계", "관리", "공무원"],
    SipSin.PYEON_GWAN: ["법조", "군경", "스포츠", "경쟁업계"],
    SipSin.JEONG_GWAN: ["공직", "대기업", "교육", "의료"],
    SipSin.PYEON_IN: ["연구", "종교", "예술", "상담"],
    SipSin.JEONG_IN: ["교육", "의료", "학문", "복지"]
}

def normalize_to_hangul(char: str) -> str:
    """한자를 한글로 변환 (필요시)"""
    return HANJA_TO_HANGUL.get(char, char)

def get_cheongan_wuxing(cheongan: str) -> WuXing:
    """천간의 오행 반환 (한자/한글 자동 처리)"""
    hangul_cheongan = normalize_to_hangul(cheongan)
    return CHEONGAN_WUXING.get(hangul_cheongan)

def get_jiji_wuxing(jiji: str) -> WuXing:
    """지지의 오행 반환 (한자/한글 자동 처리)"""
    hangul_jiji = normalize_to_hangul(jiji)
    return JIJI_WUXING.get(hangul_jiji)

def get_sipsin_relation(ilgan: str, target: str) -> SipSin:
    """일간 기준 십신 관계 반환 (한자/한글 자동 처리)"""
    hangul_ilgan = normalize_to_hangul(ilgan)
    hangul_target = normalize_to_hangul(target)
    return SIPSIN_RELATIONS.get(hangul_ilgan, {}).get(hangul_target)

def get_jijanggan(jiji: str) -> List[Tuple[str, int]]:
    """지지의 지장간 반환 (한자/한글 자동 처리)"""
    hangul_jiji = normalize_to_hangul(jiji)
    return JIJANGGAN.get(hangul_jiji, [])

def get_season_by_month(month: int) -> str:
    """월로 계절 판정"""
    for season, months in SEASON_MONTHS.items():
        if month in months:
            return season
    return "spring"  # 기본값

def get_wuxing_strength_in_season(wuxing: WuXing, season: str) -> str:
    """계절별 오행 왕상휴수사 반환"""
    return SEASONAL_WUXING_STRENGTH.get(season, {}).get(wuxing, "휴")