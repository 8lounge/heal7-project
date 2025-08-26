#!/usr/bin/env python3
"""
HEAL7 키워드 시스템 API
실제 데이터베이스 연동 키워드 관리 및 매트릭스 API
"""

import logging
from typing import List, Optional, Dict, Any
from datetime import datetime

from fastapi import APIRouter, HTTPException, Depends, Query
from pydantic import BaseModel
import asyncpg
import redis
import json
import os

# 로깅 설정
logger = logging.getLogger(__name__)

# API 라우터 생성 (관리자 백엔드용)
router = APIRouter(prefix="/admin-api/keywords", tags=["Keywords"])

# 데이터베이스 연결 정보
DATABASE_URL = "postgresql://devuser:devpass@localhost:5432/devdb"
REDIS_URL = "redis://localhost:6379"

# Pydantic 모델 정의
class KeywordResponse(BaseModel):
    id: int
    name: str
    category: str
    subcategory: str
    weight: float
    connections: int
    status: str
    dependencies: List[int]
    position: Optional[List[float]] = None
    color: Optional[str] = None

class KeywordCreate(BaseModel):
    name: str
    subcategory: str
    weight: Optional[float] = 5.0
    is_active: Optional[bool] = True

class KeywordUpdate(BaseModel):
    name: Optional[str] = None
    subcategory: Optional[str] = None
    weight: Optional[float] = None
    is_active: Optional[bool] = None

class KeywordMatrix(BaseModel):
    total_keywords: int
    active_keywords: int
    total_connections: int
    network_density: float
    keywords: List[KeywordResponse]
    last_updated: datetime

class DependencyNetwork(BaseModel):
    keyword_id: int
    dependencies: List[Dict[str, Any]]
    strength_scores: Dict[int, float]

# 카테고리별 색상 매핑
CATEGORY_COLORS = {
    'A-1': '#3B82F6', 'A-2': '#06B6D4', 'A-3': '#10B981', 'A-4': '#8B5CF6', 'A-5': '#F59E0B',
    'B-1': '#EF4444', 'B-2': '#EC4899', 'B-3': '#6366F1', 'B-4': '#84CC16', 'B-5': '#F97316', 'B-6': '#14B8A6',
    'C-1': '#DC2626', 'C-2': '#7C2D12', 'C-3': '#991B1B', 'C-4': '#7C2D12', 'C-5': '#BE123C',
    'C-6': '#A21CAF', 'C-7': '#581C87', 'C-8': '#1E1B4B', 'C-9': '#450A0A'
}

# 유틸리티 함수들
async def get_db_connection():
    """데이터베이스 연결 획득"""
    try:
        return await asyncpg.connect(DATABASE_URL)
    except Exception as e:
        logger.error(f"Database connection failed: {e}")
        raise HTTPException(status_code=500, detail="Database connection failed")

def get_redis_client():
    """Redis 클라이언트 획득"""
    try:
        return redis.from_url(REDIS_URL, decode_responses=True)
    except Exception as e:
        logger.error(f"Redis connection failed: {e}")
        return None

def generate_sphere_positions(count: int, radius: float = 2.2) -> List[List[float]]:
    """구체 표면에 균등하게 점들을 분산시키는 함수 (Golden Spiral)"""
    import math
    
    positions = []
    phi = math.pi * (3 - math.sqrt(5))  # Golden angle

    for i in range(count):
        y = 1 - (i / (count - 1)) * 2  # y goes from 1 to -1
        radius_at_y = math.sqrt(1 - y * y) * radius
        theta = phi * i

        x = math.cos(theta) * radius_at_y
        z = math.sin(theta) * radius_at_y
        
        positions.append([x, y * radius, z])

    return positions

# API 엔드포인트들

