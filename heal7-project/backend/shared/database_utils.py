"""
HEAL7 프로젝트 - SQLAlchemy 2.0 데이터베이스 유틸리티
현대적인 세션 관리와 연결 처리

@author HEAL7 Team
@version 2.0.0
@updated 2025-08-31
"""

import os
import asyncio
from typing import Generator, AsyncGenerator, Optional
from contextlib import contextmanager, asynccontextmanager
from sqlalchemy import create_engine, text, event
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool, QueuePool
from functools import wraps
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DatabaseConnection:
    """SQLAlchemy 2.0 데이터베이스 연결 매니저"""
    
    def __init__(self):
        self.sync_engine = None
        self.async_engine = None
        self.sync_session_factory = None
        self.async_session_factory = None
        self._initialized = False
    
    def initialize_sync(
        self,
        database_url: Optional[str] = None,
        echo: bool = False,
        pool_size: int = 10,
        max_overflow: int = 20,
        pool_timeout: int = 30,
        pool_recycle: int = 3600
    ):
        """동기 데이터베이스 엔진 초기화"""
        if not database_url:
            database_url = self._get_database_url()
        
        self.sync_engine = create_engine(
            database_url,
            echo=echo,
            poolclass=QueuePool,
            pool_size=pool_size,
            max_overflow=max_overflow,
            pool_timeout=pool_timeout,
            pool_recycle=pool_recycle,
            # Modern SQLAlchemy 2.0 settings
            future=True
        )
        
        # Add connection event listeners
        self._add_sync_event_listeners()
        
        self.sync_session_factory = sessionmaker(
            bind=self.sync_engine,
            class_=Session,
            expire_on_commit=False  # SQLAlchemy 2.0 recommended
        )
        
        logger.info("Sync database engine initialized")
    
    def initialize_async(
        self,
        database_url: Optional[str] = None,
        echo: bool = False,
        pool_size: int = 10,
        max_overflow: int = 20,
        pool_timeout: int = 30,
        pool_recycle: int = 3600
    ):
        """비동기 데이터베이스 엔진 초기화"""
        if not database_url:
            database_url = self._get_async_database_url()
        
        self.async_engine = create_async_engine(
            database_url,
            echo=echo,
            pool_size=pool_size,
            max_overflow=max_overflow,
            pool_timeout=pool_timeout,
            pool_recycle=pool_recycle,
            # Modern async settings
            future=True
        )
        
        self.async_session_factory = async_sessionmaker(
            bind=self.async_engine,
            class_=AsyncSession,
            expire_on_commit=False
        )
        
        logger.info("Async database engine initialized")
    
    def _get_database_url(self) -> str:
        """동기 데이터베이스 URL 생성"""
        host = os.getenv("DB_HOST", "localhost")
        port = os.getenv("DB_PORT", "5432")
        database = os.getenv("DB_NAME", "heal7_db")
        username = os.getenv("DB_USER", "postgres")
        password = os.getenv("DB_PASSWORD", "")
        
        return f"postgresql://{username}:{password}@{host}:{port}/{database}"
    
    def _get_async_database_url(self) -> str:
        """비동기 데이터베이스 URL 생성"""
        return self._get_database_url().replace("postgresql://", "postgresql+asyncpg://")
    
    def _add_sync_event_listeners(self):
        """동기 엔진에 이벤트 리스너 추가"""
        
        @event.listens_for(self.sync_engine, "connect")
        def set_sqlite_pragma(dbapi_connection, connection_record):
            """SQLite 최적화 (필요시)"""
            if "sqlite" in str(self.sync_engine.url):
                cursor = dbapi_connection.cursor()
                cursor.execute("PRAGMA foreign_keys=ON")
                cursor.close()
        
        @event.listens_for(self.sync_engine, "checkout")
        def receive_checkout(dbapi_connection, connection_record, connection_proxy):
            """연결 체크아웃 로깅"""
            logger.debug("Connection checked out from pool")
        
        @event.listens_for(self.sync_engine, "checkin")
        def receive_checkin(dbapi_connection, connection_record):
            """연결 체크인 로깅"""
            logger.debug("Connection checked in to pool")
    
    @contextmanager
    def get_sync_session(self) -> Generator[Session, None, None]:
        """동기 세션 컨텍스트 매니저"""
        if not self.sync_session_factory:
            raise RuntimeError("Sync database not initialized. Call initialize_sync() first.")
        
        session = self.sync_session_factory()
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            logger.error(f"Database session error: {e}")
            raise
        finally:
            session.close()
    
    @asynccontextmanager
    async def get_async_session(self) -> AsyncGenerator[AsyncSession, None]:
        """비동기 세션 컨텍스트 매니저"""
        if not self.async_session_factory:
            raise RuntimeError("Async database not initialized. Call initialize_async() first.")
        
        session = self.async_session_factory()
        try:
            yield session
            await session.commit()
        except Exception as e:
            await session.rollback()
            logger.error(f"Async database session error: {e}")
            raise
        finally:
            await session.close()
    
    async def test_connection(self) -> bool:
        """데이터베이스 연결 테스트"""
        try:
            if self.async_engine:
                async with self.get_async_session() as session:
                    result = await session.execute(text("SELECT 1"))
                    return result.scalar() == 1
            elif self.sync_engine:
                with self.get_sync_session() as session:
                    result = session.execute(text("SELECT 1"))
                    return result.scalar() == 1
            else:
                return False
        except Exception as e:
            logger.error(f"Database connection test failed: {e}")
            return False
    
    async def close_connections(self):
        """모든 데이터베이스 연결 정리"""
        if self.async_engine:
            await self.async_engine.dispose()
            logger.info("Async engine disposed")
        
        if self.sync_engine:
            self.sync_engine.dispose()
            logger.info("Sync engine disposed")

