#!/usr/bin/env python3
"""
🛠️ 크롤링 도구 선택 라우터 (3단계 간소화 시스템)
단계별 크롤링 도구 추천 및 관리

🎯 3단계 도구 체계:
- 단계 1: HTTPX (빠른 HTTP 요청)
- 단계 2: HTTPX + BeautifulSoup (HTML 파싱)
- 단계 3: Playwright (JavaScript 렌더링)

Author: HEAL7 Development Team
Version: 2.0.0 (Simplified)
Date: 2025-09-03
"""

from typing import List, Dict, Any, Optional
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field
from enum import Enum
import logging

logger = logging.getLogger(__name__)

# ================================
# 데이터 모델들 (간소화)
# ================================

class CrawlerToolType(str, Enum):
    """3단계 크롤링 도구 타입"""
    HTTPX = "httpx"
    HTTPX_BEAUTIFULSOUP = "httpx_beautifulsoup" 
    PLAYWRIGHT = "playwright"

class UseCaseType(str, Enum):
    """사용 사례 타입"""
    STATIC_CONTENT = "static_content"      # 정적 콘텐츠
    DYNAMIC_CONTENT = "dynamic_content"    # 동적 콘텐츠 (JS)
    API_SCRAPING = "api_scraping"         # API 기반 수집
    SPEED_CRITICAL = "speed_critical"     # 속도 중시
    RELIABILITY_CRITICAL = "reliability_critical" # 안정성 중시

class CrawlerToolSpec(BaseModel):
    """크롤링 도구 사양"""
    tool_type: CrawlerToolType
    display_name: str
    description: str
    strengths: List[str] = []
    weaknesses: List[str] = []
    best_use_cases: List[UseCaseType] = []
    performance_score: float = Field(ge=0, le=10)  # 0-10 점수
    reliability_score: float = Field(ge=0, le=10)
    ease_of_use_score: float = Field(ge=0, le=10)
    resource_usage: str = Field(description="low/medium/high")
    javascript_support: bool = False
    async_support: bool = False
    installation_complexity: str = Field(description="easy/medium/hard")
    recommended_fallbacks: List[CrawlerToolType] = []

# ================================
# 3단계 도구 사양 정의
# ================================

CRAWLER_TOOLS_SPECS: Dict[CrawlerToolType, CrawlerToolSpec] = {
    
    # 단계 1: HTTPX (기본)
    CrawlerToolType.HTTPX: CrawlerToolSpec(
        tool_type=CrawlerToolType.HTTPX,
        display_name="HTTPX",
        description="⚡ 초고속 비동기 HTTP 클라이언트",
        strengths=[
            "🚀 매우 빠른 속도",
            "💾 낮은 메모리 사용",
            "🔄 비동기 지원",
            "📡 HTTP/2 지원",
            "🛠️ 간단한 설정"
        ],
        weaknesses=[
            "❌ JavaScript 미지원",
            "🔍 HTML 파싱 불가",
            "📝 정적 콘텐츠만 가능"
        ],
        best_use_cases=[UseCaseType.API_SCRAPING, UseCaseType.SPEED_CRITICAL],
        performance_score=10.0,
        reliability_score=8.0,
        ease_of_use_score=9.0,
        resource_usage="low",
        javascript_support=False,
        async_support=True,
        installation_complexity="easy",
        recommended_fallbacks=[CrawlerToolType.HTTPX_BEAUTIFULSOUP, CrawlerToolType.PLAYWRIGHT]
    ),
    
    # 단계 2: HTTPX + BeautifulSoup (중간)
    CrawlerToolType.HTTPX_BEAUTIFULSOUP: CrawlerToolSpec(
        tool_type=CrawlerToolType.HTTPX_BEAUTIFULSOUP,
        display_name="HTTPX + BeautifulSoup",
        description="🍜 빠른 HTTP + 강력한 HTML 파싱",
        strengths=[
            "⚡ 빠른 속도",
            "🔍 HTML 파싱 지원",
            "💾 보통 메모리 사용",
            "🔄 비동기 지원",
            "📊 정확한 데이터 추출"
        ],
        weaknesses=[
            "❌ JavaScript 미지원",
            "🖱️ 사용자 상호작용 불가",
            "🌐 동적 콘텐츠 제한"
        ],
        best_use_cases=[UseCaseType.STATIC_CONTENT, UseCaseType.SPEED_CRITICAL],
        performance_score=8.0,
        reliability_score=8.0,
        ease_of_use_score=8.0,
        resource_usage="medium",
        javascript_support=False,
        async_support=True,
        installation_complexity="easy",
        recommended_fallbacks=[CrawlerToolType.PLAYWRIGHT, CrawlerToolType.HTTPX]
    ),
    
    # 단계 3: Playwright (최고급)
    CrawlerToolType.PLAYWRIGHT: CrawlerToolSpec(
        tool_type=CrawlerToolType.PLAYWRIGHT,
        display_name="Playwright",
        description="🎭 최신 브라우저 자동화의 정점",
        strengths=[
            "🌐 완전한 JavaScript 지원",
            "📱 모든 브라우저 지원",
            "🖱️ 사용자 상호작용",
            "📸 스크린샷 지원",
            "🛡️ 안티봇 우회",
            "⚡ 빠른 실행 속도"
        ],
        weaknesses=[
            "💾 높은 메모리 사용",
            "🔧 복잡한 설정",
            "⏱️ 상대적 느린 시작"
        ],
        best_use_cases=[UseCaseType.DYNAMIC_CONTENT, UseCaseType.RELIABILITY_CRITICAL],
        performance_score=7.0,
        reliability_score=9.0,
        ease_of_use_score=7.0,
        resource_usage="high",
        javascript_support=True,
        async_support=True,
        installation_complexity="medium",
        recommended_fallbacks=[CrawlerToolType.HTTPX_BEAUTIFULSOUP, CrawlerToolType.HTTPX]
    )
}