@router.get("/", response_model=List[KeywordResponse])
async def get_keywords(
    category: Optional[str] = Query(None, description="필터링할 카테고리 (A, B, C)"),
    search: Optional[str] = Query(None, description="검색할 키워드 텍스트"),
    limit: int = Query(100, description="반환할 키워드 수 제한")
):
    """키워드 목록 조회 (키워드 관리용)"""
    
    # Redis 캐시 확인
    redis_client = get_redis_client()
    cache_key = f"keywords:{category or 'all'}:{search or 'none'}:{limit}"
    
    if redis_client:
        cached_data = redis_client.get(cache_key)
        if cached_data:
            logger.info("Returning cached keyword data")
            return json.loads(cached_data)
    
    conn = await get_db_connection()
    try:
        # 키워드와 의존성 정보를 함께 조회
        query = """
        SELECT 
            k.id,
            k.text as name,
            COALESCE(ksc.name, 'Unknown') as subcategory,
            COUNT(kd.dependent_keyword_id) as connections,
            COALESCE(AVG(kd.weight), 0) as avg_weight,
            k.is_active
        FROM keywords k
        LEFT JOIN keyword_subcategories ksc ON k.subcategory_id = ksc.id
        LEFT JOIN keyword_dependencies kd ON k.id = kd.parent_keyword_id AND kd.is_active = true
        WHERE k.is_active = true
        """
        
        params = []
        param_count = 0
        
        if category:
            param_count += 1
            query += f" AND ksc.name LIKE ${param_count}"
            params.append(f"{category}%")
            
        if search:
            param_count += 1
            query += f" AND k.text ILIKE ${param_count}"
            params.append(f"%{search}%")
        
        query += " GROUP BY k.id, k.text, ksc.name, k.is_active ORDER BY connections DESC"
        
        if limit:
            param_count += 1
            query += f" LIMIT ${param_count}"
            params.append(limit)
        
        rows = await conn.fetch(query, *params)
        
        # 의존성 관계 조회
        dependency_query = """
        SELECT parent_keyword_id, array_agg(dependent_keyword_id) as dependencies
        FROM keyword_dependencies 
        WHERE is_active = true 
        GROUP BY parent_keyword_id
        """
        dependency_rows = await conn.fetch(dependency_query)
        dependency_map = {row['parent_keyword_id']: row['dependencies'] for row in dependency_rows}
        
        keywords = []
        for row in rows:
            keyword = KeywordResponse(
                id=row['id'],
                name=row['name'],
                category=row['subcategory'][:3] if row['subcategory'] != 'Unknown' else 'Unknown',
                subcategory=row['subcategory'],
                weight=float(row['avg_weight'] or 0),
                connections=row['connections'],
                status='active' if row['is_active'] else 'inactive',
                dependencies=dependency_map.get(row['id'], []),
                color=CATEGORY_COLORS.get(row['subcategory'][:3], '#888888')
            )
            keywords.append(keyword)
        
        # Redis 캐시에 저장 (5분 TTL)
        if redis_client:
            redis_client.setex(
                cache_key, 
                300, 
                json.dumps([k.dict() for k in keywords], default=str)
            )
        
        logger.info(f"Retrieved {len(keywords)} keywords from database")
        return keywords
        
    except Exception as e:
        logger.error(f"Error fetching keywords: {e}")
        raise HTTPException(status_code=500, detail=f"Error fetching keywords: {str(e)}")
    finally:
        await conn.close()

