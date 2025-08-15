"""
HEAL7 사주명리학 시스템 - AI 모델링 라우터

이 모듈은 AI를 활용한 사주 분석 및 해석을 처리합니다:
- GPT-4, Claude, Gemini를 활용한 다각도 분석
- 개인화된 해석 생성
- 운세 예측 및 조언
- 궁합 분석 및 추천
- 성격 분석 및 직업 추천

다중 AI 모델을 활용하여 보다 정확하고 신뢰할 수 있는 분석을 제공합니다.

@author HEAL7 Development Team
@version 1.0.0
@since 2025-08-12
"""

import asyncio
import json
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional, Union
import logging

from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field, validator

from core.database import DatabaseManager
from core.redis_client import RedisManager
from services.ai_models import (
    OpenAIAnalyzer,
    ClaudeAnalyzer,
    GeminiAnalyzer,
    AIModelManager
)
from services.prompt_templates import PromptTemplateManager
from services.analysis_aggregator import AnalysisAggregator
from models.saju_models import SajuResult, WuXingAnalysis, SipSinAnalysis
from models.ai_models import (
    AIAnalysisRequest,
    AIAnalysisResponse,
    MultiModelAnalysisResponse,
    PersonalityAnalysis,
    CareerAnalysis,
    RelationshipAnalysis,
    HealthAnalysis,
    WealthAnalysis
)
from utils.cache_keys import CacheKeys
from utils.rate_limiter import AIRateLimiter
from utils.text_processor import TextProcessor

router = APIRouter()
logger = logging.getLogger("heal7.ai_modeling")

# ============================================================================
# Request/Response 모델 정의
# ============================================================================

class PersonalityAnalysisRequest(BaseModel):
    """성격 분석 요청 모델"""
    
    saju_result: Dict[str, Any] = Field(..., description="사주 계산 결과")
    wuxing_analysis: Dict[str, Any] = Field(..., description="오행 분석 결과")
    sipsin_analysis: Dict[str, Any] = Field(..., description="십신 분석 결과")
    
    # 분석 옵션
    analysis_depth: str = Field("detailed", regex="^(basic|detailed|comprehensive)$", description="분석 깊이")
    language: str = Field("ko", regex="^(ko|en)$", description="언어")
    user_level: str = Field("beginner", regex="^(beginner|intermediate|expert)$", description="사용자 수준")
    
    # 개인화 옵션
    focus_areas: Optional[List[str]] = Field(None, description="집중 분석 영역")
    avoid_negative: bool = Field(False, description="부정적 표현 완화")
    include_advice: bool = Field(True, description="조언 포함")

class CareerAnalysisRequest(BaseModel):
    """직업 분석 요청 모델"""
    
    saju_result: Dict[str, Any] = Field(..., description="사주 계산 결과")
    wuxing_analysis: Dict[str, Any] = Field(..., description="오행 분석 결과")
    sipsin_analysis: Dict[str, Any] = Field(..., description="십신 분석 결과")
    
    # 추가 정보
    current_job: Optional[str] = Field(None, description="현재 직업")
    career_interests: Optional[List[str]] = Field(None, description="관심 분야")
    education_level: Optional[str] = Field(None, description="교육 수준")
    experience_years: Optional[int] = Field(None, ge=0, le=50, description="경력 년수")
    
    # 분석 옵션
    include_timing: bool = Field(True, description="시기 분석 포함")
    include_industry_match: bool = Field(True, description="업계 적합성 포함")

class CompatibilityAnalysisRequest(BaseModel):
    """궁합 분석 요청 모델"""
    
    person1_data: Dict[str, Any] = Field(..., description="첫 번째 사람 데이터")
    person2_data: Dict[str, Any] = Field(..., description="두 번째 사람 데이터")
    
    # 관계 타입
    relationship_type: str = Field(..., regex="^(romantic|marriage|friendship|business|family)$", description="관계 유형")
    
    # 분석 옵션
    include_timing: bool = Field(True, description="시기 분석 포함")
    include_advice: bool = Field(True, description="조언 포함")
    focus_on_harmony: bool = Field(False, description="조화 중심 분석")

class MultiModelAnalysisRequest(BaseModel):
    """다중 모델 분석 요청"""
    
    saju_result: Dict[str, Any] = Field(..., description="사주 계산 결과")
    wuxing_analysis: Dict[str, Any] = Field(..., description="오행 분석 결과")
    sipsin_analysis: Dict[str, Any] = Field(..., description="십신 분석 결과")
    
    # 분석 타입
    analysis_types: List[str] = Field(..., description="분석 유형 목록")
    
    # 모델 선택
    models: List[str] = Field(["gpt-4", "claude-3", "gemini-pro"], description="사용할 AI 모델")
    
    # 집계 옵션
    aggregation_method: str = Field("weighted_average", regex="^(simple_average|weighted_average|consensus)$", description="집계 방법")
    confidence_threshold: float = Field(0.8, ge=0.0, le=1.0, description="신뢰도 임계값")

