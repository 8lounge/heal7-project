"""
HEAL7 프로젝트 - 현대적 타입 정의
SQLAlchemy 2.0 및 FastAPI와 완전 호환되는 타입 시스템

@author HEAL7 Team
@version 2.0.0
@updated 2025-08-31
"""

from typing import (
    TypeVar, Generic, Optional, List, Dict, Any, Union, Tuple, Set,
    Protocol, TypedDict, Literal, Annotated, AsyncGenerator, Generator
)
from typing_extensions import NotRequired
from pydantic import BaseModel, Field, ConfigDict, validator
from sqlalchemy.orm import Mapped
from datetime import datetime, date
from decimal import Decimal
from enum import Enum
import uuid

# ================================
# 🔧 Generic Types
# ================================

T = TypeVar('T')
ModelType = TypeVar('ModelType', bound=BaseModel)
EntityType = TypeVar('EntityType')

# ID Types
UserId = Annotated[str, Field(description="사용자 고유 ID")]
DreamId = Annotated[int, Field(description="꿈풀이 고유 ID", gt=0)]
CategoryId = Annotated[int, Field(description="카테고리 고유 ID", gt=0)]
SessionId = Annotated[str, Field(description="세션 고유 ID")]

# Score Types  
ConfidenceScore = Annotated[float, Field(description="신뢰도 점수", ge=0.0, le=1.0)]
AccuracyRating = Annotated[float, Field(description="정확도 평가", ge=0.0, le=5.0)]
TrendScore = Annotated[float, Field(description="트렌드 점수", ge=0.0, le=1.0)]

# ================================
# 🌙 Dream Service Enums
# ================================

class FortuneAspect(str, Enum):
    """운세 측면"""
    POSITIVE = "positive"
    NEGATIVE = "negative" 
    NEUTRAL = "neutral"

class SearchMode(str, Enum):
    """검색 모드"""
    ANY = "any"        # 하나라도 일치
    ALL = "all"        # 모두 일치
    FUZZY = "fuzzy"    # 유사도 검색

class SourceQuality(str, Enum):
    """데이터 소스 품질"""
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    UNKNOWN = "unknown"

class DreamMood(str, Enum):
    """꿈의 기분"""
    HAPPY = "happy"
    SCARY = "scary"
    PEACEFUL = "peaceful"
    ANXIOUS = "anxious"
    CONFUSED = "confused"
    EXCITED = "excited"

# ================================
# 🎯 TypedDict Protocols
# ================================

class DreamSearchFilters(TypedDict, total=False):
    """꿈풀이 검색 필터"""
    categories: NotRequired[List[str]]
    fortune_aspect: NotRequired[FortuneAspect]
    confidence_threshold: NotRequired[ConfidenceScore]
    source_quality: NotRequired[List[SourceQuality]]
    verified_only: NotRequired[bool]
    date_range: NotRequired[Tuple[datetime, datetime]]

class SearchStatistics(TypedDict):
    """검색 통계"""
    total_results: int
    processing_time_ms: float
    cache_hit: bool
    filters_applied: int
    suggested_terms: List[str]

class DatabaseMetrics(TypedDict):
    """데이터베이스 메트릭스"""
    connection_pool_size: int
    active_connections: int
    total_queries: int
    avg_query_time_ms: float
    error_count: int

# ================================
# 🔧 Protocol Definitions
# ================================

class Searchable(Protocol):
    """검색 가능한 객체 프로토콜"""
    keyword: str
    search_frequency: int
    
    def matches_query(self, query: str) -> bool: ...

class Rateable(Protocol):
    """평가 가능한 객체 프로토콜"""
    user_rating_avg: Optional[float]
    confidence_score: ConfidenceScore
    
    def update_rating(self, rating: float) -> None: ...

class Timestamped(Protocol):
    """타임스탬프가 있는 객체 프로토콜"""
    created_at: datetime
    updated_at: Optional[datetime]

# ================================
# 🏗️ Base Response Models
# ================================

class BaseResponse(BaseModel):
    """기본 응답 모델"""
    model_config = ConfigDict(
        from_attributes=True,
        validate_assignment=True,
        use_enum_values=True,
        json_encoders={
            datetime: lambda v: v.isoformat(),
            date: lambda v: v.isoformat(),
            Decimal: lambda v: float(v)
        }
    )

class PaginatedResponse(BaseResponse, Generic[T]):
    """페이지네이션 응답"""
    items: List[T]
    total: int
    page: int = Field(ge=1)
    size: int = Field(ge=1, le=100)
    pages: int
    has_next: bool
    has_prev: bool

class APIResponse(BaseResponse, Generic[T]):
    """표준 API 응답"""
    success: bool = True
    data: Optional[T] = None
    message: Optional[str] = None
    errors: Optional[List[str]] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    request_id: Optional[str] = None

# ================================
# 🌙 Dream Service Specific Types  
# ================================

class KeywordVariant(BaseModel):
    """키워드 변형"""
    original: str
    variant: str
    similarity_score: ConfidenceScore
    usage_count: int = 0

