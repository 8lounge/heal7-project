"""
HEAL7 꿈풀이/해몽 API 엔드포인트 - 고성능 clean_dream_interpretations 연동
364개→15,000개 확장 데이터와 완전 연동된 최신 꿈풀이 API

@author HEAL7 Team  
@version 4.0.0 - Clean Dream System Integration
@updated 2025-09-04 - AI 확장 데이터 지원
"""

from fastapi import APIRouter, HTTPException
from typing import List, Optional
from pydantic import BaseModel
import subprocess
import json
import logging
import re
from datetime import datetime

logger = logging.getLogger(__name__)

# 메인 라우터
router = APIRouter(prefix="/api/dreams", tags=["dream-interpretation-v4"])

# 요청/응답 모델
class DreamKeywordSearch(BaseModel):
    keywords: List[str]
    search_mode: str = "smart"  # "smart", "exact", "fuzzy"
    limit: int = 10
    quality_threshold: float = 0.5

class DreamInterpretationResponse(BaseModel):
    keyword: str
    category: str
    traditional_meaning: str
    modern_meaning: str
    psychological_meaning: Optional[str] = None
    fortune_aspect: str  # 길몽/흉몽
    confidence_score: float
    related_keywords: List[str] = []
    lucky_numbers: List[int] = []
    search_relevance: float = 1.0

def parse_pg_array(pg_array: str) -> List[str]:
    """PostgreSQL 배열 파싱"""
    if not pg_array or pg_array == '{}':
        return []
    
    try:
        pg_array = pg_array.strip('{}')
        if not pg_array:
            return []
        
        items = []
        for item in pg_array.split(','):
            item = item.strip().strip('"').strip("'")
            if item:
                items.append(item)
        return items
        
    except Exception:
        return []

def parse_pg_int_array(pg_array: str) -> List[int]:
    """PostgreSQL 정수 배열 파싱"""
    if not pg_array or pg_array == '{}':
        return []
    
    try:
        pg_array = pg_array.strip('{}')
        if not pg_array:
            return []
        
        numbers = []
        for item in pg_array.split(','):
            try:
                num = int(item.strip())
                numbers.append(num)
            except ValueError:
                continue
        return numbers
        
    except Exception:
        return []

