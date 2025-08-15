#!/usr/bin/env python3
"""
HEAL7 통합 AI 모델 관리 시스템
모든 서비스(사주, 마케팅, 설문 등)에서 공통으로 사용하는 AI 모델 관리 및 폴백 시스템
"""

import asyncio
import logging
import json
import time
import psutil
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from enum import Enum
import aiohttp
from fastapi import HTTPException

# 로깅 설정
logger = logging.getLogger(__name__)

class AIModelStatus(Enum):
    """AI 모델 상태"""
    ACTIVE = "active"          # 정상 작동
    OFFLINE = "offline"        # 오프라인
    ERROR = "error"            # 오류 상태
    MAINTENANCE = "maintenance" # 자가 점검 중
    QUOTA_EXCEEDED = "quota_exceeded"  # 할당량 초과
    COOLING_DOWN = "cooling_down"      # 쿨다운 (일시적 사용 중지)

@dataclass
class AIModelConfig:
    """AI 모델 설정"""
    name: str
    provider: str
    api_key_env: str
    endpoint: str
    max_tokens_per_minute: int
    max_requests_per_minute: int
    cost_per_1k_tokens: float
    strengths: List[str]
    weaknesses: List[str]
    use_cases: List[str]
    priority: int = 999  # 낮을수록 우선순위 높음
    is_free: bool = False

@dataclass 
class AIModelState:
    """AI 모델 실시간 상태"""
    status: AIModelStatus = AIModelStatus.ACTIVE
    tokens_used_today: int = 0
    requests_today: int = 0
    last_used: Optional[datetime] = None
    last_error: Optional[str] = None
    error_count: int = 0
    success_rate: float = 100.0
    avg_response_time: float = 0.0
    health_check_passed: bool = True