# ================================
# 라우터 설정
# ================================

router = APIRouter(prefix="/api/crawler-tools", tags=["crawler-tools"])

# ================================
# API 엔드포인트들
# ================================

@router.get("/", response_model=Dict[str, Any])
async def get_all_tools():
    """모든 크롤링 도구 사양 조회"""
    try:
        tools_data = {}
        for tool_type, spec in CRAWLER_TOOLS_SPECS.items():
            tools_data[tool_type.value] = spec.dict()
        
        return {
            "success": True,
            "data": tools_data,
            "system_info": {
                "total_tools": len(CRAWLER_TOOLS_SPECS),
                "system_type": "3단계 간소화 시스템",
                "available_stages": ["httpx", "httpx_beautifulsoup", "playwright"]
            }
        }
    except Exception as e:
        logger.error(f"도구 목록 조회 실패: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/recommend", response_model=Dict[str, Any])
async def recommend_tool(
    url: str = Query(..., description="대상 URL"),
    use_case: Optional[UseCaseType] = Query(None, description="사용 사례"),
    priority: str = Query("balanced", description="우선순위: speed, reliability, balanced")
):
    """URL과 사용 사례에 따른 도구 추천"""
    try:
        # URL 분석
        url_analysis = _analyze_url(url)
        
        # 도구 추천 로직
        recommended_tool = _get_recommended_tool(url_analysis, use_case, priority)
        
        # 폴백 체인 생성
        fallback_chain = _create_fallback_chain(recommended_tool)
        
        return {
            "success": True,
            "data": {
                "primary_recommendation": recommended_tool.value,
                "fallback_chain": [tool.value for tool in fallback_chain],
                "url_analysis": url_analysis,
                "reasoning": _get_recommendation_reasoning(recommended_tool, url_analysis)
            }
        }
    except Exception as e:
        logger.error(f"도구 추천 실패: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/performance", response_model=Dict[str, Any])
