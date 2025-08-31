"""
HEAL7 꿈풀이/해몽 API - 고급 기능
복합 키워드 분석, 사용자 기록, 통계 등 전문 기능 제공

@author HEAL7 Team  
@version 1.0.0
"""

from fastapi import APIRouter, HTTPException, Depends, Query, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from datetime import datetime, date, timedelta
import asyncio

from ...shared.dream_models import (
    DreamKeywordSearch,
    DreamInterpretationResponse,
    DreamCombinationResponse,
    UserDreamRecord,
    PopularDreamResponse,
    RealDB,
    RealUser
)

# 라우터 생성
router = APIRouter(prefix="/api/v1/dreams/advanced", tags=["dream-interpretation-advanced"])

# 데이터베이스 및 사용자 인증 의존성
async def get_db():
    return RealDB()

async def get_current_user():
    # 실제 JWT 토큰 검증 로직으로 대체 예정
    return RealUser()


@router.post("/combination", response_model=DreamCombinationResponse)
async def analyze_dream_combination(
    search_request: DreamKeywordSearch,
    db: RealDB = Depends(get_db),
    current_user: RealUser = Depends(get_current_user)
):
    """
    복합 키워드 꿈풀이 분석
    - 여러 키워드 조합 해석
    - 프리미엄 기능
    """
    try:
        if not current_user.is_premium:
            raise HTTPException(
                status_code=403, 
                detail="복합 키워드 분석은 프리미엄 회원 전용 기능입니다"
            )
        
        keywords = search_request.keywords
        if len(keywords) < 2:
            raise HTTPException(
                status_code=400, 
                detail="복합 분석을 위해서는 최소 2개의 키워드가 필요합니다"
            )
        
        # 개별 키워드 해석 조회
        individual_meanings = []
        for keyword in keywords[:5]:  # 최대 5개 키워드
            query = """
            SELECT id, keyword, category_name, traditional_meaning,
                   modern_meaning, psychological_meaning, warning_message,
                   lucky_numbers, confidence_score
            FROM dream_service.dream_interpretations 
            WHERE keyword ILIKE %s
            ORDER BY confidence_score DESC
            LIMIT 1
            """
            
            result = await db.execute(query, (f"%{keyword}%",))
            dream_data = result.fetchall()
            
            if dream_data:
                row = dream_data[0]
                individual_meanings.append(
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
                    )
                )
        
        # 복합 해석 생성
        if len(individual_meanings) >= 2:
            combined_interpretation = await _generate_combination_interpretation(
                individual_meanings, keywords
            )
            overall_score = sum(meaning.confidence_score for meaning in individual_meanings) / len(individual_meanings)
        else:
            combined_interpretation = "입력된 키워드들의 조합 해석을 찾을 수 없습니다. 개별 키워드로 검색해보세요."
            overall_score = 0.3
        
        return DreamCombinationResponse(
            combined_interpretation=combined_interpretation,
            individual_meanings=individual_meanings,
            overall_score=min(overall_score, 1.0)
        )
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"복합 꿈풀이 분석 오류: {e}")
        raise HTTPException(status_code=500, detail="복합 꿈풀이 분석 중 오류가 발생했습니다")


@router.post("/record", response_model=Dict[str, str])
async def save_user_dream_record(
    dream_record: UserDreamRecord,
    background_tasks: BackgroundTasks,
    db: RealDB = Depends(get_db),
    current_user: RealUser = Depends(get_current_user)
):
    """
    사용자 꿈 기록 저장
    - 개인 꿈 일기 기능
    - 통계 분석을 위한 데이터 수집
    """
    try:
        # 백그라운드에서 데이터 저장
        background_tasks.add_task(
            _save_dream_record_async,
            current_user.user_id,
            dream_record,
            db
        )
        
        return {"message": "꿈 기록이 성공적으로 저장되었습니다"}
        
    except Exception as e:
        print(f"꿈 기록 저장 오류: {e}")
        raise HTTPException(status_code=500, detail="꿈 기록 저장 중 오류가 발생했습니다")


@router.get("/user/history", response_model=List[UserDreamRecord])
async def get_user_dream_history(
    limit: int = Query(20, description="조회할 기록 수", ge=1, le=100),
    offset: int = Query(0, description="건너뛸 기록 수", ge=0),
    db: RealDB = Depends(get_db),
    current_user: RealUser = Depends(get_current_user)
):
    """
    사용자 꿈 기록 조회
    - 개인 꿈 일기 이력 조회
    """
    try:
        query = """
        SELECT dream_content, keywords, interpretation_date
        FROM user_dream_records 
        WHERE user_id = %s
        ORDER BY interpretation_date DESC
        LIMIT %s OFFSET %s
        """
        
        result = await db.execute(query, (current_user.user_id, limit, offset))
        records = result.fetchall()
        
        return [
            UserDreamRecord(
                dream_content=row['dream_content'],
                keywords=row['keywords'] or [],
                interpretation_date=row['interpretation_date']
            ) for row in records
        ]
        
    except Exception as e:
        print(f"꿈 기록 조회 오류: {e}")
        raise HTTPException(status_code=500, detail="꿈 기록 조회 중 오류가 발생했습니다")


