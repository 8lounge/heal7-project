"""
꿈풀이 다각도 해석 API 엔드포인트
6개 문화적 관점별 해석 데이터 제공
"""

from fastapi import APIRouter, HTTPException, Query
from typing import List, Dict, Optional, Any
import json
import subprocess
from pathlib import Path

router = APIRouter(
    prefix="/api/dream-multi",
    tags=["dream-multi-perspective"]
)

def execute_db_query(query: str, params: tuple = ()) -> List[Dict[str, Any]]:
    """PostgreSQL 쿼리 실행 (subprocess 기반 안전한 DB 연결)"""
    try:
        cmd = [
            "psql", 
            "-d", "heal7_saju",
            "-U", "ubuntu", 
            "-t", "-A", "-F", "\t",
            "-c", query
        ]
        
        result = subprocess.run(
            cmd, 
            capture_output=True, 
            text=True, 
            check=True,
            timeout=10
        )
        
        if not result.stdout.strip():
            return []
            
        rows = []
        for line in result.stdout.strip().split('\n'):
            if line.strip():
                parts = line.split('\t')
                rows.append(parts)
                
        return rows
        
    except subprocess.TimeoutExpired:
        raise HTTPException(status_code=504, detail="데이터베이스 쿼리 시간 초과")
    except subprocess.CalledProcessError as e:
        raise HTTPException(status_code=500, detail=f"데이터베이스 오류: {e.stderr}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"서버 오류: {str(e)}")

@router.get("/search")
async def search_multi_perspective_dreams(
    keyword: str = Query(..., description="검색할 꿈 키워드"),
    category: Optional[str] = Query(None, description="카테고리 필터 (동물, 자연현상, 인간관계, 상황감정, 사물)"),
    fortune_type: Optional[str] = Query(None, description="길흉 필터 (길몽, 흉몽, 길흉반반, 중립)"),
    min_confidence: Optional[float] = Query(None, description="최소 신뢰도 점수", ge=1.0, le=10.0)
):
    """
    꿈 키워드 검색 - 6개 관점별 해석 제공
    """
    try:
        where_conditions = ["keyword ILIKE %s"]
        params = [f"%{keyword}%"]
        
        if category:
            where_conditions.append("category = %s")
            params.append(category)
            
        if fortune_type:
            where_conditions.append("primary_fortune_type = %s")
            params.append(fortune_type)
            
        if min_confidence:
            where_conditions.append("average_confidence >= %s")
            params.append(str(min_confidence))
            
        # SQL 쿼리 직접 구성 (subprocess 방식)
        query_parts = [f"keyword ILIKE '%{keyword}%'"]
        
        if category:
            query_parts.append(f"category = '{category}'")
        if fortune_type:
            query_parts.append(f"primary_fortune_type = '{fortune_type}'")
        if min_confidence:
            query_parts.append(f"average_confidence >= {min_confidence}")
            
        where_clause = " AND ".join(query_parts)
        
        query_with_params = f"""
        SELECT 
            keyword_id, keyword, category,
            korean_traditional::text, chinese_traditional::text, 
            western_psychology::text, islamic_perspective::text,
            buddhist_perspective::text, scientific_perspective::text,
            primary_fortune_type, average_confidence, quality_score
        FROM dream_service.multi_perspective_interpretations 
        WHERE {where_clause}
        ORDER BY average_confidence DESC, quality_score DESC
        LIMIT 20;
        """
        
        rows = execute_db_query(query_with_params)
        
        results = []
        for row in rows:
            if len(row) >= 12:
                try:
                    result_item = {
                        "keyword_id": int(row[0]) if row[0].isdigit() else 0,
                        "keyword": row[1],
                        "category": row[2],
                        "perspectives": {
                            "korean_traditional": json.loads(row[3]) if row[3] and row[3] != '{}' else {},
                            "chinese_traditional": json.loads(row[4]) if row[4] and row[4] != '{}' else {},
                            "western_psychology": json.loads(row[5]) if row[5] and row[5] != '{}' else {},
                            "islamic_perspective": json.loads(row[6]) if row[6] and row[6] != '{}' else {},
                            "buddhist_perspective": json.loads(row[7]) if row[7] and row[7] != '{}' else {},
                            "scientific_perspective": json.loads(row[8]) if row[8] and row[8] != '{}' else {}
                        },
                        "primary_fortune_type": row[9],
                        "average_confidence": float(row[10]) if row[10] else 8.0,
                        "quality_score": float(row[11]) if row[11] else 8.0
                    }
                    results.append(result_item)
                except (json.JSONDecodeError, ValueError) as e:
                    continue
        
        return {
            "status": "success",
            "query": keyword,
            "filters": {
                "category": category,
                "fortune_type": fortune_type,
                "min_confidence": min_confidence
            },
            "total_results": len(results),
            "results": results
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"검색 실패: {str(e)}")

@router.get("/categories")
async def get_keywords_by_categories():
    """
    카테고리별 키워드 목록 조회
    """
    try:
        query = """
        SELECT category, array_agg(keyword ORDER BY keyword_id) as keywords
        FROM dream_service.multi_perspective_interpretations 
        GROUP BY category 
        ORDER BY category;
        """
        
        rows = execute_db_query(query)
        
        categories = {}
        for row in rows:
            if len(row) >= 2:
                category = row[0]
                keywords_str = row[1].strip('{}')  # PostgreSQL array 형태 처리
                keywords = [k.strip('"') for k in keywords_str.split(',') if k.strip()]
                categories[category] = keywords
        
        return {
            "status": "success", 
            "categories": categories,
            "total_categories": len(categories)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"카테고리 조회 실패: {str(e)}")

@router.get("/stats/fortune-types")
async def get_fortune_type_statistics():
    """
    길흉 유형별 통계 조회
    """
    try:
        query = """
        SELECT 
            primary_fortune_type,
            COUNT(*) as count,
            AVG(average_confidence) as avg_confidence,
            AVG(quality_score) as avg_quality,
            MIN(average_confidence) as min_confidence,
            MAX(average_confidence) as max_confidence
        FROM dream_service.multi_perspective_interpretations 
        GROUP BY primary_fortune_type 
        ORDER BY count DESC;
        """
        
        rows = execute_db_query(query)
        
        stats = []
        for row in rows:
            if len(row) >= 6:
                stats.append({
                    "fortune_type": row[0],
                    "count": int(row[1]) if row[1].isdigit() else 0,
                    "avg_confidence": round(float(row[2]), 1) if row[2] else 0.0,
                    "avg_quality": round(float(row[3]), 1) if row[3] else 0.0,
                    "confidence_range": {
                        "min": round(float(row[4]), 1) if row[4] else 0.0,
                        "max": round(float(row[5]), 1) if row[5] else 0.0
                    }
                })
        
        return {
            "status": "success",
            "statistics": stats,
            "total_keywords": sum([s["count"] for s in stats])
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"통계 조회 실패: {str(e)}")

@router.get("/keyword/{keyword_id}")
async def get_keyword_detail(keyword_id: int):
    """
    특정 키워드 ID의 상세 정보 조회
    """
    try:
        query = f"""
        SELECT 
            keyword_id, keyword, category,
            korean_traditional::text, chinese_traditional::text,
            western_psychology::text, islamic_perspective::text,
            buddhist_perspective::text, scientific_perspective::text,
            primary_fortune_type, average_confidence, quality_score,
            created_at, updated_at
        FROM dream_service.multi_perspective_interpretations 
        WHERE keyword_id = {keyword_id};
        """
        
        rows = execute_db_query(query)
        
        if not rows or len(rows[0]) < 13:
            raise HTTPException(status_code=404, detail=f"키워드 ID {keyword_id}를 찾을 수 없습니다")
            
        row = rows[0]
        
        result = {
            "keyword_id": int(row[0]) if row[0].isdigit() else 0,
            "keyword": row[1],
            "category": row[2],
            "perspectives": {
                "korean_traditional": json.loads(row[3]) if row[3] and row[3] != '{}' else {},
                "chinese_traditional": json.loads(row[4]) if row[4] and row[4] != '{}' else {},
                "western_psychology": json.loads(row[5]) if row[5] and row[5] != '{}' else {},
                "islamic_perspective": json.loads(row[6]) if row[6] and row[6] != '{}' else {},
                "buddhist_perspective": json.loads(row[7]) if row[7] and row[7] != '{}' else {},
                "scientific_perspective": json.loads(row[8]) if row[8] and row[8] != '{}' else {}
            },
            "primary_fortune_type": row[9],
            "average_confidence": float(row[10]) if row[10] else 8.0,
            "quality_score": float(row[11]) if row[11] else 8.0,
            "metadata": {
                "created_at": row[12] if len(row) > 12 else None,
                "updated_at": row[13] if len(row) > 13 else None
            }
        }
        
        return {
            "status": "success",
            "keyword_detail": result
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"키워드 조회 실패: {str(e)}")

@router.get("/health")
async def health_check():
    """
    다각도 해석 시스템 상태 확인
    """
    try:
        query = """
        SELECT 
            COUNT(*) as total_keywords,
            COUNT(DISTINCT category) as total_categories,
            AVG(average_confidence) as system_avg_confidence,
            AVG(quality_score) as system_avg_quality
        FROM dream_service.multi_perspective_interpretations;
        """
        
        rows = execute_db_query(query)
        
        if rows and len(rows[0]) >= 4:
            row = rows[0]
            return {
                "status": "healthy",
                "system_info": {
                    "total_keywords": int(row[0]) if row[0].isdigit() else 0,
                    "total_categories": int(row[1]) if row[1].isdigit() else 0,
                    "avg_confidence": round(float(row[2]), 1) if row[2] else 0.0,
                    "avg_quality": round(float(row[3]), 1) if row[3] else 0.0
                },
                "perspectives_supported": [
                    "korean_traditional", "chinese_traditional", "western_psychology",
                    "islamic_perspective", "buddhist_perspective", "scientific_perspective"
                ],
                "database_connection": "active"
            }
        else:
            raise HTTPException(status_code=503, detail="시스템 상태 확인 실패")
            
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"상태 확인 실패: {str(e)}")