class LuckyNumber(BaseModel):
    """행운 번호"""
    number: Annotated[int, Field(ge=1, le=99)]
    significance: Optional[str] = None
    cultural_meaning: Optional[str] = None

class DreamCombination(BaseModel):
    """꿈 조합"""
    primary_keyword: str
    secondary_keywords: List[str]
    combined_meaning: str
    strength_level: Annotated[int, Field(ge=1, le=5)]
    frequency: float = Field(ge=0.0, le=1.0)

class InterpretationPerspective(BaseModel):
    """해석 관점"""
    perspective_id: str
    name: str
    cultural_background: str
    interpretation: str
    confidence: ConfidenceScore
    tags: List[str] = []

# ================================
# 🔍 Search and Query Types
# ================================

class SearchQuery(BaseModel):
    """검색 쿼리"""
    terms: List[str] = Field(min_items=1, max_items=10)
    mode: SearchMode = SearchMode.ANY
    filters: Optional[DreamSearchFilters] = None
    limit: int = Field(default=20, ge=1, le=100)
    offset: int = Field(default=0, ge=0)

class QueryResult(BaseResponse, Generic[T]):
    """쿼리 결과"""
    items: List[T]
    total_count: int
    query_info: SearchStatistics
    suggestions: Optional[List[str]] = None

# ================================
# 🚀 Advanced Type Utilities
# ================================

class TypeSafeDict(Dict[str, T], Generic[T]):
    """타입 안전 딕셔너리"""
    def __init__(self, expected_type: type[T]) -> None:
        super().__init__()
        self._expected_type = expected_type
    
    def __setitem__(self, key: str, value: T) -> None:
        if not isinstance(value, self._expected_type):
            raise TypeError(f"Expected {self._expected_type}, got {type(value)}")
        super().__setitem__(key, value)

class Repository(Protocol, Generic[T]):
    """저장소 프로토콜"""
    async def get_by_id(self, id: int) -> Optional[T]: ...
    async def create(self, entity: T) -> T: ...
    async def update(self, entity: T) -> T: ...
    async def delete(self, id: int) -> bool: ...
    async def search(self, query: SearchQuery) -> QueryResult[T]: ...

# ================================
# 🧪 Validation Helpers
# ================================

def validate_keywords(keywords: List[str]) -> List[str]:
    """키워드 유효성 검사"""
    cleaned = []
    for keyword in keywords:
        clean_keyword = keyword.strip()
        if len(clean_keyword) >= 1 and len(clean_keyword) <= 50:
            cleaned.append(clean_keyword)
    return cleaned

def normalize_confidence_score(score: Union[int, float]) -> ConfidenceScore:
    """신뢰도 점수 정규화"""
    if isinstance(score, int):
        score = float(score)
    return max(0.0, min(1.0, score))

# ================================
# 🎯 Factory Functions
# ================================

def create_paginated_response(
    items: List[T],
    total: int,
    page: int,
    size: int
) -> PaginatedResponse[T]:
    """페이지네이션 응답 생성"""
    pages = (total + size - 1) // size
    return PaginatedResponse(
        items=items,
        total=total,
        page=page,
        size=size,
        pages=pages,
        has_next=page < pages,
        has_prev=page > 1
    )

def create_api_response(
    data: Optional[T] = None,
    message: Optional[str] = None,
    success: bool = True,
    errors: Optional[List[str]] = None
) -> APIResponse[T]:
    """API 응답 생성"""
    return APIResponse(
        success=success,
        data=data,
        message=message,
        errors=errors,
        request_id=str(uuid.uuid4())
    )

# ================================
# 🔗 SQLAlchemy 2.0 Integration
# ================================

# Modern Mapped type aliases
MappedId = Mapped[int]
MappedStr = Mapped[str]
MappedOptionalStr = Mapped[Optional[str]]
MappedDateTime = Mapped[datetime]
MappedOptionalDateTime = Mapped[Optional[datetime]]
MappedBool = Mapped[bool]
MappedFloat = Mapped[float]
MappedOptionalFloat = Mapped[Optional[float]]
MappedStrList = Mapped[Optional[List[str]]]
MappedIntList = Mapped[Optional[List[int]]]

# Session type aliases  
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

SyncSession = Session
AsyncDatabaseSession = AsyncSession

# ================================
# 🧪 Example Usage
# ================================

if __name__ == "__main__":
    # Example: Type-safe dream search
    search_query = SearchQuery(
        terms=["물", "바다"],
        mode=SearchMode.ANY,
        filters=DreamSearchFilters(
            fortune_aspect=FortuneAspect.POSITIVE,
            confidence_threshold=0.7
        )
    )
    
    # Example: API response
    response = create_api_response(
        data={"query": search_query.terms},
        message="검색 완료"
    )
    
    print(f"Query: {search_query}")
    print(f"Response: {response}")
    
    # Example: Type validation
    try:
        cleaned_keywords = validate_keywords(["  물  ", "", "바다", "x" * 100])
        print(f"Cleaned keywords: {cleaned_keywords}")
    except Exception as e:
        print(f"Validation error: {e}")