# ============================================================================
# AI 분석 엔드포인트들
# ============================================================================

@router.post("/personality", response_model=PersonalityAnalysis)
async def analyze_personality(
    request: PersonalityAnalysisRequest,
    background_tasks: BackgroundTasks,
    db: DatabaseManager = Depends(),
    redis: RedisManager = Depends()
) -> PersonalityAnalysis:
    """
    AI 기반 성격 분석
    
    사주 데이터를 바탕으로 AI가 개인의 성격을 상세히 분석합니다.
    """
    analysis_id = f"personality_{int(datetime.now().timestamp())}"
    
    try:
        logger.info(f"성격 분석 시작: {analysis_id}")
        
        # 캐시 키 생성
        cache_key = CacheKeys.ai_analysis("personality", request.dict())
        
        # 캐시에서 먼저 확인
        cached_result = await redis.get_json(cache_key)
        if cached_result:
            logger.info(f"캐시에서 성격 분석 결과 반환: {analysis_id}")
            return PersonalityAnalysis(**cached_result)
        
        # Rate limiting 확인
        rate_limiter = AIRateLimiter(redis)
        if not await rate_limiter.check_limit("personality_analysis"):
            raise HTTPException(
                status_code=429,
                detail="AI 분석 요청 한도를 초과했습니다. 잠시 후 다시 시도해 주세요."
            )
        
        # AI 모델 매니저 초기화
        ai_manager = AIModelManager()
        
        # 프롬프트 템플릿 생성
        prompt_manager = PromptTemplateManager()
        prompt = await prompt_manager.create_personality_prompt(
            saju_result=request.saju_result,
            wuxing_analysis=request.wuxing_analysis,
            sipsin_analysis=request.sipsin_analysis,
            analysis_depth=request.analysis_depth,
            user_level=request.user_level,
            language=request.language
        )
        
        # AI 분석 실행
        analysis_start = datetime.now()
        
        if request.user_level == "expert":
            # 전문가용: 다중 모델 분석
            openai_analyzer = OpenAIAnalyzer()
            claude_analyzer = ClaudeAnalyzer()
            
            openai_result, claude_result = await asyncio.gather(
                openai_analyzer.analyze_personality(prompt),
                claude_analyzer.analyze_personality(prompt),
                return_exceptions=True
            )
            
            # 결과 집계
            aggregator = AnalysisAggregator()
            final_analysis = await aggregator.aggregate_personality_analyses(
                [openai_result, claude_result]
            )
            
        else:
            # 일반 사용자: 단일 모델
            primary_model = await ai_manager.get_primary_model("personality")
            final_analysis = await primary_model.analyze_personality(prompt)
        
        analysis_time = (datetime.now() - analysis_start).total_seconds()
        
        # 후처리
        text_processor = TextProcessor()
        final_analysis = await text_processor.post_process_personality_analysis(
            final_analysis,
            avoid_negative=request.avoid_negative,
            language=request.language
        )
        
        # 응답 생성
        response = PersonalityAnalysis(
            analysis_id=analysis_id,
            analysis_type="personality",
            **final_analysis,
            processing_time=analysis_time,
            confidence_score=final_analysis.get("confidence_score", 85),
            model_info={
                "primary_model": "gpt-4" if request.user_level != "expert" else "multi-model",
                "analysis_depth": request.analysis_depth,
                "language": request.language
            }
        )
        
        # 백그라운드에서 결과 캐싱 및 로깅
        background_tasks.add_task(
            cache_and_log_ai_analysis,
            cache_key, response.dict(), analysis_id, analysis_time,
            "personality", db, redis
        )
        
        logger.info(f"성격 분석 완료: {analysis_id} ({analysis_time:.3f}초)")
        return response
        
    except Exception as e:
        logger.error(f"성격 분석 오류: {analysis_id} - {str(e)}")
        
        # 에러 로깅
        background_tasks.add_task(
            log_ai_analysis_error,
            analysis_id, "personality", str(e), request.dict(), db
        )
        
        raise HTTPException(
            status_code=500,
            detail=f"성격 분석 중 오류가 발생했습니다: {str(e)}"
        )

