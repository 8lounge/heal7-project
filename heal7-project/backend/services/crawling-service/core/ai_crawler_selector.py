#!/usr/bin/env python3
"""
🧠 AI 기반 크롤러 선택 엔진 (Gemini 2.0 통합)
URL 분석을 통한 최적 크롤링 도구 자동 선택

🎯 핵심 기능:
- URL 패턴 및 콘텐츠 타입 AI 분석  
- 3단계 도구 체계 최적화 (httpx → httpx+beautifulsoup → playwright)
- 실시간 품질 평가 및 도구 전환
- 학습 기반 성능 최적화

Author: HEAL7 Development Team  
Version: 1.0.0 (Gemini 2.0 Integration)
Date: 2025-09-03
"""

import asyncio
import json
import logging
import time
import re
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
from urllib.parse import urlparse, urljoin

# AI 분석기 import
try:
    from ..multimodal.ai_analyzer import MultimodalAnalyzer, AIModel
except ImportError:
    # 폴백 구현
    class AIModel:
        GEMINI_FLASH = "gemini_flash"
    
    class MultimodalAnalyzer:
        async def analyze_text(self, text, model, analysis_type):
            return {"success": False, "error": "AI 분석기 미설치"}

from .crawlers.base_crawler import CrawlerType

logger = logging.getLogger(__name__)


class CrawlComplexity(Enum):
    """크롤링 복잡도 레벨"""
    SIMPLE = "simple"       # API 또는 정적 HTML (httpx)
    MODERATE = "moderate"   # HTML 파싱 필요 (httpx + beautifulsoup)
    COMPLEX = "complex"     # JavaScript 렌더링 필요 (playwright)


class AIConfidence(Enum):
    """AI 분석 신뢰도"""
    HIGH = "high"       # 90%+ 신뢰도
    MEDIUM = "medium"   # 70-89% 신뢰도  
    LOW = "low"         # 50-69% 신뢰도
    FALLBACK = "fallback"  # 50% 미만, 기본 규칙 사용


@dataclass
class CrawlerRecommendation:
    """크롤러 추천 결과"""
    primary_crawler: CrawlerType
    fallback_crawler: CrawlerType
    complexity_level: CrawlComplexity
    confidence_score: float
    reasoning: str
    analysis_time_ms: float
    ai_analysis: Dict[str, Any] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "primary_crawler": self.primary_crawler.value,
            "fallback_crawler": self.fallback_crawler.value,
            "complexity_level": self.complexity_level.value,
            "confidence_score": self.confidence_score,
            "reasoning": self.reasoning,
            "analysis_time_ms": self.analysis_time_ms,
            "ai_analysis": self.ai_analysis
        }


@dataclass
class URLAnalysisContext:
    """URL 분석 컨텍스트"""
    url: str
    domain: str
    path: str
    params: str
    initial_content: Optional[str] = None
    response_headers: Optional[Dict[str, str]] = None
    status_code: Optional[int] = None


