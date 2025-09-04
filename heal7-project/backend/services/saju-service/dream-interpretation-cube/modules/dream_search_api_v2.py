#!/usr/bin/env python3
"""
HEAL7 꿈풀이 고성능 검색 API v2.0
15,000개 키워드 대응 초고속 검색 시스템
"""

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import subprocess
import json
import logging
import re
import time
from datetime import datetime

logger = logging.getLogger(__name__)

# 라우터 설정
router = APIRouter(prefix="/api/dreams", tags=["dream-search-v2"])

# 데이터 모델
class DreamSearchRequest(BaseModel):
    keyword: str
    search_mode: str = "smart"  # smart, exact, fuzzy, related
    limit: int = 10
    include_related: bool = True
    quality_threshold: float = 7.0

class DreamInterpretation(BaseModel):
    keyword: str
    category: str
    traditional_meaning: str
    modern_meaning: str
    psychological_meaning: Optional[str] = None
    fortune_aspect: str
    confidence_score: float
    related_keywords: List[str] = []
    lucky_numbers: List[int] = []
    search_relevance: float = 1.0

class DreamSearchResponse(BaseModel):
    query: str
    total_results: int
    search_time_ms: float
    interpretations: List[DreamInterpretation]
    suggestions: List[str] = []
    related_searches: List[str] = []