@router.post("/career", response_model=CareerAnalysis)
async def analyze_career(
    request: CareerAnalysisRequest,
    background_tasks: BackgroundTasks,
    db: DatabaseManager = Depends(),
    redis: RedisManager = Depends()
) -> CareerAnalysis:
    """
    AI 기반 직업/진로 분석
    
    사주 데이터를 바탕으로 적합한 직업과 진로를 분석합니다.
    """
    analysis_id = f"career_{int(datetime.now().timestamp())}"
    
    try:
        logger.info(f"진로 분석 시작: {analysis_id}")
        
        # 캐시 확인
        cache_key = CacheKeys.ai_analysis("career", request.dict())
        cached_result = await redis.get_json(cache_key)
        if cached_result:
            return CareerAnalysis(**cached_result)
        
        # Rate limiting
        rate_limiter = AIRateLimiter(redis)
        if not await rate_limiter.check_limit("career_analysis"):
            raise HTTPException(status_code=429, detail="요청 한도 초과")
        
        # AI 분석 실행
        ai_manager = AIModelManager()
        primary_model = await ai_manager.get_primary_model("career")
        
        prompt_manager = PromptTemplateManager()
        prompt = await prompt_manager.create_career_prompt(
            saju_result=request.saju_result,
            wuxing_analysis=request.wuxing_analysis,
            sipsin_analysis=request.sipsin_analysis,
            current_job=request.current_job,
            career_interests=request.career_interests,
            education_level=request.education_level,
            experience_years=request.experience_years
        )
        
        analysis_start = datetime.now()
        career_analysis = await primary_model.analyze_career(prompt)
        analysis_time = (datetime.now() - analysis_start).total_seconds()
        
        # 응답 생성
        response = CareerAnalysis(
            analysis_id=analysis_id,
            analysis_type="career",
            **career_analysis,
            processing_time=analysis_time
        )
        
        # 백그라운드 작업
        background_tasks.add_task(
            cache_and_log_ai_analysis,
            cache_key, response.dict(), analysis_id, analysis_time,
            "career", db, redis
        )
        
        logger.info(f"진로 분석 완료: {analysis_id}")
        return response
        
    except Exception as e:
        logger.error(f"진로 분석 오류: {analysis_id} - {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/compatibility", response_model=Dict[str, Any])
async def analyze_compatibility(
    request: CompatibilityAnalysisRequest,
    background_tasks: BackgroundTasks,
    db: DatabaseManager = Depends(),
    redis: RedisManager = Depends()
) -> Dict[str, Any]:
    """
    AI 기반 궁합 분석
    
    두 사람의 사주를 비교하여 AI가 상세한 궁합을 분석합니다.
    """
    analysis_id = f"compatibility_{int(datetime.now().timestamp())}"
    
    try:
        logger.info(f"궁합 분석 시작: {analysis_id}")
        
        # 캐시 확인
        cache_key = CacheKeys.ai_analysis("compatibility", request.dict())
        cached_result = await redis.get_json(cache_key)
        if cached_result:
            return cached_result
        
        # Rate limiting
        rate_limiter = AIRateLimiter(redis)
        if not await rate_limiter.check_limit("compatibility_analysis"):
            raise HTTPException(status_code=429, detail="요청 한도 초과")
        
        # 전문적인 궁합 분석을 위해 다중 모델 사용
        openai_analyzer = OpenAIAnalyzer()
        claude_analyzer = ClaudeAnalyzer()
        
        prompt_manager = PromptTemplateManager()
        prompt = await prompt_manager.create_compatibility_prompt(
            person1_data=request.person1_data,
            person2_data=request.person2_data,
            relationship_type=request.relationship_type
        )
        
        analysis_start = datetime.now()
        
        # 병렬 분석 실행
        openai_result, claude_result = await asyncio.gather(
            openai_analyzer.analyze_compatibility(prompt),
            claude_analyzer.analyze_compatibility(prompt),
            return_exceptions=True
        )
        
        # 결과 집계
        aggregator = AnalysisAggregator()
        final_analysis = await aggregator.aggregate_compatibility_analyses(
            [openai_result, claude_result]
        )
        
        analysis_time = (datetime.now() - analysis_start).total_seconds()
        
        response = {
            "analysis_id": analysis_id,
            "analysis_type": "compatibility",
            "relationship_type": request.relationship_type,
            "overall_score": final_analysis.get("overall_score", 75),
            "detailed_analysis": final_analysis.get("detailed_analysis", {}),
            "strengths": final_analysis.get("strengths", []),
            "challenges": final_analysis.get("challenges", []),
            "recommendations": final_analysis.get("recommendations", []),
            "timing_advice": final_analysis.get("timing_advice", {}),
            "processing_time": analysis_time,
            "confidence_score": final_analysis.get("confidence_score", 80),
            "model_info": {
                "models_used": ["gpt-4", "claude-3"],
                "aggregation_method": "consensus"
            }
        }
        
        # 백그라운드 작업
        background_tasks.add_task(
            cache_and_log_ai_analysis,
            cache_key, response, analysis_id, analysis_time,
            "compatibility", db, redis
        )
        
        logger.info(f"궁합 분석 완료: {analysis_id}")
        return response
        
    except Exception as e:
        logger.error(f"궁합 분석 오류: {analysis_id} - {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/multi-model", response_model=MultiModelAnalysisResponse)
