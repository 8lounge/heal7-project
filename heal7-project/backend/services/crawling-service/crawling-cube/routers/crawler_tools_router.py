#!/usr/bin/env python3
"""
🔧 크롤링 도구 선택 및 추천 시스템
목적에 맞는 크롤링 도구 조합 추천 및 폴백 시스템

Created: 2025-09-01
Author: HEAL7 Development Team
"""

import logging
from typing import Dict, List, Optional, Any
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from enum import Enum
import json

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# API 라우터 생성
router = APIRouter(prefix="/api/crawler-tools", tags=["crawler-tools"])

# ================================
# 데이터 모델들
# ================================

class CrawlerToolType(str, Enum):
    HTTPX = "httpx"
    PLAYWRIGHT = "playwright"
    SELENIUM = "selenium"
    HTTPX_BEAUTIFULSOUP = "httpx_beautifulsoup"
    REQUESTS_BEAUTIFULSOUP = "requests_beautifulsoup"
    SCRAPY = "scrapy"
    HTTPX_LXML = "httpx_lxml"
    AIOHTTP_BEAUTIFULSOUP = "aiohttp_beautifulsoup"
    MECHANICALSOUP = "mechanicalsoup"

class UseCaseType(str, Enum):
    STATIC_CONTENT = "static_content"      # 정적 콘텐츠
    DYNAMIC_CONTENT = "dynamic_content"    # 동적 콘텐츠 (JS)
    LARGE_SCALE = "large_scale"           # 대용량 스크래핑
    FORM_INTERACTION = "form_interaction" # 폼 상호작용
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

class ToolRecommendation(BaseModel):
    """도구 추천 결과"""
    primary_tool: CrawlerToolType
    confidence_score: float = Field(ge=0, le=100)
    reasoning: str
    fallback_tools: List[CrawlerToolType] = []
    setup_steps: List[str] = []
    estimated_performance: Dict[str, Any] = {}

class CrawlingRequest(BaseModel):
    """크롤링 요청 사양"""
    target_urls: List[str] = []
    expected_data_types: List[str] = []  # text, images, tables, forms
    javascript_required: bool = False
    form_interaction_required: bool = False
    expected_volume: str = Field(default="small", description="small/medium/large")
    priority: str = Field(default="balanced", description="speed/reliability/balanced")
    budget_constraint: str = Field(default="medium", description="low/medium/high")

# ================================
# 크롤링 도구 사양 데이터
# ================================

