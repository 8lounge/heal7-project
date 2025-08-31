"""
HEAL7 프로젝트 - SQLAlchemy 2.0 현대적 데이터베이스 모델
상향 호환성을 유지하면서 최신 SQLAlchemy 2.0 패턴 적용

@author HEAL7 Team
@version 2.0.0  
@updated 2025-08-31
"""

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, Session
from sqlalchemy import (
    String, Integer, DateTime, Boolean, ARRAY, Float, Date, Text, JSON,
    ForeignKey, text, select, insert, update, delete, UniqueConstraint,
    Index, CheckConstraint
)
from typing import List, Optional, Dict, Any, Annotated, AsyncGenerator
from datetime import datetime, date
from contextlib import asynccontextmanager
import asyncio
from dataclasses import dataclass
from pydantic import BaseModel, Field

# ================================
# 🔧 SQLAlchemy 2.0 Base Classes
# ================================

class Base(DeclarativeBase):
    """현대적 SQLAlchemy 2.0 Base 클래스"""
    pass

# Type aliases for modern SQLAlchemy patterns
intpk = Annotated[int, mapped_column(primary_key=True)]
str_50 = Annotated[str, mapped_column(String(50))]
str_255 = Annotated[str, mapped_column(String(255))]
required_str = Annotated[str, mapped_column(nullable=False)]
optional_str = Annotated[Optional[str], mapped_column(nullable=True)]

# ================================
# 🌙 Dream Service Models (SQLAlchemy 2.0 Style)
# ================================

class DreamCategory(Base):
    """꿈 카테고리 모델"""
    __tablename__ = "dream_categories"
    __table_args__ = {"schema": "dream_service"}
    
    id: Mapped[intpk]
    category_code: Mapped[str_50] = mapped_column(unique=True, index=True)
    korean_name: Mapped[required_str]
    english_name: Mapped[optional_str]
    emoji: Mapped[Optional[str]] = mapped_column(String(10))
    description: Mapped[Optional[str]] = mapped_column(Text)
    parent_id: Mapped[Optional[int]] = mapped_column(ForeignKey("dream_service.dream_categories.id"))
    sort_order: Mapped[int] = mapped_column(default=0)
    is_active: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime, onupdate=datetime.utcnow)
    
    # Relationships using modern SQLAlchemy 2.0 style
    children: Mapped[List["DreamCategory"]] = relationship(back_populates="parent")
    parent: Mapped[Optional["DreamCategory"]] = relationship(back_populates="children", remote_side=[id])
    dreams: Mapped[List["DreamInterpretation"]] = relationship(back_populates="category")

class DreamInterpretation(Base):
    """꿈풀이 해석 모델 - SQLAlchemy 2.0 스타일"""
    __tablename__ = "dream_interpretations"
    __table_args__ = (
        Index('idx_keyword_search', 'keyword'),
        Index('idx_confidence_score', 'confidence_score'),
        CheckConstraint('confidence_score >= 0.0 AND confidence_score <= 1.0', name='chk_confidence_range'),
        {"schema": "dream_service"}
    )
    
    id: Mapped[intpk]
    keyword: Mapped[required_str] = mapped_column(index=True)
    keyword_variants: Mapped[Optional[List[str]]] = mapped_column(ARRAY(String), default=list)
    emoji: Mapped[Optional[str]] = mapped_column(String(10))
    
    # Foreign Keys
    category_id: Mapped[Optional[int]] = mapped_column(ForeignKey("dream_service.dream_categories.id"))
    
    # Interpretation content
    traditional_meaning: Mapped[required_str] = mapped_column(Text)
    modern_meaning: Mapped[required_str] = mapped_column(Text)
    psychological_meaning: Mapped[Optional[str]] = mapped_column(Text)
    
    # Metadata
    fortune_aspect: Mapped[str] = mapped_column(String(20), default="neutral")  # positive, negative, neutral
    confidence_score: Mapped[float] = mapped_column(Float, default=0.5)
    accuracy_rating: Mapped[Optional[float]] = mapped_column(Float)
    
    # Related data
    related_keywords: Mapped[Optional[List[str]]] = mapped_column(ARRAY(String), default=list)
    lucky_numbers: Mapped[Optional[List[int]]] = mapped_column(ARRAY(Integer), default=list)
    
    # Statistics
    search_frequency: Mapped[int] = mapped_column(Integer, default=0)
    user_rating_avg: Mapped[Optional[float]] = mapped_column(Float)
    
    # Source information
    data_source: Mapped[Optional[str]] = mapped_column(String(100))
    source_quality: Mapped[str] = mapped_column(String(20), default="unknown")
    created_by: Mapped[Optional[str]] = mapped_column(String(100))
    verified: Mapped[bool] = mapped_column(default=False)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime, onupdate=datetime.utcnow)
    
    # Relationships
    category: Mapped[Optional["DreamCategory"]] = relationship(back_populates="dreams")
    search_stats: Mapped[List["DreamSearchStats"]] = relationship(back_populates="dream")