async def multi_model_analysis(
    request: MultiModelAnalysisRequest,
    background_tasks: BackgroundTasks,
    db: DatabaseManager = Depends(),
    redis: RedisManager = Depends()
) -> MultiModelAnalysisResponse:
    """
    다중 AI 모델을 활용한 종합 분석
    
    여러 AI 모델의 결과를 종합하여 보다 정확하고 신뢰할 수 있는 분석을 제공합니다.
    """
    analysis_id = f"multi_model_{int(datetime.now().timestamp())}"
    
    try:
        logger.info(f"다중 모델 분석 시작: {analysis_id}")
        
        # 캐시 확인
        cache_key = CacheKeys.ai_analysis("multi_model", request.dict())
        cached_result = await redis.get_json(cache_key)
        if cached_result:
            return MultiModelAnalysisResponse(**cached_result)
        
        # Rate limiting (다중 모델은 더 엄격)
        rate_limiter = AIRateLimiter(redis)
        if not await rate_limiter.check_limit("multi_model_analysis", limit=2):
            raise HTTPException(status_code=429, detail="다중 모델 분석 한도 초과")
        
        analysis_start = datetime.now()
        
        # AI 모델 초기화
        analyzers = {}
        if "gpt-4" in request.models:
            analyzers["gpt-4"] = OpenAIAnalyzer()
        if "claude-3" in request.models:
            analyzers["claude-3"] = ClaudeAnalyzer()
        if "gemini-pro" in request.models:
            analyzers["gemini-pro"] = GeminiAnalyzer()
        
        # 분석 타입별 결과 저장
        analysis_results = {}
        
        for analysis_type in request.analysis_types:
            # 프롬프트 생성
            prompt_manager = PromptTemplateManager()
            prompt = await prompt_manager.create_prompt_by_type(
                analysis_type=analysis_type,
                saju_result=request.saju_result,
                wuxing_analysis=request.wuxing_analysis,
                sipsin_analysis=request.sipsin_analysis
            )
            
            # 각 모델별 분석 실행
            model_results = {}
            tasks = []
            
            for model_name, analyzer in analyzers.items():
                task = asyncio.create_task(
                    analyzer.analyze_by_type(analysis_type, prompt),
                    name=f"{model_name}_{analysis_type}"
                )
                tasks.append(task)
            
            # 모든 모델 결과 대기
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            for i, result in enumerate(results):
                model_name = list(analyzers.keys())[i]
                if not isinstance(result, Exception):
                    model_results[model_name] = result
                else:
                    logger.warning(f"모델 {model_name} 분석 실패: {result}")
            
            # 결과 집계
            if model_results:
                aggregator = AnalysisAggregator()
                aggregated_result = await aggregator.aggregate_by_method(
                    model_results,
                    method=request.aggregation_method,
                    confidence_threshold=request.confidence_threshold
                )
                analysis_results[analysis_type] = aggregated_result
        
        analysis_time = (datetime.now() - analysis_start).total_seconds()
        
        # 전체 신뢰도 계산
        overall_confidence = sum(
            result.get("confidence_score", 0) for result in analysis_results.values()
        ) / len(analysis_results) if analysis_results else 0
        
        response = MultiModelAnalysisResponse(
            analysis_id=analysis_id,
            analysis_types=request.analysis_types,
            models_used=request.models,
            aggregation_method=request.aggregation_method,
            analysis_results=analysis_results,
            overall_confidence=overall_confidence,
            processing_time=analysis_time,
            model_agreement_score=await calculate_model_agreement(analysis_results),
            metadata={
                "total_models": len(analyzers),
                "successful_analyses": len(analysis_results),
                "failed_analyses": len(request.analysis_types) - len(analysis_results),
                "timestamp": datetime.now().isoformat()
            }
        )
        
        # 백그라운드 작업
        background_tasks.add_task(
            cache_and_log_ai_analysis,
            cache_key, response.dict(), analysis_id, analysis_time,
            "multi_model", db, redis
        )
        
        logger.info(f"다중 모델 분석 완료: {analysis_id}")
        return response
        
    except Exception as e:
        logger.error(f"다중 모델 분석 오류: {analysis_id} - {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/streaming/{analysis_type}")