CRAWLER_TOOLS_SPECS: Dict[CrawlerToolType, CrawlerToolSpec] = {
    CrawlerToolType.HTTPX: CrawlerToolSpec(
        tool_type=CrawlerToolType.HTTPX,
        display_name="HTTPX",
        description="현대적이고 빠른 HTTP 클라이언트",
        strengths=[
            "⚡ 매우 빠른 성능",
            "🔄 HTTP/2 지원",
            "⚙️ 비동기 처리",
            "🎯 API 스크래핑에 최적화",
            "📦 가벼운 리소스 사용"
        ],
        weaknesses=[
            "❌ JavaScript 미지원",
            "❌ 동적 콘텐츠 처리 불가",
            "❌ 복잡한 인증 처리 어려움"
        ],
        best_use_cases=[UseCaseType.API_SCRAPING, UseCaseType.SPEED_CRITICAL, UseCaseType.STATIC_CONTENT],
        performance_score=9.5,
        reliability_score=8.5,
        ease_of_use_score=8.0,
        resource_usage="low",
        javascript_support=False,
        async_support=True,
        installation_complexity="easy",
        recommended_fallbacks=[CrawlerToolType.HTTPX_BEAUTIFULSOUP, CrawlerToolType.REQUESTS_BEAUTIFULSOUP]
    ),
    
    CrawlerToolType.PLAYWRIGHT: CrawlerToolSpec(
        tool_type=CrawlerToolType.PLAYWRIGHT,
        display_name="Playwright",
        description="현대적인 브라우저 자동화 도구",
        strengths=[
            "🌟 완벽한 JavaScript 지원",
            "🎭 멀티 브라우저 지원",
            "📱 모바일 시뮬레이션",
            "🔍 네트워크 인터셉션",
            "⚡ 상대적으로 빠른 실행"
        ],
        weaknesses=[
            "💾 높은 메모리 사용량",
            "🐛 간헐적 안정성 이슈",
            "🔧 복잡한 디버깅",
            "💰 높은 리소스 비용"
        ],
        best_use_cases=[UseCaseType.DYNAMIC_CONTENT, UseCaseType.FORM_INTERACTION],
        performance_score=8.0,
        reliability_score=7.0,
        ease_of_use_score=7.5,
        resource_usage="high",
        javascript_support=True,
        async_support=True,
        installation_complexity="medium",
        recommended_fallbacks=[CrawlerToolType.SELENIUM, CrawlerToolType.HTTPX_BEAUTIFULSOUP]
    ),
    
    CrawlerToolType.SELENIUM: CrawlerToolSpec(
        tool_type=CrawlerToolType.SELENIUM,
        display_name="Selenium",
        description="검증된 전통적인 브라우저 자동화",
        strengths=[
            "🛡️ 높은 호환성",
            "📚 풍부한 문서화",
            "🏢 엔터프라이즈 검증됨",
            "🔧 안정적인 동작",
            "👥 대규모 커뮤니티"
        ],
        weaknesses=[
            "🐌 상대적으로 느림",
            "📊 높은 리소스 사용",
            "⚙️ 복잡한 설정",
            "🔄 느린 업데이트"
        ],
        best_use_cases=[UseCaseType.RELIABILITY_CRITICAL, UseCaseType.FORM_INTERACTION],
        performance_score=6.0,
        reliability_score=9.0,
        ease_of_use_score=6.0,
        resource_usage="high",
        javascript_support=True,
        async_support=False,
        installation_complexity="medium",
        recommended_fallbacks=[CrawlerToolType.PLAYWRIGHT, CrawlerToolType.HTTPX_BEAUTIFULSOUP]
    ),
    
    CrawlerToolType.HTTPX_BEAUTIFULSOUP: CrawlerToolSpec(
        tool_type=CrawlerToolType.HTTPX_BEAUTIFULSOUP,
        display_name="HTTPX + BeautifulSoup",
        description="빠르고 효율적인 정적 스크래핑 조합",
        strengths=[
            "⚡ 매우 빠른 처리속도",
            "🎯 정확한 HTML 파싱",
            "💡 직관적인 사용법",
            "💰 저비용 리소스",
            "🔄 비동기 처리"
        ],
        weaknesses=[
            "❌ JavaScript 미지원",
            "❌ 동적 콘텐츠 불가",
            "❌ 복잡한 인증 어려움"
        ],
        best_use_cases=[UseCaseType.STATIC_CONTENT, UseCaseType.SPEED_CRITICAL, UseCaseType.LARGE_SCALE],
        performance_score=9.0,
        reliability_score=8.5,
        ease_of_use_score=9.0,
        resource_usage="low",
        javascript_support=False,
        async_support=True,
        installation_complexity="easy",
        recommended_fallbacks=[CrawlerToolType.HTTPX, CrawlerToolType.PLAYWRIGHT]
    ),
    
    CrawlerToolType.REQUESTS_BEAUTIFULSOUP: CrawlerToolSpec(
        tool_type=CrawlerToolType.REQUESTS_BEAUTIFULSOUP,
        display_name="Requests + BeautifulSoup",
        description="가장 전통적이고 안정적인 조합",
        strengths=[
            "🛡️ 최고의 안정성",
            "📚 방대한 레퍼런스",
            "🎯 예측 가능한 동작",
            "💡 학습 용이",
            "🔧 간단한 디버깅"
        ],
        weaknesses=[
            "❌ 비동기 미지원",
            "🐌 상대적 저성능",
            "❌ HTTP/2 미지원"
        ],
        best_use_cases=[UseCaseType.RELIABILITY_CRITICAL, UseCaseType.STATIC_CONTENT],
        performance_score=7.0,
        reliability_score=9.5,
        ease_of_use_score=9.5,
        resource_usage="low",
        javascript_support=False,
        async_support=False,
        installation_complexity="easy",
        recommended_fallbacks=[CrawlerToolType.HTTPX_BEAUTIFULSOUP, CrawlerToolType.SELENIUM]
    ),
    
    CrawlerToolType.SCRAPY: CrawlerToolSpec(
        tool_type=CrawlerToolType.SCRAPY,
        display_name="Scrapy",
        description="대용량 스크래핑 전용 프레임워크",
        strengths=[
            "🏭 대용량 처리 특화",
            "⚙️ 강력한 미들웨어",
            "🔄 자동 재시도",
            "📊 내장 통계",
            "🕷️ 분산 스크래핑"
        ],
        weaknesses=[
            "📈 높은 학습 곡선",
            "❌ JavaScript 미지원",
            "🔧 복잡한 설정",
            "💾 오버헤드"
        ],
        best_use_cases=[UseCaseType.LARGE_SCALE, UseCaseType.STATIC_CONTENT],
        performance_score=8.5,
        reliability_score=8.0,
        ease_of_use_score=5.0,
        resource_usage="medium",
        javascript_support=False,
        async_support=True,
        installation_complexity="hard",
        recommended_fallbacks=[CrawlerToolType.HTTPX_BEAUTIFULSOUP, CrawlerToolType.AIOHTTP_BEAUTIFULSOUP]
    ),
    
    CrawlerToolType.HTTPX_LXML: CrawlerToolSpec(
        tool_type=CrawlerToolType.HTTPX_LXML,
        display_name="HTTPX + lxml",
        description="초고성능 XML/HTML 파싱 조합",
        strengths=[
            "🚀 최고 파싱 성능",
            "💡 메모리 효율적",
            "🎯 XPath 지원",
            "⚡ C 기반 라이브러리"
        ],
        weaknesses=[
            "🔧 설치 복잡성",
            "📚 상대적 학습 곡선",
            "❌ JavaScript 미지원"
        ],
        best_use_cases=[UseCaseType.LARGE_SCALE, UseCaseType.SPEED_CRITICAL],
        performance_score=9.5,
        reliability_score=8.0,
        ease_of_use_score=6.0,
        resource_usage="low",
        javascript_support=False,
        async_support=True,
        installation_complexity="hard",
        recommended_fallbacks=[CrawlerToolType.HTTPX_BEAUTIFULSOUP, CrawlerToolType.SCRAPY]
    ),
    
    CrawlerToolType.AIOHTTP_BEAUTIFULSOUP: CrawlerToolSpec(
        tool_type=CrawlerToolType.AIOHTTP_BEAUTIFULSOUP,
        display_name="aiohttp + BeautifulSoup",
        description="비동기 HTTP 클라이언트 조합",
        strengths=[
            "⚡ 비동기 고성능",
            "🔄 동시 처리",
            "💰 효율적 리소스",
            "📊 서버 사이드 최적화"
        ],
        weaknesses=[
            "📈 비동기 복잡성",
            "❌ JavaScript 미지원",
            "🔧 디버깅 어려움"
        ],
        best_use_cases=[UseCaseType.LARGE_SCALE, UseCaseType.SPEED_CRITICAL],
        performance_score=8.5,
        reliability_score=7.5,
        ease_of_use_score=6.5,
        resource_usage="medium",
        javascript_support=False,
        async_support=True,
        installation_complexity="medium",
        recommended_fallbacks=[CrawlerToolType.HTTPX_BEAUTIFULSOUP, CrawlerToolType.SCRAPY]
    ),
    
    CrawlerToolType.MECHANICALSOUP: CrawlerToolSpec(
        tool_type=CrawlerToolType.MECHANICALSOUP,
        display_name="MechanicalSoup",
        description="브라우저 시뮬레이션이 가능한 편리한 도구",
        strengths=[
            "🎭 브라우저 시뮬레이션",
            "📝 폼 처리 편의",
            "💡 간단한 사용법",
            "🔧 쿠키/세션 자동"
        ],
        weaknesses=[
            "❌ JavaScript 미지원",
            "🐌 상대적 저성능",
            "❌ 제한적 기능"
        ],
        best_use_cases=[UseCaseType.FORM_INTERACTION, UseCaseType.STATIC_CONTENT],
        performance_score=6.5,
        reliability_score=8.0,
        ease_of_use_score=8.5,
        resource_usage="low",
        javascript_support=False,
        async_support=False,
        installation_complexity="easy",
        recommended_fallbacks=[CrawlerToolType.REQUESTS_BEAUTIFULSOUP, CrawlerToolType.SELENIUM]
    )
}

