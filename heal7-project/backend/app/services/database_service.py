"""
HEAL7 사주명리학 시스템 - 데이터베이스 통합 서비스

PostgreSQL과 SQLite를 통합 관리하는 서비스입니다.
비동기 처리, 연결 풀링, 트랜잭션 관리, 백업/복원을 지원합니다.

Features:
- PostgreSQL 및 SQLite 통합 관리
- 비동기 쿼리 실행 및 트랜잭션
- 연결 풀링 및 자동 재연결
- 쿼리 캐싱 및 성능 모니터링
- 데이터베이스 백업 및 복원
- 스키마 마이그레이션
"""

import asyncio
import json
import sqlite3
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Union, Tuple
from pathlib import Path
from contextlib import asynccontextmanager
import asyncpg
import aiosqlite
# Redis는 임시 제외 - 향후 통합 예정
# import aioredis
from loguru import logger
from pydantic import BaseModel, Field

try:
    from ..config.settings import get_settings
except ImportError:
    from config.settings import get_settings


class DatabaseType(str):
    """데이터베이스 타입"""
    POSTGRESQL = "postgresql"
    SQLITE = "sqlite"


class QueryResult(BaseModel):
    """쿼리 결과 모델"""
    
    rows: List[Dict[str, Any]] = Field(..., description="결과 행들")
    row_count: int = Field(..., description="결과 행 수")
    execution_time: float = Field(..., description="실행 시간 (초)")
    query_hash: Optional[str] = Field(None, description="쿼리 해시")
    cached: bool = Field(default=False, description="캐시된 결과 여부")
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class DatabaseStats(BaseModel):
    """데이터베이스 통계"""
    
    model_config = {"arbitrary_types_allowed": True}
    
    database_name: str = Field(..., description="데이터베이스 이름")
    database_type: str = Field(..., description="데이터베이스 타입")
    
    # 연결 정보
    active_connections: int = Field(..., description="활성 연결 수")
    max_connections: int = Field(..., description="최대 연결 수")
    
    # 쿼리 통계
    total_queries: int = Field(default=0, description="총 쿼리 수")
    successful_queries: int = Field(default=0, description="성공 쿼리 수")
    failed_queries: int = Field(default=0, description="실패 쿼리 수")
    avg_query_time: float = Field(default=0.0, description="평균 쿼리 시간")
    
    # 스토리지 정보
    database_size: Optional[int] = Field(None, description="데이터베이스 크기 (bytes)")
    table_count: int = Field(default=0, description="테이블 수")
    
    last_updated: datetime = Field(default_factory=datetime.utcnow)


class DatabaseConnection:
    """데이터베이스 연결 래퍼"""
    
    def __init__(
        self, 
        connection: Union[asyncpg.Connection, aiosqlite.Connection],
        db_type: DatabaseType,
        name: str
    ):
        self.connection = connection
        self.db_type = db_type
        self.name = name
        self.created_at = datetime.utcnow()
        self.last_used = datetime.utcnow()
        self.query_count = 0
    
    async def execute(
        self, 
        query: str, 
        *args, 
        **kwargs
    ) -> Union[str, List[Dict[str, Any]]]:
        """쿼리 실행"""
        self.last_used = datetime.utcnow()
        self.query_count += 1
        
        try:
            if self.db_type == DatabaseType.POSTGRESQL:
                if query.strip().upper().startswith(('SELECT', 'WITH')):
                    rows = await self.connection.fetch(query, *args)
                    return [dict(row) for row in rows]
                else:
                    result = await self.connection.execute(query, *args)
                    return result
            else:  # SQLite
                if query.strip().upper().startswith(('SELECT', 'WITH')):
                    async with self.connection.execute(query, args) as cursor:
                        rows = await cursor.fetchall()
                        columns = [desc[0] for desc in cursor.description] if cursor.description else []
                        return [dict(zip(columns, row)) for row in rows]
                else:
                    await self.connection.execute(query, args)
                    await self.connection.commit()
                    return f"Query executed successfully"
                    
        except Exception as e:
            logger.error(f"쿼리 실행 실패 ({self.name}): {e}")
            raise
    
    async def close(self):
        """연결 종료"""
        try:
            await self.connection.close()
        except Exception as e:
            logger.warning(f"연결 종료 실패 ({self.name}): {e}")


