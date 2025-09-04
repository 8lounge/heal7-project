#!/usr/bin/env python3
"""
🔍 꿈풀이 검색 API 및 필터링 시스템 최적화
- 고성능 검색 알고리즘
- 카테고리별 필터링
- 다중 해석 반환 시스템
- 실시간 성능 모니터링
- 캐싱 최적화
"""

import json
import time
import logging
import subprocess
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime
import re
import hashlib

@dataclass
class SearchQuery:
    """검색 쿼리"""
    keyword: str
    category: Optional[str] = None
    interpretation_types: List[str] = None  # ['traditional', 'modern', 'psychological']
    sentiment_filter: Optional[str] = None  # 'positive', 'negative', 'neutral'
    quality_threshold: float = 7.0
    limit: int = 10
    offset: int = 0

@dataclass
class SearchResult:
    """검색 결과"""
    keyword_id: int
    keyword: str
    category: str
    quality_score: float
    interpretations: List[Dict]  # [{'type': 'traditional', 'text': '...', 'sentiment': '...'}]
    related_keywords: List[str]
    search_count: int
    match_score: float  # 검색어와의 일치도

@dataclass
class SearchResponse:
    """검색 응답"""
    query: str
    total_results: int
    results: List[SearchResult]
    response_time_ms: int
    suggestions: List[str]
    categories: List[Dict]  # [{'category': 'water', 'count': 5}]