async def stream_analysis(
    analysis_type: str,
    saju_data: str,
    redis: RedisManager = Depends()
):
    """
    스트리밍 방식 AI 분석
    
    실시간으로 분석 결과를 스트리밍합니다.
    """
    async def generate_analysis_stream():
        try:
            # AI 모델 초기화
            ai_manager = AIModelManager()
            model = await ai_manager.get_streaming_model(analysis_type)
            
            # 스트리밍 분석 시작
            async for chunk in model.stream_analysis(saju_data):
                yield f"data: {json.dumps(chunk, ensure_ascii=False)}\n\n"
                
        except Exception as e:
            error_chunk = {
                "type": "error",
                "message": str(e),
                "timestamp": datetime.now().isoformat()
            }
            yield f"data: {json.dumps(error_chunk, ensure_ascii=False)}\n\n"
    
    return StreamingResponse(
        generate_analysis_stream(),
        media_type="text/plain",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive"
        }
    )

@router.get("/models/status")
async def get_ai_models_status(
    redis: RedisManager = Depends()
) -> Dict[str, Any]:
    """
    AI 모델 상태 조회
    
    현재 사용 가능한 AI 모델들의 상태를 반환합니다.
    """
    try:
        ai_manager = AIModelManager()
        status = await ai_manager.get_all_models_status()
        
        return {
            "models": status,
            "total_models": len(status),
            "active_models": len([m for m in status.values() if m.get("status") == "active"]),
            "last_updated": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"모델 상태 조회 오류: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# ============================================================================
# 헬퍼 함수들
# ============================================================================

async def cache_and_log_ai_analysis(
    cache_key: str,
    result_data: dict,
    analysis_id: str,
    processing_time: float,
    analysis_type: str,
    db: DatabaseManager,
    redis: RedisManager
):
    """
    AI 분석 결과 캐싱 및 로깅 (백그라운드 작업)
    """
    try:
        # Redis에 결과 캐싱 (분석 타입별 다른 TTL)
        ttl = {
            "personality": 21600,  # 6시간
            "career": 43200,       # 12시간
            "compatibility": 10800, # 3시간
            "multi_model": 7200    # 2시간
        }.get(analysis_type, 3600)
        
        await redis.set_json(cache_key, result_data, expire=ttl)
        
        # AI 분석 통계 업데이트
        await redis.update_ai_analysis_stats(
            analysis_id, analysis_type, processing_time, success=True
        )
        
        # 데이터베이스에 분석 로그 저장
        await db.log_ai_analysis(
            analysis_id=analysis_id,
            analysis_type=analysis_type,
            processing_time=processing_time,
            cache_key=cache_key,
            success=True
        )
        
    except Exception as e:
        logger.error(f"AI 분석 결과 캐싱/로깅 오류: {analysis_id} - {str(e)}")

async def log_ai_analysis_error(
    analysis_id: str,
    analysis_type: str,
    error_message: str,
    request_data: dict,
    db: DatabaseManager
):
    """
    AI 분석 오류 로깅 (백그라운드 작업)
    """
    try:
        await db.log_ai_analysis_error(
            analysis_id=analysis_id,
            analysis_type=analysis_type,
            error_message=error_message,
            request_data=request_data
        )
        
    except Exception as e:
        logger.error(f"AI 분석 오류 로깅 실패: {analysis_id} - {str(e)}")

async def calculate_model_agreement(analysis_results: Dict[str, Any]) -> float:
    """
    모델 간 일치도 계산
    """
    if len(analysis_results) < 2:
        return 100.0
    
    # 간단한 일치도 계산 (실제로는 더 정교한 알고리즘 필요)
    confidence_scores = [
        result.get("confidence_score", 0) 
        for result in analysis_results.values()
    ]
    
    if not confidence_scores:
        return 0.0
    
    avg_confidence = sum(confidence_scores) / len(confidence_scores)
    variance = sum((score - avg_confidence) ** 2 for score in confidence_scores) / len(confidence_scores)
    
    # 분산이 낮을수록 높은 일치도
    agreement_score = max(0, 100 - variance)
    return round(agreement_score, 2)