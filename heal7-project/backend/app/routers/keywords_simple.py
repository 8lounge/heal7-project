#!/usr/bin/env python3
"""
HEAL7 키워드 시스템 API - 간소화 버전
실제 데이터베이스 연동 키워드 관리 및 매트릭스 API (복잡한 조인 없이)
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
import math

# 로깅 설정
logger = logging.getLogger(__name__)

# API 라우터 생성 (관리자 백엔드용)
router = APIRouter(prefix="/admin-api/keywords-simple", tags=["Keywords Simple"])

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

class KeywordMatrix(BaseModel):
    total_keywords: int
    active_keywords: int
    total_connections: int
    network_density: float
    keywords: List[KeywordResponse]
    last_updated: datetime

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
async def get_keywords_simple(
    limit: int = Query(100, description="반환할 키워드 수 제한")
):
    """키워드 목록 조회 (간소화 버전)"""
    
    conn = await get_db_connection()
    try:
        # 간단한 키워드 조회 (조인 없이)
        query = """
        SELECT 
            k.id,
            k.text as name,
            k.subcategory_id,
            k.is_active
        FROM keywords k
        WHERE k.is_active = true
        ORDER BY k.id
        LIMIT $1
        """
        
        rows = await conn.fetch(query, limit)
        
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
            # 기본값으로 처리
            subcategory = row['subcategory_id'] if row['subcategory_id'] else 'Unknown'
            category = subcategory[:1] if subcategory != 'Unknown' else 'Unknown'
            
            keyword = KeywordResponse(
                id=row['id'],
                name=row['name'],
                category=category,
                subcategory=subcategory,
                weight=5.0,  # 기본 가중치
                connections=len(dependency_map.get(row['id'], [])),
                status='active' if row['is_active'] else 'inactive',
                dependencies=dependency_map.get(row['id'], []),
                color=CATEGORY_COLORS.get(subcategory[:3], '#888888')
            )
            keywords.append(keyword)
        
        logger.info(f"Retrieved {len(keywords)} keywords from database (simple)")
        return keywords
        
    except Exception as e:
        logger.error(f"Error fetching keywords: {e}")
        raise HTTPException(status_code=500, detail=f"Error fetching keywords: {str(e)}")
    finally:
        await conn.close()

@router.get("/matrix", response_model=KeywordMatrix)
async def get_keyword_matrix_simple():
    """키워드 매트릭스 데이터 조회 (3D 시각화용, 간소화 버전)"""
    
    conn = await get_db_connection()
    try:
        # 모든 키워드 조회 (간단한 쿼리)
        keywords_query = """
        SELECT 
            k.id,
            k.text as name,
            k.subcategory_id,
            k.is_active
        FROM keywords k
        WHERE k.is_active = true
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
        
        # 전체 연결 수 계산
        total_connections = sum(len(deps) for deps in dependency_map.values())
        
        # 3D 위치 생성
        positions = generate_sphere_positions(len(keyword_rows))
        
        keywords = []
        for i, row in enumerate(keyword_rows):
            subcategory = row['subcategory_id'] if row['subcategory_id'] else 'Unknown'
            category = subcategory[:1] if subcategory != 'Unknown' else 'Unknown'
            dependencies = dependency_map.get(row['id'], [])
            
            keyword = KeywordResponse(
                id=row['id'],
                name=row['name'],
                category=category,
                subcategory=subcategory,
                weight=float(len(dependencies) + 2),  # 연결수 기반 가중치
                connections=len(dependencies),
                status='active' if row['is_active'] else 'inactive',
                dependencies=dependencies,
                position=positions[i] if i < len(positions) else [0, 0, 0],
                color=CATEGORY_COLORS.get(subcategory[:3], '#888888')
            )
            keywords.append(keyword)
        
        # 네트워크 밀도 계산
        total_possible_connections = len(keywords) * (len(keywords) - 1)
        network_density = (total_connections * 2 / total_possible_connections * 100) if total_possible_connections > 0 else 0
        
        matrix = KeywordMatrix(
            total_keywords=len(keywords),
            active_keywords=len(keywords),
            total_connections=total_connections,
            network_density=round(network_density, 1),
            keywords=keywords,
            last_updated=datetime.now()
        )
        
        logger.info(f"Generated matrix with {len(keywords)} keywords (simple)")
        return matrix
        
    except Exception as e:
        logger.error(f"Error generating keyword matrix: {e}")
        raise HTTPException(status_code=500, detail=f"Error generating matrix: {str(e)}")
    finally:
        await conn.close()

# 헬스체크 엔드포인트
@router.get("/health")
async def keyword_health_check_simple():
    """키워드 API 헬스체크 (간소화 버전)"""
    
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
        "service": "keywords_api_simple",
        "status": "healthy" if (db_status == "connected") else "degraded",
        "database": db_status,
        "redis": redis_status,
        "timestamp": datetime.now().isoformat()
    }