def query_dream_database(query: str) -> List[dict]:
    """Subprocess를 사용한 안전한 DB 쿼리 - Clean Dreams 테이블 지원"""
    try:
        cmd = [
            'sudo', '-u', 'postgres', 'psql', 'heal7',
            '-c', query,
            '-t', '-A', '--field-separator=☆'  # 특수 구분자
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            lines = result.stdout.strip().split('\n')
            records = []
            for line in lines:
                if line and line.strip():
                    parts = line.split('☆')
                    if len(parts) >= 8:  # clean_dream_interpretations 필드 수
                        records.append({
                            'keyword': parts[0],
                            'category': parts[1],
                            'traditional_meaning': parts[2],
                            'modern_meaning': parts[3],
                            'psychological_meaning': parts[4] if parts[4] else None,
                            'fortune_aspect': parts[5],
                            'confidence_score': float(parts[6]) if parts[6] else 8.0,
                            'related_keywords': parse_pg_array(parts[7]) if len(parts) > 7 else [],
                            'lucky_numbers': parse_pg_int_array(parts[8]) if len(parts) > 8 else []
                        })
            return records
        else:
            logger.error(f"Database query failed: {result.stderr}")
            return []
    except Exception as e:
        logger.error(f"Database query error: {e}")
        return []

def calculate_search_relevance(keyword: str, search_terms: List[str]) -> float:
    """검색 관련성 점수 계산"""
    keyword_lower = keyword.lower()
    max_relevance = 0.0
    
    for term in search_terms:
        term_lower = term.lower()
        
        if keyword_lower == term_lower:
            return 1.0  # 완전 일치
        elif term_lower in keyword_lower:
            max_relevance = max(max_relevance, 0.9)
        elif keyword_lower in term_lower:
            max_relevance = max(max_relevance, 0.8)
        elif keyword_lower.startswith(term_lower):
            max_relevance = max(max_relevance, 0.85)
        elif keyword_lower.endswith(term_lower):
            max_relevance = max(max_relevance, 0.75)
        else:
            # 문자 유사도
            common = len(set(keyword_lower) & set(term_lower))
            total = len(set(keyword_lower) | set(term_lower))
            if total > 0:
                similarity = common / total
                max_relevance = max(max_relevance, similarity * 0.6)
    
    return max_relevance

@router.post("/search", response_model=List[DreamInterpretationResponse])
async def search_dreams(search_request: DreamKeywordSearch):
    """고성능 꿈풀이 키워드 검색 - Clean Dreams 연동"""
    try:
        if not search_request.keywords:
            raise HTTPException(status_code=400, detail="검색 키워드가 필요합니다")
        
        # 검색 모드별 쿼리 생성
        if search_request.search_mode == "exact":
            # 정확 일치 검색
            keywords_str = "'" + "','".join([kw.replace("'", "''") for kw in search_request.keywords]) + "'"
            query = f"""
            SELECT di.keyword, dc.korean_name as category, di.traditional_meaning, di.modern_meaning, di.psychological_meaning,
                   di.fortune_aspect, di.confidence_score, di.related_keywords, di.lucky_numbers
            FROM dream_interpretations di
            LEFT JOIN dream_categories dc ON di.category_id = dc.id 
            WHERE LOWER(di.keyword) IN ({keywords_str})
               AND di.confidence_score >= {search_request.quality_threshold}
            ORDER BY di.confidence_score DESC
            LIMIT {search_request.limit};
            """
        elif search_request.search_mode == "fuzzy":
            # 퍼지 검색
            keyword_conditions = []
            for kw in search_request.keywords:
                clean_kw = kw.replace("'", "''")
                keyword_conditions.append(f"(LOWER(di.keyword) LIKE LOWER('%{clean_kw}%') OR LOWER(di.traditional_meaning) LIKE LOWER('%{clean_kw}%'))")
            
            query = f"""
            SELECT di.keyword, dc.korean_name as category, di.traditional_meaning, di.modern_meaning, di.psychological_meaning,
                   di.fortune_aspect, di.confidence_score, di.related_keywords, di.lucky_numbers
            FROM dream_interpretations di
            LEFT JOIN dream_categories dc ON di.category_id = dc.id
            WHERE ({' OR '.join(keyword_conditions)})
               AND di.confidence_score >= {search_request.quality_threshold}
            ORDER BY di.confidence_score DESC
            LIMIT {search_request.limit * 2};
            """
        else:  # smart 모드 (기본)
            # 스마트 검색 (다단계)
            smart_conditions = []
            for kw in search_request.keywords:
                clean_kw = kw.replace("'", "''")
                smart_conditions.extend([
                    f"LOWER(di.keyword) = LOWER('{clean_kw}')",
                    f"LOWER(di.keyword) LIKE LOWER('{clean_kw}%')",
                    f"LOWER(di.keyword) LIKE LOWER('%{clean_kw}%')",
                    f"'{clean_kw}' = ANY(ARRAY(SELECT LOWER(unnest(di.related_keywords))))"
                ])
            
            query = f"""
            SELECT di.keyword, dc.korean_name as category, di.traditional_meaning, di.modern_meaning, di.psychological_meaning,
                   di.fortune_aspect, di.confidence_score, di.related_keywords, di.lucky_numbers
            FROM dream_interpretations di
            LEFT JOIN dream_categories dc ON di.category_id = dc.id
            WHERE ({' OR '.join(smart_conditions)})
               AND di.confidence_score >= {search_request.quality_threshold}
            ORDER BY 
                CASE 
                    WHEN LOWER(di.keyword) = LOWER('{search_request.keywords[0].replace("'", "''")}') THEN 1
                    WHEN LOWER(di.keyword) LIKE LOWER('{search_request.keywords[0].replace("'", "''")}%') THEN 2
                    ELSE 3
                END,
                di.confidence_score DESC
            LIMIT {search_request.limit * 2};
            """
        
        results = query_dream_database(query)
        
        # 결과 변환 및 관련성 점수 계산
        interpretations = []
        for row in results:
            relevance = calculate_search_relevance(row['keyword'], search_request.keywords)
            
            interpretations.append(DreamInterpretationResponse(
                keyword=row['keyword'],
                category=row['category'],
                traditional_meaning=row['traditional_meaning'],
                modern_meaning=row['modern_meaning'],
                psychological_meaning=row.get('psychological_meaning'),
                fortune_aspect=row['fortune_aspect'],
                confidence_score=row['confidence_score'],
                related_keywords=row.get('related_keywords', []),
                lucky_numbers=row.get('lucky_numbers', []),
                search_relevance=relevance
            ))
        
        # 관련성과 품질 점수로 정렬
        interpretations.sort(key=lambda x: (x.search_relevance, x.confidence_score), reverse=True)
        
        return interpretations[:search_request.limit]
        
    except Exception as e:
        logger.error(f"Dream search error: {e}")
        raise HTTPException(status_code=500, detail="검색 중 오류가 발생했습니다")

# 새로운 엔드포인트들 추가

@router.get("/search-simple/{keyword}")
async def simple_search(keyword: str, limit: int = 5):
    """간단한 키워드 검색 (사주 사이트용)"""
    try:
        query = f"""
        SELECT di.keyword, dc.korean_name as category, di.traditional_meaning, di.modern_meaning, di.psychological_meaning,
               di.fortune_aspect, di.confidence_score, di.related_keywords, di.lucky_numbers
        FROM dream_interpretations di
        LEFT JOIN dream_categories dc ON di.category_id = dc.id
        WHERE LOWER(di.keyword) LIKE LOWER('%{keyword.replace("'", "''")}%')
           OR LOWER(di.traditional_meaning) LIKE LOWER('%{keyword.replace("'", "''")}%')
        ORDER BY 
            CASE 
                WHEN LOWER(di.keyword) = LOWER('{keyword.replace("'", "''")}') THEN 1
                WHEN LOWER(di.keyword) LIKE LOWER('{keyword.replace("'", "''")}%') THEN 2
                ELSE 3
            END,
            di.confidence_score DESC
        LIMIT {limit};
        """
        
        results = query_dream_database(query)
        return {
            "keyword": keyword,
            "total_results": len(results),
            "interpretations": [
                {
                    "keyword": row['keyword'],
                    "category": row['category'],
                    "traditional_meaning": row['traditional_meaning'],
                    "modern_meaning": row['modern_meaning'],
                    "psychological_meaning": row.get('psychological_meaning'),
                    "fortune_aspect": row['fortune_aspect'],
                    "confidence_score": row['confidence_score'],
                    "related_keywords": row.get('related_keywords', [])[:3],  # 최대 3개
                    "lucky_numbers": row.get('lucky_numbers', [])[:6]  # 최대 6개
                }
                for row in results
            ]
        }
    except Exception as e:
        logger.error(f"Simple search error: {e}")
        raise HTTPException(status_code=500, detail="검색 중 오류가 발생했습니다")

@router.get("/categories")
async def get_categories():
    """카테고리 목록 및 통계"""
    query = """
    SELECT dc.korean_name as category, COUNT(*) as count, AVG(di.confidence_score) as avg_score
    FROM dream_interpretations di
    LEFT JOIN dream_categories dc ON di.category_id = dc.id
    GROUP BY dc.korean_name
    ORDER BY count DESC;
    """
    
    results = query_dream_database(query)
    categories = {}
    total_keywords = 0
    
    for row in results:
        if len(row) >= 3:
            cat_name = list(row.values())[0]
            cat_count = int(list(row.values())[1]) if len(row) > 1 else 0
            cat_avg = float(list(row.values())[2]) if len(row) > 2 else 0.0
            
            categories[cat_name] = {
                "count": cat_count,
                "avg_quality": round(cat_avg, 1)
            }
            total_keywords += cat_count
    
    return {
        "categories": categories,
        "total_categories": len(categories),
        "total_keywords": total_keywords
    }

@router.get("/popular")
async def get_popular_dreams(limit: int = 20):
    """인기/고품질 꿈풀이 키워드"""
    query = f"""
    SELECT di.keyword, dc.korean_name as category, di.confidence_score, di.traditional_meaning
    FROM dream_interpretations di
    LEFT JOIN dream_categories dc ON di.category_id = dc.id
    ORDER BY di.confidence_score DESC, LENGTH(di.keyword) ASC
    LIMIT {limit};
    """
    
    results = query_dream_database(query)
    return {
        "popular_dreams": [
            {
                "keyword": row['keyword'],
                "category": row['category'],
                "quality_score": row['confidence_score'],
                "preview": row['traditional_meaning'][:100] + "..." if len(row['traditional_meaning']) > 100 else row['traditional_meaning']
            }
            for row in results
        ]
    }

@router.get("/random")
async def get_random_dream():
    """랜덤 고품질 꿈풀이"""
    try:
        query = """
        SELECT di.keyword, dc.korean_name as category, di.traditional_meaning, di.modern_meaning, di.psychological_meaning,
               di.fortune_aspect, di.confidence_score, di.related_keywords, di.lucky_numbers
        FROM dream_interpretations di
        LEFT JOIN dream_categories dc ON di.category_id = dc.id
        WHERE di.confidence_score >= 8.0
        ORDER BY RANDOM()
        LIMIT 1;
        """
        
        results = query_dream_database(query)
        if not results:
            raise HTTPException(status_code=404, detail="꿈풀이 데이터를 찾을 수 없습니다")
        
        dream = results[0]
        return {
            "keyword": dream['keyword'],
            "category": dream['category'],
            "traditional_meaning": dream['traditional_meaning'],
            "modern_meaning": dream['modern_meaning'],
            "psychological_meaning": dream.get('psychological_meaning'),
            "fortune_aspect": dream['fortune_aspect'],
            "confidence_score": dream['confidence_score'],
            "related_keywords": dream.get('related_keywords', []),
            "lucky_numbers": dream.get('lucky_numbers', []),
            "message": f"오늘의 꿈풀이는 '{dream['keyword']}'입니다. {dream['fortune_aspect']}의 의미를 가집니다."
        }
        
    except Exception as e:
        logger.error(f"Random dream error: {e}")
        raise HTTPException(status_code=500, detail="랜덤 꿈풀이 중 오류가 발생했습니다")

@router.get("/stats")
async def get_dream_stats():
    """꿈풀이 시스템 통계"""
    try:
        # 전체 통계
        total_query = "SELECT COUNT(*) as total FROM dream_interpretations;"
        total_result = query_dream_database(total_query)
        total_count = int(list(total_result[0].values())[0]) if total_result else 0
        
        # 품질 분포
        quality_query = """
        SELECT 
            CASE 
                WHEN confidence_score >= 9.0 THEN 'A급'
                WHEN confidence_score >= 8.0 THEN 'B급' 
                WHEN confidence_score >= 7.0 THEN 'C급'
                ELSE 'D급'
            END as grade,
            COUNT(*) as count
        FROM dream_interpretations
        GROUP BY grade
        ORDER BY AVG(confidence_score) DESC;
        """
        
        quality_results = query_dream_database(quality_query)
        quality_distribution = {}
        for row in quality_results:
            row_values = list(row.values())
            if len(row_values) >= 2:
                quality_distribution[row_values[0]] = int(row_values[1])
        
        return {
            "total_keywords": total_count,
            "quality_distribution": quality_distribution,
            "system_status": "operational",
            "last_updated": datetime.now().isoformat(),
            "expansion_target": "15,000개 목표 (AI 확장 진행중)"
        }
        
    except Exception as e:
        logger.error(f"Stats error: {e}")
        raise HTTPException(status_code=500, detail="통계 조회 중 오류가 발생했습니다")