# ================================
# 추천 시스템 로직
# ================================

def calculate_tool_score(tool_spec: CrawlerToolSpec, request: CrawlingRequest) -> float:
    """요청 사양에 따른 도구 점수 계산"""
    score = 0.0
    max_score = 100.0
    
    # JavaScript 요구사항 확인 (30점)
    if request.javascript_required:
        if tool_spec.javascript_support:
            score += 30
        else:
            return 0  # JavaScript 필수인 경우 미지원 도구는 제외
    else:
        score += 20  # JavaScript 불필요시 보너스
    
    # 폼 상호작용 요구사항 (20점)
    if request.form_interaction_required:
        if UseCaseType.FORM_INTERACTION in tool_spec.best_use_cases:
            score += 20
        else:
            score += 5  # 부분적 지원
    else:
        score += 10
    
    # 볼륨에 따른 점수 (25점)
    volume_scores = {
        "small": {"performance": 0.3, "reliability": 0.7},
        "medium": {"performance": 0.5, "reliability": 0.5},
        "large": {"performance": 0.7, "reliability": 0.3}
    }
    volume_weight = volume_scores.get(request.expected_volume, volume_scores["medium"])
    volume_score = (tool_spec.performance_score * volume_weight["performance"] + 
                   tool_spec.reliability_score * volume_weight["reliability"]) * 2.5
    score += volume_score
    
    # 우선순위에 따른 점수 (15점)
    priority_weights = {
        "speed": {"performance": 0.8, "reliability": 0.2},
        "reliability": {"performance": 0.2, "reliability": 0.8},
        "balanced": {"performance": 0.5, "reliability": 0.5}
    }
    priority_weight = priority_weights.get(request.priority, priority_weights["balanced"])
    priority_score = (tool_spec.performance_score * priority_weight["performance"] + 
                     tool_spec.reliability_score * priority_weight["reliability"]) * 1.5
    score += priority_score
    
    # 예산 제약에 따른 점수 (10점)
    resource_scores = {"low": 10, "medium": 7, "high": 3}
    budget_penalty = {"low": 0, "medium": 3, "high": 7}
    
    if tool_spec.resource_usage == "low":
        score += resource_scores.get(request.budget_constraint, 7)
    elif tool_spec.resource_usage == "medium":
        score += max(0, 7 - budget_penalty.get(request.budget_constraint, 3))
    else:  # high
        score += max(0, 3 - budget_penalty.get(request.budget_constraint, 7))
    
    return min(score, max_score)

