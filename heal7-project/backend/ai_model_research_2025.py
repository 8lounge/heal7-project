#!/usr/bin/env python3
"""
HEAL7 AI 모델 상세 연구 및 분석 시스템 (2025)
각 AI 모델의 구체적인 버전, 특징, 강점/약점을 게임 캐릭터처럼 분석
"""

import asyncio
import aiohttp
import json
import os
import time
from datetime import datetime
from typing import Dict, List, Any, Optional
from dotenv import load_dotenv

# 환경변수 로드
load_dotenv('/home/ubuntu/project/backend/api/.env.ai')

class AIModelResearcher:
    """AI 모델 상세 연구 및 분석"""
    
    def __init__(self):
        self.models = {
            # Google Gemini 계열
            "gemini-2.0-flash-exp": {
                "name": "Gemini 2.0 Flash Experimental",
                "provider": "Google",
                "family": "Gemini",
                "generation": 2.0,
                "variant": "Flash",
                "release_date": "2024-12",
                "endpoint": "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-exp:generateContent",
                "api_key": os.getenv("GOOGLE_API_KEY"),
                "is_free": True,
                "cost_per_1k_input": 0.0,
                "cost_per_1k_output": 0.0,
                "context_window": 1000000,  # 1M tokens
                "max_output": 8192,
                "multimodal": True,
                "realtime": False,
                "languages": ["en", "ko", "ja", "zh", "es", "fr", "de", "pt", "ru", "ar"],
                "specialties": ["multimodal", "vision", "code", "creative", "reasoning"],
                "stats": {
                    "reasoning": 9,      # 논리적 추론
                    "creativity": 8,     # 창의성
                    "speed": 10,         # 응답 속도
                    "accuracy": 8,       # 정확성
                    "multimodal": 10,    # 멀티모달 능력
                    "cost": 10,          # 비용 효율성 (무료)
                    "reliability": 7,    # 안정성 (실험 버전)
                    "korean": 8          # 한국어 성능
                },
                "strengths": [
                    "완전 무료 사용 가능",
                    "매우 빠른 응답 속도",
                    "강력한 멀티모달 능력 (텍스트+이미지+비디오)",
                    "100만 토큰 컨텍스트 윈도우",
                    "우수한 코드 생성 능력",
                    "최신 정보 학습 (2024년 말까지)"
                ],
                "weaknesses": [
                    "실험 버전으로 불안정할 수 있음",
                    "실시간 웹 검색 불가",
                    "일부 복잡한 추론에서 오류 가능",
                    "API 사용량 제한 있을 수 있음"
                ],
                "best_for": ["일반 채팅", "코드 생성", "이미지 분석", "창의적 작업", "교육"],
                "avoid_for": ["실시간 정보 검색", "미션 크리티컬한 작업"]
            },
            
            "gemini-1.5-pro": {
                "name": "Gemini 1.5 Pro",
                "provider": "Google",
                "family": "Gemini",
                "generation": 1.5,
                "variant": "Pro",
                "release_date": "2024-02",
                "endpoint": "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-pro:generateContent",
                "api_key": os.getenv("GOOGLE_API_KEY"),
                "is_free": False,
                "cost_per_1k_input": 0.00125,
                "cost_per_1k_output": 0.00375,
                "context_window": 2000000,  # 2M tokens!
                "max_output": 8192,
                "multimodal": True,
                "realtime": False,
                "languages": ["en", "ko", "ja", "zh", "es", "fr", "de", "pt", "ru", "ar"],
                "specialties": ["long-context", "analysis", "reasoning", "multimodal"],
                "stats": {
                    "reasoning": 10,
                    "creativity": 8,
                    "speed": 7,
                    "accuracy": 9,
                    "multimodal": 10,
                    "cost": 8,
                    "reliability": 9,
                    "korean": 8
                },
                "strengths": [
                    "업계 최대 200만 토큰 컨텍스트",
                    "매우 우수한 추론 능력",
                    "안정적인 성능",
                    "강력한 멀티모달 능력",
                    "긴 문서 분석에 최적화"
                ],
                "weaknesses": [
                    "유료 모델",
                    "2.0 Flash보다 느림",
                    "실시간 웹 검색 불가"
                ],
                "best_for": ["긴 문서 분석", "복잡한 추론", "학술 연구", "법률 문서"],
                "avoid_for": ["실시간 정보", "단순 채팅"]
            },

            # OpenAI GPT 계열
            "gpt-4o": {
                "name": "GPT-4o (Omni)",
                "provider": "OpenAI",
                "family": "GPT-4",
                "generation": 4.0,
                "variant": "Omni",
                "release_date": "2024-05",
                "endpoint": "https://api.openai.com/v1/chat/completions",
                "api_key": os.getenv("OPENAI_API_KEY"),
                "is_free": False,
                "cost_per_1k_input": 0.005,
                "cost_per_1k_output": 0.015,
                "context_window": 128000,
                "max_output": 4096,
                "multimodal": True,
                "realtime": False,
                "languages": ["en", "ko", "ja", "zh", "es", "fr", "de", "pt", "ru", "ar"],
                "specialties": ["reasoning", "coding", "writing", "analysis"],
                "stats": {
                    "reasoning": 10,
                    "creativity": 9,
                    "speed": 8,
                    "accuracy": 10,
                    "multimodal": 9,
                    "cost": 6,
                    "reliability": 10,
                    "korean": 9
                },
                "strengths": [
                    "업계 최고 수준의 추론 능력",
                    "매우 높은 정확성",
                    "우수한 코딩 능력",
                    "안정적인 API",
                    "강력한 멀티모달 능력"
                ],
                "weaknesses": [
                    "상대적으로 비싼 비용",
                    "실시간 웹 검색 불가",
                    "컨텍스트 윈도우 제한적"
                ],
                "best_for": ["복잡한 분석", "코딩", "학술 작업", "비즈니스 문서"],
                "avoid_for": ["단순 작업", "실시간 정보"]
            },

            "gpt-4o-mini": {
                "name": "GPT-4o Mini",
                "provider": "OpenAI",
                "family": "GPT-4",
                "generation": 4.0,
                "variant": "Mini",
                "release_date": "2024-07",
                "endpoint": "https://api.openai.com/v1/chat/completions",
                "api_key": os.getenv("OPENAI_API_KEY"),
                "is_free": False,
                "cost_per_1k_input": 0.00015,
                "cost_per_1k_output": 0.0006,
                "context_window": 128000,
                "max_output": 16384,
                "multimodal": True,
                "realtime": False,
                "languages": ["en", "ko", "ja", "zh", "es", "fr", "de", "pt", "ru", "ar"],
                "specialties": ["cost-effective", "general", "fast"],
                "stats": {
                    "reasoning": 8,
                    "creativity": 7,
                    "speed": 9,
                    "accuracy": 8,
                    "multimodal": 8,
                    "cost": 10,       # 매우 저렴
                    "reliability": 9,
                    "korean": 8
                },
                "strengths": [
                    "매우 저렴한 비용 (GPT-4o 대비 1/10)",
                    "빠른 응답 속도",
                    "GPT-4 수준의 기본 성능",
                    "안정적인 API",
                    "대용량 처리에 적합"
                ],
                "weaknesses": [
                    "복잡한 추론에서 GPT-4o보다 약함",
                    "창의성 부분에서 제한적",
                    "실시간 웹 검색 불가"
                ],
                "best_for": ["대용량 처리", "일반 채팅", "기본 코딩", "요약"],
                "avoid_for": ["복잡한 분석", "창의적 작업"]
            },

            "gpt-4-turbo": {
                "name": "GPT-4 Turbo",
                "provider": "OpenAI",
                "family": "GPT-4",
                "generation": 4.0,
                "variant": "Turbo",
                "release_date": "2024-04",
                "endpoint": "https://api.openai.com/v1/chat/completions",
                "api_key": os.getenv("OPENAI_API_KEY"),
                "is_free": False,
                "cost_per_1k_input": 0.01,
                "cost_per_1k_output": 0.03,
                "context_window": 128000,
                "max_output": 4096,
                "multimodal": True,
                "realtime": False,
                "languages": ["en", "ko", "ja", "zh", "es", "fr", "de", "pt", "ru", "ar"],
                "specialties": ["reasoning", "coding", "analysis", "vision"],
                "stats": {
                    "reasoning": 10,
                    "creativity": 9,
                    "speed": 7,
                    "accuracy": 10,
                    "multimodal": 9,
                    "cost": 5,
                    "reliability": 10,
                    "korean": 9
                },
                "strengths": [
                    "최고 수준의 추론 능력",
                    "2024년 4월까지 최신 정보",
                    "강력한 비전 능력",
                    "안정적인 성능"
                ],
                "weaknesses": [
                    "높은 비용",
                    "GPT-4o보다 느림",
                    "실시간 정보 부족"
                ],
                "best_for": ["고급 분석", "복잡한 코딩", "연구", "전문 작업"],
                "avoid_for": ["비용 민감한 작업", "실시간 정보"]
            },

            # Anthropic Claude 계열
            "claude-3.5-sonnet": {
                "name": "Claude 3.5 Sonnet",
                "provider": "Anthropic",
                "family": "Claude 3",
                "generation": 3.5,
                "variant": "Sonnet",
                "release_date": "2024-10",
                "endpoint": "https://api.anthropic.com/v1/messages",
                "api_key": os.getenv("ANTHROPIC_API_KEY"),
                "is_free": False,
                "cost_per_1k_input": 0.003,
                "cost_per_1k_output": 0.015,
                "context_window": 200000,  # 200K tokens
                "max_output": 8192,
                "multimodal": True,
                "realtime": False,
                "languages": ["en", "ko", "ja", "zh", "es", "fr", "de", "pt"],
                "specialties": ["safety", "analysis", "writing", "reasoning"],
                "stats": {
                    "reasoning": 9,
                    "creativity": 10,      # Claude는 창의성이 강함
                    "speed": 6,
                    "accuracy": 9,
                    "multimodal": 8,
                    "cost": 7,
                    "reliability": 10,
                    "korean": 7
                },
                "strengths": [
                    "매우 우수한 창의적 글쓰기",
                    "강력한 안전성 및 윤리적 추론",
                    "긴 컨텍스트 처리 능력",
                    "정확하고 신중한 응답",
                    "코드 분석 및 리뷰 우수"
                ],
                "weaknesses": [
                    "상대적으로 느린 응답",
                    "한국어 성능 제한적",
                    "때로 과도하게 신중함",
                    "실시간 웹 검색 불가"
                ],
                "best_for": ["창의적 글쓰기", "코드 리뷰", "윤리적 분석", "안전한 AI"],
                "avoid_for": ["빠른 응답 필요", "실시간 정보"]
            },

            "claude-3-opus": {
                "name": "Claude 3 Opus",
                "provider": "Anthropic",
                "family": "Claude 3",
                "generation": 3.0,
                "variant": "Opus",
                "release_date": "2024-03",
                "endpoint": "https://api.anthropic.com/v1/messages",
                "api_key": os.getenv("ANTHROPIC_API_KEY"),
                "is_free": False,
                "cost_per_1k_input": 0.015,
                "cost_per_1k_output": 0.075,
                "context_window": 200000,
                "max_output": 4096,
                "multimodal": True,
                "realtime": False,
                "languages": ["en", "ko", "ja", "zh", "es", "fr", "de", "pt"],
                "specialties": ["reasoning", "analysis", "research", "complex-tasks"],
                "stats": {
                    "reasoning": 10,
                    "creativity": 10,
                    "speed": 5,
                    "accuracy": 10,
                    "multimodal": 8,
                    "cost": 3,        # 매우 비쌈
                    "reliability": 10,
                    "korean": 7
                },
                "strengths": [
                    "최고 수준의 추론 능력",
                    "탁월한 창의성",
                    "복잡한 문제 해결",
                    "높은 정확성"
                ],
                "weaknesses": [
                    "매우 높은 비용",
                    "매우 느린 응답",
                    "한국어 제한적"
                ],
                "best_for": ["최고 품질 필요", "복잡한 연구", "중요한 분석"],
                "avoid_for": ["일반 작업", "비용 민감", "빠른 응답"]
            },

            # Perplexity 계열
            "perplexity-sonar": {
                "name": "Perplexity Sonar",
                "provider": "Perplexity AI",
                "family": "Sonar",
                "generation": 1.0,
                "variant": "Standard",
                "release_date": "2024-01",
                "endpoint": "https://api.perplexity.ai/chat/completions",
                "api_key": os.getenv("PERPLEXITY_API_KEY"),
                "is_free": False,
                "cost_per_1k_input": 0.005,
                "cost_per_1k_output": 0.005,
                "context_window": 4096,
                "max_output": 4096,
                "multimodal": False,
                "realtime": True,     # 핵심 강점!
                "languages": ["en", "ko", "ja", "zh", "es", "fr", "de"],
                "specialties": ["realtime-search", "research", "current-events", "citations"],
                "stats": {
                    "reasoning": 7,
                    "creativity": 6,
                    "speed": 6,
                    "accuracy": 8,
                    "multimodal": 3,      # 텍스트만
                    "cost": 7,
                    "reliability": 8,
                    "korean": 6,
                    "realtime": 10        # 실시간 정보 능력
                },
                "strengths": [
                    "실시간 웹 검색 능력",
                    "최신 정보 제공",
                    "신뢰할 수 있는 출처 인용",
                    "사실 확인 우수",
                    "뉴스 및 트렌드 분석"
                ],
                "weaknesses": [
                    "제한적인 컨텍스트 윈도우",
                    "멀티모달 지원 없음",
                    "창의적 작업에 약함",
                    "한국어 성능 제한적"
                ],
                "best_for": ["실시간 정보", "뉴스 분석", "팩트 체크", "연구", "트렌드"],
                "avoid_for": ["창의적 작업", "긴 문서", "멀티모달"]
            },

            # 미래 추가 예정 모델들
            "claude-4": {
                "name": "Claude 4 (예정)",
                "provider": "Anthropic",
                "family": "Claude 4",
                "generation": 4.0,
                "variant": "Standard",
                "release_date": "2025-H1",
                "is_available": False,
                "expected_improvements": [
                    "더 빠른 응답 속도",
                    "향상된 멀티모달 능력",
                    "더 긴 컨텍스트 윈도우",
                    "비용 효율성 개선"
                ]
            },

            "gpt-5": {
                "name": "GPT-5 (예정)",
                "provider": "OpenAI",
                "family": "GPT-5",
                "generation": 5.0,
                "release_date": "2025-H2",
                "is_available": False,
                "expected_improvements": [
                    "AGI 수준의 추론",
                    "멀티모달 통합",
                    "실시간 학습 능력",
                    "에이전트 기능"
                ]
            },

            "gemini-3.0": {
                "name": "Gemini 3.0 (예정)",
                "provider": "Google",
                "family": "Gemini",
                "generation": 3.0,
                "release_date": "2025-H2",
                "is_available": False,
                "expected_improvements": [
                    "더 강력한 추론",
                    "실시간 웹 검색 통합",
                    "향상된 멀티모달",
                    "에이전트 능력"
                ]
            }
        }
        
        self.research_results = {}
    
    async def test_model_performance(self, model_id: str, test_prompts: List[str]) -> Dict[str, Any]:
        """모델 성능 테스트"""
        if model_id not in self.models or not self.models[model_id].get("is_available", True):
            return {"error": "모델을 사용할 수 없습니다"}
        
        model = self.models[model_id]
        results = []
        
        for prompt in test_prompts:
            try:
                start_time = time.time()
                
                if "gemini" in model_id:
                    response = await self._test_gemini(model, prompt)
                elif "gpt" in model_id:
                    response = await self._test_openai(model, prompt)
                elif "claude" in model_id:
                    response = await self._test_claude(model, prompt)
                elif "perplexity" in model_id:
                    response = await self._test_perplexity(model, prompt)
                else:
                    continue
                    
                elapsed_time = time.time() - start_time
                
                results.append({
                    "prompt": prompt[:50] + "...",
                    "success": response.get("success", False),
                    "response_time": elapsed_time,
                    "response_length": len(response.get("response", "")),
                    "error": response.get("error")
                })
                
            except Exception as e:
                results.append({
                    "prompt": prompt[:50] + "...",
                    "success": False,
                    "error": str(e)
                })
        
        return {
            "model": model_id,
            "total_tests": len(test_prompts),
            "successful_tests": sum(1 for r in results if r["success"]),
            "average_response_time": sum(r.get("response_time", 0) for r in results if r["success"]) / max(1, sum(1 for r in results if r["success"])),
            "results": results
        }
    
    async def _test_gemini(self, model: Dict, prompt: str) -> Dict[str, Any]:
        """Gemini 모델 테스트"""
        api_key = model["api_key"]
        if not api_key:
            return {"success": False, "error": "API 키 없음"}
        
        payload = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {"maxOutputTokens": 100}
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{model['endpoint']}?key={api_key}",
                json=payload,
                timeout=aiohttp.ClientTimeout(total=10)
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    return {
                        "success": True,
                        "response": data["candidates"][0]["content"]["parts"][0]["text"]
                    }
                else:
                    return {"success": False, "error": f"HTTP {response.status}"}
    
    async def _test_openai(self, model: Dict, prompt: str) -> Dict[str, Any]:
        """OpenAI 모델 테스트"""
        api_key = model["api_key"]
        if not api_key:
            return {"success": False, "error": "API 키 없음"}
        
        headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
        payload = {
            "model": model["name"].lower().replace(" ", "-").replace("(", "").replace(")", ""),
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 100
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(
                model["endpoint"],
                headers=headers,
                json=payload,
                timeout=aiohttp.ClientTimeout(total=10)
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    return {
                        "success": True,
                        "response": data["choices"][0]["message"]["content"]
                    }
                else:
                    return {"success": False, "error": f"HTTP {response.status}"}
    
    async def _test_claude(self, model: Dict, prompt: str) -> Dict[str, Any]:
        """Claude 모델 테스트"""
        api_key = model["api_key"]
        if not api_key:
            return {"success": False, "error": "API 키 없음"}
        
        headers = {
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json"
        }
        payload = {
            "model": "claude-3-5-sonnet-20241022",
            "max_tokens": 100,
            "messages": [{"role": "user", "content": prompt}]
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(
                model["endpoint"],
                headers=headers,
                json=payload,
                timeout=aiohttp.ClientTimeout(total=10)
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    return {
                        "success": True,
                        "response": data["content"][0]["text"]
                    }
                else:
                    return {"success": False, "error": f"HTTP {response.status}"}
    
    async def _test_perplexity(self, model: Dict, prompt: str) -> Dict[str, Any]:
        """Perplexity 모델 테스트"""
        api_key = model["api_key"]
        if not api_key:
            return {"success": False, "error": "API 키 없음"}
        
        headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
        payload = {
            "model": "sonar",
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 100
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(
                model["endpoint"],
                headers=headers,
                json=payload,
                timeout=aiohttp.ClientTimeout(total=15)
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    return {
                        "success": True,
                        "response": data["choices"][0]["message"]["content"]
                    }
                else:
                    return {"success": False, "error": f"HTTP {response.status}"}
    
    def generate_model_comparison_chart(self) -> Dict[str, Any]:
        """모델 비교 차트 생성 (게임 캐릭터 스타일)"""
        comparison = {
            "models": {},
            "categories": ["reasoning", "creativity", "speed", "accuracy", "multimodal", "cost", "reliability", "korean"],
            "analysis": {
                "speed_champions": [],
                "cost_efficient": [],
                "reasoning_masters": [],
                "creative_powerhouses": [],
                "multimodal_experts": [],
                "korean_specialists": []
            }
        }
        
        for model_id, model in self.models.items():
            if not model.get("is_available", True):
                continue
                
            stats = model.get("stats", {})
            comparison["models"][model_id] = {
                "name": model["name"],
                "provider": model["provider"],
                "stats": stats,
                "total_score": sum(stats.values()) if stats else 0,
                "strengths": model.get("strengths", []),
                "weaknesses": model.get("weaknesses", []),
                "best_for": model.get("best_for", []),
                "cost_per_1k": model.get("cost_per_1k_input", 0),
                "is_free": model.get("is_free", False)
            }
            
            # 카테고리별 챔피언 분석
            if stats.get("speed", 0) >= 9:
                comparison["analysis"]["speed_champions"].append(model_id)
            if stats.get("cost", 0) >= 9 or model.get("is_free", False):
                comparison["analysis"]["cost_efficient"].append(model_id)
            if stats.get("reasoning", 0) >= 9:
                comparison["analysis"]["reasoning_masters"].append(model_id)
            if stats.get("creativity", 0) >= 9:
                comparison["analysis"]["creative_powerhouses"].append(model_id)
            if stats.get("multimodal", 0) >= 9:
                comparison["analysis"]["multimodal_experts"].append(model_id)
            if stats.get("korean", 0) >= 8:
                comparison["analysis"]["korean_specialists"].append(model_id)
        
        return comparison
    
    def get_model_recommendations(self, use_case: str) -> List[Dict[str, Any]]:
        """사용 사례별 모델 추천"""
        recommendations = {
            "general_chat": ["gemini-2.0-flash-exp", "gpt-4o-mini", "claude-3.5-sonnet"],
            "coding": ["gpt-4o", "claude-3.5-sonnet", "gemini-2.0-flash-exp"],
            "creative_writing": ["claude-3.5-sonnet", "claude-3-opus", "gpt-4o"],
            "research": ["perplexity-sonar", "gpt-4o", "claude-3.5-sonnet"],
            "analysis": ["gpt-4o", "claude-3-opus", "gemini-1.5-pro"],
            "cost_sensitive": ["gemini-2.0-flash-exp", "gpt-4o-mini"],
            "korean": ["gpt-4o", "claude-3.5-sonnet", "gemini-2.0-flash-exp"],
            "realtime_info": ["perplexity-sonar"],
            "multimodal": ["gemini-2.0-flash-exp", "gpt-4o", "gemini-1.5-pro"],
            "long_context": ["gemini-1.5-pro", "claude-3.5-sonnet", "gpt-4o"]
        }
        
        model_list = recommendations.get(use_case, ["gemini-2.0-flash-exp"])
        
        result = []
        for model_id in model_list:
            if model_id in self.models:
                model = self.models[model_id]
                result.append({
                    "model_id": model_id,
                    "name": model["name"],
                    "reason": f"최적화됨: {use_case}",
                    "cost": model.get("cost_per_1k_input", 0),
                    "is_free": model.get("is_free", False),
                    "stats": model.get("stats", {})
                })
        
        return result
    
    async def run_comprehensive_research(self) -> Dict[str, Any]:
        """종합 연구 실행"""
        print("🔬 HEAL7 AI 모델 상세 연구 시작 (2025)")
        print("=" * 60)
        
        # 테스트 프롬프트 준비
        test_prompts = [
            "안녕하세요. 간단한 인사를 해주세요.",
            "1+1은 무엇인가요?",
            "파이썬으로 피보나치 수열을 구현해주세요.",
            "오늘 날씨는 어떤가요?",
            "창의적인 이야기를 짧게 써주세요."
        ]
        
        # 사용 가능한 모델 테스트
        available_models = [mid for mid, model in self.models.items() 
                          if model.get("is_available", True) and model.get("api_key")]
        
        print(f"\n🧪 모델 성능 테스트 ({len(available_models)}개 모델)")
        
        for model_id in available_models:
            print(f"\n테스트 중: {self.models[model_id]['name']}")
            result = await self.test_model_performance(model_id, test_prompts[:2])  # 시간 절약을 위해 2개만
            self.research_results[model_id] = result
            
            if result.get("successful_tests", 0) > 0:
                print(f"  ✅ 성공률: {result['successful_tests']}/{result['total_tests']}")
                print(f"  ⚡ 평균 응답시간: {result['average_response_time']:.2f}초")
            else:
                print(f"  ❌ 테스트 실패")
        
        # 모델 비교 차트 생성
        print(f"\n📊 모델 비교 분석 생성 중...")
        comparison = self.generate_model_comparison_chart()
        
        # 사용 사례별 추천
        print(f"\n💡 사용 사례별 추천 생성 중...")
        use_cases = ["general_chat", "coding", "creative_writing", "research", "cost_sensitive"]
        recommendations = {}
        
        for use_case in use_cases:
            recommendations[use_case] = self.get_model_recommendations(use_case)
        
        # 최종 리포트 생성
        final_report = {
            "timestamp": datetime.now().isoformat(),
            "total_models_analyzed": len(self.models),
            "available_models": len(available_models),
            "performance_tests": self.research_results,
            "model_comparison": comparison,
            "recommendations": recommendations,
            "summary": {
                "speed_champion": max(comparison["models"].items(), 
                                    key=lambda x: x[1]["stats"].get("speed", 0))[0] if comparison["models"] else None,
                "cost_champion": "gemini-2.0-flash-exp",  # 무료이므로
                "reasoning_champion": max(comparison["models"].items(), 
                                        key=lambda x: x[1]["stats"].get("reasoning", 0))[0] if comparison["models"] else None,
                "creative_champion": max(comparison["models"].items(), 
                                       key=lambda x: x[1]["stats"].get("creativity", 0))[0] if comparison["models"] else None
            }
        }
        
        # 결과 출력
        print(f"\n🏆 연구 결과 요약")
        print(f"{'카테고리':<15} {'챔피언':<25} {'점수'}")
        print("-" * 50)
        
        for category in ["speed", "cost", "reasoning", "creativity"]:
            champion = final_report["summary"].get(f"{category}_champion")
            if champion and champion in comparison["models"]:
                score = comparison["models"][champion]["stats"].get(category, 0)
                name = comparison["models"][champion]["name"]
                print(f"{category.upper():<15} {name:<25} {score}/10")
        
        # 파일 저장
        report_path = f"/home/ubuntu/logs/ai_model_research_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        os.makedirs(os.path.dirname(report_path), exist_ok=True)
        
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(final_report, f, ensure_ascii=False, indent=2)
        
        print(f"\n📄 상세 리포트 저장: {report_path}")
        
        return final_report

async def main():
    """메인 함수"""
    researcher = AIModelResearcher()
    await researcher.run_comprehensive_research()

if __name__ == "__main__":
    asyncio.run(main())