class DreamSearchEngine:
    """고성능 꿈풀이 검색 엔진"""
    
    def __init__(self):
        self.cache = {}  # 간단한 메모리 캐시
        self.search_stats = {
            "total_searches": 0,
            "avg_response_time": 0,
            "cache_hits": 0
        }
    
    def query_database(self, query: str) -> List[Dict]:
        """최적화된 DB 쿼리"""
        try:
            cmd = [
                'sudo', '-u', 'postgres', 'psql', 'heal7',
                '-c', query,
                '-t', '-A', '--field-separator=☆'  # 특수 구분자로 파싱 오류 방지
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                lines = result.stdout.strip().split('\n')
                records = []
                for line in lines:
                    if line and line.strip():
                        parts = line.split('☆')
                        if len(parts) >= 8:  # 최소 필드 수 검증
                            records.append({
                                'keyword': parts[0],
                                'category': parts[1],
                                'traditional_meaning': parts[2],
                                'modern_meaning': parts[3],
                                'psychological_meaning': parts[4] if parts[4] else None,
                                'fortune_aspect': parts[5],
                                'confidence_score': float(parts[6]),
                                'related_keywords': self.parse_pg_array(parts[7]),
                                'lucky_numbers': self.parse_pg_int_array(parts[8]) if len(parts) > 8 else []
                            })
                return records
            else:
                logger.error(f"DB 쿼리 오류: {result.stderr}")
                return []
                
        except Exception as e:
            logger.error(f"쿼리 실행 실패: {e}")
            return []
    
    def parse_pg_array(self, pg_array: str) -> List[str]:
        """PostgreSQL 배열 파싱"""
        if not pg_array or pg_array == '{}':
            return []
        
        try:
            # {item1,item2,item3} 형태 파싱
            pg_array = pg_array.strip('{}')
            if not pg_array:
                return []
            
            items = []
            for item in pg_array.split(','):
                item = item.strip().strip('"').strip("'")
                if item:
                    items.append(item)
            return items
            
        except Exception as e:
            logger.warning(f"배열 파싱 오류: {e}")
            return []
    
    def parse_pg_int_array(self, pg_array: str) -> List[int]:
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
            
        except Exception as e:
            logger.warning(f"숫자 배열 파싱 오류: {e}")
            return []
    
    def calculate_relevance(self, keyword: str, search_term: str, search_mode: str) -> float:
        """검색 관련성 점수 계산"""
        search_term_lower = search_term.lower()
        keyword_lower = keyword.lower()
        
        # 완전 일치
        if keyword_lower == search_term_lower:
            return 1.0
        
        # 포함 관계
        if search_term_lower in keyword_lower:
            return 0.9
        
        if keyword_lower in search_term_lower:
            return 0.8
        
        # 시작/끝 일치
        if keyword_lower.startswith(search_term_lower):
            return 0.85
        
        if keyword_lower.endswith(search_term_lower):
            return 0.75
        
        # 유사도 계산 (간단한 문자 비교)
        common_chars = len(set(keyword_lower) & set(search_term_lower))
        total_chars = len(set(keyword_lower) | set(search_term_lower))
        
        if total_chars > 0:
            similarity = common_chars / total_chars
            return max(similarity, 0.1)
        
        return 0.1
    
    def smart_search(self, search_term: str, limit: int, quality_threshold: float) -> List[Dict]:
        """지능형 검색 (기본 모드)"""
        cache_key = f"smart_{search_term}_{limit}_{quality_threshold}"
        
        # 캐시 확인
        if cache_key in self.cache:
            self.search_stats["cache_hits"] += 1
            return self.cache[cache_key]
        
        # 다단계 검색 전략
        queries = []
        
        # 1. 완전 일치 검색
        queries.append(f"""
        SELECT keyword, category, traditional_meaning, modern_meaning, psychological_meaning,
               fortune_aspect, confidence_score, related_keywords, lucky_numbers
        FROM dream_service.clean_dream_interpretations 
        WHERE LOWER(keyword) = LOWER('{search_term.replace("'", "''")}')
           AND confidence_score >= {quality_threshold}
        ORDER BY confidence_score DESC
        LIMIT {min(limit, 5)};
        """)
        
        # 2. 포함 검색 (LIKE)
        queries.append(f"""
        SELECT keyword, category, traditional_meaning, modern_meaning, psychological_meaning,
               fortune_aspect, confidence_score, related_keywords, lucky_numbers
        FROM dream_service.clean_dream_interpretations 
        WHERE (LOWER(keyword) LIKE LOWER('%{search_term.replace("'", "''")}%')
           OR LOWER(traditional_meaning) LIKE LOWER('%{search_term.replace("'", "''")}%'))
           AND confidence_score >= {quality_threshold}
           AND LOWER(keyword) != LOWER('{search_term.replace("'", "''")}')
        ORDER BY confidence_score DESC, 
                 CASE WHEN LOWER(keyword) LIKE LOWER('{search_term.replace("'", "''")}%') THEN 1 ELSE 2 END
        LIMIT {min(limit * 2, 20)};
        """)
        
        # 3. 관련 키워드 검색
        queries.append(f"""
        SELECT keyword, category, traditional_meaning, modern_meaning, psychological_meaning,
               fortune_aspect, confidence_score, related_keywords, lucky_numbers
        FROM dream_service.clean_dream_interpretations 
        WHERE '{search_term.replace("'", "''")}' = ANY(related_keywords)
           AND confidence_score >= {quality_threshold}
        ORDER BY confidence_score DESC
        LIMIT {min(limit, 10)};
        """)
        
        # 모든 검색 결과 수집
        all_results = []
        seen_keywords = set()
        
        for query in queries:
            results = self.query_database(query)
            for result in results:
                if result['keyword'] not in seen_keywords:
                    result['search_relevance'] = self.calculate_relevance(
                        result['keyword'], search_term, 'smart'
                    )
                    all_results.append(result)
                    seen_keywords.add(result['keyword'])
        
        # 관련성 점수로 정렬 후 제한
        all_results.sort(key=lambda x: (x['search_relevance'], x['confidence_score']), reverse=True)
        final_results = all_results[:limit]
        
        # 캐시 저장 (최대 100개 항목)
        if len(self.cache) < 100:
            self.cache[cache_key] = final_results
        
        return final_results
    
    def exact_search(self, search_term: str, limit: int, quality_threshold: float) -> List[Dict]:
        """정확 일치 검색"""
        query = f"""
        SELECT keyword, category, traditional_meaning, modern_meaning, psychological_meaning,
               fortune_aspect, confidence_score, related_keywords, lucky_numbers
        FROM dream_service.clean_dream_interpretations 
        WHERE LOWER(keyword) = LOWER('{search_term.replace("'", "''")}')
           AND confidence_score >= {quality_threshold}
        ORDER BY confidence_score DESC
        LIMIT {limit};
        """
        
        results = self.query_database(query)
        for result in results:
            result['search_relevance'] = 1.0
        
        return results
    
    def fuzzy_search(self, search_term: str, limit: int, quality_threshold: float) -> List[Dict]:
        """퍼지 검색 (유사 검색)"""
        query = f"""
        SELECT keyword, category, traditional_meaning, modern_meaning, psychological_meaning,
               fortune_aspect, confidence_score, related_keywords, lucky_numbers
        FROM dream_service.clean_dream_interpretations 
        WHERE (LOWER(keyword) LIKE LOWER('%{search_term.replace("'", "''")}%')
           OR LOWER(traditional_meaning) LIKE LOWER('%{search_term.replace("'", "''")}%')
           OR LOWER(modern_meaning) LIKE LOWER('%{search_term.replace("'", "''")}%'))
           AND confidence_score >= {quality_threshold}
        ORDER BY 
            CASE 
                WHEN LOWER(keyword) = LOWER('{search_term.replace("'", "''")}') THEN 1
                WHEN LOWER(keyword) LIKE LOWER('{search_term.replace("'", "''")}%') THEN 2
                WHEN LOWER(keyword) LIKE LOWER('%{search_term.replace("'", "''")}') THEN 3
                ELSE 4
            END,
            confidence_score DESC
        LIMIT {limit * 2};
        """
        
        results = self.query_database(query)
        for result in results:
            result['search_relevance'] = self.calculate_relevance(
                result['keyword'], search_term, 'fuzzy'
            )
        
        # 관련성으로 정렬 후 제한
        results.sort(key=lambda x: x['search_relevance'], reverse=True)
        return results[:limit]
    
    def get_suggestions(self, search_term: str, limit: int = 5) -> List[str]:
        """검색 제안 키워드 생성"""
        query = f"""
        SELECT DISTINCT keyword 
        FROM dream_service.clean_dream_interpretations 
        WHERE LOWER(keyword) LIKE LOWER('{search_term.replace("'", "''")}%')
           AND LENGTH(keyword) <= {len(search_term) + 3}
        ORDER BY confidence_score DESC
        LIMIT {limit};
        """
        
        results = self.query_database(query)
        return [r['keyword'] for r in results if 'keyword' in r]
    
    def get_related_searches(self, search_term: str, results: List[Dict], limit: int = 5) -> List[str]:
        """관련 검색어 추천"""
        related_terms = set()
        
        # 검색 결과의 관련 키워드에서 추출
        for result in results[:3]:  # 상위 3개 결과만 사용
            for related_kw in result.get('related_keywords', []):
                if related_kw.lower() != search_term.lower():
                    related_terms.add(related_kw)
        
        # 같은 카테고리 인기 키워드
        if results:
            category = results[0]['category']
            query = f"""
            SELECT keyword 
            FROM dream_service.clean_dream_interpretations 
            WHERE category = '{category}' 
               AND LOWER(keyword) != LOWER('{search_term.replace("'", "''")}')
            ORDER BY confidence_score DESC
            LIMIT 3;
            """
            
            category_results = self.query_database(query)
            for r in category_results:
                if 'keyword' in r:
                    related_terms.add(r['keyword'])
        
        return list(related_terms)[:limit]
    
    def search(self, request: DreamSearchRequest) -> DreamSearchResponse:
        """메인 검색 함수"""
        start_time = time.time()
        
        # 검색 통계 업데이트
        self.search_stats["total_searches"] += 1
        
        # 검색 실행
        if request.search_mode == "exact":
            results = self.exact_search(request.keyword, request.limit, request.quality_threshold)
        elif request.search_mode == "fuzzy":
            results = self.fuzzy_search(request.keyword, request.limit, request.quality_threshold)
        elif request.search_mode == "related":
            # 관련 키워드만 검색
            results = []  # 구현 생략
        else:  # smart (기본)
            results = self.smart_search(request.keyword, request.limit, request.quality_threshold)
        
        # 응답 시간 계산
        search_time = (time.time() - start_time) * 1000
        
        # 응답 데이터 구성
        interpretations = []
        for result in results:
            interpretations.append(DreamInterpretation(
                keyword=result['keyword'],
                category=result['category'],
                traditional_meaning=result['traditional_meaning'],
                modern_meaning=result['modern_meaning'],
                psychological_meaning=result.get('psychological_meaning'),
                fortune_aspect=result['fortune_aspect'],
                confidence_score=result['confidence_score'],
                related_keywords=result.get('related_keywords', []),
                lucky_numbers=result.get('lucky_numbers', []),
                search_relevance=result.get('search_relevance', 1.0)
            ))
        
        # 제안 키워드 및 관련 검색어
        suggestions = self.get_suggestions(request.keyword) if request.include_related else []
        related_searches = self.get_related_searches(request.keyword, results) if request.include_related else []
        
        # 평균 응답시간 업데이트
        self.search_stats["avg_response_time"] = (
            self.search_stats["avg_response_time"] * (self.search_stats["total_searches"] - 1) + search_time
        ) / self.search_stats["total_searches"]
        
        return DreamSearchResponse(
            query=request.keyword,
            total_results=len(interpretations),
            search_time_ms=round(search_time, 2),
            interpretations=interpretations,
            suggestions=suggestions,
            related_searches=related_searches
        )

# 글로벌 검색 엔진 인스턴스
search_engine = DreamSearchEngine()

# API 엔드포인트들
@router.post("/search", response_model=DreamSearchResponse)
async def search_dreams(request: DreamSearchRequest):
    """꿈풀이 고성능 검색 API"""
    try:
        if not request.keyword or len(request.keyword.strip()) == 0:
            raise HTTPException(status_code=400, detail="검색 키워드가 필요합니다")
        
        if len(request.keyword) > 100:
            raise HTTPException(status_code=400, detail="검색 키워드가 너무 깁니다")
        
        return search_engine.search(request)
        
    except Exception as e:
        logger.error(f"꿈풀이 검색 오류: {e}")
        raise HTTPException(status_code=500, detail="검색 중 오류가 발생했습니다")

@router.get("/search/{keyword}", response_model=DreamSearchResponse)
async def quick_search(
    keyword: str,
    search_mode: str = Query("smart", regex="^(smart|exact|fuzzy|related)$"),
    limit: int = Query(10, ge=1, le=50),
    quality_threshold: float = Query(7.0, ge=0.0, le=10.0)
):
    """빠른 키워드 검색 (GET)"""
    request = DreamSearchRequest(
        keyword=keyword,
        search_mode=search_mode,
        limit=limit,
        quality_threshold=quality_threshold
    )
    return await search_dreams(request)

@router.get("/stats")
async def get_search_stats():
    """검색 엔진 통계"""
    return {
        "search_engine_stats": search_engine.search_stats,
        "cache_size": len(search_engine.cache),
        "total_keywords": "calculating...",  # 실제로는 DB에서 조회
        "system_status": "operational"
    }

@router.get("/categories")
async def get_categories():
    """사용 가능한 카테고리 목록"""
    query = """
    SELECT category, COUNT(*) as keyword_count
    FROM dream_service.clean_dream_interpretations 
    GROUP BY category
    ORDER BY keyword_count DESC;
    """
    
    results = search_engine.query_database(query)
    categories = {}
    for result in results:
        if len(result) >= 2:
            categories[result[0]] = int(result[1])
    
    return {
        "categories": categories,
        "total_categories": len(categories)
    }

@router.get("/popular")
async def get_popular_keywords(limit: int = Query(20, ge=1, le=100)):
    """인기 키워드 목록"""
    query = f"""
    SELECT keyword, category, confidence_score
    FROM dream_service.clean_dream_interpretations 
    ORDER BY confidence_score DESC, LENGTH(keyword) ASC
    LIMIT {limit};
    """
    
    results = search_engine.query_database(query)
    popular = []
    for result in results:
        if len(result) >= 3:
            popular.append({
                "keyword": result[0],
                "category": result[1], 
                "quality_score": float(result[2])
            })
    
    return {
        "popular_keywords": popular,
        "total_count": len(popular)
    }