def get_reasoning(tool_spec: CrawlerToolSpec, request: CrawlingRequest, score: float) -> str:
    """추천 이유 생성"""
    reasons = []
    
    if request.javascript_required and tool_spec.javascript_support:
        reasons.append("JavaScript 처리 능력")
    elif not request.javascript_required and not tool_spec.javascript_support:
        reasons.append("빠른 정적 콘텐츠 처리")
    
    if request.expected_volume == "large" and tool_spec.performance_score >= 8:
        reasons.append("대용량 처리 성능")
    
    if request.priority == "speed" and tool_spec.performance_score >= 8:
        reasons.append("우수한 처리 속도")
    elif request.priority == "reliability" and tool_spec.reliability_score >= 8:
        reasons.append("높은 안정성")
    
    if tool_spec.resource_usage == "low":
        reasons.append("효율적인 리소스 사용")
    
    reasoning = f"{tool_spec.display_name}은(는) {', '.join(reasons)}으로 이 작업에 적합합니다."
    reasoning += f" 종합 적합도: {score:.1f}%"
    
    return reasoning

# ================================
# API 엔드포인트들
# ================================

@router.get("/available-tools")
async def get_available_tools():
    """🔧 사용 가능한 크롤링 도구 목록 조회"""
    try:
        logger.info("[API] 크롤링 도구 목록 요청 처리 중...")
        
        tools_data = []
        for tool_type, spec in CRAWLER_TOOLS_SPECS.items():
            tool_info = spec.dict()
            tool_info["radial_data"] = {
                "performance": spec.performance_score,
                "reliability": spec.reliability_score,
                "ease_of_use": spec.ease_of_use_score,
                "resource_efficiency": 10 - (2 if spec.resource_usage == "high" else 1 if spec.resource_usage == "medium" else 0)
            }
            tools_data.append(tool_info)
        
        logger.info(f"[API] 크롤링 도구 목록 반환 - {len(tools_data)}개 도구")
        return {
            "tools": tools_data,
            "total_count": len(tools_data),
            "categories": {
                "browser_automation": ["playwright", "selenium"],
                "http_clients": ["httpx", "httpx_beautifulsoup", "requests_beautifulsoup", "aiohttp_beautifulsoup"],
                "frameworks": ["scrapy"],
                "specialized": ["httpx_lxml", "mechanicalsoup"]
            }
        }
        
    except Exception as e:
        logger.error(f"[API] 크롤링 도구 목록 조회 실패: {str(e)}")
        raise HTTPException(status_code=500, detail=f"도구 목록 조회 실패: {str(e)}")

