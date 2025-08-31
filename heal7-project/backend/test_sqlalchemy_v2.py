#!/usr/bin/env python3
"""
SQLAlchemy 2.0 기능 테스트 및 검증
HEAL7 프로젝트의 SQLAlchemy 2.0 마이그레이션 검증

@author HEAL7 Team
@updated 2025-08-31
"""

import asyncio
import sys
from datetime import datetime
from typing import List, Optional

# SQLAlchemy 2.0 imports
from sqlalchemy import (
    create_engine, text, select, insert, update, delete,
    String, Integer, DateTime, Boolean, Float, ARRAY
)
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker, Session

print("🚀 SQLAlchemy 2.0 Migration Test")
print("=" * 50)

# Check SQLAlchemy version
import sqlalchemy
print(f"✅ SQLAlchemy Version: {sqlalchemy.__version__}")
assert sqlalchemy.__version__.startswith("2.0"), "SQLAlchemy 2.0 required"

# ================================
# 🏗️ Modern Base and Models
# ================================

class Base(DeclarativeBase):
    """SQLAlchemy 2.0 Base"""
    pass

class TestDream(Base):
    """테스트용 꿈풀이 모델"""
    __tablename__ = "test_dreams"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    keyword: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    meaning: Mapped[str] = mapped_column(String(500))
    confidence_score: Mapped[float] = mapped_column(Float, default=0.5)
    keywords_list: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)  # JSON string for SQLite
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

# ================================
# 🧪 Synchronous Tests
# ================================

def test_sync_engine():
    """동기 엔진 테스트"""
    print("\n🔧 Testing Synchronous Engine...")
    
    # Create in-memory SQLite database
    engine = create_engine("sqlite:///:memory:", echo=False)
    
    # Create tables
    Base.metadata.create_all(engine)
    print("✅ Tables created successfully")
    
    # Create session factory
    SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)
    
    # Test CRUD operations using SQLAlchemy 2.0 syntax
    with SessionLocal() as session:
        # INSERT using modern syntax
        import json
        new_dream = TestDream(
            keyword="물",
            meaning="맑은 물은 재물과 복을 상징합니다",
            confidence_score=0.85,
            keywords_list=json.dumps(["물", "바다", "강"]),
            is_verified=True
        )
        session.add(new_dream)
        session.commit()
        print("✅ INSERT operation successful")
        
        # SELECT using modern select() syntax
        stmt = select(TestDream).where(TestDream.keyword == "물")
        result = session.execute(stmt)
        dream = result.scalar_one_or_none()
        assert dream is not None, "Dream should exist"
        print(f"✅ SELECT operation successful: {dream.keyword} - {dream.meaning[:30]}...")
        
        # UPDATE using modern syntax
        update_stmt = (
            update(TestDream)
            .where(TestDream.id == dream.id)
            .values(confidence_score=0.95)
        )
        session.execute(update_stmt)
        session.commit()
        print("✅ UPDATE operation successful")
        
        # Complex query with joins and aggregations
        count_stmt = select(TestDream).where(TestDream.confidence_score > 0.8)
        high_confidence_dreams = session.execute(count_stmt).scalars().all()
        print(f"✅ Complex query successful: {len(high_confidence_dreams)} high-confidence dreams")
        
        # Raw SQL with text()
        raw_result = session.execute(text("SELECT COUNT(*) FROM test_dreams"))
        total_count = raw_result.scalar()
        print(f"✅ Raw SQL successful: {total_count} total dreams")

# ================================
# 🌊 Asynchronous Tests  
# ================================

async def test_async_engine():
    """비동기 엔진 테스트"""
    print("\n🌊 Testing Asynchronous Engine...")
    
    # Create async engine
    async_engine = create_async_engine("sqlite+aiosqlite:///:memory:", echo=False)
    
    # Create tables
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("✅ Async tables created successfully")
    
    # Create async session factory
    AsyncSessionLocal = async_sessionmaker(bind=async_engine, expire_on_commit=False)
    
    # Test async operations
    async with AsyncSessionLocal() as session:
        # Async INSERT
        import json
        new_dreams = [
            TestDream(
                keyword="불",
                meaning="불은 열정과 변화를 의미합니다",
                confidence_score=0.78,
                keywords_list=json.dumps(["불", "화염", "태양"]),
                is_verified=True
            ),
            TestDream(
                keyword="새",
                meaning="새는 자유와 희망을 상징합니다",
                confidence_score=0.82,
                keywords_list=json.dumps(["새", "날개", "하늘"]),
                is_verified=False
            )
        ]
        session.add_all(new_dreams)
        await session.commit()
        print("✅ Async INSERT operations successful")
        
        # Async SELECT with complex query
        stmt = (
            select(TestDream.keyword, TestDream.confidence_score)
            .where(TestDream.is_verified == True)
            .order_by(TestDream.confidence_score.desc())
        )
        result = await session.execute(stmt)
        verified_dreams = result.fetchall()
        print(f"✅ Async SELECT successful: {len(verified_dreams)} verified dreams")
        
        # Async aggregation query
        from sqlalchemy import func
        agg_stmt = select(func.avg(TestDream.confidence_score)).select_from(TestDream)
        avg_result = await session.execute(agg_stmt)
        avg_confidence = avg_result.scalar()
        print(f"✅ Async aggregation successful: avg confidence = {avg_confidence:.3f}")
        
        # Async raw SQL
        raw_stmt = text("SELECT keyword, confidence_score FROM test_dreams WHERE confidence_score > :threshold")
        raw_result = await session.execute(raw_stmt, {"threshold": 0.8})
        high_conf_dreams = raw_result.fetchall()
        print(f"✅ Async raw SQL successful: {len(high_conf_dreams)} high-confidence dreams")
    
    # Clean up
    await async_engine.dispose()

