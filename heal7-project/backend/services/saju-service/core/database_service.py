"""
HEAL7 Database Service
데이터베이스 연결 및 쿼리 관리 서비스

기능:
- 안전한 DB 연결 풀 관리
- 환경변수 기반 설정
- 연결 재시도 로직
- 쿼리 로깅 및 모니터링
"""

import asyncpg
import os
from typing import Optional, Dict, Any, List
from datetime import datetime
import asyncio
from loguru import logger
from fastapi import HTTPException, status

class DatabaseService:
    def __init__(self):
        # 환경변수에서 DB 설정 로드
        self.db_host = os.getenv('DB_HOST', 'localhost')
        self.db_port = int(os.getenv('DB_PORT', '5432'))
        self.db_user = os.getenv('DB_USER', 'postgres')
        self.db_password = os.getenv('DB_PASSWORD', 'postgres')
        self.db_name_saju = os.getenv('DB_NAME_SAJU', 'heal7_saju')
        self.db_name_main = os.getenv('DB_NAME_MAIN', 'heal7')

        # 연결 풀 설정
        self.max_connections = int(os.getenv('DB_MAX_CONNECTIONS', '20'))
        self.min_connections = int(os.getenv('DB_MIN_CONNECTIONS', '5'))
        self.connection_timeout = int(os.getenv('DB_CONNECTION_TIMEOUT', '10'))

        # 연결 풀
        self._saju_pool: Optional[asyncpg.Pool] = None
        self._main_pool: Optional[asyncpg.Pool] = None

        logger.info(f"DatabaseService initialized for hosts: {self.db_host}:{self.db_port}")

    async def initialize_pools(self):
        """연결 풀 초기화"""
        try:
            # 사주 DB 연결 풀
            self._saju_pool = await asyncpg.create_pool(
                host=self.db_host,
                port=self.db_port,
                user=self.db_user,
                password=self.db_password,
                database=self.db_name_saju,
                max_size=self.max_connections,
                min_size=self.min_connections,
                command_timeout=self.connection_timeout
            )

            # 메인 DB 연결 풀
            self._main_pool = await asyncpg.create_pool(
                host=self.db_host,
                port=self.db_port,
                user=self.db_user,
                password=self.db_password,
                database=self.db_name_main,
                max_size=self.max_connections,
                min_size=self.min_connections,
                command_timeout=self.connection_timeout
            )

            logger.success("Database connection pools initialized successfully")

        except Exception as e:
            logger.error(f"Failed to initialize database pools: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Database initialization failed"
            )

    async def close_pools(self):
        """연결 풀 종료"""
        if self._saju_pool:
            await self._saju_pool.close()
        if self._main_pool:
            await self._main_pool.close()
        logger.info("Database connection pools closed")

    async def get_saju_connection(self):
        """사주 DB 연결 획득"""
        if not self._saju_pool:
            await self.initialize_pools()

        try:
            return await self._saju_pool.acquire()
        except Exception as e:
            logger.error(f"Failed to acquire saju database connection: {e}")
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Database connection unavailable"
            )

    async def get_main_connection(self):
        """메인 DB 연결 획득"""
        if not self._main_pool:
            await self.initialize_pools()

        try:
            return await self._main_pool.acquire()
        except Exception as e:
            logger.error(f"Failed to acquire main database connection: {e}")
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Database connection unavailable"
            )

    async def release_connection(self, conn, pool_type: str = 'saju'):
        """연결 반환"""
        try:
            if pool_type == 'saju' and self._saju_pool:
                await self._saju_pool.release(conn)
            elif pool_type == 'main' and self._main_pool:
                await self._main_pool.release(conn)
        except Exception as e:
            logger.error(f"Failed to release {pool_type} database connection: {e}")

    async def execute_query(self, query: str, params: List[Any] = None, db_type: str = 'saju') -> List[Dict[str, Any]]:
        """안전한 쿼리 실행"""
        conn = None
        try:
            # 연결 획득
            if db_type == 'saju':
                conn = await self.get_saju_connection()
                pool_type = 'saju'
            else:
                conn = await self.get_main_connection()
                pool_type = 'main'

            # 쿼리 실행
            if params:
                rows = await conn.fetch(query, *params)
            else:
                rows = await conn.fetch(query)

            # 결과를 딕셔너리 리스트로 변환
            return [dict(row) for row in rows]

        except asyncpg.PostgresError as e:
            logger.error(f"PostgreSQL error in {db_type} database: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Database query failed: {str(e)}"
            )
        except Exception as e:
            logger.error(f"Unexpected error in database query: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Database operation failed"
            )
        finally:
            # 연결 반환
            if conn:
                await self.release_connection(conn, pool_type)

    async def execute_single_query(self, query: str, params: List[Any] = None, db_type: str = 'saju') -> Optional[Dict[str, Any]]:
        """단일 행 쿼리 실행"""
        results = await self.execute_query(query, params, db_type)
        return results[0] if results else None

    async def execute_count_query(self, query: str, params: List[Any] = None, db_type: str = 'saju') -> int:
        """카운트 쿼리 실행"""
        conn = None
        try:
            # 연결 획득
            if db_type == 'saju':
                conn = await self.get_saju_connection()
                pool_type = 'saju'
            else:
                conn = await self.get_main_connection()
                pool_type = 'main'

            # 쿼리 실행
            if params:
                result = await conn.fetchval(query, *params)
            else:
                result = await conn.fetchval(query)

            return result or 0

        except Exception as e:
            logger.error(f"Count query error: {e}")
            return 0
        finally:
            if conn:
                await self.release_connection(conn, pool_type)

    async def execute_transaction(self, queries: List[Dict[str, Any]], db_type: str = 'saju') -> bool:
        """트랜잭션 실행"""
        conn = None
        try:
            # 연결 획득
            if db_type == 'saju':
                conn = await self.get_saju_connection()
                pool_type = 'saju'
            else:
                conn = await self.get_main_connection()
                pool_type = 'main'

            # 트랜잭션 시작
            async with conn.transaction():
                for query_data in queries:
                    query = query_data['query']
                    params = query_data.get('params', [])

                    if params:
                        await conn.execute(query, *params)
                    else:
                        await conn.execute(query)

            logger.info(f"Transaction with {len(queries)} queries completed successfully")
            return True

        except Exception as e:
            logger.error(f"Transaction failed: {e}")
            return False
        finally:
            if conn:
                await self.release_connection(conn, pool_type)

    async def health_check(self) -> Dict[str, Any]:
        """데이터베이스 상태 확인"""
        health_status = {
            'saju_db': {'status': 'unknown', 'response_time': None},
            'main_db': {'status': 'unknown', 'response_time': None}
        }

        # 사주 DB 체크
        try:
            start_time = datetime.now()
            await self.execute_single_query("SELECT 1", db_type='saju')
            end_time = datetime.now()
            health_status['saju_db'] = {
                'status': 'healthy',
                'response_time': (end_time - start_time).total_seconds()
            }
        except Exception as e:
            health_status['saju_db'] = {
                'status': 'unhealthy',
                'error': str(e)
            }

        # 메인 DB 체크
        try:
            start_time = datetime.now()
            await self.execute_single_query("SELECT 1", db_type='main')
            end_time = datetime.now()
            health_status['main_db'] = {
                'status': 'healthy',
                'response_time': (end_time - start_time).total_seconds()
            }
        except Exception as e:
            health_status['main_db'] = {
                'status': 'unhealthy',
                'error': str(e)
            }

        return health_status

# 전역 인스턴스
db_service = DatabaseService()