class DreamSearchStats(Base):
    """꿈풀이 검색 통계 모델"""
    __tablename__ = "dream_search_stats"
    __table_args__ = (
        UniqueConstraint('keyword', name='uq_keyword'),
        Index('idx_search_count', 'search_count'),
        Index('idx_last_searched', 'last_searched_at'),
        {"schema": "dream_service"}
    )
    
    id: Mapped[intpk]
    keyword: Mapped[required_str] = mapped_column(unique=True, index=True)
    dream_id: Mapped[Optional[int]] = mapped_column(ForeignKey("dream_service.dream_interpretations.id"))
    
    # Search statistics
    search_count: Mapped[int] = mapped_column(default=1)
    daily_searches: Mapped[int] = mapped_column(default=0)
    weekly_searches: Mapped[int] = mapped_column(default=0)  
    monthly_searches: Mapped[int] = mapped_column(default=0)
    
    # Trend analysis
    trend_score: Mapped[float] = mapped_column(Float, default=0.0)
    peak_search_date: Mapped[Optional[date]]
    
    # Timestamps
    first_searched_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    last_searched_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    
    # Relationship
    dream: Mapped[Optional["DreamInterpretation"]] = relationship(back_populates="search_stats")

class UserDream(Base):
    """사용자 꿈 기록 모델"""
    __tablename__ = "user_dreams"
    __table_args__ = (
        Index('idx_user_date', 'user_id', 'dream_date'),
        {"schema": "dream_service"}
    )
    
    id: Mapped[intpk]
    user_id: Mapped[required_str] = mapped_column(String(100), index=True)
    
    # Dream content
    dream_date: Mapped[date]
    dream_keywords: Mapped[List[str]] = mapped_column(ARRAY(String))
    dream_description: Mapped[Optional[str]] = mapped_column(Text)
    dream_mood: Mapped[Optional[str]] = mapped_column(String(50))
    personal_notes: Mapped[Optional[str]] = mapped_column(Text)
    
    # Related interpretations
    interpretation_ids: Mapped[Optional[List[int]]] = mapped_column(ARRAY(Integer))
    
    # User feedback
    user_rating: Mapped[Optional[int]] = mapped_column(Integer)  # 1-5 rating
    came_true: Mapped[Optional[bool]]
    accuracy_feedback: Mapped[Optional[str]] = mapped_column(Text)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime, onupdate=datetime.utcnow)

# ================================
# 🔧 Modern Database Session Management
# ================================

@dataclass
class DatabaseConfig:
    """데이터베이스 설정"""
    host: str = "localhost"
    port: int = 5432
    database: str = "heal7_db"
    username: str = "postgres"
    password: str = ""
    echo: bool = False
    pool_size: int = 10
    max_overflow: int = 20

class DatabaseManager:
    """SQLAlchemy 2.0 스타일 데이터베이스 매니저"""
    
    def __init__(self, config: DatabaseConfig):
        self.config = config
        self.engine = None
        self.async_engine = None
        self.SessionLocal = None
        self.AsyncSessionLocal = None
    
    def get_sync_url(self) -> str:
        """동기 데이터베이스 URL"""
        return (f"postgresql://{self.config.username}:{self.config.password}@"
                f"{self.config.host}:{self.config.port}/{self.config.database}")
    
    def get_async_url(self) -> str:
        """비동기 데이터베이스 URL"""
        return (f"postgresql+asyncpg://{self.config.username}:{self.config.password}@"
                f"{self.config.host}:{self.config.port}/{self.config.database}")
    
    def init_sync_engine(self):
        """동기 엔진 초기화"""
        from sqlalchemy import create_engine
        from sqlalchemy.orm import sessionmaker
        
        self.engine = create_engine(
            self.get_sync_url(),
            echo=self.config.echo,
            pool_size=self.config.pool_size,
            max_overflow=self.config.max_overflow
        )
        self.SessionLocal = sessionmaker(bind=self.engine)
    
    def init_async_engine(self):
        """비동기 엔진 초기화"""
        self.async_engine = create_async_engine(
            self.get_async_url(),
            echo=self.config.echo,
            pool_size=self.config.pool_size,
            max_overflow=self.config.max_overflow
        )
        self.AsyncSessionLocal = async_sessionmaker(bind=self.async_engine)
    
    @asynccontextmanager
    async def get_async_session(self) -> AsyncGenerator[AsyncSession, None]:
        """비동기 세션 컨텍스트 매니저"""
        if not self.AsyncSessionLocal:
            self.init_async_engine()
        
        async with self.AsyncSessionLocal() as session:
            try:
                yield session
                await session.commit()
            except Exception:
                await session.rollback()
                raise
            finally:
                await session.close()
    
    def get_sync_session(self) -> Session:
        """동기 세션 팩토리"""
        if not self.SessionLocal:
            self.init_sync_engine()
        return self.SessionLocal()