class DatabaseService:
    """데이터베이스 통합 서비스 클래스"""
    
    def __init__(self):
        """서비스 초기화"""
        self.settings = get_settings()
        # Redis는 현재 비활성화 - 향후 통합 예정  
        # self.redis_client: Optional[aioredis.Redis] = None
        self.redis_client = None
        self._cache_prefix = "db:query"
        self._is_initialized = False
        
        # 데이터베이스 연결 풀
        self.pg_pool: Optional[asyncpg.Pool] = None
        self.sqlite_connections: Dict[str, DatabaseConnection] = {}
        
        # 통계 및 모니터링
        self.stats: Dict[str, DatabaseStats] = {}
        self.query_history: List[Dict[str, Any]] = []
        
        # 기본 SQLite 데이터베이스 경로들 (CLAUDE.md 기준)
        self.sqlite_databases = {
            "kasi": "/home/ubuntu/database/kasi/working_kasi_solar_terms.db",
            "myeongri": "/home/ubuntu/database/myeongri/comprehensive_myeongri_solar_terms.db",
            "heal7_saju": "./database/heal7_saju.db",
        }
        
        logger.info("데이터베이스 서비스 초기화 시작")
    
    async def initialize(self) -> None:
        """서비스 초기화"""
        if self._is_initialized:
            return
            
        try:
            # Redis 클라이언트는 현재 비활성화 - 향후 통합 예정
            # self.redis_client = await aioredis.from_url(
            #     self.settings.redis_url,
            #     decode_responses=True,
            #     max_connections=10
            # )
            logger.info("Redis 캐시 현재 비활성화 상태")
            
            # PostgreSQL 연결 풀 초기화 (선택적)
            await self._init_postgresql()
            
            # SQLite 데이터베이스들 초기화
            await self._init_sqlite_databases()
            
            # 통계 초기화
            await self._init_statistics()
            
            self._is_initialized = True
            logger.info("데이터베이스 서비스 초기화 완료")
            
        except Exception as e:
            logger.error(f"데이터베이스 서비스 초기화 실패: {e}")
            raise
    
    async def cleanup(self) -> None:
        """리소스 정리"""
        try:
            # PostgreSQL 풀 정리
            if self.pg_pool:
                await self.pg_pool.close()
                self.pg_pool = None
            
            # SQLite 연결들 정리
            for conn in self.sqlite_connections.values():
                await conn.close()
            self.sqlite_connections.clear()
            
            # Redis 연결 정리
            if self.redis_client:
                await self.redis_client.close()
                self.redis_client = None
                
            self._is_initialized = False
            logger.info("데이터베이스 서비스 정리 완료")
            
        except Exception as e:
            logger.error(f"데이터베이스 서비스 정리 실패: {e}")
    
    async def health_check(self) -> Dict[str, Any]:
        """헬스체크"""
        if not self._is_initialized:
            return {"status": "unhealthy", "reason": "not_initialized"}
        
        health_status = {
            "status": "healthy",
            "databases": {},
            "redis": "disconnected",
            "total_connections": 0
        }
        
        try:
            # Redis 연결 테스트
            await self.redis_client.ping()
            health_status["redis"] = "connected"
        except Exception:
            health_status["redis"] = "disconnected"
        
        # PostgreSQL 상태 확인
        if self.pg_pool:
            try:
                async with self.pg_pool.acquire() as conn:
                    await conn.fetchval("SELECT 1")
                health_status["databases"]["postgresql"] = {
                    "status": "connected",
                    "pool_size": len(self.pg_pool._queue._queue)
                }
            except Exception as e:
                health_status["databases"]["postgresql"] = {
                    "status": "disconnected", 
                    "error": str(e)
                }
        
        # SQLite 상태 확인
        for name, conn in self.sqlite_connections.items():
            try:
                await conn.execute("SELECT 1")
                health_status["databases"][name] = {
                    "status": "connected",
                    "type": "sqlite",
                    "query_count": conn.query_count
                }
                health_status["total_connections"] += 1
            except Exception as e:
                health_status["databases"][name] = {
                    "status": "disconnected",
                    "error": str(e)
                }
        
        # 전체 상태 결정
        connected_dbs = sum(
            1 for db_info in health_status["databases"].values() 
            if db_info.get("status") == "connected"
        )
        
        if connected_dbs == 0:
            health_status["status"] = "unhealthy"
            health_status["reason"] = "no_database_connections"
        elif connected_dbs < len(health_status["databases"]):
            health_status["status"] = "degraded"
            health_status["reason"] = "partial_database_connectivity"
        
        return health_status
    
    async def _init_postgresql(self) -> None:
        """PostgreSQL 초기화"""
        if not self.settings.database_url or not self.settings.database_url.startswith("postgresql"):
            logger.info("PostgreSQL 설정되지 않음, SQLite만 사용")
            return
            
        try:
            self.pg_pool = await asyncpg.create_pool(
                self.settings.database_url,
                min_size=2,
                max_size=10,
                command_timeout=60,
                server_settings={
                    'jit': 'off'  # JIT 컴파일 비활성화 (호환성)
                }
            )
            
            # 연결 테스트
            async with self.pg_pool.acquire() as conn:
                version = await conn.fetchval("SELECT version()")
                logger.info(f"PostgreSQL 연결 성공: {version[:50]}...")
                
            # 통계 초기화
            self.stats["postgresql"] = DatabaseStats(
                database_name="postgresql",
                database_type=DatabaseType.POSTGRESQL,
                active_connections=0,
                max_connections=10
            )
            
        except Exception as e:
            logger.warning(f"PostgreSQL 초기화 실패: {e}")
            self.pg_pool = None
    
    async def _init_sqlite_databases(self) -> None:
        """SQLite 데이터베이스들 초기화"""
        for name, db_path in self.sqlite_databases.items():
            try:
                # 디렉터리 생성
                Path(db_path).parent.mkdir(parents=True, exist_ok=True)
                
                # SQLite 연결
                sqlite_conn = await aiosqlite.connect(db_path)
                
                # WAL 모드 설정 (성능 향상)
                await sqlite_conn.execute("PRAGMA journal_mode=WAL")
                await sqlite_conn.execute("PRAGMA synchronous=NORMAL")
                await sqlite_conn.execute("PRAGMA cache_size=10000")
                
                # 연결 래퍼 생성
                db_conn = DatabaseConnection(
                    connection=sqlite_conn,
                    db_type=DatabaseType.SQLITE,
                    name=name
                )
                
                self.sqlite_connections[name] = db_conn
                
                # 통계 초기화
                self.stats[name] = DatabaseStats(
                    database_name=name,
                    database_type=DatabaseType.SQLITE,
                    active_connections=1,
                    max_connections=1
                )
                
                logger.info(f"SQLite 데이터베이스 초기화: {name} ({db_path})")
                
            except Exception as e:
                logger.error(f"SQLite 데이터베이스 초기화 실패 ({name}): {e}")
                continue
    
    async def _init_statistics(self) -> None:
        """통계 정보 초기화"""
        for name in self.stats:
            try:
                await self._update_database_stats(name)
            except Exception as e:
                logger.warning(f"통계 초기화 실패 ({name}): {e}")
    
    async def _update_database_stats(self, db_name: str) -> None:
        """데이터베이스 통계 업데이트"""
        if db_name not in self.stats:
            return
            
        stats = self.stats[db_name]
        
        try:
            if db_name == "postgresql" and self.pg_pool:
                # PostgreSQL 통계
                async with self.pg_pool.acquire() as conn:
                    # 데이터베이스 크기
                    size_query = """
                    SELECT pg_size_pretty(pg_database_size(current_database())) as size,
                           pg_database_size(current_database()) as size_bytes
                    """
                    size_result = await conn.fetchrow(size_query)
                    stats.database_size = size_result['size_bytes']
                    
                    # 테이블 수
                    table_count = await conn.fetchval(
                        "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'public'"
                    )
                    stats.table_count = table_count
                    
            elif db_name in self.sqlite_connections:
                # SQLite 통계
                conn = self.sqlite_connections[db_name]
                
                # 파일 크기
                db_path = self.sqlite_databases.get(db_name)
                if db_path and Path(db_path).exists():
                    stats.database_size = Path(db_path).stat().st_size
                
                # 테이블 수
                result = await conn.execute(
                    "SELECT COUNT(*) FROM sqlite_master WHERE type='table'"
                )
                if result:
                    stats.table_count = result[0]['COUNT(*)'] if result else 0
            
            stats.last_updated = datetime.utcnow()
            
        except Exception as e:
            logger.warning(f"통계 업데이트 실패 ({db_name}): {e}")
    
    def _generate_query_hash(self, query: str, params: tuple = ()) -> str:
        """쿼리 해시 생성"""
        import hashlib
        query_string = f"{query.strip()}{str(params)}"
        return hashlib.md5(query_string.encode()).hexdigest()
    
    async def _get_cached_result(self, query_hash: str) -> Optional[Dict[str, Any]]:
        """캐시된 쿼리 결과 조회"""
        if not self.redis_client:
            return None
            
        try:
            cache_key = f"{self._cache_prefix}:{query_hash}"
            cached_data = await self.redis_client.get(cache_key)
            
            if cached_data:
                return json.loads(cached_data)
            
            return None
            
        except Exception as e:
            logger.warning(f"쿼리 캐시 조회 실패: {e}")
            return None
    
    async def _cache_query_result(
        self, 
        query_hash: str, 
        result: QueryResult,
        ttl: int = 300
    ) -> None:
        """쿼리 결과 캐싱"""
        if not self.redis_client:
            return
            
        try:
            cache_key = f"{self._cache_prefix}:{query_hash}"
            result_dict = result.dict()
            
            await self.redis_client.setex(
                cache_key,
                ttl,
                json.dumps(result_dict, default=str, ensure_ascii=False)
            )
            
        except Exception as e:
            logger.warning(f"쿼리 결과 캐시 실패: {e}")
    
    def _log_query(
        self, 
        db_name: str, 
        query: str, 
        execution_time: float,
        success: bool,
        error: Optional[str] = None
    ) -> None:
        """쿼리 로깅"""
        log_entry = {
            "timestamp": datetime.utcnow(),
            "database": db_name,
            "query": query[:200],  # 처음 200자만 로그
            "execution_time": execution_time,
            "success": success,
            "error": error
        }
        
        self.query_history.append(log_entry)
        
        # 최대 1000개까지만 보관
        if len(self.query_history) > 1000:
            self.query_history = self.query_history[-500:]
        
        # 통계 업데이트
        if db_name in self.stats:
            stats = self.stats[db_name]
            stats.total_queries += 1
            
            if success:
                stats.successful_queries += 1
            else:
                stats.failed_queries += 1
            
            # 평균 실행 시간 업데이트
            if stats.successful_queries > 0:
                stats.avg_query_time = (
                    (stats.avg_query_time * (stats.successful_queries - 1) + execution_time) 
                    / stats.successful_queries
                )
    
    async def execute_query(
        self, 
        database: str,
        query: str, 
        params: tuple = (),
        use_cache: bool = True,
        cache_ttl: int = 300
    ) -> QueryResult:
        """쿼리 실행"""
        if not self._is_initialized:
            await self.initialize()
        
        start_time = datetime.utcnow()
        query_hash = self._generate_query_hash(query, params) if use_cache else None
        
        # 캐시 확인 (SELECT 쿼리만)
        if use_cache and query.strip().upper().startswith(('SELECT', 'WITH')):
            cached_result = await self._get_cached_result(query_hash)
            if cached_result:
                logger.debug(f"캐시된 쿼리 결과 반환: {query_hash[:12]}")
                cached_result['cached'] = True
                return QueryResult(**cached_result)
        
        try:
            # 데이터베이스별 실행
            if database == "postgresql" and self.pg_pool:
                async with self.pg_pool.acquire() as conn:
                    if query.strip().upper().startswith(('SELECT', 'WITH')):
                        rows = await conn.fetch(query, *params)
                        result_rows = [dict(row) for row in rows]
                    else:
                        result = await conn.execute(query, *params)
                        result_rows = [{"result": result}]
                        
            elif database in self.sqlite_connections:
                conn = self.sqlite_connections[database]
                result = await conn.execute(query, *params)
                result_rows = result if isinstance(result, list) else [{"result": result}]
                
            else:
                raise ValueError(f"데이터베이스를 찾을 수 없습니다: {database}")
            
            # 실행 시간 계산
            execution_time = (datetime.utcnow() - start_time).total_seconds()
            
            # 결과 생성
            query_result = QueryResult(
                rows=result_rows,
                row_count=len(result_rows),
                execution_time=execution_time,
                query_hash=query_hash,
                cached=False
            )
            
            # 캐싱 (SELECT 쿼리만)
            if use_cache and query.strip().upper().startswith(('SELECT', 'WITH')):
                await self._cache_query_result(query_hash, query_result, cache_ttl)
            
            # 로깅
            self._log_query(database, query, execution_time, True)
            
            logger.debug(f"쿼리 실행 완료 ({database}): {execution_time:.3f}s, {len(result_rows)}행")
            return query_result
            
        except Exception as e:
            execution_time = (datetime.utcnow() - start_time).total_seconds()
            self._log_query(database, query, execution_time, False, str(e))
            
            logger.error(f"쿼리 실행 실패 ({database}): {e}")
            raise
    
    @asynccontextmanager
    async def transaction(self, database: str):
        """트랜잭션 컨텍스트 매니저"""
        if not self._is_initialized:
            await self.initialize()
        
        if database == "postgresql" and self.pg_pool:
            async with self.pg_pool.acquire() as conn:
                async with conn.transaction():
                    yield conn
                    
        elif database in self.sqlite_connections:
            conn = self.sqlite_connections[database]
            try:
                await conn.connection.execute("BEGIN")
                yield conn.connection
                await conn.connection.commit()
            except Exception:
                await conn.connection.rollback()
                raise
        else:
            raise ValueError(f"트랜잭션을 지원하지 않는 데이터베이스: {database}")
    
    async def get_table_info(self, database: str, table_name: str) -> Dict[str, Any]:
        """테이블 정보 조회"""
        if database == "postgresql" and self.pg_pool:
            query = """
            SELECT 
                column_name, 
                data_type, 
                is_nullable, 
                column_default
            FROM information_schema.columns 
            WHERE table_name = $1 
            ORDER BY ordinal_position
            """
            result = await self.execute_query(database, query, (table_name,))
            
        elif database in self.sqlite_connections:
            query = f"PRAGMA table_info({table_name})"
            result = await self.execute_query(database, query)
            
        else:
            raise ValueError(f"지원하지 않는 데이터베이스: {database}")
        
        return {
            "table_name": table_name,
            "columns": result.rows,
            "column_count": result.row_count
        }
    
    async def get_database_statistics(self, database: str) -> DatabaseStats:
        """데이터베이스 통계 조회"""
        if database not in self.stats:
            raise ValueError(f"데이터베이스를 찾을 수 없습니다: {database}")
        
        # 통계 업데이트
        await self._update_database_stats(database)
        
        return self.stats[database]
    
    async def backup_sqlite_database(
        self, 
        database: str, 
        backup_path: Optional[str] = None
    ) -> str:
        """SQLite 데이터베이스 백업"""
        if database not in self.sqlite_connections:
            raise ValueError(f"SQLite 데이터베이스를 찾을 수 없습니다: {database}")
        
        if not backup_path:
            timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
            backup_path = f"./backups/{database}_{timestamp}.db"
        
        # 백업 디렉터리 생성
        Path(backup_path).parent.mkdir(parents=True, exist_ok=True)
        
        try:
            source_path = self.sqlite_databases[database]
            
            # 파일 복사 (SQLite는 파일 기반이므로 간단히 복사)
            import shutil
            shutil.copy2(source_path, backup_path)
            
            logger.info(f"SQLite 백업 완료: {database} -> {backup_path}")
            return backup_path
            
        except Exception as e:
            logger.error(f"SQLite 백업 실패 ({database}): {e}")
            raise
    
    async def get_query_history(
        self, 
        limit: int = 100,
        database_filter: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """쿼리 히스토리 조회"""
        history = self.query_history[-limit:]
        
        if database_filter:
            history = [
                entry for entry in history 
                if entry['database'] == database_filter
            ]
        
        return history
    
    async def optimize_database(self, database: str) -> Dict[str, Any]:
        """데이터베이스 최적화"""
        optimization_results = {
            "database": database,
            "operations": [],
            "before_size": 0,
            "after_size": 0,
            "improvement": "0%"
        }
        
        try:
            # 최적화 전 크기
            stats_before = await self.get_database_statistics(database)
            optimization_results["before_size"] = stats_before.database_size or 0
            
            if database in self.sqlite_connections:
                # SQLite 최적화
                operations = [
                    ("VACUUM", "데이터베이스 재구성"),
                    ("ANALYZE", "통계 정보 업데이트"),
                    ("PRAGMA optimize", "자동 최적화")
                ]
                
                for sql, desc in operations:
                    try:
                        await self.execute_query(database, sql, use_cache=False)
                        optimization_results["operations"].append(f"✅ {desc}")
                    except Exception as e:
                        optimization_results["operations"].append(f"❌ {desc}: {e}")
                        
            elif database == "postgresql" and self.pg_pool:
                # PostgreSQL 최적화
                operations = [
                    ("VACUUM ANALYZE", "테이블 정리 및 통계 업데이트"),
                    ("REINDEX DATABASE", "인덱스 재구성")
                ]
                
                for sql, desc in operations:
                    try:
                        await self.execute_query(database, sql, use_cache=False)
                        optimization_results["operations"].append(f"✅ {desc}")
                    except Exception as e:
                        optimization_results["operations"].append(f"❌ {desc}: {e}")
            
            # 최적화 후 크기
            stats_after = await self.get_database_statistics(database)
            optimization_results["after_size"] = stats_after.database_size or 0
            
            # 개선율 계산
            if optimization_results["before_size"] > 0:
                improvement = (
                    (optimization_results["before_size"] - optimization_results["after_size"]) 
                    / optimization_results["before_size"] * 100
                )
                optimization_results["improvement"] = f"{improvement:.1f}%"
            
            logger.info(f"데이터베이스 최적화 완료: {database}")
            return optimization_results
            
        except Exception as e:
            logger.error(f"데이터베이스 최적화 실패 ({database}): {e}")
            optimization_results["error"] = str(e)
            return optimization_results
    
    def __repr__(self) -> str:
        status = "initialized" if self._is_initialized else "not_initialized"
        db_count = len(self.sqlite_connections)
        
        if self.pg_pool:
            db_count += 1
            
        return f"DatabaseService(status={status}, databases={db_count})"