class AIModelManager:
    """통합 AI 모델 관리자"""
    
    def __init__(self):
        # AI 모델 설정 초기화
        self.models = self._initialize_models()
        
        # 모델별 상태 초기화
        self.model_states: Dict[str, AIModelState] = {
            model_name: AIModelState() for model_name in self.models
        }
        
        # 서비스별 폴백 순서 설정
        self.service_fallback_order = {
            "saju": ["gemini", "claude", "gpt-4", "gpt-3.5"],  # 사주: 정확성 중시
            "marketing": ["gemini", "gpt-3.5", "claude"],      # 마케팅: 창의성과 비용 균형
            "survey": ["gemini", "claude", "gpt-3.5"],         # 설문: 분석력 중시
            "research": ["perplexity", "gemini", "gpt-4"],     # 리서치: 최신 정보 중시
            "default": ["gemini", "gpt-3.5", "claude", "gpt-4"] # 기본값: Gemini 우선
        }
        
        # 시스템 리소스 임계값
        self.resource_thresholds = {
            "cpu_critical": 90.0,      # CPU 90% 이상 시 위급
            "cpu_warning": 80.0,       # CPU 80% 이상 시 경고
            "memory_critical": 90.0,   # 메모리 90% 이상 시 위급
            "memory_warning": 80.0     # 메모리 80% 이상 시 경고
        }
        
        # 통계 및 리포트 데이터
        self.usage_stats = {
            "total_requests": 0,
            "total_tokens": 0,
            "total_cost": 0.0,
            "service_usage": {},
            "model_usage": {}
        }
        
        # 백그라운드 작업
        self._monitoring_task = None
        self._health_check_interval = 60  # 60초마다 헬스체크
        
    def _initialize_models(self) -> Dict[str, AIModelConfig]:
        """AI 모델 초기화"""
        return {
            "gemini": AIModelConfig(
                name="Gemini Pro",
                provider="Google",
                api_key_env="GOOGLE_API_KEY",
                endpoint="https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent",
                max_tokens_per_minute=60000,
                max_requests_per_minute=60,
                cost_per_1k_tokens=0.0,  # 무료!
                is_free=True,
                priority=1,  # 최우선순위 (무료이므로)
                strengths=[
                    "무료 사용 가능",
                    "빠른 응답 속도",
                    "한국어 성능 우수",
                    "다양한 작업 처리 가능"
                ],
                weaknesses=[
                    "최신 정보 부족 (2023년 기준)",
                    "이미지 생성 불가",
                    "컨텍스트 길이 제한"
                ],
                use_cases=["general", "saju", "survey", "marketing"]
            ),
            
            "gpt-4": AIModelConfig(
                name="GPT-4",
                provider="OpenAI",
                api_key_env="OPENAI_API_KEY",
                endpoint="https://api.openai.com/v1/chat/completions",
                max_tokens_per_minute=10000,
                max_requests_per_minute=200,
                cost_per_1k_tokens=0.03,  # 입력 기준
                priority=4,
                strengths=[
                    "최고 수준의 추론 능력",
                    "복잡한 작업 처리 우수",
                    "코드 생성 능력 탁월",
                    "긴 컨텍스트 처리 가능"
                ],
                weaknesses=[
                    "높은 비용",
                    "상대적으로 느린 응답",
                    "토큰 제한이 타이트함"
                ],
                use_cases=["complex_analysis", "code_generation", "research"]
            ),
            
            "gpt-3.5": AIModelConfig(
                name="GPT-3.5 Turbo",
                provider="OpenAI",
                api_key_env="OPENAI_API_KEY",
                endpoint="https://api.openai.com/v1/chat/completions",
                max_tokens_per_minute=90000,
                max_requests_per_minute=3500,
                cost_per_1k_tokens=0.002,
                priority=2,
                strengths=[
                    "빠른 응답 속도",
                    "저렴한 비용",
                    "안정적인 성능",
                    "높은 처리량"
                ],
                weaknesses=[
                    "GPT-4 대비 낮은 추론력",
                    "복잡한 작업에서 한계",
                    "최신 정보 부족"
                ],
                use_cases=["general", "marketing", "simple_tasks"]
            ),
            
            "claude": AIModelConfig(
                name="Claude 3 Sonnet",
                provider="Anthropic",
                api_key_env="ANTHROPIC_API_KEY",
                endpoint="https://api.anthropic.com/v1/messages",
                max_tokens_per_minute=20000,
                max_requests_per_minute=1000,
                cost_per_1k_tokens=0.003,
                priority=3,
                strengths=[
                    "윤리적이고 안전한 응답",
                    "긴 문서 처리 능력",
                    "정확한 분석 능력",
                    "한국어 성능 우수"
                ],
                weaknesses=[
                    "실시간 정보 접근 불가",
                    "이미지 생성 불가",
                    "때때로 과도하게 신중함"
                ],
                use_cases=["analysis", "writing", "saju", "survey"]
            ),
            
            "perplexity": AIModelConfig(
                name="Perplexity",
                provider="Perplexity AI",
                api_key_env="PERPLEXITY_API_KEY",
                endpoint="https://api.perplexity.ai/chat/completions",
                max_tokens_per_minute=10000,
                max_requests_per_minute=100,
                cost_per_1k_tokens=0.005,
                priority=5,
                strengths=[
                    "실시간 웹 검색 통합",
                    "최신 정보 제공",
                    "출처 제공",
                    "리서치 작업 특화"
                ],
                weaknesses=[
                    "일반 대화에서는 평범",
                    "창의적 작업 부적합",
                    "한국어 자료 제한적"
                ],
                use_cases=["research", "fact_checking", "news_analysis"]
            ),
            
            "llama": AIModelConfig(
                name="Llama 3",
                provider="Meta/Local",
                api_key_env="",  # 로컬 실행
                endpoint="http://localhost:11434/api/generate",  # Ollama
                max_tokens_per_minute=50000,
                max_requests_per_minute=1000,
                cost_per_1k_tokens=0.0,  # 로컬 실행 무료
                is_free=True,
                priority=6,
                strengths=[
                    "완전 무료 (로컬 실행)",
                    "데이터 프라이버시",
                    "커스터마이징 가능",
                    "오프라인 작동 가능"
                ],
                weaknesses=[
                    "서버 리소스 소비",
                    "상용 모델 대비 낮은 성능",
                    "모델 업데이트 수동 관리"
                ],
                use_cases=["privacy_sensitive", "offline_tasks", "testing"]
            )
        }
    
    async def get_ai_response(
        self,
        prompt: str,
        service: str = "default",
        preferred_model: Optional[str] = None,
        max_retries: int = 3,
        **kwargs
    ) -> Tuple[str, str, Dict[str, Any]]:
        """
        AI 응답 가져오기 (자동 폴백 지원)
        
        Returns:
            (응답 텍스트, 사용된 모델명, 메타데이터)
        """
        # 시스템 리소스 체크
        if not await self._check_system_resources():
            raise HTTPException(
                status_code=503,
                detail="시스템 리소스 부족으로 AI 서비스를 일시적으로 사용할 수 없습니다"
            )
        
        # 폴백 순서 결정
        if preferred_model and preferred_model in self.models:
            fallback_order = [preferred_model] + [
                m for m in self.service_fallback_order.get(service, self.service_fallback_order["default"])
                if m != preferred_model
            ]
        else:
            fallback_order = self.service_fallback_order.get(service, self.service_fallback_order["default"])
        
        last_error = None
        
        # 폴백 순서대로 시도
        for model_name in fallback_order:
            if model_name not in self.models:
                continue
                
            model_config = self.models[model_name]
            model_state = self.model_states[model_name]
            
            # 모델 상태 확인
            if model_state.status not in [AIModelStatus.ACTIVE, AIModelStatus.COOLING_DOWN]:
                logger.warning(f"모델 {model_name} 사용 불가 상태: {model_state.status}")
                continue
            
            # 할당량 확인
            if not self._check_quota(model_name):
                logger.warning(f"모델 {model_name} 할당량 초과")
                continue
            
            try:
                # AI 모델 호출
                start_time = time.time()
                response = await self._call_ai_model(model_name, prompt, **kwargs)
                elapsed_time = time.time() - start_time
                
                # 통계 업데이트
                await self._update_statistics(model_name, service, response, elapsed_time)
                
                # 성공 시 메타데이터 생성
                metadata = {
                    "model": model_name,
                    "provider": model_config.provider,
                    "response_time": elapsed_time,
                    "fallback_index": fallback_order.index(model_name),
                    "timestamp": datetime.now().isoformat()
                }
                
                return response["content"], model_name, metadata
                
            except Exception as e:
                last_error = str(e)
                logger.error(f"모델 {model_name} 호출 실패: {e}")
                await self._handle_model_error(model_name, e)
                
                # 재시도 로직
                if max_retries > 0:
                    await asyncio.sleep(1)  # 짧은 대기
                    continue
        
        # 모든 모델 실패 시
        raise HTTPException(
            status_code=503,
            detail=f"모든 AI 모델 호출 실패. 마지막 오류: {last_error}"
        )
    
    async def _call_ai_model(self, model_name: str, prompt: str, **kwargs) -> Dict[str, Any]:
        """실제 AI 모델 API 호출"""
        model_config = self.models[model_name]
        
        # API 키 확인
        api_key = os.getenv(model_config.api_key_env) if model_config.api_key_env else None
        if model_config.api_key_env and not api_key:
            raise ValueError(f"{model_name} API 키가 설정되지 않았습니다")
        
        # 모델별 요청 포맷팅
        if model_name == "gemini":
            return await self._call_gemini(prompt, api_key, **kwargs)
        elif model_name in ["gpt-4", "gpt-3.5"]:
            return await self._call_openai(model_name, prompt, api_key, **kwargs)
        elif model_name == "claude":
            return await self._call_claude(prompt, api_key, **kwargs)
        elif model_name == "perplexity":
            return await self._call_perplexity(prompt, api_key, **kwargs)
        elif model_name == "llama":
            return await self._call_llama(prompt, **kwargs)
        else:
            raise ValueError(f"지원하지 않는 모델: {model_name}")
    
    async def _call_gemini(self, prompt: str, api_key: str, **kwargs) -> Dict[str, Any]:
        """Gemini API 호출"""
        async with aiohttp.ClientSession() as session:
            url = f"{self.models['gemini'].endpoint}?key={api_key}"
            
            payload = {
                "contents": [{
                    "parts": [{
                        "text": prompt
                    }]
                }],
                "generationConfig": {
                    "temperature": kwargs.get("temperature", 0.7),
                    "maxOutputTokens": kwargs.get("max_tokens", 2048),
                }
            }
            
            async with session.post(url, json=payload) as response:
                if response.status != 200:
                    raise Exception(f"Gemini API 오류: {response.status}")
                
                data = await response.json()
                content = data["candidates"][0]["content"]["parts"][0]["text"]
                
                return {
                    "content": content,
                    "tokens": len(content.split()),  # 대략적인 토큰 수
                    "model": "gemini-pro"
                }
    
    async def _call_openai(self, model_name: str, prompt: str, api_key: str, **kwargs) -> Dict[str, Any]:
        """OpenAI API 호출"""
        async with aiohttp.ClientSession() as session:
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }
            
            model_id = "gpt-4-turbo-preview" if model_name == "gpt-4" else "gpt-3.5-turbo"
            
            payload = {
                "model": model_id,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": kwargs.get("temperature", 0.7),
                "max_tokens": kwargs.get("max_tokens", 2048)
            }
            
            async with session.post(
                self.models[model_name].endpoint,
                headers=headers,
                json=payload
            ) as response:
                if response.status != 200:
                    raise Exception(f"OpenAI API 오류: {response.status}")
                
                data = await response.json()
                
                return {
                    "content": data["choices"][0]["message"]["content"],
                    "tokens": data["usage"]["total_tokens"],
                    "model": model_id
                }
    
    async def _call_claude(self, prompt: str, api_key: str, **kwargs) -> Dict[str, Any]:
        """Claude API 호출"""
        async with aiohttp.ClientSession() as session:
            headers = {
                "x-api-key": api_key,
                "anthropic-version": "2023-06-01",
                "content-type": "application/json"
            }
            
            payload = {
                "model": "claude-3-sonnet-20240229",
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": kwargs.get("max_tokens", 2048),
                "temperature": kwargs.get("temperature", 0.7)
            }
            
            async with session.post(
                self.models["claude"].endpoint,
                headers=headers,
                json=payload
            ) as response:
                if response.status != 200:
                    raise Exception(f"Claude API 오류: {response.status}")
                
                data = await response.json()
                
                return {
                    "content": data["content"][0]["text"],
                    "tokens": data.get("usage", {}).get("total_tokens", 0),
                    "model": "claude-3-sonnet"
                }
    
    async def _call_perplexity(self, prompt: str, api_key: str, **kwargs) -> Dict[str, Any]:
        """Perplexity API 호출 (웹 검색 포함)"""
        async with aiohttp.ClientSession() as session:
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": "pplx-70b-online",  # 온라인 검색 모델
                "messages": [{"role": "user", "content": prompt}],
                "temperature": kwargs.get("temperature", 0.7),
                "max_tokens": kwargs.get("max_tokens", 2048)
            }
            
            async with session.post(
                self.models["perplexity"].endpoint,
                headers=headers,
                json=payload
            ) as response:
                if response.status != 200:
                    raise Exception(f"Perplexity API 오류: {response.status}")
                
                data = await response.json()
                
                return {
                    "content": data["choices"][0]["message"]["content"],
                    "tokens": data.get("usage", {}).get("total_tokens", 0),
                    "model": "pplx-70b-online"
                }
    
    async def _call_llama(self, prompt: str, **kwargs) -> Dict[str, Any]:
        """로컬 Llama 모델 호출 (Ollama 사용)"""
        async with aiohttp.ClientSession() as session:
            payload = {
                "model": "llama3",
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": kwargs.get("temperature", 0.7),
                    "num_predict": kwargs.get("max_tokens", 2048)
                }
            }
            
            try:
                async with session.post(
                    self.models["llama"].endpoint,
                    json=payload,
                    timeout=aiohttp.ClientTimeout(total=30)
                ) as response:
                    if response.status != 200:
                        raise Exception(f"Ollama API 오류: {response.status}")
                    
                    data = await response.json()
                    
                    return {
                        "content": data["response"],
                        "tokens": len(data["response"].split()),
                        "model": "llama3"
                    }
            except aiohttp.ClientError:
                raise Exception("Ollama 서버에 연결할 수 없습니다. 로컬 서버가 실행 중인지 확인하세요.")
    
    def _check_quota(self, model_name: str) -> bool:
        """모델 할당량 확인"""
        model_config = self.models[model_name]
        model_state = self.model_states[model_name]
        
        # 무료 모델은 할당량 체크 완화
        if model_config.is_free:
            return True
        
        # 분당 요청 수 체크
        if model_state.requests_today >= model_config.max_requests_per_minute * 60 * 24:
            model_state.status = AIModelStatus.QUOTA_EXCEEDED
            return False
        
        # 분당 토큰 수 체크
        if model_state.tokens_used_today >= model_config.max_tokens_per_minute * 60 * 24:
            model_state.status = AIModelStatus.QUOTA_EXCEEDED
            return False
        
        return True
    
    async def _check_system_resources(self) -> bool:
        """시스템 리소스 체크"""
        cpu_percent = psutil.cpu_percent(interval=0.1)
        memory_percent = psutil.virtual_memory().percent
        
        # 위급 상황 체크
        if cpu_percent >= self.resource_thresholds["cpu_critical"]:
            logger.critical(f"CPU 사용률 위급: {cpu_percent}%")
            await self._emergency_shutdown()
            return False
        
        if memory_percent >= self.resource_thresholds["memory_critical"]:
            logger.critical(f"메모리 사용률 위급: {memory_percent}%")
            await self._emergency_shutdown()
            return False
        
        # 경고 상황
        if cpu_percent >= self.resource_thresholds["cpu_warning"]:
            logger.warning(f"CPU 사용률 경고: {cpu_percent}%")
        
        if memory_percent >= self.resource_thresholds["memory_warning"]:
            logger.warning(f"메모리 사용률 경고: {memory_percent}%")
        
        return True
    
    async def _emergency_shutdown(self):
        """비상 시 AI 서비스 차단"""
        logger.critical("시스템 리소스 위급 - AI 서비스 일시 중단")
        
        # 모든 모델 비활성화
        for model_name in self.model_states:
            self.model_states[model_name].status = AIModelStatus.OFFLINE
        
        # 알림 발송 (구현 필요)
        # await self._send_emergency_alert()
    
    async def _update_statistics(
        self,
        model_name: str,
        service: str,
        response: Dict[str, Any],
        elapsed_time: float
    ):
        """통계 업데이트"""
        model_state = self.model_states[model_name]
        model_config = self.models[model_name]
        
        # 모델 상태 업데이트
        model_state.last_used = datetime.now()
        model_state.tokens_used_today += response.get("tokens", 0)
        model_state.requests_today += 1
        
        # 응답 시간 평균 계산
        if model_state.avg_response_time == 0:
            model_state.avg_response_time = elapsed_time
        else:
            model_state.avg_response_time = (model_state.avg_response_time * 0.9) + (elapsed_time * 0.1)
        
        # 전체 통계 업데이트
        self.usage_stats["total_requests"] += 1
        self.usage_stats["total_tokens"] += response.get("tokens", 0)
        
        # 비용 계산
        if not model_config.is_free:
            cost = (response.get("tokens", 0) / 1000) * model_config.cost_per_1k_tokens
            self.usage_stats["total_cost"] += cost
        
        # 서비스별 통계
        if service not in self.usage_stats["service_usage"]:
            self.usage_stats["service_usage"][service] = {"requests": 0, "tokens": 0}
        
        self.usage_stats["service_usage"][service]["requests"] += 1
        self.usage_stats["service_usage"][service]["tokens"] += response.get("tokens", 0)
        
        # 모델별 통계
        if model_name not in self.usage_stats["model_usage"]:
            self.usage_stats["model_usage"][model_name] = {"requests": 0, "tokens": 0, "errors": 0}
        
        self.usage_stats["model_usage"][model_name]["requests"] += 1
        self.usage_stats["model_usage"][model_name]["tokens"] += response.get("tokens", 0)
    
    async def _handle_model_error(self, model_name: str, error: Exception):
        """모델 오류 처리"""
        model_state = self.model_states[model_name]
        
        model_state.last_error = str(error)
        model_state.error_count += 1
        
        # 성공률 재계산
        total_requests = self.usage_stats["model_usage"].get(model_name, {}).get("requests", 1)
        model_state.success_rate = ((total_requests - model_state.error_count) / total_requests) * 100
        
        # 오류가 많으면 쿨다운
        if model_state.error_count >= 5:
            model_state.status = AIModelStatus.COOLING_DOWN
            # 5분 후 재활성화 스케줄
            asyncio.create_task(self._reactivate_model_after_cooldown(model_name, 300))
    
    async def _reactivate_model_after_cooldown(self, model_name: str, cooldown_seconds: int):
        """쿨다운 후 모델 재활성화"""
        await asyncio.sleep(cooldown_seconds)
        
        model_state = self.model_states[model_name]
        if model_state.status == AIModelStatus.COOLING_DOWN:
            model_state.status = AIModelStatus.ACTIVE
            model_state.error_count = 0
            logger.info(f"모델 {model_name} 재활성화됨")
    
    async def perform_health_check(self) -> Dict[str, Any]:
        """전체 시스템 헬스체크"""
        health_report = {
            "timestamp": datetime.now().isoformat(),
            "system_resources": {
                "cpu_percent": psutil.cpu_percent(interval=0.1),
                "memory_percent": psutil.virtual_memory().percent,
                "disk_percent": psutil.disk_usage('/').percent
            },
            "models": {}
        }
        
        # 각 모델 헬스체크
        for model_name, model_config in self.models.items():
            model_state = self.model_states[model_name]
            
            # 간단한 테스트 프롬프트로 확인
            if model_state.status == AIModelStatus.ACTIVE:
                try:
                    test_prompt = "안녕하세요"
                    await asyncio.wait_for(
                        self._call_ai_model(model_name, test_prompt),
                        timeout=10.0
                    )
                    model_state.health_check_passed = True
                except Exception as e:
                    logger.warning(f"모델 {model_name} 헬스체크 실패: {e}")
                    model_state.health_check_passed = False
                    if "rate limit" in str(e).lower():
                        model_state.status = AIModelStatus.QUOTA_EXCEEDED
                    elif model_state.error_count >= 3:
                        model_state.status = AIModelStatus.ERROR
            
            health_report["models"][model_name] = {
                "status": model_state.status.value,
                "health_check_passed": model_state.health_check_passed,
                "success_rate": model_state.success_rate,
                "avg_response_time": model_state.avg_response_time,
                "tokens_used_today": model_state.tokens_used_today,
                "last_error": model_state.last_error
            }
        
        return health_report
    
    async def generate_daily_report(self) -> Dict[str, Any]:
        """일일 사용 리포트 생성"""
        report = {
            "date": datetime.now().strftime("%Y-%m-%d"),
            "summary": {
                "total_requests": self.usage_stats["total_requests"],
                "total_tokens": self.usage_stats["total_tokens"],
                "total_cost": round(self.usage_stats["total_cost"], 2),
                "avg_cost_per_request": round(
                    self.usage_stats["total_cost"] / max(self.usage_stats["total_requests"], 1), 4
                )
            },
            "by_service": self.usage_stats["service_usage"],
            "by_model": {},
            "recommendations": []
        }
        
        # 모델별 상세 리포트
        for model_name, usage in self.usage_stats["model_usage"].items():
            model_config = self.models[model_name]
            model_state = self.model_states[model_name]
            
            report["by_model"][model_name] = {
                "requests": usage["requests"],
                "tokens": usage["tokens"],
                "errors": usage["errors"],
                "success_rate": model_state.success_rate,
                "avg_response_time": round(model_state.avg_response_time, 2),
                "cost": 0 if model_config.is_free else round(
                    (usage["tokens"] / 1000) * model_config.cost_per_1k_tokens, 2
                ),
                "status": model_state.status.value
            }
        
        # 추천사항 생성
        if self.usage_stats["total_cost"] > 100:  # $100 이상 사용 시
            report["recommendations"].append("비용이 높습니다. 무료 모델(Gemini) 사용 비중을 늘리는 것을 고려하세요.")
        
        # 오류율이 높은 모델 확인
        for model_name, usage in self.usage_stats["model_usage"].items():
            if usage["requests"] > 0:
                error_rate = (usage["errors"] / usage["requests"]) * 100
                if error_rate > 10:
                    report["recommendations"].append(
                        f"{model_name} 모델의 오류율이 {error_rate:.1f}%로 높습니다. 점검이 필요합니다."
                    )
        
        return report
    
    async def start_monitoring(self):
        """백그라운드 모니터링 시작"""
        self._monitoring_task = asyncio.create_task(self._monitoring_loop())
    
    async def stop_monitoring(self):
        """백그라운드 모니터링 중지"""
        if self._monitoring_task:
            self._monitoring_task.cancel()
            try:
                await self._monitoring_task
            except asyncio.CancelledError:
                pass
    
    async def _monitoring_loop(self):
        """백그라운드 모니터링 루프"""
        while True:
            try:
                # 헬스체크 수행
                await self.perform_health_check()
                
                # 시스템 리소스 체크
                await self._check_system_resources()
                
                # 일일 통계 리셋 (자정)
                now = datetime.now()
                if now.hour == 0 and now.minute < 1:
                    await self._reset_daily_stats()
                
                await asyncio.sleep(self._health_check_interval)
                
            except asyncio.CancelledError:
                raise
            except Exception as e:
                logger.error(f"모니터링 루프 오류: {e}")
                await asyncio.sleep(self._health_check_interval)
    
    async def _reset_daily_stats(self):
        """일일 통계 리셋"""
        # 리포트 생성 및 저장
        daily_report = await self.generate_daily_report()
        
        # 파일로 저장
        report_path = f"/home/ubuntu/logs/ai_reports/daily_{datetime.now().strftime('%Y%m%d')}.json"
        os.makedirs(os.path.dirname(report_path), exist_ok=True)
        
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(daily_report, f, ensure_ascii=False, indent=2)
        
        # 통계 리셋
        for model_state in self.model_states.values():
            model_state.tokens_used_today = 0
            model_state.requests_today = 0
            model_state.error_count = 0
    
    def get_service_fallback_order(self, service: str) -> List[str]:
        """서비스별 폴백 순서 조회"""
        return self.service_fallback_order.get(service, self.service_fallback_order["default"])
    
    def update_service_fallback_order(self, service: str, order: List[str]):
        """서비스별 폴백 순서 업데이트"""
        # 유효성 검증
        valid_models = [m for m in order if m in self.models]
        if not valid_models:
            raise ValueError("유효한 모델이 없습니다")
        
        self.service_fallback_order[service] = valid_models
        logger.info(f"서비스 {service}의 폴백 순서 업데이트: {valid_models}")
    
    def get_model_info(self, model_name: str) -> Dict[str, Any]:
        """특정 모델 정보 조회"""
        if model_name not in self.models:
            raise ValueError(f"모델 {model_name}을 찾을 수 없습니다")
        
        model_config = self.models[model_name]
        model_state = self.model_states[model_name]
        
        return {
            "config": {
                "name": model_config.name,
                "provider": model_config.provider,
                "is_free": model_config.is_free,
                "cost_per_1k_tokens": model_config.cost_per_1k_tokens,
                "strengths": model_config.strengths,
                "weaknesses": model_config.weaknesses,
                "use_cases": model_config.use_cases
            },
            "state": {
                "status": model_state.status.value,
                "tokens_used_today": model_state.tokens_used_today,
                "requests_today": model_state.requests_today,
                "success_rate": model_state.success_rate,
                "avg_response_time": model_state.avg_response_time,
                "last_used": model_state.last_used.isoformat() if model_state.last_used else None,
                "last_error": model_state.last_error
            }
        }
    
    async def toggle_model(self, model_name: str, enable: bool):
        """모델 활성화/비활성화"""
        if model_name not in self.models:
            raise ValueError(f"모델 {model_name}을 찾을 수 없습니다")
        
        model_state = self.model_states[model_name]
        
        if enable:
            model_state.status = AIModelStatus.ACTIVE
            logger.info(f"모델 {model_name} 활성화됨")
        else:
            model_state.status = AIModelStatus.OFFLINE
            logger.info(f"모델 {model_name} 비활성화됨")