async def get_performance_comparison():
    """도구별 성능 비교 데이터"""
    try:
        performance_data = {}
        
        for tool_type, spec in CRAWLER_TOOLS_SPECS.items():
            performance_data[tool_type.value] = {
                "performance_score": spec.performance_score,
                "reliability_score": spec.reliability_score,
                "ease_of_use_score": spec.ease_of_use_score,
                "resource_usage": spec.resource_usage,
                "async_support": spec.async_support,
                "javascript_support": spec.javascript_support,
                "overall_score": (spec.performance_score + spec.reliability_score + spec.ease_of_use_score) / 3
            }
        
        return {
            "success": True,
            "data": {
                "tools": performance_data,
                "recommendations": {
                    "fastest": "httpx",
                    "most_reliable": "playwright", 
                    "most_versatile": "httpx_beautifulsoup",
                    "least_resources": "httpx"
                }
            }
        }
    except Exception as e:
        logger.error(f"성능 비교 데이터 조회 실패: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# ================================
# 내부 헬퍼 함수들
# ================================

def _analyze_url(url: str) -> Dict[str, Any]:
    """URL 분석"""
    url_lower = url.lower()
    
    analysis = {
        "is_api": any(keyword in url_lower for keyword in ['api', '.json', '/rest/', '/graphql']),
        "is_dynamic": any(keyword in url_lower for keyword in ['spa', 'app', 'react', 'vue', 'angular']),
        "requires_js": False,  # 기본값, 나중에 AI가 판단
        "complexity_level": "low"
    }
    
    # 복잡도 판단
    if analysis["is_api"]:
        analysis["complexity_level"] = "low"
    elif analysis["is_dynamic"]:
        analysis["complexity_level"] = "high"
    else:
        analysis["complexity_level"] = "medium"
    
    return analysis

def _get_recommended_tool(url_analysis: Dict[str, Any], use_case: Optional[UseCaseType], priority: str) -> CrawlerToolType:
    """추천 도구 결정"""
    
    # API 요청인 경우
    if url_analysis["is_api"]:
        return CrawlerToolType.HTTPX
    
    # 동적 콘텐츠인 경우
    if url_analysis["is_dynamic"] or url_analysis.get("requires_js", False):
        return CrawlerToolType.PLAYWRIGHT
    
    # 사용 사례 기반 판단
    if use_case:
        if use_case == UseCaseType.SPEED_CRITICAL:
            return CrawlerToolType.HTTPX
        elif use_case == UseCaseType.DYNAMIC_CONTENT:
            return CrawlerToolType.PLAYWRIGHT
        elif use_case == UseCaseType.STATIC_CONTENT:
            return CrawlerToolType.HTTPX_BEAUTIFULSOUP
    
    # 우선순위 기반 판단
    if priority == "speed":
        return CrawlerToolType.HTTPX
    elif priority == "reliability":
        return CrawlerToolType.PLAYWRIGHT
    else:  # balanced
        return CrawlerToolType.HTTPX_BEAUTIFULSOUP

def _create_fallback_chain(primary_tool: CrawlerToolType) -> List[CrawlerToolType]:
    """폴백 체인 생성"""
    spec = CRAWLER_TOOLS_SPECS[primary_tool]
    fallback_chain = [primary_tool] + spec.recommended_fallbacks
    return fallback_chain

def _get_recommendation_reasoning(tool: CrawlerToolType, analysis: Dict[str, Any]) -> str:
    """추천 사유 설명"""
    if tool == CrawlerToolType.HTTPX:
        if analysis["is_api"]:
            return "API 엔드포인트이므로 빠른 HTTPX가 최적입니다."
        else:
            return "단순한 요청이므로 빠르고 효율적인 HTTPX를 권장합니다."
    elif tool == CrawlerToolType.HTTPX_BEAUTIFULSOUP:
        return "HTML 파싱이 필요하지만 JavaScript는 불요하므로 HTTPX + BeautifulSoup이 적합합니다."
    elif tool == CrawlerToolType.PLAYWRIGHT:
        return "동적 콘텐츠 또는 JavaScript 처리가 필요하므로 Playwright가 필요합니다."
    
    return "균형잡힌 접근을 위해 선택되었습니다."

# ================================
# 시스템 정보
# ================================

@router.get("/system-info")
async def get_system_info():
    """3단계 시스템 정보"""
    return {
        "system_version": "2.0.0",
        "system_type": "3단계 간소화 시스템",
        "available_tools": [tool.value for tool in CrawlerToolType],
        "total_tools": len(CrawlerToolType),
        "removed_tools": ["selenium", "scrapy", "requests_beautifulsoup", "mechanicalsoup"],
        "optimization_focus": ["speed", "memory_efficiency", "maintainability"]
    }