@router.get("/matrix", response_model=KeywordMatrix)
async def get_keyword_matrix():
    """키워드 매트릭스 데이터 조회 (3D 시각화용)"""
    
    # Redis 캐시 확인
    redis_client = get_redis_client()
    cache_key = "keyword_matrix:full"
    
    if redis_client:
        cached_data = redis_client.get(cache_key)
        if cached_data:
            logger.info("Returning cached matrix data")
            cached_dict = json.loads(cached_data)
            cached_dict['last_updated'] = datetime.fromisoformat(cached_dict['last_updated'])
            return KeywordMatrix(**cached_dict)
    
    conn = await get_db_connection()
    try:
        # 전체 키워드 통계 조회
        stats_query = """
        SELECT 
            COUNT(DISTINCT k.id) as total_keywords,
            COUNT(DISTINCT CASE WHEN k.is_active THEN k.id END) as active_keywords,
            COUNT(DISTINCT kd.id) as total_connections
        FROM keywords k
        LEFT JOIN keyword_dependencies kd ON k.id = kd.parent_keyword_id AND kd.is_active = true
        """
        stats_row = await conn.fetchrow(stats_query)
        
        # 모든 키워드와 연결 정보 조회
        keywords_query = """
        SELECT 
            k.id,
            k.text as name,
            COALESCE(ksc.name, 'Unknown') as subcategory,
            COUNT(kd.dependent_keyword_id) as connections,
            COALESCE(AVG(kd.weight), 0) as avg_weight,
            k.is_active
        FROM keywords k
        LEFT JOIN keyword_subcategories ksc ON k.subcategory_id = ksc.id
        LEFT JOIN keyword_dependencies kd ON k.id = kd.parent_keyword_id AND kd.is_active = true
        WHERE k.is_active = true
        GROUP BY k.id, k.text, ksc.name, k.is_active
        ORDER BY k.id
        """
        keyword_rows = await conn.fetch(keywords_query)
        
        # 의존성 관계 조회
        dependency_query = """
        SELECT parent_keyword_id, array_agg(dependent_keyword_id) as dependencies
        FROM keyword_dependencies 
        WHERE is_active = true 
        GROUP BY parent_keyword_id
        """
        dependency_rows = await conn.fetch(dependency_query)
        dependency_map = {row['parent_keyword_id']: row['dependencies'] for row in dependency_rows}
        
        # 3D 위치 생성
        positions = generate_sphere_positions(len(keyword_rows))
        
        keywords = []
        for i, row in enumerate(keyword_rows):
            keyword = KeywordResponse(
                id=row['id'],
                name=row['name'],
                category=row['subcategory'][:3] if row['subcategory'] != 'Unknown' else 'Unknown',
                subcategory=row['subcategory'],
                weight=float(row['avg_weight'] or 0),
                connections=row['connections'],
                status='active' if row['is_active'] else 'inactive',
                dependencies=dependency_map.get(row['id'], []),
                position=positions[i] if i < len(positions) else [0, 0, 0],
                color=CATEGORY_COLORS.get(row['subcategory'][:3], '#888888')
            )
            keywords.append(keyword)
        
        # 네트워크 밀도 계산
        total_possible_connections = len(keywords) * (len(keywords) - 1)
        network_density = (stats_row['total_connections'] * 2 / total_possible_connections * 100) if total_possible_connections > 0 else 0
        
        matrix = KeywordMatrix(
            total_keywords=stats_row['total_keywords'],
            active_keywords=stats_row['active_keywords'],
            total_connections=stats_row['total_connections'],
            network_density=round(network_density, 1),
            keywords=keywords,
            last_updated=datetime.now()
        )
        
        # Redis 캐시에 저장 (10분 TTL)
        if redis_client:
            cache_data = matrix.dict()
            cache_data['last_updated'] = cache_data['last_updated'].isoformat()
            redis_client.setex(
                cache_key, 
                600, 
                json.dumps(cache_data, default=str)
            )
        
        logger.info(f"Generated matrix with {len(keywords)} keywords")
        return matrix
        
    except Exception as e:
        logger.error(f"Error generating keyword matrix: {e}")
        raise HTTPException(status_code=500, detail=f"Error generating matrix: {str(e)}")
    finally:
        await conn.close()