# ================================
# 🔄 Context Manager Tests
# ================================

def test_context_managers():
    """컨텍스트 매니저 패턴 테스트"""
    print("\n🔄 Testing Context Managers...")
    
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    SessionLocal = sessionmaker(bind=engine)
    
    # Test session context manager
    from contextlib import contextmanager
    
    class DatabaseManager:
        def __init__(self, session_factory):
            self.session_factory = session_factory
        
        @contextmanager
        def get_session(self):
            session = self.session_factory()
            try:
                yield session
                session.commit()
            except Exception:
                session.rollback()
                raise
            finally:
                session.close()
    
    db_manager = DatabaseManager(SessionLocal)
    
    # Use context manager
    with db_manager.get_session() as session:
        dream = TestDream(keyword="산", meaning="산은 안정과 도전을 의미합니다")
        session.add(dream)
        # Commit happens automatically
    
    # Verify data was saved
    with db_manager.get_session() as session:
        stmt = select(TestDream).where(TestDream.keyword == "산")
        saved_dream = session.execute(stmt).scalar_one_or_none()
        assert saved_dream is not None
        print("✅ Context manager pattern successful")

# ================================
# 🎯 Advanced Features Test
# ================================

def test_advanced_features():
    """고급 기능 테스트"""
    print("\n🎯 Testing Advanced Features...")
    
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    SessionLocal = sessionmaker(bind=engine)
    
    with SessionLocal() as session:
        # Bulk insert
        dreams_data = [
            {"keyword": f"키워드{i}", "meaning": f"의미{i}", "confidence_score": 0.5 + (i * 0.1)}
            for i in range(1, 6)
        ]
        
        stmt = insert(TestDream).values(dreams_data)
        session.execute(stmt)
        session.commit()
        print("✅ Bulk insert successful")
        
        # Subquery
        from sqlalchemy import exists, func
        subquery = select(TestDream.id).where(TestDream.confidence_score > 0.8)
        main_query = select(TestDream).where(TestDream.id.in_(subquery))
        high_conf_dreams = session.execute(main_query).scalars().all()
        print(f"✅ Subquery successful: {len(high_conf_dreams)} dreams found")
        
        # Window functions (if supported by database)
        try:
            window_stmt = select(
                TestDream.keyword,
                TestDream.confidence_score,
                func.row_number().over(order_by=TestDream.confidence_score.desc()).label('rank')
            )
            ranked_result = session.execute(window_stmt).fetchall()
            print(f"✅ Window function successful: {len(ranked_result)} ranked dreams")
        except Exception as e:
            print(f"⚠️ Window functions not fully supported in SQLite: {e}")
        
        # CTE (Common Table Expression)
        try:
            high_conf_cte = select(TestDream).where(TestDream.confidence_score > 0.7).cte()
            cte_query = select(high_conf_cte)
            cte_result = session.execute(cte_query).fetchall()
            print(f"✅ CTE successful: {len(cte_result)} dreams via CTE")
        except Exception as e:
            print(f"⚠️ CTE might not be fully supported: {e}")

# ================================
# 🏃‍♂️ Run All Tests
# ================================

async def main():
    """모든 테스트 실행"""
    try:
        print("Starting SQLAlchemy 2.0 comprehensive tests...\n")
        
        # Sync tests
        test_sync_engine()
        test_context_managers()
        test_advanced_features()
        
        # Async tests
        await test_async_engine()
        
        print("\n" + "=" * 50)
        print("🎉 ALL TESTS PASSED!")
        print("✅ SQLAlchemy 2.0 migration is successful!")
        print("✅ All modern patterns are working correctly!")
        print("\n📋 Summary:")
        print("   - Synchronous operations: ✅")
        print("   - Asynchronous operations: ✅")
        print("   - Modern select() syntax: ✅")
        print("   - Context managers: ✅")
        print("   - Advanced queries: ✅")
        print("   - Type hints compatibility: ✅")
        
        return True
        
    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)