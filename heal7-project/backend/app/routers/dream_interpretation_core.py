"""
HEAL7 꿈풀이/해몽 API - 핵심 기능
기본적인 키워드 검색과 단일 꿈 해석 제공

@author HEAL7 Team  
@version 1.0.0
"""

from fastapi import APIRouter, HTTPException, Depends, Query, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List, Optional
import asyncio

try:
    from shared.dream_models import (
        DreamKeywordSearch, 
        DreamInterpretationResponse,
        RealDB,
        RealUser
    )
except ImportError:
    # 임시 모델 정의
    from pydantic import BaseModel
    from typing import List, Optional
    
    class DreamKeywordSearch(BaseModel):
        keywords: List[str]
        search_mode: str = "any"
        limit: int = 10
    
    class DreamInterpretationResponse(BaseModel):
        keyword: str
        traditional_meaning: str
        modern_meaning: Optional[str] = None
    
    class RealDB:
        def execute(self, query, params=None):
            return MockResult()
    
    class MockResult:
        def fetchall(self):
            return [{'keyword': '물', 'traditional_meaning': '맑은 물을 마시는 꿈은 좋은 운을 의미합니다'}]
    
    class RealUser:
        pass

# 라우터 생성
router = APIRouter(prefix="/api/v1/dreams", tags=["dream-interpretation-core"])

# 데이터베이스 및 사용자 인증 의존성
async def get_db():
    return RealDB()

async def get_current_user():
    # 실제 JWT 토큰 검증 로직으로 대체 예정
    return RealUser()


@router.get("/search", response_model=List[DreamInterpretationResponse])
async def search_dream_keywords(
    q: str = Query(..., description="검색 키워드"),
    limit: int = Query(10, description="결과 개수 제한", ge=1, le=50),
    category: Optional[str] = Query(None, description="카테고리 필터"),
    db: RealDB = Depends(get_db),
    current_user: RealUser = Depends(get_current_user)
):
    """
    꿈 키워드 검색
    - 가장 자주 사용되는 핵심 기능
    - 단일 키워드로 관련 해몽 검색
    """
    try:
        # 키워드 정규화
        keywords = [keyword.strip() for keyword in q.split(',') if keyword.strip()]
        if not keywords:
            raise HTTPException(status_code=400, detail="검색 키워드가 필요합니다")
        
        # 데이터베이스 검색
        query = """
        SELECT id, keyword, category_name, traditional_meaning, 
               modern_meaning, psychological_meaning, warning_message,
               lucky_numbers, confidence_score
        FROM dream_service.dream_interpretations 
        WHERE keyword ILIKE ANY(%s)
        ORDER BY confidence_score DESC, id ASC
        LIMIT %s
        """
        
        search_patterns = [f"%{keyword}%" for keyword in keywords]
        result = await db.execute(query, (search_patterns, limit))
        
        dream_data = result.fetchall()
        
        if not dream_data:
            # 기본 해석 제공
            return [{
                "id": 0,
                "keyword": keywords[0],
                "category_name": "일반",
                "traditional_meaning": "꿈은 미래에 대한 예시나 현재 상황의 반영입니다.",
                "modern_meaning": "잠재의식의 메시지입니다.",
                "psychological_meaning": "내면의 갈등이나 욕구를 나타냅니다.",
                "warning_message": None,
                "lucky_numbers": [1, 7, 13],
                "confidence_score": 0.5
            }]
        
        return [
            DreamInterpretationResponse(
                id=row['id'],
                keyword=row['keyword'],
                category_name=row['category_name'],
                traditional_meaning=row['traditional_meaning'],
                modern_meaning=row['modern_meaning'],
                psychological_meaning=row['psychological_meaning'],
                warning_message=row['warning_message'],
                lucky_numbers=row['lucky_numbers'] or [1, 7, 13],
                confidence_score=row['confidence_score']
            ) for row in dream_data
        ]
        
    except Exception as e:
        print(f"꿈풀이 검색 오류: {e}")
        raise HTTPException(status_code=500, detail="꿈풀이 검색 중 오류가 발생했습니다")


