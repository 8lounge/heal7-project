#!/usr/bin/env python3
"""
환경변수 API 엔드포인트 (FastAPI 버전)
- /home/ubuntu/.env.ai 파일에서 안전하게 환경변수를 로드
- 보안을 위해 실제 키는 전달하지 않고 구조만 반환
"""

import os
import logging
from typing import Dict, Any
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

logger = logging.getLogger(__name__)

# FastAPI 라우터 생성
router = APIRouter(
    prefix="/api/env-config",
    tags=["env-config"],
)

class EnvConfigResponse(BaseModel):
    success: bool
    data: Dict[str, Any]
    timestamp: str

def load_env_file() -> Dict[str, str]:
    """환경변수 파일 로드"""
    env_file_path = '/home/ubuntu/.env.ai'
    env_vars = {}
    
    if not os.path.exists(env_file_path):
        raise FileNotFoundError('.env.ai 파일을 찾을 수 없습니다')
    
    if not os.access(env_file_path, os.R_OK):
        raise PermissionError('.env.ai 파일을 읽을 수 없습니다 (권한 확인 필요)')
    
    try:
        with open(env_file_path, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                
                # 주석 및 빈 줄 건너뛰기
                if not line or line.startswith('#'):
                    continue
                
                # KEY=VALUE 형식 파싱
                if '=' in line:
                    key, value = line.split('=', 1)
                    key = key.strip()
                    value = value.strip().strip('"\'')  # 따옴표 제거
                    
                    if key:
                        env_vars[key] = value
                else:
                    logger.warning(f"Invalid format at line {line_num}: {line}")
    
    except Exception as e:
        logger.error(f"Error reading .env.ai file: {e}")
        raise
    
    return env_vars

def create_safe_config(env_vars: Dict[str, str]) -> Dict[str, Any]:
    """보안을 위해 실제 키는 숨기고 구조만 반환"""
    
    # AI 모델 매핑
    model_mappings = {
        'ANTHROPIC_API_KEY': {
            'provider': 'Anthropic',
            'models': ['claude-3-5-sonnet-20241022', 'claude-3-haiku-20240307', 'claude-3-opus-20240229'],
            'available': bool(env_vars.get('ANTHROPIC_API_KEY'))
        },
        'OPENAI_API_KEY': {
            'provider': 'OpenAI',
            'models': ['gpt-4o', 'gpt-4o-mini', 'gpt-4-turbo', 'gpt-3.5-turbo'],
            'available': bool(env_vars.get('OPENAI_API_KEY'))
        },
        'GOOGLE_AI_API_KEY': {
            'provider': 'Google',
            'models': ['gemini-2.0-flash-exp', 'gemini-1.5-pro', 'gemini-1.5-flash'],
            'available': bool(env_vars.get('GOOGLE_AI_API_KEY'))
        }
    }
    
    # 사용 가능한 모델들만 필터링
    available_models = {}
    total_available = 0
    
    for key, info in model_mappings.items():
        if info['available']:
            available_models[info['provider'].lower()] = {
                'provider': info['provider'],
                'models': info['models'],
                'status': 'active'
            }
            total_available += 1
    
    # Paperwork AI 설정 구조
    config = {
        'ai_models': available_models,
        'system_info': {
            'total_providers': total_available,
            'total_models': sum(len(info['models']) for info in available_models.values()),
            'env_file_loaded': True,
            'env_file_path': '/home/ubuntu/.env.ai'
        },
        'features': {
            'ai_proxy': True,
            'multi_model_support': total_available > 1,
            'api_key_security': True,
            'cors_enabled': True
        }
    }
    
    # 개별 API 키 상태 (보안상 키 값은 숨김)
    for key in ['ANTHROPIC_API_KEY', 'OPENAI_API_KEY', 'GOOGLE_AI_API_KEY', 'GEMINI_API_KEY']:
        if key in env_vars:
            # 키의 앞 4자리와 뒤 4자리만 표시
            masked_key = f"{env_vars[key][:4]}...{env_vars[key][-4:]}" if len(env_vars[key]) > 8 else "****"
            config['system_info'][f'{key.lower()}_status'] = {
                'available': True,
                'masked_value': masked_key,
                'length': len(env_vars[key])
            }
    
    return config

@router.get("", response_model=EnvConfigResponse)
async def get_env_config():
    """환경변수 설정 조회 (보안 처리된)"""
    try:
        env_vars = load_env_file()
        safe_config = create_safe_config(env_vars)
        
        from datetime import datetime
        
        return EnvConfigResponse(
            success=True,
            data=safe_config,
            timestamp=datetime.now().isoformat()
        )
        
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except Exception as e:
        logger.error(f"Env config error: {e}")
        raise HTTPException(status_code=500, detail=f"서버 오류: {str(e)}")

@router.get("/health")
async def health_check():
    """헬스 체크"""
    try:
        env_vars = load_env_file()
        available_keys = sum(1 for key in ['ANTHROPIC_API_KEY', 'OPENAI_API_KEY', 'GOOGLE_AI_API_KEY'] if key in env_vars)
        
        return {
            "status": "healthy",
            "service": "Env Config API",
            "available_api_keys": available_keys,
            "env_file_accessible": True
        }
        
    except Exception as e:
        return {
            "status": "unhealthy",
            "service": "Env Config API",
            "error": str(e),
            "env_file_accessible": False
        }