"""
HEAL7 사주명리학 관리자 설정 시스템
사주 계산 로직의 모든 핵심 설정을 관리하는 중앙화된 설정 체계
"""

from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Literal, Union
from enum import Enum
from datetime import datetime
import json

# --- 기본 설정 열거형들 ---

class TimeZoneSystem(Enum):
    """시간 체계"""
    STANDARD = "standard"  # 표준시
    APPARENT_SOLAR = "apparent_solar"  # 진태양시

class SajuLogicType(Enum):
    """사주 로직 타입"""
    TRADITIONAL = "traditional"  # 전통사주
    MODERN = "modern"  # 현대사주
    HYBRID = "hybrid"  # 하이브리드

class CalendarSystem(Enum):
    """달력 시스템"""
    JULIAN = "julian"  # 율리우스력
    GREGORIAN = "gregorian"  # 그레고리력

class CountryCode(Enum):
    """국가 코드 (경도 설정용)"""
    KOREA = "KR"  # 한국 (127.5°E)
    USA = "US"  # 미국 (다양한 시간대)
    JAPAN = "JP"  # 일본 (135°E)
    CHINA = "CN"  # 중국 (120°E)
    EUROPE = "EU"  # 유럽 (다양한 시간대)

# --- 핵심 설정 모델들 ---

class TimeSettings(BaseModel):
    """시간 관련 설정"""
    timezone_system: TimeZoneSystem = TimeZoneSystem.STANDARD
    use_sidubup: bool = Field(True, description="시두법 적용 여부")
    use_woldubup: bool = Field(True, description="월두법 적용 여부")
    calendar_system: CalendarSystem = CalendarSystem.GREGORIAN
    
class GeographicSettings(BaseModel):
    """지리적 설정"""
    default_country: CountryCode = CountryCode.KOREA
    longitude_offset: float = Field(127.5, description="기준 경도")
    timezone_offset: float = Field(9.0, description="시간대 오프셋")
    
    # 다국가 경도 설정
    country_longitudes: Dict[str, float] = Field(default_factory=lambda: {
        "KR": 127.5,  # 한국
        "US": -75.0,  # 미국 동부
        "JP": 135.0,  # 일본
        "CN": 120.0,  # 중국
        "EU": 15.0,   # 유럽 중부
    })

class SajuLogicSettings(BaseModel):
    """사주 로직 설정"""
    logic_type: SajuLogicType = SajuLogicType.HYBRID
    use_kasi_precision: bool = Field(True, description="KASI 정밀 계산 사용")
    manseeryeok_count: int = Field(74000, description="만세력 데이터 개수")
    hybrid_voting_threshold: float = Field(0.7, description="하이브리드 다수결 임계값")
    
class KasiSettings(BaseModel):
    """KASI API 설정"""
    api_key: str = Field(default="", description="KASI API 키")
    base_url: str = Field(
        default="http://apis.data.go.kr/B090041/openapi/service/SpcdeInfoService",
        description="KASI API 베이스 URL"
    )
    use_cache: bool = Field(True, description="KASI 결과 캐시 사용")
    cache_ttl: int = Field(86400, description="캐시 TTL (초)")

class CheonganInterpretation(BaseModel):
    """천간 해석"""
    korean_name: str
    chinese_char: str
    element: str  # 오행
    yin_yang: str  # 음양
    keywords: List[str] = Field(default_factory=list)
    description: str = ""
    personality_traits: List[str] = Field(default_factory=list)
    
class JijiInterpretation(BaseModel):
    """지지 해석"""
    korean_name: str
    chinese_char: str
    zodiac_animal: str  # 십이지
    element: str  # 오행
    season: str  # 계절
    keywords: List[str] = Field(default_factory=list)
    description: str = ""
    personality_traits: List[str] = Field(default_factory=list)

class GapjaInterpretation(BaseModel):
    """60갑자 해석"""
    korean_name: str
    cheongan: str  # 천간
    jiji: str  # 지지
    napyin: str  # 납음
    keywords: List[str] = Field(default_factory=list)
    description: str = ""
    compatibility: Dict[str, str] = Field(default_factory=dict)  # 궁합 정보
    fortune_aspects: Dict[str, str] = Field(default_factory=dict)  # 운세 측면

