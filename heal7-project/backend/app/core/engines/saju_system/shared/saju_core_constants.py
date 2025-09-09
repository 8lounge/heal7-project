
from enum import Enum
from typing import List, Tuple, Optional

# 🔥 중복 제거: atomic 모듈에서 단일 소스로 import
from ....core.atomic.constants import GANJI_60 as ATOMIC_GANJI_60

# --- Heavenly Stems (천간) ---
class Cheongan(Enum):
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

# --- Earthly Branches (지지) ---
class Jiji(Enum):
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

# --- Five Elements (오행) ---
class WuXing(Enum):
    MOK = "목"
    HWA = "화"
    TO = "토"
    GEUM = "금"
    SU = "수"

# --- Ten Gods (십신) ---
class SipSin(Enum):
    BI_GYEON = "비견"
    GEOB_JAE = "겁재"
    SIG_SIN = "식신"
    SANG_GWAN = "상관"
    PYEON_JAE = "편재"
    JEONG_JAE = "정재"
    PYEON_GWAN = "편관"
    JEONG_GWAN = "정관"
    PYEON_IN = "편인"
    JEONG_IN = "정인"

# --- Ganji (갑자) ---
# 🔥 중복 제거: atomic/constants.py에서 import된 배열 사용
GANJI_60 = ATOMIC_GANJI_60

# --- Myeongrihak Constants and Helper Functions (from saju_system/myeongrihak_constants.py) ---

CHEONGAN_WUXING = {
    Cheongan.GAB: WuXing.MOK, Cheongan.EUL: WuXing.MOK,
    Cheongan.BYEONG: WuXing.HWA, Cheongan.JEONG: WuXing.HWA,
    Cheongan.MU: WuXing.TO, Cheongan.GI: WuXing.TO,
    Cheongan.GYEONG: WuXing.GEUM, Cheongan.SIN: WuXing.GEUM,
    Cheongan.IM: WuXing.SU, Cheongan.GYE: WuXing.SU
}

JIJI_WUXING = {
    Jiji.IN: WuXing.MOK, Jiji.MYO: WuXing.MOK,
    Jiji.SA: WuXing.HWA, Jiji.O: WuXing.HWA,
    Jiji.JIN: WuXing.TO, Jiji.SUL: WuXing.TO, Jiji.CHUK: WuXing.TO, Jiji.MI: WuXing.TO,
    Jiji.SIN: WuXing.GEUM, Jiji.YU: WuXing.GEUM,
    Jiji.JA: WuXing.SU, Jiji.HAE: WuXing.SU
}

JIJANGGAN = {
    Jiji.JA: [("임", 10), ("계", 20)],
    Jiji.CHUK: [("계", 9), ("신", 3), ("기", 18)],
    Jiji.IN: [("무", 7), ("병", 7), ("갑", 16)],
    Jiji.MYO: [("갑", 10), ("을", 20)],
    Jiji.JIN: [("을", 9), ("계", 3), ("무", 18)],
    Jiji.SA: [("무", 7), ("경", 7), ("병", 16)],
    Jiji.O: [("병", 10), ("기", 10), ("정", 10)],
    Jiji.MI: [("정", 9), ("을", 3), ("기", 18)],
    Jiji.SIN: [("경", 10), ("임", 20)],
    Jiji.YU: [("경", 10), ("신", 20)],
    Jiji.SUL: [("신", 9), ("정", 3), ("무", 18)],
    Jiji.HAE: [("무", 7), ("갑", 7), ("임", 16)]
}

def split_ganji(ganji: str) -> Tuple[str, str]:
    """갑자(ganji)를 천간(gan)과 지지(ji)로 분리합니다."""
    if len(ganji) != 2:
        raise ValueError("Ganji must be a 2-character string.")
    return ganji[0], ganji[1]

def get_sipsin_relation(ilgan: str, target_gan: str) -> Optional[SipSin]:
    """일간(ilgan)과 대상 천간(target_gan)의 십신 관계를 반환합니다."""
    # Placeholder for actual sipsin calculation logic
    # This would involve complex rules based on ilgan and target_gan's wuxing and yin/yang
    return SipSin.BI_GYEON # Dummy value

def get_jijanggan(jiji: Jiji) -> List[Tuple[str, int]]:
    """지지(jiji)의 지장간 정보를 반환합니다."""
    return JIJANGGAN.get(jiji, [])

def get_cheongan_wuxing(cheongan: Cheongan) -> Optional[WuXing]:
    """천간(cheongan)의 오행을 반환합니다."""
    return CHEONGAN_WUXING.get(cheongan)

def get_jiji_wuxing(jiji: Jiji) -> Optional[WuXing]:
    """지지(jiji)의 오행을 반환합니다."""
    return JIJI_WUXING.get(jiji)
