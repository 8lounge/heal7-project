#!/usr/bin/env python3
"""
AI API 프록시 서버 - CORS 우회 및 보안 강화
FastAPI 버전으로 변환
"""

import os
import json
import logging
from typing import Dict, Any, Optional
import httpx
from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel

logger = logging.getLogger(__name__)

# FastAPI 라우터 생성
router = APIRouter(
    prefix="/api/ai-proxy",
    tags=["ai-proxy"],
)

# Pydantic 모델
class AIProxyRequest(BaseModel):
    provider: str
    model: str 
    prompt: str
    options: Optional[Dict[str, Any]] = {}

class AIProxyResponse(BaseModel):
    success: bool
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None

def load_env_variables() -> Dict[str, str]:
    """환경변수 로드"""
    env_vars = {}
    env_file_path = '/home/ubuntu/.env.ai'
    
    if os.path.exists(env_file_path):
        try:
            with open(env_file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and '=' in line and not line.startswith('#'):
                        key, value = line.split('=', 1)
                        env_vars[key.strip()] = value.strip().strip('"\'')
        except Exception as e:
            logger.error(f"Failed to load .env.ai: {e}")
    
    # 시스템 환경변수도 확인
    ai_keys = [
        'ANTHROPIC_API_KEY', 'OPENAI_API_KEY', 'GOOGLE_AI_API_KEY',
        'GEMINI_API_KEY', 'CLAUDE_API_KEY'
    ]
    
    for key in ai_keys:
        if key in os.environ:
            env_vars[key] = os.environ[key]
    
    return env_vars

async def call_anthropic_api(model: str, prompt: str, options: Dict, api_key: str) -> Dict:
    """Anthropic Claude API 호출"""
    headers = {
        'Content-Type': 'application/json',
        'x-api-key': api_key,
        'anthropic-version': '2023-06-01'
    }
    
    data = {
        'model': model,
        'max_tokens': options.get('max_tokens', 4000),
        'messages': [{'role': 'user', 'content': prompt}],
        'temperature': options.get('temperature', 0.7)
    }
    
    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.post(
            'https://api.anthropic.com/v1/messages',
            headers=headers,
            json=data
        )
        
        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code,
                detail=f"Anthropic API error: {response.text}"
            )
        
        return response.json()

async def call_openai_api(model: str, prompt: str, options: Dict, api_key: str) -> Dict:
    """OpenAI API 호출"""
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}'
    }
    
    data = {
        'model': model,
        'messages': [{'role': 'user', 'content': prompt}],
        'max_tokens': options.get('max_tokens', 4000),
        'temperature': options.get('temperature', 0.7)
    }
    
    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.post(
            'https://api.openai.com/v1/chat/completions',
            headers=headers,
            json=data
        )
        
        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code,
                detail=f"OpenAI API error: {response.text}"
            )
        
        return response.json()

async def call_gemini_api(model: str, prompt: str, options: Dict, api_key: str) -> Dict:
    """Google Gemini API 호출"""
    headers = {
        'Content-Type': 'application/json'
    }
    
    data = {
        'contents': [{'parts': [{'text': prompt}]}],
        'generationConfig': {
            'maxOutputTokens': options.get('max_tokens', 4000),
            'temperature': options.get('temperature', 0.7)
        }
    }
    
    url = f'https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}'
    
    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.post(url, headers=headers, json=data)
        
        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code,
                detail=f"Gemini API error: {response.text}"
            )
        
        return response.json()

@router.post("", response_model=AIProxyResponse)
async def ai_proxy(request: AIProxyRequest):
    """AI API 프록시 엔드포인트"""
    try:
        # 환경변수 로드
        env_vars = load_env_variables()
        
        provider = request.provider.lower()
        model = request.model
        prompt = request.prompt
        options = request.options
        
        # 프로바이더별 API 호출
        if provider == 'anthropic':
            api_key = env_vars.get('ANTHROPIC_API_KEY') or env_vars.get('CLAUDE_API_KEY')
            if not api_key:
                raise HTTPException(status_code=400, detail="Anthropic API key not found")
            
            result = await call_anthropic_api(model, prompt, options, api_key)
            
        elif provider == 'openai':
            api_key = env_vars.get('OPENAI_API_KEY')
            if not api_key:
                raise HTTPException(status_code=400, detail="OpenAI API key not found")
            
            result = await call_openai_api(model, prompt, options, api_key)
            
        elif provider == 'google' or provider == 'gemini':
            api_key = env_vars.get('GOOGLE_AI_API_KEY') or env_vars.get('GEMINI_API_KEY')
            if not api_key:
                raise HTTPException(status_code=400, detail="Google AI API key not found")
            
            result = await call_gemini_api(model, prompt, options, api_key)
            
        else:
            raise HTTPException(status_code=400, detail=f"Unsupported provider: {provider}")
        
        return AIProxyResponse(
            success=True,
            data=result
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"AI proxy error: {e}")
        return AIProxyResponse(
            success=False,
            error=str(e)
        )

@router.get("/health")
async def health_check():
    """헬스 체크"""
    env_vars = load_env_variables()
    
    available_providers = []
    if env_vars.get('ANTHROPIC_API_KEY') or env_vars.get('CLAUDE_API_KEY'):
        available_providers.append('anthropic')
    if env_vars.get('OPENAI_API_KEY'):
        available_providers.append('openai')
    if env_vars.get('GOOGLE_AI_API_KEY') or env_vars.get('GEMINI_API_KEY'):
        available_providers.append('google')
    
    return {
        "status": "healthy",
        "service": "AI Proxy",
        "available_providers": available_providers,
        "total_providers": len(available_providers)
    }