class JijangganSettings(BaseModel):
    """지장간 설정"""
    data: Dict[str, List[Dict[str, Union[str, int]]]] = Field(default_factory=lambda: {
        "자": [{"cheongan": "계", "strength": 100}],
        "축": [{"cheongan": "기", "strength": 60}, {"cheongan": "계", "strength": 30}, {"cheongan": "신", "strength": 10}],
        # ... 나머지 지지들
    })

class GyeokgukSettings(BaseModel):
    """격국 설정"""
    rules: Dict[str, Dict] = Field(default_factory=dict)
    priority_order: List[str] = Field(default_factory=list)

class DaewoonSettings(BaseModel):
    """대운 설정"""
    start_age_calculation: Literal["korean", "international"] = "korean"
    gender_reverse_rule: bool = Field(True, description="남녀 순역 규칙 적용")

# --- 통합 관리자 설정 ---

class SajuAdminSettings(BaseModel):
    """사주 관리자 설정 통합 모델"""
    
    # 기본 정보
    version: str = Field("2.0.0", description="설정 버전")
    last_updated: datetime = Field(default_factory=datetime.now)
    updated_by: str = Field("system", description="최종 수정자")
    
    # 핵심 설정들
    time_settings: TimeSettings = Field(default_factory=TimeSettings)
    geographic_settings: GeographicSettings = Field(default_factory=GeographicSettings)
    logic_settings: SajuLogicSettings = Field(default_factory=SajuLogicSettings)
    kasi_settings: KasiSettings = Field(default_factory=KasiSettings)
    
    # 지장간, 격국, 대운 설정
    jijanggan_settings: JijangganSettings = Field(default_factory=JijangganSettings)
    gyeokguk_settings: GyeokgukSettings = Field(default_factory=GyeokgukSettings)
    daewoon_settings: DaewoonSettings = Field(default_factory=DaewoonSettings)
    
    # 해석 데이터
    cheongan_interpretations: Dict[str, CheonganInterpretation] = Field(default_factory=dict)
    jiji_interpretations: Dict[str, JijiInterpretation] = Field(default_factory=dict)  
    gapja_interpretations: Dict[str, GapjaInterpretation] = Field(default_factory=dict)
    
    # 24절기 설정
    solar_terms: Dict[str, Dict] = Field(default_factory=dict)
    
    # 일주 60갑자 기준점
    ilju_reference_points: Dict[str, Dict] = Field(default_factory=dict)
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
        
    def to_json(self) -> str:
        """JSON 문자열로 변환"""
        return self.model_dump_json(indent=2, by_alias=False)
    
    @classmethod
    def from_json(cls, json_str: str) -> 'SajuAdminSettings':
        """JSON 문자열에서 생성"""
        return cls.model_validate_json(json_str)
    
    def save_to_file(self, file_path: str):
        """파일로 저장"""
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(self.to_json())
    
    @classmethod
    def load_from_file(cls, file_path: str) -> 'SajuAdminSettings':
        """파일에서 로드"""
        with open(file_path, 'r', encoding='utf-8') as f:
            return cls.from_json(f.read())

# --- 기본 데이터 초기화 함수들 ---

