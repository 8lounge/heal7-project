"""
HEAL7 사주명리학 시스템 - 서비스 레이어

핵심 비즈니스 로직을 담당하는 서비스 클래스들을 정의합니다.
각 서비스는 비동기 처리, 에러 핸들링, 캐싱, 로깅을 지원합니다.

서비스 구조:
- KASIService: KASI API 통합 및 24절기 데이터 관리
- AIService: OpenAI, Anthropic, Google AI 통합
- DatabaseService: PostgreSQL/SQLite 통합 관리  
- SajuService: 사주 계산 및 분석 엔진 (핵심)

Usage:
    from services import SajuService, KASIService
    
    saju_service = SajuService()
    await saju_service.initialize()
    
    # 사주 계산
    result = await saju_service.calculate_saju(birth_info)
    
    # AI 분석
    ai_analysis = await saju_service.analyze_with_ai(result, AnalysisType.FORTUNE)
"""

from .kasi_service import (
    KASIService, 
    SolarTermData, 
    SolarTermType,
    KASIAPIResponse
)

# AI 서비스는 향후 통합 예정 - 현재 보류
# from .ai_service import (
#     AIService,
#     AIProvider,
#     AnalysisType, 
#     AIRequest,
#     AIResponse,
#     TokenUsage
# )

from .database_service import (
    DatabaseService,
    DatabaseType,
    QueryResult,
    DatabaseStats,
    DatabaseConnection
)

from .saju_service import (
    SajuService,
    BirthInfo,
    SajuResult,
    Gender,
    ElementType,
    SipsinType,
    Pillar
)

__all__ = [
    # 서비스 클래스들
    "KASIService",
    # "AIService",  # 현재 보류
    "DatabaseService",
    "SajuService",
    
    # KASI 관련
    "SolarTermData",
    "SolarTermType", 
    "KASIAPIResponse",
    
    # AI 관련 (현재 보류)
    # "AIProvider",
    # "AnalysisType",
    # "AIRequest", 
    # "AIResponse",
    # "TokenUsage",
    
    # 데이터베이스 관련
    "DatabaseType",
    "QueryResult",
    "DatabaseStats",
    "DatabaseConnection",
    
    # 사주 관련
    "BirthInfo",
    "SajuResult", 
    "Gender",
    "ElementType",
    "SipsinType",
    "Pillar"
]

# 서비스 버전 정보
__version__ = "1.0.0"
__author__ = "HEAL7 Development Team"
__description__ = "HEAL7 사주명리학 시스템 - 현대적 사주 계산 및 AI 분석 서비스"