# 싱글톤 인스턴스
ai_manager = AIModelManager()

# FastAPI 라우터용 엔드포인트
from fastapi import APIRouter

router = APIRouter(prefix="/ai", tags=["AI Model Management"])

@router.post("/chat")
async def ai_chat(
    prompt: str,
    service: str = "default",
    preferred_model: Optional[str] = None
):
    """AI 채팅 API"""
    try:
        response, model_used, metadata = await ai_manager.get_ai_response(
            prompt=prompt,
            service=service,
            preferred_model=preferred_model
        )
        
        return {
            "success": True,
            "response": response,
            "model_used": model_used,
            "metadata": metadata
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

@router.get("/models")
async def list_models():
    """사용 가능한 모델 목록"""
    models = {}
    for model_name in ai_manager.models:
        models[model_name] = ai_manager.get_model_info(model_name)
    
    return {
        "success": True,
        "models": models
    }

@router.get("/health")
async def health_check():
    """시스템 헬스체크"""
    health_report = await ai_manager.perform_health_check()
    return {
        "success": True,
        "report": health_report
    }

@router.get("/report/daily")
async def get_daily_report():
    """일일 사용 리포트"""
    report = await ai_manager.generate_daily_report()
    return {
        "success": True,
        "report": report
    }

@router.post("/models/{model_name}/toggle")
async def toggle_model(model_name: str, enable: bool):
    """모델 활성화/비활성화"""
    try:
        await ai_manager.toggle_model(model_name, enable)
        return {
            "success": True,
            "message": f"모델 {model_name} {'활성화' if enable else '비활성화'}됨"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

@router.put("/services/{service}/fallback-order")
async def update_fallback_order(service: str, order: List[str]):
    """서비스별 폴백 순서 업데이트"""
    try:
        ai_manager.update_service_fallback_order(service, order)
        return {
            "success": True,
            "message": f"서비스 {service}의 폴백 순서가 업데이트되었습니다"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

# 앱 시작 시 모니터링 시작
async def startup():
    await ai_manager.start_monitoring()

# 앱 종료 시 모니터링 중지
async def shutdown():
    await ai_manager.stop_monitoring()