def initialize_default_cheongan() -> Dict[str, CheonganInterpretation]:
    """천간 기본 해석 데이터 초기화 - 10개 천간 완전 구현"""
    return {
        "갑": CheonganInterpretation(
            korean_name="갑",
            chinese_char="甲",
            element="목",
            yin_yang="양",
            keywords=["지도력", "개척정신", "강직함"],
            description="큰 나무와 같은 성질로 곧고 강직하며 개척정신이 강함",
            personality_traits=["리더십", "정의감", "추진력", "고집"]
        ),
        "을": CheonganInterpretation(
            korean_name="을",
            chinese_char="乙", 
            element="목",
            yin_yang="음",
            keywords=["유연함", "적응력", "섬세함"],
            description="작은 나무나 꽃과 같은 성질로 유연하고 적응력이 뛰어남",
            personality_traits=["유연성", "협조성", "예술성", "감성적"]
        ),
        "병": CheonganInterpretation(
            korean_name="병",
            chinese_char="丙",
            element="화",
            yin_yang="양",
            keywords=["열정", "창조력", "밝음"],
            description="태양의 성질로 밝고 열정적이며 창조적인 에너지가 강함",
            personality_traits=["활발함", "적극성", "창의성", "직선적"]
        ),
        "정": CheonganInterpretation(
            korean_name="정",
            chinese_char="丁",
            element="화",
            yin_yang="음",
            keywords=["따뜻함", "배려", "세심함"],
            description="촛불의 성질로 따뜻하고 섬세하며 배려심이 깊음",
            personality_traits=["온화함", "세심함", "인내심", "봉사정신"]
        ),
        "무": CheonganInterpretation(
            korean_name="무",
            chinese_char="戊",
            element="토",
            yin_yang="양",
            keywords=["포용력", "신뢰성", "안정감"],
            description="산의 성질로 포용력이 크고 신뢰할 수 있으며 안정적임",
            personality_traits=["포용력", "신중함", "책임감", "보수적"]
        ),
        "기": CheonganInterpretation(
            korean_name="기",
            chinese_char="己",
            element="토",
            yin_yang="음",
            keywords=["겸손", "실용성", "섬세함"],
            description="밭의 성질로 겸손하고 실용적이며 세심한 배려를 함",
            personality_traits=["겸손함", "꼼꼼함", "현실적", "친화력"]
        ),
        "경": CheonganInterpretation(
            korean_name="경",
            chinese_char="庚",
            element="금",
            yin_yang="양",
            keywords=["강인함", "정의감", "원칙주의"],
            description="칼의 성질로 강인하고 정의로우며 원칙을 중시함",
            personality_traits=["의지력", "결단력", "공정함", "엄격함"]
        ),
        "신": CheonganInterpretation(
            korean_name="신",
            chinese_char="辛",
            element="금",
            yin_yang="음",
            keywords=["세련됨", "정교함", "미적감각"],
            description="보석의 성질로 세련되고 정교하며 미적 감각이 뛰어남",
            personality_traits=["섬세함", "완벽주의", "예술성", "신경질적"]
        ),
        "임": CheonganInterpretation(
            korean_name="임",
            chinese_char="壬",
            element="수",
            yin_yang="양",
            keywords=["지혜", "유연함", "포용력"],
            description="바다의 성질로 지혜롭고 유연하며 모든 것을 포용함",
            personality_traits=["지혜로움", "적응력", "포용력", "변화무쌍"]
        ),
        "계": CheonganInterpretation(
            korean_name="계",
            chinese_char="癸",
            element="수",
            yin_yang="음",
            keywords=["순수함", "직관력", "신비로움"],
            description="이슬의 성질로 순수하고 직관력이 뛰어나며 신비로운 면이 있음",
            personality_traits=["순수함", "직관력", "상상력", "내성적"]
        )
    }

