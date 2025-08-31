"""
HEAL7 꿈풀이/해몽 API 엔드포인트 - 통합 DB 연동 버전
dream_service 스키마와 완전히 연동된 실용적인 꿈풀이 API

@author HEAL7 Team  
@version 3.0.0
"""

from fastapi import APIRouter, HTTPException
from typing import List, Optional
from pydantic import BaseModel
import subprocess
import json
import logging

logger = logging.getLogger(__name__)

# 메인 라우터
router = APIRouter(prefix="/api/dreams", tags=["dream-interpretation"])

# 요청/응답 모델
class DreamKeywordSearch(BaseModel):
    keywords: List[str]
    search_mode: str = "any"  # "any" 또는 "like"
    limit: int = 10

class DreamInterpretationResponse(BaseModel):
    keyword: str
    traditional_meaning: str
    modern_meaning: Optional[str] = None

def query_dream_database(query: str) -> List[dict]:
    """Subprocess를 사용한 안전한 DB 쿼리"""
    try:
        cmd = [
            'sudo', '-u', 'postgres', 'psql', 'heal7',
            '-c', query,
            '-t', '-A', '--field-separator=|'
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            lines = result.stdout.strip().split('\n')
            records = []
            for line in lines:
                if line and '|' in line:
                    parts = line.split('|')
                    if len(parts) >= 2:
                        records.append({
                            'keyword': parts[0],
                            'traditional_meaning': parts[1],
                            'modern_meaning': parts[2] if len(parts) > 2 else ''
                        })
            return records
        else:
            logger.error(f"Database query failed: {result.stderr}")
            return []
    except Exception as e:
        logger.error(f"Database query error: {e}")
        return []

@router.post("/search", response_model=List[DreamInterpretationResponse])
async def search_dreams(search_request: DreamKeywordSearch):
    """꿈풀이 키워드 검색"""
    try:
        if search_request.search_mode == "any":
            # 정확한 키워드 매칭
            keywords_str = "'" + "','".join(search_request.keywords) + "'"
            query = f"""
            SELECT keyword, traditional_meaning, COALESCE(modern_meaning, '') as modern_meaning
            FROM dream_service.dream_interpretations 
            WHERE keyword IN ({keywords_str})
            LIMIT {search_request.limit};
            """
        else:
            # 유사한 키워드 검색
            keyword_conditions = ' OR '.join([f"keyword ILIKE '%{kw}%'" for kw in search_request.keywords])
            query = f"""
            SELECT keyword, traditional_meaning, COALESCE(modern_meaning, '') as modern_meaning
            FROM dream_service.dream_interpretations 
            WHERE {keyword_conditions}
            LIMIT {search_request.limit};
            """
        
        results = query_dream_database(query)
        return [
            DreamInterpretationResponse(
                keyword=row['keyword'],
                traditional_meaning=row['traditional_meaning'],
                modern_meaning=row.get('modern_meaning', '')
            ) for row in results
        ]
        
    except Exception as e:
        logger.error(f"Dream search error: {e}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@router.get("/random")
async def get_random_dream():
    """랜덤 꿈풀이"""
    try:
        query = """
        SELECT keyword, traditional_meaning, COALESCE(modern_meaning, '') as modern_meaning 
        FROM dream_service.dream_interpretations 
        ORDER BY RANDOM() 
        LIMIT 1;
        """
        results = query_dream_database(query)
        if results:
            result = results[0]
            return DreamInterpretationResponse(
                keyword=result['keyword'],
                traditional_meaning=result['traditional_meaning'],
                modern_meaning=result.get('modern_meaning', '')
            )
        else:
            raise HTTPException(status_code=404, detail="No dreams found")
    except Exception as e:
        logger.error(f"Random dream error: {e}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@router.get("/stats")
async def get_dream_stats():
    """꿈풀이 데이터 통계"""
    try:
        query = """
        SELECT 
            COUNT(*) as total_dreams,
            COUNT(DISTINCT keyword) as unique_keywords
        FROM dream_service.dream_interpretations;
        """
        # subprocess로 숫자 쿼리는 다르게 처리
        cmd = ['sudo', '-u', 'postgres', 'psql', 'heal7', '-c', query, '-t', '-A']
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            lines = result.stdout.strip().split('\n')
            if lines and '|' in lines[0]:
                parts = lines[0].split('|')
                return {
                    "total_dreams": int(parts[0]),
                    "unique_keywords": int(parts[1]),
                    "status": "healthy"
                }
        
        return {"total_dreams": 0, "unique_keywords": 0, "status": "error"}
    except Exception as e:
        logger.error(f"Dream stats error: {e}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@router.get("/keyword/{keyword}")
async def get_dream_by_keyword(keyword: str):
    """특정 키워드로 꿈풀이 조회"""
    try:
        query = f"""
        SELECT keyword, traditional_meaning, COALESCE(modern_meaning, '') as modern_meaning 
        FROM dream_service.dream_interpretations 
        WHERE keyword = '{keyword}'
        LIMIT 1;
        """
        results = query_dream_database(query)
        if results:
            result = results[0]
            return DreamInterpretationResponse(
                keyword=result['keyword'],
                traditional_meaning=result['traditional_meaning'],
                modern_meaning=result.get('modern_meaning', '')
            )
        else:
            raise HTTPException(status_code=404, detail=f"Dream interpretation for '{keyword}' not found")
    except Exception as e:
        logger.error(f"Dream keyword search error: {e}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")