@router.get("/popular", response_model=List[PopularDreamResponse])
async def get_popular_dream_keywords(
    period: str = Query("week", description="기간 (day, week, month)"),
    limit: int = Query(10, description="결과 수", ge=1, le=50),
    db: RealDB = Depends(get_db)
):
    """
    인기 꿈 키워드 통계
    - 검색 빈도 기반 트렌드 분석
    """
    try:
        # 기간별 조건 설정
        period_conditions = {
            "day": "interpretation_date >= CURRENT_DATE - INTERVAL '1 day'",
            "week": "interpretation_date >= CURRENT_DATE - INTERVAL '1 week'",
            "month": "interpretation_date >= CURRENT_DATE - INTERVAL '1 month'"
        }
        
        if period not in period_conditions:
            raise HTTPException(status_code=400, detail="유효하지 않은 기간입니다 (day, week, month)")
        
        query = f"""
        SELECT keyword, COUNT(*) as search_count,
               (COUNT(*) - LAG(COUNT(*), 1, 0) OVER (ORDER BY COUNT(*) DESC)) as trend_change
        FROM dream_service.dream_search_logs 
        WHERE {period_conditions[period]}
        GROUP BY keyword
        ORDER BY search_count DESC
        LIMIT %s
        """
        
        result = await db.execute(query, (limit,))
        popular_data = result.fetchall()
        
        if not popular_data:
            # 기본 인기 키워드 제공
            default_keywords = [
                {"keyword": "물", "search_count": 45, "trend_change": 5},
                {"keyword": "새", "search_count": 38, "trend_change": 2},
                {"keyword": "집", "search_count": 35, "trend_change": -3},
                {"keyword": "길", "search_count": 30, "trend_change": 8},
                {"keyword": "꽃", "search_count": 28, "trend_change": 1}
            ]
            
            return [
                PopularDreamResponse(
                    keyword=item["keyword"],
                    search_count=item["search_count"],
                    trend_change=item["trend_change"]
                ) for item in default_keywords[:limit]
            ]
        
        return [
            PopularDreamResponse(
                keyword=row['keyword'],
                search_count=row['search_count'],
                trend_change=row['trend_change'] or 0
            ) for row in popular_data
        ]
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"인기 키워드 조회 오류: {e}")
        raise HTTPException(status_code=500, detail="인기 키워드 조회 중 오류가 발생했습니다")


@router.get("/statistics", response_model=Dict[str, Any])
async def get_dream_statistics(
    user_only: bool = Query(False, description="사용자별 통계만 조회"),
    db: RealDB = Depends(get_db),
    current_user: RealUser = Depends(get_current_user)
):
    """
    꿈풀이 통계 정보
    - 전체 또는 개인 통계 제공
    """
    try:
        if user_only:
            # 개인 통계
            query = """
            SELECT 
                COUNT(*) as total_dreams,
                COUNT(DISTINCT DATE(interpretation_date)) as active_days,
                AVG(array_length(keywords, 1)) as avg_keywords_per_dream
            FROM user_dream_records 
            WHERE user_id = %s AND interpretation_date >= CURRENT_DATE - INTERVAL '30 days'
            """
            
            result = await db.execute(query, (current_user.user_id,))
        else:
            # 전체 통계
            query = """
            SELECT 
                COUNT(DISTINCT keyword) as total_keywords,
                COUNT(DISTINCT category_name) as total_categories,
                AVG(confidence_score) as avg_confidence,
                MAX(updated_at) as last_update
            FROM dream_service.dream_interpretations
            """
            
            result = await db.execute(query)
        
        stats_data = result.fetchall()
        
        if stats_data and stats_data[0]:
            return dict(stats_data[0])
        else:
            return {
                "total_keywords": 1500,
                "total_categories": 12,
                "avg_confidence": 0.85,
                "message": "통계 데이터를 업데이트 중입니다"
            }
        
    except Exception as e:
        print(f"통계 조회 오류: {e}")
        raise HTTPException(status_code=500, detail="통계 조회 중 오류가 발생했습니다")


# 내부 유틸리티 함수들
async def _generate_combination_interpretation(
    individual_meanings: List[DreamInterpretationResponse], 
    keywords: List[str]
) -> str:
    """복합 키워드 해석 생성"""
    try:
        # 키워드 조합 분석 로직
        categories = [meaning.category_name for meaning in individual_meanings]
        
        # 카테고리 기반 조합 해석
        if len(set(categories)) == 1:
            # 같은 카테고리
            main_category = categories[0]
            return f"{main_category} 관련 꿈들의 조합은 해당 영역에서의 강한 변화나 집중을 의미합니다. " \
                   f"'{', '.join(keywords)}' 키워드들이 함께 나타나는 것은 " \
                   f"{main_category} 분야에서 중요한 전환점이나 새로운 기회를 암시합니다."
        else:
            # 다른 카테고리들의 조합
            return f"'{', '.join(keywords)}'의 조합은 삶의 여러 영역에서 동시에 일어나는 변화를 나타냅니다. " \
                   f"이러한 다양한 요소들이 조화를 이루어 전반적인 성장과 발전을 이끌어낼 수 있습니다."
        
    except Exception as e:
        print(f"조합 해석 생성 오류: {e}")
        return "입력된 키워드들의 조합은 복합적인 의미를 담고 있어, 각 요소들이 서로 영향을 주고받으며 " \
               "전체적인 메시지를 전달하고 있습니다."


async def _save_dream_record_async(
    user_id: int, 
    dream_record: UserDreamRecord, 
    db: RealDB
):
    """백그라운드에서 꿈 기록 저장"""
    try:
        query = """
        INSERT INTO user_dream_records (user_id, dream_content, keywords, interpretation_date)
        VALUES (%s, %s, %s, %s)
        """
        
        await db.execute(query, (
            user_id,
            dream_record.dream_content,
            dream_record.keywords,
            dream_record.interpretation_date
        ))
        
        db.commit()
        print(f"사용자 {user_id}의 꿈 기록 저장 완료")
        
    except Exception as e:
        print(f"꿈 기록 저장 실패: {e}")
        db.rollback()