def initialize_default_jiji() -> Dict[str, JijiInterpretation]:
    """지지 기본 해석 데이터 초기화 - 12개 지지 완전 구현"""
    return {
        "자": JijiInterpretation(
            korean_name="자",
            chinese_char="子",
            zodiac_animal="쥐",
            element="수",
            season="겨울",
            keywords=["지혜", "민첩성", "적응력"],
            description="쥐의 성질로 영리하고 적응력이 뛰어나며 기회를 잘 포착함",
            personality_traits=["영리함", "기민함", "사교성", "현실적"]
        ),
        "축": JijiInterpretation(
            korean_name="축",
            chinese_char="丑",
            zodiac_animal="소",
            element="토",
            season="겨울",
            keywords=["근면", "성실", "인내력"],
            description="소의 성질로 근면하고 성실하며 강한 인내력을 가짐",
            personality_traits=["성실함", "끈기", "책임감", "보수적"]
        ),
        "인": JijiInterpretation(
            korean_name="인",
            chinese_char="寅",
            zodiac_animal="호랑이",
            element="목",
            season="봄",
            keywords=["용맹", "도전정신", "카리스마"],
            description="호랑이의 성질로 용맹하고 도전정신이 강하며 카리스마가 있음",
            personality_traits=["용감함", "독립적", "진취적", "자존심"]
        ),
        "묘": JijiInterpretation(
            korean_name="묘",
            chinese_char="卯",
            zodiac_animal="토끼",
            element="목",
            season="봄",
            keywords=["온순함", "조심스러움", "예의"],
            description="토끼의 성질로 온순하고 조심스러우며 예의를 중시함",
            personality_traits=["온화함", "신중함", "예의바름", "평화주의"]
        ),
        "진": JijiInterpretation(
            korean_name="진",
            chinese_char="辰",
            zodiac_animal="용",
            element="토",
            season="봄",
            keywords=["웅대함", "권위", "변화"],
            description="용의 성질로 웅대하고 권위적이며 변화를 주도함",
            personality_traits=["웅장함", "권위적", "변화무쌍", "야심적"]
        ),
        "사": JijiInterpretation(
            korean_name="사",
            chinese_char="巳",
            zodiac_animal="뱀",
            element="화",
            season="여름",
            keywords=["지혜", "신비로움", "직관력"],
            description="뱀의 성질로 지혜롭고 신비로우며 뛰어난 직관력을 가짐",
            personality_traits=["지혜로움", "신비로움", "직관적", "집중력"]
        ),
        "오": JijiInterpretation(
            korean_name="오",
            chinese_char="午",
            zodiac_animal="말",
            element="화",
            season="여름",
            keywords=["활동력", "열정", "자유로움"],
            description="말의 성질로 활동력이 넘치고 열정적이며 자유를 추구함",
            personality_traits=["활발함", "열정적", "자유분방", "직진적"]
        ),
        "미": JijiInterpretation(
            korean_name="미",
            chinese_char="未",
            zodiac_animal="양",
            element="토",
            season="여름",
            keywords=["온화함", "예술성", "감성"],
            description="양의 성질로 온화하고 예술적 감각이 뛰어나며 감성적임",
            personality_traits=["온순함", "예술적", "감성적", "배려심"]
        ),
        "신": JijiInterpretation(
            korean_name="신",
            chinese_char="申",
            zodiac_animal="원숭이",
            element="금",
            season="가을",
            keywords=["재치", "유머", "창의성"],
            description="원숭이의 성질로 재치가 있고 유머러스하며 창의적임",
            personality_traits=["재치있음", "유머러스", "창의적", "활발함"]
        ),
        "유": JijiInterpretation(
            korean_name="유",
            chinese_char="酉",
            zodiac_animal="닭",
            element="금",
            season="가을",
            keywords=["정확성", "성실", "책임감"],
            description="닭의 성질로 정확하고 성실하며 강한 책임감을 가짐",
            personality_traits=["정확함", "성실함", "꼼꼼함", "시간관념"]
        ),
        "술": JijiInterpretation(
            korean_name="술",
            chinese_char="戌",
            zodiac_animal="개",
            element="토",
            season="가을",
            keywords=["충성심", "정의감", "보호본능"],
            description="개의 성질로 충성스럽고 정의로우며 보호 본능이 강함",
            personality_traits=["충성심", "정의감", "보호본능", "솔직함"]
        ),
        "해": JijiInterpretation(
            korean_name="해",
            chinese_char="亥",
            zodiac_animal="돼지",
            element="수",
            season="겨울",
            keywords=["순수함", "관대함", "풍요"],
            description="돼지의 성질로 순수하고 관대하며 풍요로움을 상징함",
            personality_traits=["순수함", "관대함", "후덕함", "단순함"]
        )
    }

# --- 싱글톤 관리 ---
_admin_settings: Optional[SajuAdminSettings] = None

def get_admin_settings() -> SajuAdminSettings:
    """관리자 설정 인스턴스 반환"""
    global _admin_settings
    if _admin_settings is None:
        _admin_settings = SajuAdminSettings()
        # 기본 데이터 초기화
        _admin_settings.cheongan_interpretations = initialize_default_cheongan()
        _admin_settings.jiji_interpretations = initialize_default_jiji()
    return _admin_settings

def update_admin_settings(new_settings: SajuAdminSettings):
    """관리자 설정 업데이트"""
    global _admin_settings
    _admin_settings = new_settings
    _admin_settings.last_updated = datetime.now()
    return _admin_settings