class DreamSearchAPIOptimizer:
    """꿈풀이 검색 API 최적화 클래스"""
    
    def __init__(self):
        self.logger = self._setup_logger()
        self.cache = {}  # 간단한 메모리 캐시
        self.cache_ttl = 3600  # 1시간 캐시
        
    def _setup_logger(self):
        """로거 설정"""
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)
        
        if not logger.handlers:
            handler = logging.FileHandler('/home/ubuntu/logs/dream_search_api.log')
            formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            
            console = logging.StreamHandler()
            console.setFormatter(formatter)
            logger.addHandler(console)
        
        return logger
    
    def search_dreams(self, query: SearchQuery) -> SearchResponse:
        """꿈풀이 검색 메인 함수"""
        start_time = time.time()
        
        # 캐시 확인
        cache_key = self._generate_cache_key(query)
        cached_result = self._get_from_cache(cache_key)
        if cached_result:
            self.logger.info(f"캐시에서 검색 결과 반환: {query.keyword}")
            return cached_result
        
        # 검색 실행
        results = self._execute_search(query)
        
        # 응답 시간 계산
        response_time = int((time.time() - start_time) * 1000)
        
        # 검색 제안 생성
        suggestions = self._generate_suggestions(query.keyword)
        
        # 카테고리별 결과 집계
        categories = self._aggregate_categories(results)
        
        # 검색 로그 기록
        self._log_search(query.keyword, len(results), response_time)
        
        # 응답 생성
        response = SearchResponse(
            query=query.keyword,
            total_results=len(results),
            results=results,
            response_time_ms=response_time,
            suggestions=suggestions,
            categories=categories
        )
        
        # 캐시에 저장
        self._save_to_cache(cache_key, response)
        
        return response
    
    def _execute_search(self, query: SearchQuery) -> List[SearchResult]:
        """검색 실행"""
        # SQL 쿼리 구성
        base_query = """
            SELECT DISTINCT k.id, k.keyword, k.category_id, k.quality_score,
                   k.frequency_score, s.search_count
            FROM dream_keywords k
            LEFT JOIN dream_keyword_stats s ON k.id = s.keyword_id
            WHERE k.status = 'active'
        """
        
        conditions = []
        params = []
        
        # 키워드 검색 조건
        search_term = query.keyword.strip().lower()
        if search_term:
            # 정확한 일치 우선, 부분 일치 보조
            conditions.append("""
                (k.keyword_normalized LIKE %s 
                 OR k.keyword LIKE %s 
                 OR EXISTS (
                     SELECT 1 FROM unnest(k.variations) AS var 
                     WHERE lower(var) LIKE %s
                 ))
            """)
            like_pattern = f"%{search_term}%"
            params.extend([like_pattern, like_pattern, like_pattern])
        
        # 카테고리 필터
        if query.category:
            conditions.append("k.category_id = %s")
            params.append(query.category)
        
        # 품질 임계값
        if query.quality_threshold:
            conditions.append("k.quality_score >= %s")
            params.append(query.quality_threshold)
        
        # 조건 추가
        if conditions:
            base_query += " AND " + " AND ".join(conditions)
        
        # 정렬 및 제한
        base_query += """
            ORDER BY 
                CASE 
                    WHEN k.keyword_normalized = %s THEN 1  -- 정확한 일치 우선
                    WHEN k.keyword_normalized LIKE %s THEN 2  -- 시작 일치
                    ELSE 3 
                END,
                k.quality_score DESC,
                COALESCE(s.search_count, 0) DESC
            LIMIT %s OFFSET %s
        """
        params.extend([search_term, f"{search_term}%", query.limit, query.offset])
        
        # PostgreSQL 쿼리 실행
        results = self._execute_pg_query(base_query, params)
        
        # 결과 처리
        search_results = []
        for row in results:
            keyword_id, keyword, category, quality_score, frequency_score, search_count = row
            
            # 해석 데이터 조회
            interpretations = self._get_keyword_interpretations(keyword_id, query.interpretation_types)
            
            # 관련 키워드 조회  
            related_keywords = self._get_related_keywords(keyword_id)
            
            # 매치 스코어 계산
            match_score = self._calculate_match_score(query.keyword, keyword)
            
            # 감정 필터 적용
            if query.sentiment_filter:
                interpretations = [i for i in interpretations if i['sentiment'] == query.sentiment_filter]
                if not interpretations:  # 해당 감정의 해석이 없으면 스킵
                    continue
            
            search_result = SearchResult(
                keyword_id=keyword_id,
                keyword=keyword,
                category=category,
                quality_score=float(quality_score) if quality_score else 8.0,
                interpretations=interpretations,
                related_keywords=related_keywords,
                search_count=search_count or 0,
                match_score=match_score
            )
            
            search_results.append(search_result)
        
        return search_results
    
    def _execute_pg_query(self, query: str, params: List) -> List[Tuple]:
        """PostgreSQL 쿼리 실행"""
        try:
            # 파라미터를 SQL 문자열에 안전하게 삽입
            # 실제 환경에서는 psycopg2나 다른 안전한 방법 사용 권장
            safe_params = []
            for param in params:
                if isinstance(param, str):
                    safe_params.append(f"'{param.replace('\'', '\'\'')}'")
                else:
                    safe_params.append(str(param))
            
            # %s를 실제 값으로 치환
            formatted_query = query
            for param in safe_params:
                formatted_query = formatted_query.replace('%s', param, 1)
            
            # PostgreSQL 실행
            cmd = [
                'sudo', '-u', 'postgres', 'psql', '-d', 'dream_service', 
                '-t', '-A', '-F', '|', '-c', formatted_query
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode != 0:
                self.logger.error(f"PostgreSQL 쿼리 실행 오류: {result.stderr}")
                return []
            
            # 결과 파싱
            rows = []
            for line in result.stdout.strip().split('\n'):
                if line.strip():
                    # None 값 처리
                    values = []
                    for value in line.split('|'):
                        if value.strip() == '':
                            values.append(None)
                        else:
                            # 숫자 변환 시도
                            try:
                                if '.' in value:
                                    values.append(float(value))
                                else:
                                    values.append(int(value))
                            except ValueError:
                                values.append(value)
                    rows.append(tuple(values))
            
            return rows
            
        except Exception as e:
            self.logger.error(f"쿼리 실행 오류: {e}")
            return []
    
    def _get_keyword_interpretations(self, keyword_id: int, 
                                   types_filter: Optional[List[str]] = None) -> List[Dict]:
        """키워드 해석 조회"""
        query = """
            SELECT interpretation_type, interpretation_text, sentiment, confidence_score
            FROM dream_interpretations
            WHERE keyword_id = %s
        """
        
        if types_filter:
            placeholders = ','.join([f"'{t}'" for t in types_filter])
            query += f" AND interpretation_type IN ({placeholders})"
        
        query += " ORDER BY interpretation_type"
        
        results = self._execute_pg_query(query, [keyword_id])
        
        interpretations = []
        for row in results:
            if row:  # 빈 행 제외
                interp_type, text, sentiment, confidence = row
                interpretations.append({
                    'type': interp_type,
                    'text': text,
                    'sentiment': sentiment,
                    'confidence': float(confidence) if confidence else 8.0
                })
        
        return interpretations
    
    def _get_related_keywords(self, keyword_id: int) -> List[str]:
        """관련 키워드 조회"""
        query = """
            SELECT k.keyword
            FROM dream_keyword_relations r
            JOIN dream_keywords k ON r.target_keyword_id = k.id
            WHERE r.source_keyword_id = %s
            ORDER BY r.strength DESC
            LIMIT 5
        """
        
        results = self._execute_pg_query(query, [keyword_id])
        return [row[0] for row in results if row]
    
    def _calculate_match_score(self, query_keyword: str, result_keyword: str) -> float:
        """검색어와 결과 키워드 간의 일치도 계산"""
        query_lower = query_keyword.lower().strip()
        result_lower = result_keyword.lower().strip()
        
        # 정확한 일치
        if query_lower == result_lower:
            return 1.0
        
        # 시작 일치
        if result_lower.startswith(query_lower):
            return 0.9
        
        # 부분 일치
        if query_lower in result_lower:
            return 0.7
        
        # 글자 수 차이 기반 유사도
        if len(query_lower) > 0:
            common_chars = sum(1 for a, b in zip(query_lower, result_lower) if a == b)
            max_len = max(len(query_lower), len(result_lower))
            return common_chars / max_len * 0.5
        
        return 0.0
    
    def _generate_suggestions(self, keyword: str) -> List[str]:
        """검색 제안 생성"""
        if not keyword or len(keyword) < 2:
            return []
        
        # 유사한 키워드 검색
        query = """
            SELECT keyword
            FROM dream_keywords
            WHERE keyword_normalized LIKE %s
            AND keyword != %s
            ORDER BY quality_score DESC
            LIMIT 5
        """
        
        like_pattern = f"%{keyword.lower()}%"
        results = self._execute_pg_query(query, [like_pattern, keyword])
        
        return [row[0] for row in results if row]
    
    def _aggregate_categories(self, results: List[SearchResult]) -> List[Dict]:
        """카테고리별 결과 집계"""
        category_counts = {}
        
        for result in results:
            category = result.category
            if category in category_counts:
                category_counts[category] += 1
            else:
                category_counts[category] = 1
        
        # 카테고리명 한국어 변환 (간단한 매핑)
        category_names = {
            'water': '물 관련', 'fire': '불 관련', 'zodiac_animals': '십이지신',
            'family': '가족', 'money': '돈/재물', 'animals': '동물',
            'body_parts': '신체', 'emotions': '감정'
        }
        
        categories = []
        for category, count in sorted(category_counts.items(), key=lambda x: x[1], reverse=True):
            categories.append({
                'category': category,
                'name': category_names.get(category, category),
                'count': count
            })
        
        return categories
    
    def _log_search(self, search_term: str, result_count: int, response_time: int):
        """검색 로그 기록"""
        try:
            log_query = """
                INSERT INTO dream_search_logs 
                (search_term, result_count, response_time_ms, created_at)
                VALUES (%s, %s, %s, NOW())
            """
            
            self._execute_pg_query(log_query, [search_term, result_count, response_time])
            
        except Exception as e:
            self.logger.error(f"검색 로그 기록 오류: {e}")
    
    def _generate_cache_key(self, query: SearchQuery) -> str:
        """캐시 키 생성"""
        query_dict = asdict(query)
        query_str = json.dumps(query_dict, sort_keys=True)
        return hashlib.md5(query_str.encode()).hexdigest()
    
    def _get_from_cache(self, cache_key: str) -> Optional[SearchResponse]:
        """캐시에서 조회"""
        if cache_key in self.cache:
            cached_data, timestamp = self.cache[cache_key]
            if time.time() - timestamp < self.cache_ttl:
                return cached_data
            else:
                del self.cache[cache_key]  # 만료된 캐시 삭제
        return None
    
    def _save_to_cache(self, cache_key: str, response: SearchResponse):
        """캐시에 저장"""
        self.cache[cache_key] = (response, time.time())
        
        # 캐시 크기 제한 (100개 항목)
        if len(self.cache) > 100:
            oldest_key = min(self.cache.keys(), key=lambda k: self.cache[k][1])
            del self.cache[oldest_key]
    
    def get_popular_keywords(self, limit: int = 10) -> List[Dict]:
        """인기 키워드 조회"""
        query = """
            SELECT k.keyword, k.category_id, s.search_count
            FROM dream_keywords k
            JOIN dream_keyword_stats s ON k.id = s.keyword_id
            WHERE s.search_count > 0
            ORDER BY s.search_count DESC, k.quality_score DESC
            LIMIT %s
        """
        
        results = self._execute_pg_query(query, [limit])
        
        popular = []
        for row in results:
            if row:
                keyword, category, search_count = row
                popular.append({
                    'keyword': keyword,
                    'category': category,
                    'search_count': search_count
                })
        
        return popular
    
    def get_category_stats(self) -> List[Dict]:
        """카테고리별 통계"""
        query = """
            SELECT k.category_id, COUNT(*) as keyword_count,
                   AVG(k.quality_score) as avg_quality,
                   SUM(COALESCE(s.search_count, 0)) as total_searches
            FROM dream_keywords k
            LEFT JOIN dream_keyword_stats s ON k.id = s.keyword_id
            WHERE k.status = 'active'
            GROUP BY k.category_id
            ORDER BY keyword_count DESC
        """
        
        results = self._execute_pg_query(query, [])
        
        stats = []
        for row in results:
            if row:
                category, count, avg_quality, total_searches = row
                stats.append({
                    'category': category,
                    'keyword_count': count,
                    'avg_quality': float(avg_quality) if avg_quality else 8.0,
                    'total_searches': total_searches or 0
                })
        
        return stats
    
    def optimize_search_performance(self):
        """검색 성능 최적화 작업"""
        self.logger.info("검색 성능 최적화 시작")
        
        # 1. 검색 통계 업데이트
        update_stats_query = """
            INSERT INTO dream_keyword_stats (keyword_id, search_count, last_searched)
            SELECT keyword_id, COUNT(*), MAX(created_at)
            FROM dream_search_logs
            WHERE keyword_id IS NOT NULL
            GROUP BY keyword_id
            ON CONFLICT (keyword_id) 
            DO UPDATE SET 
                search_count = dream_keyword_stats.search_count + EXCLUDED.search_count,
                last_searched = EXCLUDED.last_searched
        """
        self._execute_pg_query(update_stats_query, [])
        
        # 2. 오래된 검색 로그 정리 (30일 이상)
        cleanup_query = """
            DELETE FROM dream_search_logs 
            WHERE created_at < NOW() - INTERVAL '30 days'
        """
        self._execute_pg_query(cleanup_query, [])
        
        # 3. 캐시 초기화
        self.cache.clear()
        
        self.logger.info("검색 성능 최적화 완료")

# 테스트 실행
if __name__ == "__main__":
    optimizer = DreamSearchAPIOptimizer()
    
    print("🔍 꿈풀이 검색 API 최적화 테스트")
    print("=" * 50)
    
    # 테스트 쿼리들
    test_queries = [
        SearchQuery(keyword="물", limit=5),
        SearchQuery(keyword="호랑이", category="zodiac_animals"),
        SearchQuery(keyword="아버지", interpretation_types=["traditional", "modern"]),
        SearchQuery(keyword="돈", sentiment_filter="positive", limit=3)
    ]
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n🔸 테스트 {i}: '{query.keyword}'")
        
        response = optimizer.search_dreams(query)
        
        print(f"   검색 결과: {response.total_results}개")
        print(f"   응답 시간: {response.response_time_ms}ms")
        
        for j, result in enumerate(response.results[:2]):  # 처음 2개만 표시
            print(f"   {j+1}. {result.keyword} (카테고리: {result.category}, 품질: {result.quality_score:.1f})")
            for interp in result.interpretations[:1]:  # 첫 번째 해석만
                print(f"      └ {interp['type']}: {interp['text'][:50]}...")
        
        if response.suggestions:
            print(f"   제안: {', '.join(response.suggestions[:3])}")
    
    # 인기 키워드 조회
    print(f"\n📊 인기 키워드:")
    popular = optimizer.get_popular_keywords(5)
    for keyword_data in popular:
        print(f"   🔥 {keyword_data['keyword']} ({keyword_data['search_count']}회)")
    
    # 카테고리 통계
    print(f"\n📈 카테고리 통계:")
    category_stats = optimizer.get_category_stats()
    for stat in category_stats[:5]:
        print(f"   📂 {stat['category']}: {stat['keyword_count']}개 키워드, 품질 {stat['avg_quality']:.1f}")
    
    # 성능 최적화 실행
    print(f"\n⚡ 성능 최적화 실행 중...")
    optimizer.optimize_search_performance()
    print("✅ 최적화 완료")