@router.get("/dependencies/{keyword_id}", response_model=DependencyNetwork)
async def get_keyword_dependencies(keyword_id: int):
    """특정 키워드의 의존성 네트워크 조회"""
    
    conn = await get_db_connection()
    try:
        # 키워드 존재 확인
        keyword_check = await conn.fetchrow(
            "SELECT id, text FROM keywords WHERE id = $1 AND is_active = true", 
            keyword_id
        )
        
        if not keyword_check:
            raise HTTPException(status_code=404, detail="Keyword not found")
        
        # 의존성 관계 조회 (양방향)
        dependencies_query = """
        SELECT 
            kd.dependent_keyword_id as dep_id,
            k.text as dep_name,
            kd.dependency_strength,
            kd.weight,
            kd.dependency_type,
            'outgoing' as direction
        FROM keyword_dependencies kd
        JOIN keywords k ON kd.dependent_keyword_id = k.id
        WHERE kd.parent_keyword_id = $1 AND kd.is_active = true AND k.is_active = true
        
        UNION ALL
        
        SELECT 
            kd.parent_keyword_id as dep_id,
            k.text as dep_name,
            kd.dependency_strength,
            kd.weight,
            kd.dependency_type,
            'incoming' as direction
        FROM keyword_dependencies kd
        JOIN keywords k ON kd.parent_keyword_id = k.id
        WHERE kd.dependent_keyword_id = $1 AND kd.is_active = true AND k.is_active = true
        """
        
        dependency_rows = await conn.fetch(dependencies_query, keyword_id)
        
        dependencies = []
        strength_scores = {}
        
        for row in dependency_rows:
            dep_info = {
                'id': row['dep_id'],
                'name': row['dep_name'],
                'strength': float(row['dependency_strength'] or 0),
                'weight': float(row['weight'] or 0),
                'type': row['dependency_type'] or 'general',
                'direction': row['direction']
            }
            dependencies.append(dep_info)
            strength_scores[row['dep_id']] = float(row['dependency_strength'] or 0)
        
        network = DependencyNetwork(
            keyword_id=keyword_id,
            dependencies=dependencies,
            strength_scores=strength_scores
        )
        
        logger.info(f"Retrieved {len(dependencies)} dependencies for keyword {keyword_id}")
        return network
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching dependencies for keyword {keyword_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Error fetching dependencies: {str(e)}")
    finally:
        await conn.close()

@router.get("/matrix/data")
async def get_keyword_matrix_data():
    """레거시 3D 시각화용 키워드 매트릭스 데이터 (특별 형식)"""
    
    # Redis 캐시 확인
    redis_client = get_redis_client()
    cache_key = "keyword_matrix:legacy_format"
    
    if redis_client:
        cached_data = redis_client.get(cache_key)
        if cached_data:
            logger.info("Returning cached legacy matrix data")
            return json.loads(cached_data)
    
    conn = await get_db_connection()
    try:
        # 모든 활성 키워드 조회
        keywords_query = """
        SELECT 
            k.id,
            k.text,
            COALESCE(ksc.name, 'Unknown') as subcategory,
            k.is_active
        FROM keywords k
        LEFT JOIN keyword_subcategories ksc ON k.subcategory_id = ksc.id
        WHERE k.is_active = true
        ORDER BY k.id
        """
        keyword_rows = await conn.fetch(keywords_query)
        
        # 의존성 관계 조회
        dependencies_query = """
        SELECT 
            kd.parent_keyword_id,
            kd.dependent_keyword_id,
            kd.weight,
            kd.dependency_strength
        FROM keyword_dependencies kd
        WHERE kd.is_active = true
        """
        dependency_rows = await conn.fetch(dependencies_query)
        
        # 레거시 형식으로 변환
        keywords_legacy = []
        for row in keyword_rows:
            keywords_legacy.append({
                'id': row['id'],
                'text': row['text'],  # 레거시는 'text' 필드 사용
                'subcategory': row['subcategory']
            })
        
        dependencies_legacy = []
        for row in dependency_rows:
            dependencies_legacy.append({
                'parent_keyword_id': row['parent_keyword_id'],
                'dependent_keyword_id': row['dependent_keyword_id'],
                'weight': float(row['weight'] or 1.0),
                'dependency_strength': float(row['dependency_strength'] or 1.0)
            })
        
        # 레거시 HTML이 기대하는 형식
        result = {
            'keywords': keywords_legacy,
            'dependencies': dependencies_legacy,
            'stats': {
                'total_keywords': len(keywords_legacy),
                'total_dependencies': len(dependencies_legacy),
                'cache_status': 'database_fresh'
            }
        }
        
        # Redis 캐시에 저장 (5분 TTL)
        if redis_client:
            redis_client.setex(
                cache_key, 
                300, 
                json.dumps(result, default=str)
            )
        
        logger.info(f"Generated legacy matrix data: {len(keywords_legacy)} keywords, {len(dependencies_legacy)} dependencies")
        return result
        
    except Exception as e:
        logger.error(f"Error generating legacy matrix data: {e}")
        raise HTTPException(status_code=500, detail=f"Error generating legacy matrix data: {str(e)}")
    finally:
        await conn.close()

@router.get("/stats")
async def get_keyword_stats():
    """키워드 시스템 통계 조회"""
    
    conn = await get_db_connection()
    try:
        stats_query = """
        SELECT 
            COUNT(DISTINCT k.id) as total_keywords,
            COUNT(DISTINCT CASE WHEN k.is_active THEN k.id END) as active_keywords,
            COUNT(DISTINCT kd.id) as total_dependencies,
            COUNT(DISTINCT ksc.name) as total_categories,
            AVG(kd.weight) as avg_dependency_weight,
            MAX(k.updated_at) as last_updated
        FROM keywords k
        LEFT JOIN keyword_dependencies kd ON k.id = kd.parent_keyword_id AND kd.is_active = true
        LEFT JOIN keyword_subcategories ksc ON k.subcategory_id = ksc.name
        """
        
        stats_row = await conn.fetchrow(stats_query)
        
        # 카테고리별 분포 조회
        category_query = """
        SELECT 
            LEFT(ksc.name, 1) as category_group,
            COUNT(k.id) as keyword_count
        FROM keywords k
        JOIN keyword_subcategories ksc ON k.subcategory_id = ksc.name
        WHERE k.is_active = true
        GROUP BY LEFT(ksc.name, 1)
        ORDER BY category_group
        """
        
        category_rows = await conn.fetch(category_query)
        category_distribution = {row['category_group']: row['keyword_count'] for row in category_rows}
        
        stats = {
            'total_keywords': stats_row['total_keywords'],
            'active_keywords': stats_row['active_keywords'],
            'total_dependencies': stats_row['total_dependencies'],
            'total_categories': stats_row['total_categories'],
            'avg_dependency_weight': float(stats_row['avg_dependency_weight'] or 0),
            'category_distribution': category_distribution,
            'last_updated': stats_row['last_updated'],
            'cache_status': 'redis_connected' if get_redis_client() else 'redis_disconnected'
        }
        
        return stats
        
    except Exception as e:
        logger.error(f"Error fetching keyword stats: {e}")
        raise HTTPException(status_code=500, detail=f"Error fetching stats: {str(e)}")
    finally:
        await conn.close()

@router.post("/refresh-cache")
async def refresh_keyword_cache():
    """키워드 캐시 새로고침"""
    
    redis_client = get_redis_client()
    if not redis_client:
        raise HTTPException(status_code=503, detail="Redis not available")
    
    try:
        # 모든 키워드 관련 캐시 삭제
        cache_keys = redis_client.keys("keywords:*") + redis_client.keys("keyword_matrix:*")
        if cache_keys:
            redis_client.delete(*cache_keys)
            
        logger.info(f"Refreshed {len(cache_keys)} cache keys")
        return {"message": f"Cache refreshed successfully. Cleared {len(cache_keys)} keys."}
        
    except Exception as e:
        logger.error(f"Error refreshing cache: {e}")
        raise HTTPException(status_code=500, detail=f"Error refreshing cache: {str(e)}")

# 헬스체크 엔드포인트
@router.get("/health")
async def keyword_health_check():
    """키워드 API 헬스체크"""
    
    try:
        # 데이터베이스 연결 테스트
        conn = await get_db_connection()
        db_status = "connected"
        await conn.close()
    except:
        db_status = "disconnected"
    
    # Redis 연결 테스트
    redis_client = get_redis_client()
    redis_status = "connected" if redis_client else "disconnected"
    
    return {
        "service": "keywords_api",
        "status": "healthy" if (db_status == "connected") else "degraded",
        "database": db_status,
        "redis": redis_status,
        "timestamp": datetime.now().isoformat()
    }

# CRUD 엔드포인트들

@router.post("/", response_model=KeywordResponse)
async def create_keyword(keyword_data: KeywordCreate):
    """새 키워드 생성"""
    
    conn = await get_db_connection()
    try:
        # 서브카테고리 ID 확인
        subcategory_check = await conn.fetchrow(
            "SELECT id FROM keyword_subcategories WHERE name = $1", 
            keyword_data.subcategory
        )
        
        if not subcategory_check:
            raise HTTPException(status_code=400, detail=f"Subcategory '{keyword_data.subcategory}' not found")
        
        subcategory_id = subcategory_check['id']
        
        # 키워드 중복 확인
        existing_keyword = await conn.fetchrow(
            "SELECT id FROM keywords WHERE text = $1 AND is_active = true", 
            keyword_data.name
        )
        
        if existing_keyword:
            raise HTTPException(status_code=400, detail=f"Keyword '{keyword_data.name}' already exists")
        
        # 새 키워드 생성
        new_keyword = await conn.fetchrow("""
            INSERT INTO keywords (text, subcategory_id, is_active, created_at, updated_at)
            VALUES ($1, $2, $3, NOW(), NOW())
            RETURNING id, text, is_active, created_at
        """, keyword_data.name, subcategory_id, keyword_data.is_active)
        
        # 응답 데이터 구성
        keyword_response = KeywordResponse(
            id=new_keyword['id'],
            name=new_keyword['text'],
            category=keyword_data.subcategory[:3] if len(keyword_data.subcategory) >= 3 else keyword_data.subcategory,
            subcategory=keyword_data.subcategory,
            weight=keyword_data.weight,
            connections=0,  # 새 키워드는 연결이 없음
            status='active' if new_keyword['is_active'] else 'inactive',
            dependencies=[],
            color=CATEGORY_COLORS.get(keyword_data.subcategory[:3], '#888888')
        )
        
        # 캐시 삭제
        redis_client = get_redis_client()
        if redis_client:
            cache_keys = redis_client.keys("keywords:*") + redis_client.keys("keyword_matrix:*")
            if cache_keys:
                redis_client.delete(*cache_keys)
        
        logger.info(f"Created new keyword: {keyword_data.name}")
        return keyword_response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating keyword: {e}")
        raise HTTPException(status_code=500, detail=f"Error creating keyword: {str(e)}")
    finally:
        await conn.close()

@router.put("/{keyword_id}", response_model=KeywordResponse)
async def update_keyword(keyword_id: int, keyword_data: KeywordUpdate):
    """키워드 수정"""
    
    conn = await get_db_connection()
    try:
        # 키워드 존재 확인
        existing_keyword = await conn.fetchrow(
            "SELECT id, text, subcategory_id, is_active FROM keywords WHERE id = $1", 
            keyword_id
        )
        
        if not existing_keyword:
            raise HTTPException(status_code=404, detail="Keyword not found")
        
        # 업데이트할 필드들 준비
        update_fields = []
        params = []
        param_count = 0
        
        if keyword_data.name is not None:
            param_count += 1
            update_fields.append(f"text = ${param_count}")
            params.append(keyword_data.name)
            
        if keyword_data.subcategory is not None:
            # 서브카테고리 ID 확인
            subcategory_check = await conn.fetchrow(
                "SELECT id FROM keyword_subcategories WHERE name = $1", 
                keyword_data.subcategory
            )
            
            if not subcategory_check:
                raise HTTPException(status_code=400, detail=f"Subcategory '{keyword_data.subcategory}' not found")
            
            param_count += 1
            update_fields.append(f"subcategory_id = ${param_count}")
            params.append(subcategory_check['id'])
            
        if keyword_data.is_active is not None:
            param_count += 1
            update_fields.append(f"is_active = ${param_count}")
            params.append(keyword_data.is_active)
        
        # updated_at 필드 추가
        param_count += 1
        update_fields.append(f"updated_at = ${param_count}")
        params.append(datetime.now())
        
        # WHERE 절을 위한 키워드 ID 추가
        param_count += 1
        params.append(keyword_id)
        
        if not update_fields:
            raise HTTPException(status_code=400, detail="No fields to update")
        
        # 업데이트 실행
        update_query = f"""
            UPDATE keywords 
            SET {', '.join(update_fields)}
            WHERE id = ${param_count}
            RETURNING id, text, subcategory_id, is_active
        """
        
        updated_keyword = await conn.fetchrow(update_query, *params)
        
        # 서브카테고리 이름 조회
        subcategory_name = await conn.fetchval(
            "SELECT name FROM keyword_subcategories WHERE id = $1",
            updated_keyword['subcategory_id']
        )
        
        # 연결 수 조회
        connections_count = await conn.fetchval(
            "SELECT COUNT(*) FROM keyword_dependencies WHERE parent_keyword_id = $1 AND is_active = true",
            keyword_id
        )
        
        # 평균 가중치 조회
        avg_weight = await conn.fetchval(
            "SELECT COALESCE(AVG(weight), 0) FROM keyword_dependencies WHERE parent_keyword_id = $1 AND is_active = true",
            keyword_id
        )
        
        # 응답 데이터 구성
        keyword_response = KeywordResponse(
            id=updated_keyword['id'],
            name=updated_keyword['text'],
            category=subcategory_name[:3] if subcategory_name and len(subcategory_name) >= 3 else 'Unknown',
            subcategory=subcategory_name or 'Unknown',
            weight=float(avg_weight or keyword_data.weight or 5.0),
            connections=connections_count or 0,
            status='active' if updated_keyword['is_active'] else 'inactive',
            dependencies=[],
            color=CATEGORY_COLORS.get(subcategory_name[:3] if subcategory_name else 'Unknown', '#888888')
        )
        
        # 캐시 삭제
        redis_client = get_redis_client()
        if redis_client:
            cache_keys = redis_client.keys("keywords:*") + redis_client.keys("keyword_matrix:*")
            if cache_keys:
                redis_client.delete(*cache_keys)
        
        logger.info(f"Updated keyword {keyword_id}: {updated_keyword['text']}")
        return keyword_response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating keyword {keyword_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Error updating keyword: {str(e)}")
    finally:
        await conn.close()

@router.delete("/{keyword_id}")
async def delete_keyword(keyword_id: int):
    """키워드 삭제 (소프트 삭제)"""
    
    conn = await get_db_connection()
    try:
        # 키워드 존재 확인
        existing_keyword = await conn.fetchrow(
            "SELECT id, text, is_active FROM keywords WHERE id = $1", 
            keyword_id
        )
        
        if not existing_keyword:
            raise HTTPException(status_code=404, detail="Keyword not found")
        
        # 소프트 삭제 (is_active = false)
        await conn.execute("""
            UPDATE keywords 
            SET is_active = false, updated_at = NOW()
            WHERE id = $1
        """, keyword_id)
        
        # 관련 의존성도 비활성화
        await conn.execute("""
            UPDATE keyword_dependencies 
            SET is_active = false, updated_at = NOW()
            WHERE parent_keyword_id = $1 OR dependent_keyword_id = $1
        """, keyword_id)
        
        # 캐시 삭제
        redis_client = get_redis_client()
        if redis_client:
            cache_keys = redis_client.keys("keywords:*") + redis_client.keys("keyword_matrix:*")
            if cache_keys:
                redis_client.delete(*cache_keys)
        
        logger.info(f"Deleted keyword {keyword_id}: {existing_keyword['text']}")
        return {"message": f"Keyword '{existing_keyword['text']}' deleted successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting keyword {keyword_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Error deleting keyword: {str(e)}")
    finally:
        await conn.close()

@router.get("/{keyword_id}", response_model=KeywordResponse)
async def get_keyword(keyword_id: int):
    """특정 키워드 조회"""
    
    conn = await get_db_connection()
    try:
        # 키워드 정보 조회
        keyword_query = """
        SELECT 
            k.id,
            k.text as name,
            COALESCE(ksc.name, 'Unknown') as subcategory,
            COUNT(kd.dependent_keyword_id) as connections,
            COALESCE(AVG(kd.weight), 0) as avg_weight,
            k.is_active
        FROM keywords k
        LEFT JOIN keyword_subcategories ksc ON k.subcategory_id = ksc.id
        LEFT JOIN keyword_dependencies kd ON k.id = kd.parent_keyword_id AND kd.is_active = true
        WHERE k.id = $1
        GROUP BY k.id, k.text, ksc.name, k.is_active
        """
        
        keyword_row = await conn.fetchrow(keyword_query, keyword_id)
        
        if not keyword_row:
            raise HTTPException(status_code=404, detail="Keyword not found")
        
        # 의존성 목록 조회
        dependencies = await conn.fetch(
            "SELECT dependent_keyword_id FROM keyword_dependencies WHERE parent_keyword_id = $1 AND is_active = true",
            keyword_id
        )
        dependency_ids = [dep['dependent_keyword_id'] for dep in dependencies]
        
        # 응답 데이터 구성
        keyword_response = KeywordResponse(
            id=keyword_row['id'],
            name=keyword_row['name'],
            category=keyword_row['subcategory'][:3] if keyword_row['subcategory'] != 'Unknown' else 'Unknown',
            subcategory=keyword_row['subcategory'],
            weight=float(keyword_row['avg_weight'] or 0),
            connections=keyword_row['connections'],
            status='active' if keyword_row['is_active'] else 'inactive',
            dependencies=dependency_ids,
            color=CATEGORY_COLORS.get(keyword_row['subcategory'][:3], '#888888')
        )
        
        return keyword_response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching keyword {keyword_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Error fetching keyword: {str(e)}")
    finally:
        await conn.close()