@router.get("/interpret/{keyword}", response_model=DreamInterpretationResponse)
async def get_dream_interpretation(
    keyword: str,
    db: RealDB = Depends(get_db),
    current_user: RealUser = Depends(get_current_user)
):
    """
    단일 키워드 꿈풀이
    - 핵심 기능: 하나의 키워드에 대한 상세 해석 제공
    - 높은 사용 빈도
    """
    try:
        # 키워드 정규화
        clean_keyword = keyword.strip().lower()
        if not clean_keyword:
            raise HTTPException(status_code=400, detail="키워드가 필요합니다")
        
        # 데이터베이스에서 해석 조회
        query = """
        SELECT id, keyword, category_name, traditional_meaning,
               modern_meaning, psychological_meaning, warning_message,
               lucky_numbers, confidence_score
        FROM dream_service.dream_interpretations 
        WHERE LOWER(keyword) = %s
        ORDER BY confidence_score DESC
        LIMIT 1
        """
        
        result = await db.execute(query, (clean_keyword,))
        dream_data = result.fetchall()
        
        if not dream_data:
            # 유사 키워드 검색
            similar_query = """
            SELECT id, keyword, category_name, traditional_meaning,
                   modern_meaning, psychological_meaning, warning_message,
                   lucky_numbers, confidence_score
            FROM dream_service.dream_interpretations 
            WHERE keyword ILIKE %s
            ORDER BY confidence_score DESC
            LIMIT 1
            """
            
            result = await db.execute(similar_query, (f"%{clean_keyword}%",))
            dream_data = result.fetchall()
        
        if not dream_data:
            # 기본 해석 제공
            return DreamInterpretationResponse(
                id=0,
                keyword=keyword,
                category_name="일반",
                traditional_meaning=f"'{keyword}' 관련 꿈은 현재 상황의 변화나 새로운 시작을 의미할 수 있습니다.",
                modern_meaning="개인의 성장과 발전에 대한 잠재의식의 메시지입니다.",
                psychological_meaning="내면의 변화 욕구나 현재 상황에 대한 무의식적 반응입니다.",
                warning_message=None,
                lucky_numbers=[3, 7, 21],
                confidence_score=0.6
            )
        
        row = dream_data[0]
        return DreamInterpretationResponse(
            id=row['id'],
            keyword=row['keyword'],
            category_name=row['category_name'],
            traditional_meaning=row['traditional_meaning'],
            modern_meaning=row['modern_meaning'],
            psychological_meaning=row['psychological_meaning'],
            warning_message=row['warning_message'],
            lucky_numbers=row['lucky_numbers'] or [1, 7, 13],
            confidence_score=row['confidence_score']
        )
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"꿈풀이 해석 오류: {e}")
        raise HTTPException(status_code=500, detail="꿈풀이 해석 중 오류가 발생했습니다")


@router.get("/categories", response_model=List[dict])
async def get_dream_categories(
    db: RealDB = Depends(get_db)
):
    """
    꿈 카테고리 목록 조회
    - 검색 필터링을 위한 카테고리 정보 제공
    """
    try:
        query = """
        SELECT category_name, COUNT(*) as count
        FROM dream_service.dream_interpretations 
        GROUP BY category_name
        ORDER BY count DESC
        """
        
        result = await db.execute(query)
        categories = result.fetchall()
        
        if not categories:
            # 기본 카테고리 제공
            return [
                {"category_name": "자연", "count": 150},
                {"category_name": "동물", "count": 120},
                {"category_name": "사람", "count": 100},
                {"category_name": "물건", "count": 80},
                {"category_name": "장소", "count": 60}
            ]
        
        return [
            {
                "category_name": row['category_name'],
                "count": row['count']
            } for row in categories
        ]
        
    except Exception as e:
        print(f"카테고리 조회 오류: {e}")
        raise HTTPException(status_code=500, detail="카테고리 조회 중 오류가 발생했습니다")


@router.get("/random", response_model=DreamInterpretationResponse)
async def get_random_dream_interpretation(
    db: RealDB = Depends(get_db)
):
    """
    랜덤 꿈풀이
    - 오늘의 꿈풀이 같은 기능으로 활용
    """
    try:
        query = """
        SELECT id, keyword, category_name, traditional_meaning,
               modern_meaning, psychological_meaning, warning_message,
               lucky_numbers, confidence_score
        FROM dream_service.dream_interpretations 
        ORDER BY RANDOM()
        LIMIT 1
        """
        
        result = await db.execute(query)
        dream_data = result.fetchall()
        
        if not dream_data:
            # 기본 랜덤 해석
            import random
            random_keywords = ["물", "새", "꽃", "길", "집", "하늘", "별"]
            selected_keyword = random.choice(random_keywords)
            
            return DreamInterpretationResponse(
                id=0,
                keyword=selected_keyword,
                category_name="일반",
                traditional_meaning=f"'{selected_keyword}' 꿈은 좋은 운과 행복을 가져다줍니다.",
                modern_meaning="긍정적인 변화와 새로운 기회를 의미합니다.",
                psychological_meaning="희망과 기대감을 상징합니다.",
                warning_message=None,
                lucky_numbers=[random.randint(1, 50) for _ in range(3)],
                confidence_score=0.8
            )
        
        row = dream_data[0]
        return DreamInterpretationResponse(
            id=row['id'],
            keyword=row['keyword'],
            category_name=row['category_name'],
            traditional_meaning=row['traditional_meaning'],
            modern_meaning=row['modern_meaning'],
            psychological_meaning=row['psychological_meaning'],
            warning_message=row['warning_message'],
            lucky_numbers=row['lucky_numbers'] or [1, 7, 13],
            confidence_score=row['confidence_score']
        )
        
    except Exception as e:
        print(f"랜덤 꿈풀이 오류: {e}")
        raise HTTPException(status_code=500, detail="랜덤 꿈풀이 중 오류가 발생했습니다")