class AICrawlerSelector:
    """🧠 AI 기반 크롤러 선택 엔진"""
    
    def __init__(self):
        self.logger = logging.getLogger(f"{__name__}.AICrawlerSelector")
        self.ai_analyzer = None
        self._initialize_ai()
        
        # 성능 통계
        self.selection_stats = {
            "total_selections": 0,
            "ai_selections": 0,
            "fallback_selections": 0,
            "accuracy_scores": []
        }
        
        # 학습 데이터 (도메인별 성공 패턴)
        self.learning_patterns = {}
    
    def _initialize_ai(self):
        """AI 분석기 초기화"""
        try:
            self.ai_analyzer = MultimodalAnalyzer()
            self.logger.info("✅ AI 크롤러 선택기 초기화 완료 (Gemini 2.0)")
        except Exception as e:
            self.logger.warning(f"⚠️ AI 분석기 초기화 실패, 폴백 모드: {e}")
            self.ai_analyzer = None
    
    async def select_optimal_crawler(
        self, 
        url: str, 
        context: Optional[URLAnalysisContext] = None,
        use_ai: bool = True
    ) -> CrawlerRecommendation:
        """최적 크롤러 선택 (AI + 휴리스틱 하이브리드)"""
        start_time = time.time()
        
        try:
            # 1단계: URL 기본 분석
            url_context = context or self._create_url_context(url)
            
            # 2단계: AI 분석 (활성화된 경우)
            ai_result = None
            if use_ai and self.ai_analyzer:
                ai_result = await self._ai_url_analysis(url_context)
            
            # 3단계: 최종 추천 결정
            recommendation = await self._make_final_recommendation(
                url_context, ai_result
            )
            
            recommendation.analysis_time_ms = (time.time() - start_time) * 1000
            
            # 4단계: 통계 업데이트
            self._update_selection_stats(recommendation, ai_result is not None)
            
            self.logger.info(
                f"🎯 크롤러 선택 완료: {recommendation.primary_crawler.value} "
                f"(신뢰도: {recommendation.confidence_score:.1f}%, "
                f"분석시간: {recommendation.analysis_time_ms:.0f}ms)"
            )
            
            return recommendation
            
        except Exception as e:
            self.logger.error(f"❌ 크롤러 선택 실패: {e}")
            return self._create_fallback_recommendation(url, str(e))
    
    def _create_url_context(self, url: str) -> URLAnalysisContext:
        """URL 컨텍스트 생성"""
        parsed = urlparse(url)
        return URLAnalysisContext(
            url=url,
            domain=parsed.netloc,
            path=parsed.path,
            params=parsed.query
        )
    
    async def _ai_url_analysis(self, context: URLAnalysisContext) -> Optional[Dict[str, Any]]:
        """AI 기반 URL 분석"""
        try:
            # Gemini Flash 모델로 URL 패턴 분석
            analysis_prompt = f"""
웹 크롤링을 위한 URL 분석을 해주세요. 3단계 도구 체계 중 최적 선택을 위해:

🎯 분석 대상 URL: {context.url}
- 도메인: {context.domain} 
- 경로: {context.path}
- 파라미터: {context.params}

🔍 판단 기준:
1. HTTPX (1단계): API 엔드포인트, 정적 파일, 단순 HTML
2. HTTPX + BeautifulSoup (2단계): HTML 파싱 필요, 정적 콘텐츠
3. Playwright (3단계): JavaScript 렌더링, 동적 콘텐츠, 복잡한 상호작용

💡 분석 요청:
- complexity_level: "simple", "moderate", "complex" 중 선택
- confidence_score: 0-100 점수 
- reasoning: 선택 이유 (한 문장)
- requires_js: JavaScript 필요 여부 (boolean)
- is_api: API 엔드포인트 여부 (boolean)
- content_type_prediction: 예상 콘텐츠 타입

JSON 형태로 응답해주세요.
"""
            
            result = await self.ai_analyzer.analyze_text(
                text=analysis_prompt,
                model=AIModel.GEMINI_FLASH,
                analysis_type="url_crawler_selection"
            )
            
            if result and result.get('success'):
                content = result.get('content', {})
                # JSON 파싱 시도
                if isinstance(content, str):
                    try:
                        content = json.loads(content)
                    except json.JSONDecodeError:
                        # JSON이 아닌 경우 키워드 추출
                        content = self._extract_analysis_keywords(content)
                
                self.logger.debug(f"🤖 AI 분석 결과: {content}")
                return content
            
        except Exception as e:
            self.logger.warning(f"⚠️ AI 분석 실패: {e}")
        
        return None
    
    def _extract_analysis_keywords(self, text: str) -> Dict[str, Any]:
        """텍스트에서 분석 키워드 추출"""
        analysis = {
            "complexity_level": "moderate",
            "confidence_score": 60.0,
            "reasoning": "키워드 기반 분석",
            "requires_js": False,
            "is_api": False
        }
        
        text_lower = text.lower()
        
        # 복잡도 판단
        if any(word in text_lower for word in ['api', 'json', 'simple', 'static']):
            analysis["complexity_level"] = "simple"
            analysis["confidence_score"] = 75.0
        elif any(word in text_lower for word in ['javascript', 'dynamic', 'complex', 'spa']):
            analysis["complexity_level"] = "complex"
            analysis["requires_js"] = True
            analysis["confidence_score"] = 80.0
        
        # API 판단
        if any(word in text_lower for word in ['api', 'rest', 'json', 'graphql']):
            analysis["is_api"] = True
            
        return analysis
    
    async def _make_final_recommendation(
        self, 
        context: URLAnalysisContext,
        ai_result: Optional[Dict[str, Any]]
    ) -> CrawlerRecommendation:
        """최종 크롤러 추천 결정"""
        
        # AI 결과가 있는 경우
        if ai_result:
            return self._ai_based_recommendation(context, ai_result)
        
        # 휴리스틱 기반 폴백
        return self._heuristic_based_recommendation(context)
    
    def _ai_based_recommendation(
        self, 
        context: URLAnalysisContext, 
        ai_result: Dict[str, Any]
    ) -> CrawlerRecommendation:
        """AI 결과 기반 추천"""
        
        complexity = ai_result.get("complexity_level", "moderate")
        confidence = ai_result.get("confidence_score", 60.0)
        reasoning = ai_result.get("reasoning", "AI 기반 분석")
        requires_js = ai_result.get("requires_js", False)
        is_api = ai_result.get("is_api", False)
        
        # 크롤러 선택 로직
        if is_api or complexity == "simple":
            primary = CrawlerType.HTTPX
            fallback = CrawlerType.PLAYWRIGHT
            complexity_level = CrawlComplexity.SIMPLE
        elif requires_js or complexity == "complex":
            primary = CrawlerType.PLAYWRIGHT
            fallback = CrawlerType.HTTPX
            complexity_level = CrawlComplexity.COMPLEX
        else:  # moderate
            primary = CrawlerType.HTTPX  # BeautifulSoup는 HTTPX에 포함됨
            fallback = CrawlerType.PLAYWRIGHT
            complexity_level = CrawlComplexity.MODERATE
        
        return CrawlerRecommendation(
            primary_crawler=primary,
            fallback_crawler=fallback,
            complexity_level=complexity_level,
            confidence_score=confidence,
            reasoning=f"AI 분석: {reasoning}",
            analysis_time_ms=0,  # 나중에 설정됨
            ai_analysis=ai_result
        )
    
    def _heuristic_based_recommendation(
        self, 
        context: URLAnalysisContext
    ) -> CrawlerRecommendation:
        """휴리스틱 기반 추천 (AI 폴백)"""
        
        url_lower = context.url.lower()
        domain_lower = context.domain.lower()
        path_lower = context.path.lower()
        
        # API 패턴 감지
        if any(pattern in url_lower for pattern in [
            'api', '.json', '/rest/', '/graphql', '/v1/', '/v2/'
        ]):
            return CrawlerRecommendation(
                primary_crawler=CrawlerType.HTTPX,
                fallback_crawler=CrawlerType.PLAYWRIGHT,
                complexity_level=CrawlComplexity.SIMPLE,
                confidence_score=85.0,
                reasoning="API 엔드포인트 패턴 감지",
                analysis_time_ms=0
            )
        
        # 정부 사이트 (복잡함)
        if '.go.kr' in domain_lower or '.gov' in domain_lower:
            return CrawlerRecommendation(
                primary_crawler=CrawlerType.PLAYWRIGHT,
                fallback_crawler=CrawlerType.HTTPX,
                complexity_level=CrawlComplexity.COMPLEX,
                confidence_score=80.0,
                reasoning="정부 사이트 - JavaScript 렌더링 필요",
                analysis_time_ms=0
            )
        
        # 동적 콘텐츠 패턴
        if any(pattern in url_lower for pattern in [
            'spa', 'app', 'react', 'vue', 'angular', 'ajax'
        ]):
            return CrawlerRecommendation(
                primary_crawler=CrawlerType.PLAYWRIGHT,
                fallback_crawler=CrawlerType.HTTPX,
                complexity_level=CrawlComplexity.COMPLEX,
                confidence_score=75.0,
                reasoning="동적 웹 애플리케이션 패턴 감지",
                analysis_time_ms=0
            )
        
        # 기본값: 중간 복잡도
        return CrawlerRecommendation(
            primary_crawler=CrawlerType.HTTPX,  # BeautifulSoup 포함
            fallback_crawler=CrawlerType.PLAYWRIGHT,
            complexity_level=CrawlComplexity.MODERATE,
            confidence_score=65.0,
            reasoning="휴리스틱 기본 분석 - HTML 파싱 중심",
            analysis_time_ms=0
        )
    
    def _create_fallback_recommendation(self, url: str, error: str) -> CrawlerRecommendation:
        """에러 시 폴백 추천"""
        return CrawlerRecommendation(
            primary_crawler=CrawlerType.HTTPX,
            fallback_crawler=CrawlerType.PLAYWRIGHT,
            complexity_level=CrawlComplexity.MODERATE,
            confidence_score=30.0,
            reasoning=f"분석 오류로 인한 기본값 적용: {error}",
            analysis_time_ms=0
        )
    
    def _update_selection_stats(self, recommendation: CrawlerRecommendation, used_ai: bool):
        """선택 통계 업데이트"""
        self.selection_stats["total_selections"] += 1
        if used_ai:
            self.selection_stats["ai_selections"] += 1
        else:
            self.selection_stats["fallback_selections"] += 1
        
        self.selection_stats["accuracy_scores"].append(recommendation.confidence_score)
        
        # 최근 100개 점수만 유지
        if len(self.selection_stats["accuracy_scores"]) > 100:
            self.selection_stats["accuracy_scores"] = self.selection_stats["accuracy_scores"][-100:]
    
    async def evaluate_crawler_performance(
        self,
        url: str,
        recommended_crawler: CrawlerType,
        actual_result: Dict[str, Any]
    ) -> float:
        """크롤러 성능 평가 및 학습"""
        try:
            success = actual_result.get('success', False)
            response_time = actual_result.get('response_time', 0)
            content_length = len(actual_result.get('html', ''))
            
            # 성능 점수 계산 (0-100)
            score = 0.0
            if success:
                score += 50.0  # 기본 성공 점수
                
                # 응답 시간 평가 (빠를수록 좋음)
                if response_time < 2.0:
                    score += 25.0
                elif response_time < 5.0:
                    score += 15.0
                elif response_time < 10.0:
                    score += 5.0
                
                # 콘텐츠 품질 평가
                if content_length > 1000:
                    score += 25.0
                elif content_length > 100:
                    score += 15.0
                elif content_length > 0:
                    score += 5.0
            
            # 도메인별 학습 패턴 업데이트
            domain = urlparse(url).netloc
            if domain not in self.learning_patterns:
                self.learning_patterns[domain] = {
                    'crawler_scores': {},
                    'total_attempts': 0,
                    'successful_attempts': 0
                }
            
            pattern = self.learning_patterns[domain]
            crawler_key = recommended_crawler.value
            
            if crawler_key not in pattern['crawler_scores']:
                pattern['crawler_scores'][crawler_key] = []
            
            pattern['crawler_scores'][crawler_key].append(score)
            pattern['total_attempts'] += 1
            if success:
                pattern['successful_attempts'] += 1
            
            # 최근 10개 점수만 유지
            if len(pattern['crawler_scores'][crawler_key]) > 10:
                pattern['crawler_scores'][crawler_key] = pattern['crawler_scores'][crawler_key][-10:]
            
            self.logger.debug(f"📊 크롤러 성능 평가: {crawler_key} → {score:.1f}점")
            return score
            
        except Exception as e:
            self.logger.error(f"❌ 성능 평가 실패: {e}")
            return 0.0
    
    def get_selection_stats(self) -> Dict[str, Any]:
        """선택 통계 조회"""
        accuracy_scores = self.selection_stats["accuracy_scores"]
        avg_accuracy = sum(accuracy_scores) / len(accuracy_scores) if accuracy_scores else 0.0
        
        return {
            "total_selections": self.selection_stats["total_selections"],
            "ai_selections": self.selection_stats["ai_selections"],
            "fallback_selections": self.selection_stats["fallback_selections"],
            "ai_usage_rate": (
                self.selection_stats["ai_selections"] / max(1, self.selection_stats["total_selections"]) * 100
            ),
            "average_accuracy": avg_accuracy,
            "learning_domains": len(self.learning_patterns),
            "ai_analyzer_status": "active" if self.ai_analyzer else "inactive"
        }


# 전역 인스턴스
_ai_selector = None

async def get_ai_crawler_selector() -> AICrawlerSelector:
    """AI 크롤러 선택기 인스턴스 조회"""
    global _ai_selector
    if _ai_selector is None:
        _ai_selector = AICrawlerSelector()
    return _ai_selector


# 편의 함수들
async def select_crawler_for_url(url: str, use_ai: bool = True) -> CrawlerRecommendation:
    """URL에 최적화된 크롤러 선택"""
    selector = await get_ai_crawler_selector()
    return await selector.select_optimal_crawler(url, use_ai=use_ai)


async def evaluate_crawl_result(
    url: str, 
    crawler: CrawlerType, 
    result: Dict[str, Any]
) -> float:
    """크롤링 결과 평가 및 학습"""
    selector = await get_ai_crawler_selector()
    return await selector.evaluate_crawler_performance(url, crawler, result)