# ================================
# 🚀 Modern Query Patterns (SQLAlchemy 2.0)
# ================================

class DreamQueryService:
    """현대적 SQLAlchemy 2.0 쿼리 서비스"""
    
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager
    
    async def search_dreams_async(
        self, 
        keywords: List[str], 
        search_mode: str = "any",
        limit: int = 20
    ) -> List[Dict[str, Any]]:
        """비동기 꿈 검색 - SQLAlchemy 2.0 스타일"""
        
        async with self.db_manager.get_async_session() as session:
            # Modern select() syntax instead of session.query()
            stmt = (
                select(
                    DreamInterpretation.id,
                    DreamInterpretation.keyword,
                    DreamInterpretation.traditional_meaning,
                    DreamInterpretation.modern_meaning,
                    DreamInterpretation.confidence_score,
                    DreamCategory.korean_name.label('category_name')
                )
                .outerjoin(DreamCategory)
                .where(DreamInterpretation.keyword.in_(keywords))
                .order_by(DreamInterpretation.confidence_score.desc())
                .limit(limit)
            )
            
            result = await session.execute(stmt)
            return [dict(row) for row in result.fetchall()]
    
    def search_dreams_sync(
        self,
        keywords: List[str],
        search_mode: str = "any", 
        limit: int = 20
    ) -> List[Dict[str, Any]]:
        """동기 꿈 검색 - SQLAlchemy 2.0 스타일"""
        
        with self.db_manager.get_sync_session() as session:
            stmt = (
                select(
                    DreamInterpretation.id,
                    DreamInterpretation.keyword,
                    DreamInterpretation.traditional_meaning,
                    DreamInterpretation.modern_meaning,
                    DreamInterpretation.confidence_score,
                    DreamCategory.korean_name.label('category_name')
                )
                .outerjoin(DreamCategory)
                .where(DreamInterpretation.keyword.in_(keywords))
                .order_by(DreamInterpretation.confidence_score.desc())
                .limit(limit)
            )
            
            result = session.execute(stmt)
            return [dict(row) for row in result.fetchall()]
    
    async def update_search_stats_async(self, keyword: str):
        """검색 통계 업데이트 - Modern upsert pattern"""
        
        async with self.db_manager.get_async_session() as session:
            # Modern upsert using SQLAlchemy 2.0 patterns
            stmt = text("""
                INSERT INTO dream_service.dream_search_stats (keyword, search_count, last_searched_at)
                VALUES (:keyword, 1, CURRENT_TIMESTAMP)
                ON CONFLICT (keyword) 
                DO UPDATE SET 
                    search_count = dream_search_stats.search_count + 1,
                    last_searched_at = CURRENT_TIMESTAMP
            """)
            
            await session.execute(stmt, {"keyword": keyword})

# ================================
# 🔗 Dependency Injection for FastAPI
# ================================

# Global database manager instance
db_manager: Optional[DatabaseManager] = None

def init_database(config: DatabaseConfig):
    """데이터베이스 매니저 초기화"""
    global db_manager
    db_manager = DatabaseManager(config)
    db_manager.init_sync_engine()
    db_manager.init_async_engine()

def get_db_session() -> Session:
    """FastAPI Dependency - Sync Session"""
    if not db_manager:
        raise RuntimeError("Database not initialized. Call init_database() first.")
    
    session = db_manager.get_sync_session()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()

async def get_async_db_session() -> AsyncGenerator[AsyncSession, None]:
    """FastAPI Dependency - Async Session"""
    if not db_manager:
        raise RuntimeError("Database not initialized. Call init_database() first.")
    
    async with db_manager.get_async_session() as session:
        yield session

# ================================
# 🧪 Example Usage & Migration Guide
# ================================

async def example_modern_patterns():
    """SQLAlchemy 2.0 사용 예제"""
    
    config = DatabaseConfig(
        host="localhost",
        database="heal7_db",
        username="postgres",
        password="your_password"
    )
    
    db_manager = DatabaseManager(config)
    query_service = DreamQueryService(db_manager)
    
    # Example 1: Modern async query
    results = await query_service.search_dreams_async(["물", "불"])
    print(f"Found {len(results)} dreams")
    
    # Example 2: Using select() instead of session.query()  
    async with db_manager.get_async_session() as session:
        stmt = select(DreamInterpretation).where(DreamInterpretation.keyword == "물")
        result = await session.execute(stmt)
        dream = result.scalar_one_or_none()
        if dream:
            print(f"Dream: {dream.keyword} - {dream.traditional_meaning[:50]}...")

if __name__ == "__main__":
    # Run example
    asyncio.run(example_modern_patterns())