@router.post("/recommend")
async def recommend_tools(request: CrawlingRequest) -> Dict[str, Any]:
    """🎯 크롤링 요구사항에 맞는 도구 추천"""
    try:
        logger.info(f"[API] 도구 추천 요청 처리 중... Volume: {request.expected_volume}, JS필요: {request.javascript_required}")
        
        recommendations = []
        
        for tool_type, tool_spec in CRAWLER_TOOLS_SPECS.items():
            score = calculate_tool_score(tool_spec, request)
            if score > 30:  # 최소 적합도 30% 이상
                reasoning = get_reasoning(tool_spec, request, score)
                
                recommendation = ToolRecommendation(
                    primary_tool=tool_type,
                    confidence_score=score,
                    reasoning=reasoning,
                    fallback_tools=tool_spec.recommended_fallbacks[:2],  # 상위 2개 폴백
                    setup_steps=generate_setup_steps(tool_spec),
                    estimated_performance=estimate_performance(tool_spec, request)
                )
                recommendations.append(recommendation)
        
        # 점수 순으로 정렬
        recommendations.sort(key=lambda x: x.confidence_score, reverse=True)
        
        logger.info(f"[API] 도구 추천 완료 - {len(recommendations)}개 추천")
        return {
            "recommendations": [r.dict() for r in recommendations[:5]],  # 상위 5개
            "request_summary": {
                "javascript_required": request.javascript_required,
                "volume": request.expected_volume,
                "priority": request.priority,
                "target_count": len(request.target_urls)
            }
        }
        
    except Exception as e:
        logger.error(f"[API] 도구 추천 실패: {str(e)}")
        raise HTTPException(status_code=500, detail=f"도구 추천 실패: {str(e)}")

def generate_setup_steps(tool_spec: CrawlerToolSpec) -> List[str]:
    """도구별 설정 단계 생성"""
    base_steps = ["가상환경 생성", "의존성 설치"]
    
    if tool_spec.tool_type == CrawlerToolType.PLAYWRIGHT:
        return base_steps + ["playwright install", "브라우저 다운로드", "헤드리스 모드 설정"]
    elif tool_spec.tool_type == CrawlerToolType.SELENIUM:
        return base_steps + ["WebDriver 설치", "브라우저 설정", "드라이버 경로 설정"]
    elif tool_spec.tool_type == CrawlerToolType.SCRAPY:
        return base_steps + ["Scrapy 프로젝트 생성", "Spider 생성", "설정 파일 구성"]
    else:
        return base_steps + ["라이브러리 import", "기본 설정 완료"]

def estimate_performance(tool_spec: CrawlerToolSpec, request: CrawlingRequest) -> Dict[str, Any]:
    """성능 추정"""
    base_speed = tool_spec.performance_score * 10  # requests/minute
    
    if request.expected_volume == "large":
        base_speed *= 0.7
    elif request.expected_volume == "small":
        base_speed *= 1.3
    
    return {
        "estimated_speed_rpm": int(base_speed),
        "estimated_reliability": f"{tool_spec.reliability_score * 10:.0f}%",
        "resource_usage": tool_spec.resource_usage,
        "maintenance_level": "low" if tool_spec.ease_of_use_score >= 8 else "medium" if tool_spec.ease_of_use_score >= 6 else "high"
    }

@router.get("/use-cases")
async def get_use_cases():
    """📋 사용 사례별 도구 매트릭스 조회"""
    try:
        logger.info("[API] 사용 사례 매트릭스 요청 처리 중...")
        
        use_case_matrix = {}
        for use_case in UseCaseType:
            suitable_tools = []
            for tool_type, tool_spec in CRAWLER_TOOLS_SPECS.items():
                if use_case in tool_spec.best_use_cases:
                    suitable_tools.append({
                        "tool": tool_type.value,
                        "display_name": tool_spec.display_name,
                        "suitability_score": tool_spec.performance_score if use_case == UseCaseType.SPEED_CRITICAL else tool_spec.reliability_score
                    })
            
            # 적합도 점수순 정렬
            suitable_tools.sort(key=lambda x: x["suitability_score"], reverse=True)
            use_case_matrix[use_case.value] = suitable_tools[:3]  # 상위 3개
        
        logger.info(f"[API] 사용 사례 매트릭스 반환 - {len(use_case_matrix)}개 케이스")
        return {
            "use_case_matrix": use_case_matrix,
            "use_case_descriptions": {
                "static_content": "정적 HTML/CSS 콘텐츠 수집",
                "dynamic_content": "JavaScript로 생성되는 동적 콘텐츠",
                "large_scale": "대량 데이터 수집 (1000+ 페이지)",
                "form_interaction": "로그인, 폼 제출 등 상호작용",
                "api_scraping": "API 엔드포인트 기반 데이터 수집",
                "speed_critical": "빠른 처리 속도가 중요한 경우",
                "reliability_critical": "안정성이 최우선인 경우"
            }
        }
        
    except Exception as e:
        logger.error(f"[API] 사용 사례 매트릭스 조회 실패: {str(e)}")
        raise HTTPException(status_code=500, detail=f"사용 사례 매트릭스 조회 실패: {str(e)}")

logger.info("🔧 크롤링 도구 선택 시스템 로드 완료")