# Global database connection instance
db_connection = DatabaseConnection()

# ================================
# 🚀 FastAPI Dependencies
# ================================

def get_db() -> Generator[Session, None, None]:
    """FastAPI dependency for sync database session"""
    with db_connection.get_sync_session() as session:
        yield session

async def get_async_db() -> AsyncGenerator[AsyncSession, None]:
    """FastAPI dependency for async database session"""  
    async with db_connection.get_async_session() as session:
        yield session

# ================================
# 🎯 Decorators for Automatic Session Management
# ================================

def with_db_session(func):
    """동기 함수에 데이터베이스 세션을 자동 주입하는 데코레이터"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        with db_connection.get_sync_session() as session:
            return func(session, *args, **kwargs)
    return wrapper

def with_async_db_session(func):
    """비동기 함수에 데이터베이스 세션을 자동 주입하는 데코레이터"""
    @wraps(func)
    async def wrapper(*args, **kwargs):
        async with db_connection.get_async_session() as session:
            return await func(session, *args, **kwargs)
    return wrapper

# ================================
# 🔧 Utility Functions
# ================================

async def init_database(
    sync_url: Optional[str] = None,
    async_url: Optional[str] = None,
    echo: bool = False
):
    """데이터베이스 초기화"""
    db_connection.initialize_sync(sync_url, echo=echo)
    db_connection.initialize_async(async_url, echo=echo)
    
    # 연결 테스트
    connection_ok = await db_connection.test_connection()
    if connection_ok:
        logger.info("✅ Database connection successful")
    else:
        logger.error("❌ Database connection failed")
        raise RuntimeError("Failed to connect to database")

async def run_migration():
    """데이터베이스 마이그레이션 실행 (예제)"""
    async with db_connection.get_async_session() as session:
        # 예: 테이블 생성
        create_schema_sql = text("""
            CREATE SCHEMA IF NOT EXISTS dream_service;
            CREATE SCHEMA IF NOT EXISTS saju_service;
            CREATE SCHEMA IF NOT EXISTS crawling_service;
        """)
        await session.execute(create_schema_sql)
        logger.info("Database schemas created/verified")

@with_async_db_session
async def health_check(session: AsyncSession) -> dict:
    """데이터베이스 헬스 체크"""
    try:
        result = await session.execute(text("SELECT version()"))
        db_version = result.scalar()
        
        # 연결 풀 상태 확인
        pool_status = {
            "size": db_connection.async_engine.pool.size(),
            "checked_in": db_connection.async_engine.pool.checkedin(),
            "checked_out": db_connection.async_engine.pool.checkedout(),
            "invalidated": db_connection.async_engine.pool.invalid(),
        }
        
        return {
            "status": "healthy",
            "database_version": db_version,
            "pool_status": pool_status,
            "connection_info": str(db_connection.async_engine.url)
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e)
        }

# ================================
# 🧪 Example Usage
# ================================

async def example_usage():
    """SQLAlchemy 2.0 사용 예제"""
    
    # 1. 데이터베이스 초기화
    await init_database(echo=True)
    
    # 2. 동기 세션 사용
    with db_connection.get_sync_session() as session:
        result = session.execute(text("SELECT 'Hello SQLAlchemy 2.0'"))
        print(result.scalar())
    
    # 3. 비동기 세션 사용
    async with db_connection.get_async_session() as session:
        result = await session.execute(text("SELECT 'Hello Async SQLAlchemy 2.0'"))
        print(result.scalar())
    
    # 4. 데코레이터 사용
    @with_async_db_session
    async def test_query(session: AsyncSession):
        result = await session.execute(text("SELECT NOW()"))
        return result.scalar()
    
    current_time = await test_query()
    print(f"Current time: {current_time}")
    
    # 5. 헬스 체크
    health = await health_check()
    print(f"Health: {health}")
    
    # 6. 연결 정리
    await db_connection.close_connections()

if __name__ == "__main__":
    asyncio.run(example_usage())